#!/usr/bin/env python3
"""MilUX agent guard: a Claude Code PreToolUse hook. Version 0.1.3 (card 6494, 13 September 2026; 11 October 2026).

    python3 .claude/hooks/guard.py pre-bash    (matcher: Bash)
    python3 .claude/hooks/guard.py pre-edit    (matcher: Edit|Write|MultiEdit|NotebookEdit)

Reads the hook event as JSON on stdin. Exit 2 refuses the tool call and puts the reason,
with the permitted route, on stderr where the agent reads it. Exit 0 allows. Garbage input
allows: the guard refuses on evidence, never on doubt, so a format change cannot brick a
session; it logs the fault instead (R-38: a mechanism that reports nothing reports a fault).

What it refuses, and the route it names instead:
  - git push to main or master (explicit, or bare while on main, including after a checkout
    earlier in the same command), force pushes, --all, --mirror, wildcard refspecs, tag
    refspecs, branch deletions                                          -> push the branch, open a pull request
  - creating or deleting tags, git update-ref on tags or main, changing push config or hooksPath -> cut-release, run by the releaser
  - gh pr merge/review/close, gh api writes, gh repo edit, gh release, gh auth (except status),
    gh alias set, gh workflow run                                        -> Matt's, after UAT
  - deploy and release commands (wrangler deploy, fly deploy, release builds, registry
    publishing, npm run deploy and the like)                              -> the pipeline behind Matt's approval
  - a script piped or substituted from a URL                             -> download, read, run under a card
  - installing or running a named registry package                       -> verify on the registry, rerun with MILUX_ALLOW_INSTALL=<card>
  - edits, by tool or by shell, to protected paths (workflows, actions, CODEOWNERS, CLAUDE.md,
    .claude/, .githooks/, the acceptance-test directory)                  -> a card naming the change and .claude/hooks/UNLOCK holding its number

Paths in the project's git worktrees are judged as the project's (0.1.3). A program run through an
interpreter (python, node, perl, ruby: a heredoc, -c or -e text, or a script file named on the
line) that writes files and names a protected path is judged as a shell write to it (0.1.3).

Known limits, by design (the layers behind this one are branch protection, required checks and
CODEOWNERS): a path a program builds at run time from pieces, a program fetched or decoded at run
time, shell variables and command substitution that resolve at run time, xargs and find -exec,
archives and patches that write files, and raw HTTP calls to the GitHub API with a token read from
the keychain. The guard reads commands and the programs they name, not intent.

Standard library only. Python 3.9 compatible (the Mac Mini's system Python). Every refusal and
every override is appended to .claude/hooks/guard.log, and mirrored to ~/.milux/guard/<repo>.log
so a git clean does not take the record with it. Values of KEY=value assignments are redacted.
"""

import datetime
import json
import os
import re
import shlex
import subprocess
import sys

VERSION = "0.1.3"

DEFAULT_PROTECTED = [
    ".github/workflows/**",
    ".github/actions/**",
    ".github/CODEOWNERS",
    "CODEOWNERS",
    "docs/CODEOWNERS",
    "CLAUDE.md",
    ".claude/**",
    ".githooks/**",
    "tests/acceptance/**",
]

MAIN_NAMES = ("main", "master", "refs/heads/main", "refs/heads/master")

WRAPPERS = (
    "sudo",
    "env",
    "command",
    "exec",
    "nohup",
    "time",
    "nice",
    "caffeinate",
    "stdbuf",
    "doas",
    "ionice",
    "timeout",
)
SHELL_WORDS = ("(", "{", "then", "do", "else", "elif", "!", "}", ")")
INTERPRETERS = ("sh", "bash", "zsh", "dash", "ksh", "fish", "node", "perl", "ruby")
CARD_SHAPE = re.compile(r"^\d{3,6}$")


# --------------------------------------------------------------------------- utilities


def project_dir(payload):
    root = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    return os.path.realpath(root)


def hooks_dir(root):
    return os.path.join(root, ".claude", "hooks")


def redact(text):
    text = re.sub(r"\b([A-Za-z_][A-Za-z0-9_]*)=(\S+)", lambda m: m.group(1) + "=***", text)
    text = re.sub(r"(\s(?:-u|--user|--password|-p)\s+)\S+", r"\1***", text)
    text = re.sub(r"(?i)(bearer\s+)\S+", r"\1***", text)
    text = re.sub(r"://[^/\s@]+@", "://***@", text)
    text = re.sub(
        r"\b(gh[pousr]_[A-Za-z0-9]{10,}|github_pat_[A-Za-z0-9_]{10,}|sk-[A-Za-z0-9_-]{10,}|xox[abp]-[A-Za-z0-9-]{10,})",
        "***",
        text,
    )
    return text


def log(root, kind, detail):
    line = None
    try:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        line = "{} {} {}\n".format(stamp, kind, redact(detail.replace("\n", " "))[:500])
        os.makedirs(hooks_dir(root), exist_ok=True)
        with open(os.path.join(hooks_dir(root), "guard.log"), "a") as fh:
            fh.write(line)
    except Exception:
        pass
    try:
        import tempfile

        if line and not os.path.realpath(root).startswith(os.path.realpath(tempfile.gettempdir())):
            mirror = os.path.join(os.path.expanduser("~"), ".milux", "guard")
            os.makedirs(mirror, exist_ok=True)
            with open(os.path.join(mirror, os.path.basename(root) + ".log"), "a") as fh:
                fh.write(line)
    except Exception:
        pass


def refuse(root, kind, detail, message):
    log(root, "REFUSED " + kind, detail)
    sys.stderr.write(f"MilUX guard ({kind}): {message}\n")
    sys.exit(2)


def unlock_card(root):
    path = os.path.join(hooks_dir(root), "UNLOCK")
    try:
        with open(path) as fh:
            value = fh.read().strip()
    except OSError:
        return None
    return value or None


def git_common_dir(top):
    """The shared .git directory of the working tree at `top` (the project, or one of its git
    worktrees), or None when `top` holds no .git."""
    dot = os.path.join(top, ".git")
    if os.path.isdir(dot):
        return os.path.realpath(dot)
    try:
        with open(dot) as fh:
            line = fh.read().strip()
    except OSError:
        return None
    if not line.startswith("gitdir:"):
        return None
    gitdir = line[len("gitdir:") :].strip()
    if not os.path.isabs(gitdir):
        gitdir = os.path.join(top, gitdir)
    gitdir = os.path.realpath(gitdir)
    try:
        with open(os.path.join(gitdir, "commondir")) as fh:
            common = fh.read().strip()
        return os.path.realpath(common if os.path.isabs(common) else os.path.join(gitdir, common))
    except OSError:
        pass
    if os.path.basename(os.path.dirname(gitdir)) == "worktrees":
        return os.path.dirname(os.path.dirname(gitdir))
    return gitdir


def same_repo_tree(path, root):
    """The working tree of this repository that holds `path`: the project itself or one of its git
    worktrees, the nearest one; None for a path in no tree of this repository. Card work happens in
    worktrees outside the project folder, and their protected paths are this repository's too
    (11 October 2026: until then a worktree had no protection at all)."""
    mine = git_common_dir(root)
    if not mine:
        return None
    d = os.path.realpath(path)
    if not os.path.isdir(d):
        d = os.path.dirname(d)
    while True:
        if os.path.exists(os.path.join(d, ".git")):
            return d if git_common_dir(d) == mine else None
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def same_repo_trees(root):
    """The project and each of its git worktrees, as git records them."""
    trees = [root]
    common = git_common_dir(root)
    if not common:
        return trees
    listed = os.path.join(common, "worktrees")
    try:
        names = sorted(os.listdir(listed))
    except OSError:
        names = []
    for name in names:
        try:
            with open(os.path.join(listed, name, "gitdir")) as fh:
                trees.append(os.path.dirname(fh.read().strip()))
        except OSError:
            pass
    return trees


def load_protected(root):
    """The defaults, and every line of protected-paths.txt in the project and in each of its
    worktrees: a branch may protect a card's tests before main does, and none can unprotect."""
    patterns = list(DEFAULT_PROTECTED)
    for tree in same_repo_trees(root):
        path = os.path.join(hooks_dir(tree), "protected-paths.txt")
        try:
            with open(path) as fh:
                for line in fh:
                    line = line.strip()
                    if line and not line.startswith("#") and line not in patterns:
                        patterns.append(line)
        except OSError:
            pass
    return patterns


_REGEX_CACHE = {}


def glob_to_regex(pattern):
    """A small ** aware glob: ** matches across slashes, * within a segment. Case-insensitive,
    because the Macs run a case-insensitive file system and CLAUDE.md is claude.md there."""
    if pattern in _REGEX_CACHE:
        return _REGEX_CACHE[pattern]
    out = ""
    i = 0
    while i < len(pattern):
        ch = pattern[i]
        if pattern.startswith("**/", i):
            out += "(?:.*/)?"
            i += 3
            continue
        if pattern.startswith("**", i):
            out += ".*"
            i += 2
            continue
        if ch == "*":
            out += "[^/]*"
        elif ch == "?":
            out += "[^/]"
        else:
            out += re.escape(ch)
        i += 1
    rx = re.compile("^" + out + "$", re.IGNORECASE)
    _REGEX_CACHE[pattern] = rx
    return rx


def norm_rel(rel):
    rel = rel.replace(os.sep, "/")
    while rel.startswith("./"):
        rel = rel[2:]
    return rel


def is_protected(rel, patterns):
    rel = norm_rel(rel)
    for p in patterns:
        if glob_to_regex(p).match(rel):
            return p
    return None


def protected_bases(patterns):
    """The directory each pattern lives under, for ancestor checks: .github/workflows, .claude, tests/acceptance."""
    bases = []
    for p in patterns:
        base = p.split("*")[0].rstrip("/")
        if base and base not in bases:
            bases.append(base)
    return bases


def relative_to_root(path, root, cwd):
    """`path` relative to the working tree of this repository that holds it (the project or one of
    its worktrees), or None when it is in neither."""
    if not os.path.isabs(path):
        path = os.path.join(cwd or root, path)
    real = os.path.realpath(path)
    tree = same_repo_tree(real, root)
    for top in ([tree] if tree else []) + [root]:
        try:
            rel = os.path.relpath(real, os.path.realpath(top))
        except ValueError:
            continue
        if not rel.startswith(".."):
            return rel
    return None


def hooks_path_is_repo_own(value, root, cwd):
    """True only when the hooks path is the repository's own .githooks directory."""
    value = value.strip("'\"")
    if not value or "$" in value or "`" in value:
        return False
    candidate = value if os.path.isabs(value) else os.path.join(cwd, value)
    return os.path.realpath(candidate) == os.path.realpath(os.path.join(root, ".githooks"))


def is_local_tag(cwd, name):
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", "refs/tags/" + name],
            cwd=cwd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )
        return out.returncode == 0
    except Exception:
        return False


def current_branch(cwd):
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )
        return out.stdout.decode("utf-8", "replace").strip()
    except Exception:
        return ""


def heredoc_marker(line):
    """The marker word of an unquoted << or <<- on this line, or None. A << inside quotes is text."""
    quote = None
    i = 0
    while i < len(line):
        ch = line[i]
        if quote:
            if ch == "\\" and quote == '"':
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in ("'", '"'):
            quote = ch
        elif ch == "\\":
            i += 2
            continue
        elif line.startswith("<<", i) and not line.startswith("<<<", i):
            m = re.match(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?", line[i:])
            return m.group(1) if m else None
        i += 1
    return None


def strip_heredocs(command):
    """Heredoc bodies are data the command feeds to a program, not commands. Cut them out."""
    out = []
    lines = command.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        marker = heredoc_marker(line)
        if marker:
            i += 1
            while i < len(lines) and lines[i].strip() != marker:
                i += 1
        i += 1
    return "\n".join(out)


def pipelines(command):
    """Split a shell command into pipelines on ; && || and newlines, each pipeline into its stages."""
    command = command.replace("\\\n", " ")
    parts = re.split(r"\s*(?:\|\||&&|;|\n)\s*", command)
    result = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        stages = [s.strip() for s in re.split(r"(?<![|<>])\|(?!\|)", p) if s.strip()]
        result.append((p, stages))
    return result


def leading_assignments(segment):
    """VAR=value words in front of a command, as a dict."""
    found = {}
    try:
        toks = shlex.split(segment, posix=True)
    except ValueError:
        toks = segment.split()
    for t in toks:
        if t in SHELL_WORDS:
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", t)
        if m:
            found[m.group(1)] = m.group(2)
            continue
        break
    return found


def tokens_of(segment):
    segment = re.sub(r"(^|\s)([({])(?=\S)", r"\1\2 ", segment)
    segment = re.sub(r"(?<=\S)([)}])(\s|$)", r" \1\2", segment)
    try:
        toks = shlex.split(segment, posix=True)
    except ValueError:
        toks = segment.split()
    changed = True
    while changed and toks:
        changed = False
        if toks[0] in SHELL_WORDS:
            toks = toks[1:]
            changed = True
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", toks[0]):
            toks = toks[1:]
            changed = True
            continue
        head = os.path.basename(toks[0])
        if head in WRAPPERS:
            toks = toks[1:]
            if head == "timeout":
                while toks and toks[0].startswith("-"):
                    opt = toks[0]
                    toks = toks[1:]
                    if opt in ("-k", "-s", "--kill-after", "--signal") and toks:
                        toks = toks[1:]
                if toks and re.match(r"^\d", toks[0]):
                    toks = toks[1:]
            else:
                while toks and toks[0].startswith("-"):
                    opt = toks[0]
                    toks = toks[1:]
                    if (
                        opt in ("-n", "-u", "-g")
                        and toks
                        and not toks[0].startswith("-")
                        and re.match(r"^[\w.-]+$", toks[0])
                    ):
                        toks = toks[1:]
            changed = True
    while toks and toks[-1] in (")", "}"):
        toks = toks[:-1]
    return toks


# --------------------------------------------------------------------------- git

GIT_OPTS_WITH_ARG = (
    "-c",
    "-C",
    "--git-dir",
    "--work-tree",
    "--namespace",
    "--exec-path",
    "--super-prefix",
    "--config-env",
)


CONFIG_KEYS = re.compile(
    r"(^|\s|')(remote\.[^\s=']+\.push|push\.default|core\.hooksPath|receive\.|uploadpack\.|core\.sshCommand|url\.[^\s=']+\.insteadOf)",
    re.IGNORECASE,
)


def git_subcommand(toks):
    """Return (subcommand, args, cwd_override, config_pairs) for a git invocation, skipping global options."""
    i = 1
    cwd = None
    pairs = []
    while i < len(toks):
        t = toks[i]
        if t in GIT_OPTS_WITH_ARG:
            if t == "-C" and i + 1 < len(toks):
                cwd = toks[i + 1]
            if t in ("-c", "--config-env") and i + 1 < len(toks):
                pairs.append(toks[i + 1])
            i += 2
            continue
        if t.startswith("--") and "=" in t:
            name, value = t.split("=", 1)
            if name in ("--config-env",):
                pairs.append(value)
            if name == "-C":
                cwd = value
            i += 1
            continue
        if t.startswith("-"):
            i += 1
            continue
        return t, toks[i + 1 :], cwd, pairs
    return "", [], cwd, pairs


PUSH_ROUTE = (
    "Pushing to main is refused. Push the branch (git push -u origin <branch>) and open a pull request; "
    "the merge is Matt's after UAT and branch protection enforces it."
)


def check_git(toks, root, state):
    if len(toks) < 2:
        return
    sub, args, cwd_override, pairs = git_subcommand(toks)
    detail = " ".join(toks)
    cwd = state["cwd"]
    if cwd_override:
        cwd = os.path.join(cwd, cwd_override) if not os.path.isabs(cwd_override) else cwd_override
    for pair in pairs:
        if CONFIG_KEYS.search(pair):
            if pair.lower().startswith("core.hookspath=") and hooks_path_is_repo_own(
                pair.split("=", 1)[1], root, cwd
            ):
                continue
            refuse(
                root,
                "config",
                detail,
                "Push defaults, hooks paths and remote rewrites are not set by an agent, on the command line or in the "
                "config: they are how the repository keeps agents on branches. Say what you need on the card.",
            )
    for key, _value in state.get("assignments", {}).items():
        if key.upper().startswith("GIT_CONFIG") or key.upper() in (
            "GIT_SSH_COMMAND",
            "GIT_DIR",
            "GIT_WORK_TREE",
            "GIT_PUSH_OPTION_COUNT",
        ):
            refuse(
                root,
                "config",
                detail,
                "Configuring git through the environment is not done by an agent. Use plain git commands on your branch; say what you need on the card.",
            )
    if sub == "push":
        if any(t.startswith(("--git-dir", "--work-tree")) for t in toks[1:]):
            refuse(
                root,
                "push",
                detail,
                "Pushing another repository by --git-dir or --work-tree is refused. Run git inside the repository you are working in, on your branch.",
            )
        remote_named = False
        positional = []
        skip = False
        for a in args:
            if skip:
                skip = False
                continue
            if a in ("--force", "-f", "--force-with-lease", "--force-if-includes") or a.startswith(
                "--force-with-lease="
            ):
                refuse(
                    root,
                    "push",
                    detail,
                    "A force push is never made by an agent. Push new commits on the branch instead; "
                    "if history must be rewritten, say so on the card and Matt does it.",
                )
            if a in ("--tags", "--follow-tags", "--all", "--mirror", "--branches", "--prune"):
                refuse(
                    root,
                    "push",
                    detail,
                    "Tags, mirrors and bulk pushes are the releaser's. Push the one branch you are on "
                    "(git push -u origin <branch>) and stop; cut-release tags the release at Matt's explicit step.",
                )
            if a in ("--delete", "-d"):
                refuse(
                    root,
                    "push",
                    detail,
                    "Deleting a remote branch is the releaser's. Leave the branch; it is removed when the pull request merges.",
                )
            if a.startswith("--repo="):
                remote_named = True
                continue
            if a == "--repo":
                remote_named = True
                skip = True
                continue
            if a in ("-o", "--push-option", "--receive-pack", "--exec"):
                skip = True
                continue
            if a.startswith("-"):
                continue
            positional.append(a)
        refspecs = positional if remote_named else positional[1:]
        for r in refspecs:
            if r.startswith("+"):
                refuse(
                    root,
                    "push",
                    detail,
                    "A forced refspec is a force push. Push the branch without the plus.",
                )
            if r.startswith(":"):
                refuse(
                    root,
                    "push",
                    detail,
                    "Deleting a remote branch is the releaser's. Leave the branch; it is removed when the pull request merges.",
                )
            if "*" in r:
                refuse(
                    root,
                    "push",
                    detail,
                    "A wildcard refspec pushes everything. Push the one branch you are on and stop.",
                )
            src, dst = (r.split(":", 1) + [None])[:2] if ":" in r else (r, r)
            if dst is None:
                dst = src
            if (
                dst.startswith("refs/tags/")
                or src.startswith("refs/tags/")
                or dst.startswith("refs/notes/")
            ):
                refuse(
                    root,
                    "push",
                    detail,
                    "Tags are pushed by the releaser with cut-release. State the intended version on the card and stop after the pull request.",
                )
            if dst in MAIN_NAMES or (src in MAIN_NAMES and dst == src):
                refuse(root, "push", detail, PUSH_ROUTE)
            if (
                ":" not in r
                and r != "HEAD"
                and (re.match(r"^v?\d+(\.\d+)+", r) or is_local_tag(cwd, r))
            ):
                refuse(
                    root,
                    "push",
                    detail,
                    "That refspec names a tag. Tags are pushed by the releaser with cut-release. State the intended version on the card and stop after the pull request.",
                )
        if not refspecs or all(r == "HEAD" for r in refspecs):
            branch = state.get("branch_override") or current_branch(cwd)
            if branch in ("main", "master"):
                refuse(
                    root,
                    "push",
                    detail,
                    f"You are on {branch}. Pushing it is refused. Take a branch or a worktree "
                    "(git worktree add ../_workspaces/<repo>-<card> -b <type>/<card>-<slug> origin/main), "
                    "commit there, push it and open a pull request.",
                )
    elif sub in ("checkout", "switch"):
        # a later bare push in the same command lands on whatever this checks out
        positional = [a for a in args if not a.startswith("-")]
        flags = [a for a in args if a.startswith("-")]
        target = None
        if positional and "--" not in args:
            target = positional[0]
        if any(f in ("-b", "-B", "-c", "-C") for f in flags) and positional:
            target = positional[0]
        if target in ("main", "master"):
            state["branch_override"] = target
        elif target:
            state["branch_override"] = None
    elif sub == "branch":
        if any(a in ("-D", "-d", "--delete") for a in args) and any(
            a in ("main", "master") for a in args
        ):
            refuse(root, "branch", detail, "main is never deleted.")
        if any(
            a in ("-M", "-m", "--move", "--force", "-f", "-c", "-C", "--copy") for a in args
        ) and any(a in ("main", "master") for a in args):
            refuse(
                root,
                "branch",
                detail,
                "Moving, resetting or renaming main is Matt's. Work on your branch; main changes only by a merged pull request.",
            )
    elif sub == "tag":
        if not args:
            return
        if any(
            a
            in (
                "-l",
                "--list",
                "-n",
                "--contains",
                "--no-contains",
                "--points-at",
                "--merged",
                "--no-merged",
                "--verify",
                "-v",
            )
            for a in args
        ):
            return
        if any(a in ("-d", "--delete") for a in args):
            refuse(
                root,
                "tag",
                detail,
                "Deleting a tag is the releaser's. A released version is immutable (R-37); say what is wrong on the card.",
            )
        refuse(
            root,
            "tag",
            detail,
            "Creating a tag is the release ritual, run by the releaser with cut-release. "
            "State the intended version on the card and stop after the pull request.",
        )
    elif sub in ("fetch", "pull"):
        if any(re.search(r":refs/tags/|^refs/tags/", a) for a in args):
            refuse(
                root,
                "tag",
                detail,
                "Fetching into refs/tags creates a tag by the back door. Tags are the releaser's; push your branch and open a pull request.",
            )
    elif sub == "remote" and args[:1] in (["set-url"], ["add"], ["rename"], ["remove"], ["rm"]):
        if args[:1] == ["set-url"] or "--push" in args:
            refuse(
                root,
                "config",
                detail,
                "Remote URLs are not changed by an agent. Keep pushing your branch to origin and say what you need on the card.",
            )
    elif sub == "symbolic-ref" and any(a in MAIN_NAMES for a in args):
        refuse(
            root,
            "branch",
            detail,
            "Pointing HEAD at main by symbolic-ref is refused. Take a branch.",
        )
    elif sub == "update-ref":
        if any(a.startswith("refs/tags/") or a in MAIN_NAMES for a in args):
            refuse(
                root,
                "tag",
                detail,
                "Writing tags or main through update-ref is the releaser's. Use a branch and a pull request.",
            )
    elif sub == "config":
        joined = " ".join(args)
        if re.search(
            r"(^|\s)(remote\.[^\s]+\.push|push\.default|core\.hooksPath)(\s|=|$)", joined
        ) and not any(a in ("--get", "-l", "--list", "--get-all") for a in args):
            plain = [a for a in args if not a.startswith("-")]
            if (
                len(plain) >= 2
                and plain[0].lower() == "core.hookspath"
                and hooks_path_is_repo_own(plain[1], root, cwd)
            ):
                return
            refuse(
                root,
                "config",
                detail,
                "Push defaults and the hooks path are not changed by an agent; they are how the repository keeps agents on branches. Say what you need on the card.",
            )


# --------------------------------------------------------------------------- gh


def gh_parts(toks):
    """gh [global flags] <command> [flags] <subcommand>: return (command, subcommand, rest)."""
    i = 1
    while i < len(toks) and toks[i].startswith("-"):
        if toks[i] in ("-R", "--repo", "--hostname") and "=" not in toks[i]:
            i += 2
        else:
            i += 1
    cmd = toks[i] if i < len(toks) else ""
    i += 1
    while i < len(toks) and toks[i].startswith("-"):
        if toks[i] in ("-R", "--repo", "--hostname", "-H") and "=" not in toks[i]:
            i += 2
        else:
            i += 1
    sub = toks[i] if i < len(toks) else ""
    return cmd, sub, toks[i + 1 :]


def check_gh(toks, root):
    if len(toks) < 2:
        return
    cmd, sub, rest = gh_parts(toks)
    detail = " ".join(toks)
    if cmd == "pr" and sub in ("merge", "review", "close", "reopen", "lock", "ready", "edit"):
        refuse(
            root,
            "gh",
            detail,
            "Reviewing, merging and closing pull requests are Matt's, after UAT. Push the branch, cite the CI run on the card "
            "and request review; gh pr create, gh pr view and gh pr checks are open to you.",
        )
    if cmd == "api":
        body = toks[2:]
        writes = False
        if (body and body[0] == "graphql") or ("graphql" in body[:2]):
            if re.search(r"\bmutation\b", detail):
                writes = True
        else:
            for i, t in enumerate(body):
                if (
                    t in ("-X", "--method")
                    and i + 1 < len(body)
                    and body[i + 1].upper() in ("PUT", "POST", "PATCH", "DELETE")
                ):
                    writes = True
                if (
                    t.startswith("-X")
                    and len(t) > 2
                    and t[2:].upper() in ("PUT", "POST", "PATCH", "DELETE")
                ) or (
                    t.startswith("--method=")
                    and t.split("=", 1)[1].upper() in ("PUT", "POST", "PATCH", "DELETE")
                ):
                    writes = True
                if (
                    t in ("-f", "-F", "--field", "--raw-field", "--input")
                    or (t.startswith(("-f", "-F")) and len(t) > 2 and "=" in t)
                    or t.startswith("--input=")
                ):
                    writes = True
        if writes:
            refuse(
                root,
                "gh",
                detail,
                "Writes through the GitHub API are Matt's. Reads (gh api <path>, gh pr checks, gh run list) are open to you.",
            )
    if cmd == "repo" and sub in (
        "edit",
        "delete",
        "archive",
        "unarchive",
        "rename",
        "deploy-key",
        "sync",
        "set-default",
    ):
        refuse(
            root,
            "gh",
            detail,
            "Repository settings are Matt's. Say what needs changing on the card.",
        )
    if cmd == "release":
        refuse(
            root,
            "gh",
            detail,
            "Releases are cut by the releaser with cut-release. Stop after the pull request.",
        )
    if cmd == "auth" and sub != "status":
        refuse(
            root,
            "gh",
            detail,
            "Credentials are never handled by an agent. gh auth status is open to you; report anything else on the card.",
        )
    if cmd in ("secret", "ssh-key", "gpg-key", "variable"):
        refuse(
            root,
            "gh",
            detail,
            "Secrets and keys are never handled by an agent. Report the need on the card.",
        )
    if cmd == "alias" and sub in ("set", "import", "delete"):
        refuse(
            root,
            "gh",
            detail,
            "gh aliases are not changed by an agent; they would let a refused command through under another name.",
        )
    if cmd == "workflow" and sub in ("run", "enable", "disable"):
        refuse(
            root,
            "gh",
            detail,
            "Workflows run on push and pull request. Triggering or changing them is Matt's.",
        )
    if (cmd == "ruleset" and sub not in ("list", "view", "check")) or (
        cmd == "run" and sub in ("cancel", "delete")
    ):
        refuse(
            root,
            "gh",
            detail,
            "Rulesets and workflow runs are Matt's to change; gh run list, gh run view and gh run rerun are open to you.",
        )


# --------------------------------------------------------------------------- deploy and release

DEPLOY_ROUTE = "Deploys run in the pipeline behind Matt's approval; never from a session. Stop after the pull request."
SCRIPT_NAMES = re.compile(r"^(deploy(:|$|-)|(release|publish|ship|promote)(:|$))")
OPTS_WITH_VALUE = (
    "--env",
    "-e",
    "-c",
    "--config",
    "-a",
    "--app",
    "-t",
    "--access-token",
    "--cwd",
    "-C",
    "--filter",
    "-F",
    "--prefix",
    "--workspace",
    "-w",
    "--dir",
    "--chdir",
    "-n",
    "--namespace",
    "--kubeconfig",
    "--context",
)


def skip_options(rest):
    while rest and rest[0].startswith("-"):
        rest = rest[2:] if rest[0] in OPTS_WITH_VALUE and "=" not in rest[0] else rest[1:]
    return rest


KNOWN_BINS = (
    "wrangler",
    "fly",
    "flyctl",
    "eslint",
    "tsc",
    "vitest",
    "playwright",
    "astro",
    "vite",
    "jest",
    "prettier",
    "next",
    "tsx",
    "ts-node",
    "terraform",
    "kubectl",
    "docker",
    "twine",
    "cargo",
    "gradle",
)


RUNNER_OPTS_WITH_VALUE = (
    "-p",
    "--package",
    "-c",
    "--call",
    "--cwd",
    "-w",
    "--workspace",
    "--filter",
    "-F",
    "--prefix",
    "-C",
)


def skip_runner_options(rest):
    while rest and rest[0].startswith("-"):
        rest = rest[2:] if rest[0] in RUNNER_OPTS_WITH_VALUE and "=" not in rest[0] else rest[1:]
    return rest


def runner_packages(rest):
    """Packages an npx/pnpm dlx/yarn dlx call fetches: -p X, --package X, --package=X."""
    out = []
    i = 0
    while i < len(rest) and rest[i].startswith("-"):
        if rest[i] in ("-p", "--package") and i + 1 < len(rest):
            out.append(rest[i + 1])
            i += 2
            continue
        if rest[i].startswith("--package="):
            out.append(rest[i].split("=", 1)[1])
        i += 1
    return out


def unwrap_runner(toks):
    """npx wrangler@3 deploy, pnpm exec wrangler deploy, yarn run wrangler deploy, bun x wrangler deploy -> wrangler deploy"""
    t = list(toks)
    if not t:
        return t
    head = os.path.basename(t[0])
    if head in ("npx", "pnpx", "bunx"):
        t = skip_runner_options(t[1:])
    elif head in ("npm", "pnpm", "yarn", "bun") and len(t) > 1:
        rest = skip_runner_options(t[1:])
        if rest and rest[0] in ("exec", "dlx", "x"):
            t = skip_runner_options(rest[1:])
        elif (
            rest
            and rest[0] in ("run", "run-script")
            and len(rest) > 1
            and rest[1].split("@")[0] in KNOWN_BINS
        ):
            t = rest[1:]
        elif head in ("yarn", "pnpm", "bun") and rest and rest[0].split("@")[0] in KNOWN_BINS:
            t = rest
        else:
            return list(toks)
    if t and "@" in os.path.basename(t[0]) and not t[0].startswith("@"):
        t[0] = t[0].split("@", 1)[0]
    return t


def check_deploy(toks, root, state):
    if not toks:
        return
    detail = " ".join(toks)
    t = unwrap_runner(toks)
    if not t:
        return
    head = os.path.basename(t[0])
    rest = skip_options(t[1:])
    if head == "wrangler" and (
        rest[:1] in (["deploy"], ["publish"], ["delete"], ["rollback"], ["secret"])
        or rest[:2] in (["versions", "deploy"], ["pages", "deploy"], ["pages", "publish"])
        or (rest[:1] == ["d1"] and "--remote" in rest)
        or (rest[:1] == ["kv:key"] and rest[1:2] not in (["list"], ["get"]))
        or (rest[:2] == ["kv", "key"] and rest[2:3] not in (["list"], ["get"]))
    ):
        refuse(
            root,
            "deploy",
            detail,
            DEPLOY_ROUTE
            + " wrangler dev and wrangler versions upload (a preview) are open to you.",
        )
    if head in ("fly", "flyctl"):
        fly_alias = {
            "m": "machine",
            "machines": "machine",
            "app": "apps",
            "cert": "certs",
            "release": "releases",
            "secret": "secrets",
            "img": "image",
            "vol": "volumes",
            "volume": "volumes",
            "redeploy": "deploy",
            "pg": "postgres",
            "ip": "ips",
        }
        sub = fly_alias.get(rest[0], rest[0]) if rest else ""
        nxt = rest[1] if len(rest) > 1 else ""
        reads = ("list", "ls", "info", "show", "status", "validate", "view", "get", "env")
        if sub in (
            "deploy",
            "secrets",
            "scale",
            "destroy",
            "launch",
            "machine",
            "releases",
            "certs",
            "apps",
            "image",
            "config",
            "volumes",
            "postgres",
            "ips",
            "orgs",
            "tokens",
            "ssh",
            "restart",
            "suspend",
            "resume",
        ):
            if nxt in reads or (sub == "releases" and nxt == ""):
                return
            if sub == "secrets" and nxt in ("list", "ls"):
                return
            refuse(
                root,
                "deploy",
                detail,
                DEPLOY_ROUTE
                + " fly status, fly logs and the list and show subcommands are open to you.",
            )
    if head in ("gradlew", "gradle"):
        joined = " ".join(rest).lower()
        if (
            any(
                k in joined
                for k in (
                    "publish",
                    "assemblerelease",
                    "bundlerelease",
                    "installrelease",
                    "uploadarchives",
                )
            )
            or re.search(r"(^|\s|:)(ar|br)(\s|$)", joined)
            or joined.split()[:1] == ["build"]
        ):
            refuse(
                root,
                "deploy",
                detail,
                "Release builds and publishing are the releaser's; the release keystore is out of reach by design. "
                "Build the debug variant (assembleDebug) and run the tests; the pipeline produces the artefact.",
            )
    if head in ("apksigner", "jarsigner") and (rest[:1] == ["sign"] or head == "jarsigner"):
        refuse(
            root, "deploy", detail, "Signing is the releaser's explicit step. Never in a session."
        )
    if head == "terraform" and rest[:1] in (["apply"], ["destroy"], ["import"], ["taint"]):
        refuse(root, "deploy", detail, DEPLOY_ROUTE + " terraform plan is open to you.")
    if head == "kubectl" and rest[:1] in (
        ["apply"],
        ["delete"],
        ["rollout"],
        ["scale"],
        ["patch"],
        ["create"],
        ["replace"],
        ["set"],
        ["edit"],
    ):
        refuse(root, "deploy", detail, DEPLOY_ROUTE + " kubectl get and describe are open to you.")
    if head in ("docker", "podman") and (
        rest[:1] == ["push"] or (rest[:2] == ["buildx", "build"] and "--push" in rest)
    ):
        refuse(root, "deploy", detail, DEPLOY_ROUTE)
    if (
        (
            head in ("twine", "cargo", "uv", "gem", "npm", "pnpm", "yarn", "poetry")
            and rest[:1] in (["upload"], ["publish"], ["push"])
            and not (head == "gem" and rest[:1] != ["push"])
        )
        and "--dry-run" not in rest
        and "-n" not in rest
    ):
        refuse(
            root,
            "deploy",
            detail,
            "Publishing to a registry is a release, cut by the releaser with cut-release.",
        )
    # package scripts and make targets named like a deploy
    script = None
    if head in ("npm", "pnpm", "yarn", "bun"):
        r = skip_options(t[1:])
        if r[:1] in (["run"], ["run-script"]) and len(r) > 1:
            script = r[1]
        elif head in ("pnpm", "yarn", "bun") and r and SCRIPT_NAMES.match(r[0]):
            script = r[0]
        if script and SCRIPT_NAMES.match(script):
            refuse(
                root,
                "deploy",
                detail,
                DEPLOY_ROUTE + f" A package script named {script} is a deploy by name.",
            )
        if script:
            body = package_script(state["cwd"], script)
            if body:
                for _, stages in pipelines(body):
                    for st in stages:
                        inner = tokens_of(st)
                        if inner:
                            check_deploy(inner, root, state)
    if head == "make" and any(SCRIPT_NAMES.match(a) for a in rest if not a.startswith("-")):
        refuse(
            root, "deploy", detail, DEPLOY_ROUTE + " A make target named like a deploy is a deploy."
        )


def package_script(cwd, name):
    try:
        with open(os.path.join(cwd, "package.json")) as fh:
            data = json.load(fh)
        body = (data.get("scripts") or {}).get(name)
        return body if isinstance(body, str) else None
    except Exception:
        return None


# --------------------------------------------------------------------------- installs

PY_INTERP = re.compile(r"^python\d*(\.\d+)?$")
PIP = re.compile(r"^pip\d*(\.\d+)?$")
NPM_INSTALL_ALIASES = (
    "install",
    "i",
    "in",
    "ins",
    "inst",
    "insta",
    "instal",
    "isnt",
    "isnta",
    "isntal",
    "isntall",
    "add",
)
LOCAL_ARG = re.compile(r"^(\.|\.\.|\./|\.\./|/|~|\[)")


def positional_packages(args, skip_after):
    out = []
    skip = False
    for a in args:
        if skip:
            skip = False
            continue
        if a in skip_after:
            skip = True
            continue
        if a.startswith("-"):
            continue
        if (
            LOCAL_ARG.match(a)
            or a.endswith(".txt")
            or a.endswith(".toml")
            or a.endswith(".lock")
            or a.endswith(".whl")
            or a.endswith(".tar.gz")
        ):
            continue
        if a in ("pip", "setuptools", "wheel"):
            continue
        out.append(a)
    return out


def check_install(toks, root, segment):
    if not toks:
        return
    head = os.path.basename(toks[0])
    rest = toks[1:]
    named = []
    if PIP.match(head) or (
        PY_INTERP.match(head) and (rest[:2] == ["-m", "pip"] or rest[:1] == ["-mpip"])
    ):
        args = (
            rest[2:] if rest[:2] == ["-m", "pip"] else (rest[1:] if rest[:1] == ["-mpip"] else rest)
        )
        if args[:1] == ["install"]:
            named = positional_packages(
                args[1:],
                (
                    "-r",
                    "--requirement",
                    "-e",
                    "--editable",
                    "-c",
                    "--constraint",
                    "-t",
                    "--target",
                    "-i",
                    "--index-url",
                    "--extra-index-url",
                    "-f",
                    "--find-links",
                ),
            )
    elif head == "uv":
        r = skip_options(rest)
        if r[:1] == ["add"]:
            named = positional_packages(
                r[1:], ("--group", "--extra", "--optional", "-r", "--requirements")
            )
        elif r[:2] == ["pip", "install"]:
            named = positional_packages(
                r[2:], ("-r", "--requirement", "-e", "--editable", "-c", "--constraint")
            )
        elif r[:2] == ["tool", "install"] or r[:1] == ["tool"] and r[1:2] == ["run"]:
            named = positional_packages(r[2:], ())
        elif r[:1] == ["run"] and "--with" in r:
            named = [r[r.index("--with") + 1]] if r.index("--with") + 1 < len(r) else []
    elif head == "uvx" or head == "pipx" and rest[:1] in (["run"], ["install"]):
        r = skip_options(rest if head == "uvx" else rest[1:])
        named = positional_packages(r[:1], ())
    elif head == "npm":
        r = skip_options(rest)
        if r[:1] and r[0] in NPM_INSTALL_ALIASES:
            named = positional_packages(r[1:], ())
        elif r[:1] in (["exec"], ["x"]):
            named = positional_packages(skip_options(r[1:])[:1], ())
    elif head in ("npx", "pnpx", "bunx"):
        named = [
            pkg
            for pkg in runner_packages(rest)
            if not local_bin_exists(state_cwd(), package_name(pkg).split("/")[-1])
        ]
        r = skip_runner_options(rest)
        if r and not r[0].startswith("-") and not named:
            # a named package fetched from the registry to run; local devDependencies pass because they resolve locally
            bare = package_name(r[0])
            binary = bare.split("/", 1)[1] if bare.startswith("@") and "/" in bare else bare
            if bare not in KNOWN_BINS and not local_bin_exists(state_cwd(), binary):
                named = [r[0]]
    elif head == "pnpm":
        r = skip_options(rest)
        if r[:1] in (["add"], ["install"], ["i"]):
            named = positional_packages(r[1:], ())
        elif r[:1] in (["dlx"], ["exec"]):
            first = skip_runner_options(r[1:])[:1]
            if (
                r[0] == "exec"
                and first
                and local_bin_exists(state_cwd(), package_name(first[0]).split("/")[-1])
            ):
                first = []
            named = runner_packages(r[1:]) + positional_packages(first, ())
    elif head == "yarn":
        r = skip_options(rest)
        if r[:1] == ["workspace"] and len(r) > 2:
            r = r[2:]
        if r[:1] == ["global"]:
            r = r[1:]
        if r[:1] == ["add"]:
            named = positional_packages(r[1:], ())
        elif r[:1] == ["dlx"]:
            named = positional_packages(skip_options(r[1:])[:1], ())
    elif head == "bun":
        r = skip_options(rest)
        if r[:1] in (["add"], ["a"], ["install"], ["i"]):
            named = positional_packages(r[1:], ())
        elif r[:1] in (["x"],):
            first = r[1:2]
            if first and (
                package_name(first[0]) in KNOWN_BINS
                or local_bin_exists(state_cwd(), package_name(first[0]).split("/")[-1])
            ):
                first = []
            named = positional_packages(first, ())
    elif (
        head == "brew"
        and rest[:1] in (["install"], ["instal"], ["cask"])
        or head == "cargo"
        and rest[:1] in (["add"], ["install"])
        or head == "go"
        and rest[:1] in (["get"], ["install"])
        or head == "gem"
        and rest[:1] == ["install"]
    ):
        named = positional_packages(rest[1:], ())
    elif head in ("poetry", "pdm", "pipenv") and rest[:1] in (["add"], ["install"]):
        named = positional_packages(rest[1:], ("--group", "-G", "-E", "--extras"))
    elif head in ("apt", "apt-get", "conda", "mamba") and rest[:1] == ["install"]:
        named = positional_packages(rest[1:], ("-n", "--name", "-c", "--channel"))
    if not named:
        return
    card = leading_assignments(segment).get("MILUX_ALLOW_INSTALL", "")
    if CARD_SHAPE.match(card or ""):
        log(root, "ALLOWED install card=" + card, " ".join(toks))
        return
    refuse(
        root,
        "install",
        " ".join(toks),
        "Installing or running {} from a registry is refused: an agent never adds a dependency unverified (agents invent package "
        "names that attackers pre-register). Verify each package on the real registry, record it on the card, then rerun the same "
        "command with MILUX_ALLOW_INSTALL=<card number> immediately in front of it; the override is logged.".format(
            ", ".join(named)
        ),
    )


_STATE = {"cwd": None}


def state_cwd():
    return _STATE["cwd"] or os.getcwd()


def local_bin_exists(cwd, name):
    return bool(name) and os.path.exists(os.path.join(cwd, "node_modules", ".bin", name))


def package_name(spec):
    """@scope/pkg@1.2 -> @scope/pkg; pkg@1.2 -> pkg"""
    if spec.startswith("@"):
        return "@" + spec[1:].split("@", 1)[0]
    return spec.split("@", 1)[0]


# --------------------------------------------------------------------------- scripts from the network

URL_FETCH = re.compile(r"\b(curl|wget)\b")
SUBST_FROM_URL = re.compile(
    r"(?:\b(?:bash|sh|zsh|dash|ksh|eval|source|python\d*(?:\.\d+)?|node|perl|ruby)\b|(?:^|\s)\.)\s+(?:-[-a-zA-Z]+\s+)*[\"']?\$\(\s*(?:\S*/)?(?:curl|wget)\b"
)
PROCSUB_FROM_URL = re.compile(
    r"(?:\b(?:bash|sh|zsh|dash|ksh|source|python\d*(?:\.\d+)?|node)\b|(?:^|\s)\.)\s*<?\s*<\(\s*(?:\S*/)?(?:curl|wget)\b"
)
URL_ROUTE = (
    "A script fetched from the network never runs unread. Download it to a file (curl -o), read it, and run the file "
    "under a card that names the dependency and its source."
)


def check_script_from_url(command, root, stages):
    if SUBST_FROM_URL.search(command) or PROCSUB_FROM_URL.search(command):
        refuse(root, "script-from-url", command, URL_ROUTE)
    fetched = False
    for st in stages:
        toks = tokens_of(st)
        if not toks:
            continue
        head = os.path.basename(toks[0])
        if head in ("curl", "wget") and any(not a.startswith("-") for a in toks[1:]):
            fetched = True
            continue
        if fetched and head in INTERPRETERS or fetched and PY_INTERP.match(head):
            args = [a for a in toks[1:]]
            # an interpreter reading the stream as a program: no script argument, or only mode flags
            harmless = any(
                a in ("-m", "--version", "-V") or a.endswith(".py") or a.endswith(".js")
                for a in args
            )
            if not harmless:
                refuse(root, "script-from-url", command, URL_ROUTE)
        if fetched and head in ("tee", "cat", "gunzip", "gzip", "tar", "base64", "xz", "zcat"):
            continue


# --------------------------------------------------------------------------- shell writes into protected paths

WRITE_ALL_ARGS = (
    "rm",
    "tee",
    "chmod",
    "chown",
    "truncate",
    "touch",
    "patch",
    "unlink",
    "rmdir",
    "shred",
    "ln",
)
WRITE_LAST_ARG = ("cp", "mv", "rsync", "install")
REDIRECT = re.compile(
    r"(?:^|[^<>&|])(\d*>{1,2}\|?|&>>?)\s*((?:\\.|\"[^\"]*\"|'[^']*'|[^\s;&|)}<>])+)"
)


def check_shell_writes(toks, segment, root, patterns, state):
    if not toks:
        return
    seen = state.setdefault("seen", [])
    for c in (state["cwd"], state.get("base_cwd")):
        if c and c not in seen:
            seen.append(c)
    for cwd in list(seen):
        check_shell_writes_from(toks, segment, root, patterns, cwd, state)


def check_shell_writes_from(toks, segment, root, patterns, cwd, state):
    head = os.path.basename(toks[0])
    targets = []
    for m in REDIRECT.finditer(segment):
        tgt = m.group(2)
        try:
            parts = shlex.split(tgt, posix=True)
            tgt = parts[0] if parts else tgt
        except ValueError:
            tgt = tgt.strip("'\"")
        if tgt.startswith("&") or tgt == "/dev/null":
            continue
        targets.append(tgt)
    args = [t for t in toks[1:] if not t.startswith("-")]
    sub = ""
    if head == "git":
        sub, gargs, _, _ = git_subcommand(toks)
        if sub in ("checkout", "restore", "rm", "mv", "clean", "apply", "am", "stash"):
            args = [a for a in gargs if not a.startswith("-")]
            if sub == "clean":
                if any(
                    a in ("-n", "--dry-run")
                    or (a.startswith("-") and not a.startswith("--") and "n" in a)
                    for a in gargs
                ):
                    pass
                elif args:
                    targets.extend(args)
                else:
                    targets.append(".")
            else:
                targets.extend(args)
    elif head in WRITE_ALL_ARGS:
        targets.extend(args)
    elif head in WRITE_LAST_ARG:
        if len(args) >= 2:
            dest = args[-1]
            targets.append(dest)
            if head == "mv":
                targets.extend(args[:-1])
            dest_rel = relative_to_root(dest.strip("'\""), root, cwd)
            if dest_rel is not None and (
                os.path.isdir(os.path.join(root, dest_rel)) or dest.endswith("/")
            ):
                for src in args[:-1]:
                    targets.append(os.path.join(dest, os.path.basename(src.rstrip("/"))))
    elif head == "sed":
        if any(
            t == "-i" or t.startswith("-i") or t == "--in-place" or t.startswith("--in-place")
            for t in toks[1:]
        ):
            targets.extend(args)
    elif head == "perl":
        if any(t.startswith("-p") and "i" in t or t.startswith("-i") for t in toks[1:]):
            targets.extend(args)
    elif head == "dd":
        for t in toks[1:]:
            if t.startswith("of="):
                targets.append(t[3:])
    bases = protected_bases(patterns)
    exact_names = [p for p in patterns if "*" not in p and "?" not in p]
    for raw in targets:
        t = raw.strip("'\"")
        spanning = t in (".", "./", "*", "./*", ".*", "..", "../", "../*")
        if not spanning and re.search(r"[*?\[{]", t):
            head_part = re.split(r"[*?\[{]", t, maxsplit=1)[0]
            dir_part = head_part if head_part.endswith("/") else os.path.dirname(head_part)
            dir_rel = relative_to_root(dir_part or ".", root, cwd)
            if dir_rel is None:
                dir_rel = "outside"
            dir_rel = norm_rel(dir_rel)
            if dir_rel in (".", ""):
                spanning = True
            else:
                low = dir_rel.lower()
                for b in bases + [os.path.dirname(n) for n in exact_names]:
                    bl = b.lower()
                    if bl and (low == bl or bl.startswith(low + "/") or low.startswith(bl + "/")):
                        spanning = True
                        break
        if spanning:
            if head in (
                "rm",
                "mv",
                "chmod",
                "chown",
                "rsync",
                "cp",
                "shred",
                "truncate",
                "tee",
                "ln",
            ) or sub in ("clean", "checkout", "restore", "rm"):
                card = unlock_card(root)
                if card:
                    log(root, "ALLOWED protected-shell card=" + card, segment)
                    return
                refuse(
                    root,
                    "protected-path",
                    segment,
                    "A write that spans the repository root, a parent directory or a wildcard next to a protected path would reach protected files. Name the files you mean.",
                )
            if re.search(r"[*?\[{]", t):
                continue
        rel = relative_to_root(t, root, cwd)
        if rel is None:
            continue
        rel = norm_rel(rel)
        hit = is_protected(rel, patterns)
        if hit is None:
            low = rel.lower()
            for b in bases:
                bl = b.lower()
                if low == bl or bl.startswith(low + "/") or low.startswith(bl + "/"):
                    hit = b
                    break
        if hit:
            card = unlock_card(root)
            if card:
                log(root, "ALLOWED protected-shell card=" + card, segment)
                return
            refuse(
                root,
                "protected-path",
                segment,
                f"{rel} is a protected path ({hit}). Changes to it need a card that names the change and Matt's approval on the pull "
                "request: ask Matt to write the card number into .claude/hooks/UNLOCK for this session, then retry. "
                "Reading it is open to you.",
            )


# --------------------------------------------------------------------------- the bash pass


def apply_cd(toks, state, root):
    """Track cd, pushd, popd and cd - across segments. A directory that does not exist is not
    entered (bash stays put when cd fails). Every write is judged against the tracked directory
    and the directory the tool call started in, so a subshell cd or a wrong guess cannot hide a
    protected target."""
    head = os.path.basename(toks[0]) if toks else ""
    if head in ("cd", "pushd"):
        target = None
        for a in toks[1:]:
            if a == "-" or not a.startswith("-"):
                target = a
                break
        stack = state.setdefault("stack", [])
        if target == "-":
            prev = state.get("prev")
            if prev:
                state["prev"], state["cwd"] = state["cwd"], prev
            return True
        if target is None:
            new = os.path.expanduser("~")
        elif "$" in target or "`" in target:
            new = root  # unknown at hook time; judged from the root, and the start cwd is judged as well
        else:
            target = os.path.expanduser(target.strip("'\""))
            new = target if os.path.isabs(target) else os.path.join(state["cwd"], target)
        new = os.path.realpath(new)
        if not os.path.isdir(new):
            return True  # cd fails at run time; the shell stays where it was
        if head == "pushd":
            stack.append(state["cwd"])
        state["prev"] = state["cwd"]
        state["cwd"] = new
        _STATE["cwd"] = new
        seen = state.setdefault("seen", [])
        if new not in seen:
            seen.append(new)
        return True
    if head == "popd":
        stack = state.setdefault("stack", [])
        if stack:
            state["prev"] = state["cwd"]
            state["cwd"] = stack.pop()
        return True
    return False


# --------------------------------------------------------------------------- programs and heredocs

PROGRAM_HEAD = re.compile(r"^(?:python\d*(?:\.\d+)?|node|nodejs|deno|bun|perl|ruby)$")
# What a program writes with: a file opened for writing, a file written whole, a move, copy,
# removal or link. By language, so prose in another language's strings does not count.
PROGRAM_WRITES = {
    "python": re.compile(
        r"\bopen\s*\((?:[^()]|\([^()]*\))*?['\"][rbt]*[wax+][rwabxt+]*['\"]"
        r"|\bopen\s*\((?:[^()]|\([^()]*\))*?\bmode\s*="
        r"|\.(?:write_text|write_bytes|touch|unlink|rename|replace|rmdir|symlink_to|hardlink_to|chmod)\s*\("
        r"|\bshutil\.(?:copy\w*|move|rmtree)\b"
        r"|\bos\.(?:remove|unlink|rename|replace|rmdir|removedirs|makedirs|mkdir|symlink|link|truncate|chmod|chown|utime)\s*\("
    ),
    "node": re.compile(
        r"\b(?:writeFile|appendFile|createWriteStream|rename|unlink|rmdir|rm|copyFile|cp|truncate|symlink|chmod|mkdir|open)(?:Sync)?\s*\("
    ),
    "perl": re.compile(r"\bopen\s*\(?[^;]*?['\"]\+?>{1,2}|\b(?:unlink|rename|truncate|rmdir|symlink|chmod)\b|\bcopy\s*\(|\bmove\s*\("),
    "ruby": re.compile(r"\bFile\.(?:write|open|rename|delete|unlink|binwrite|symlink|chmod)\b|\bFileUtils\.|\bIO\.(?:write|binwrite)\b"),
}
STRING_LITERAL = re.compile(r"(?<![A-Za-z0-9_])(?:[rRbBfFuU]{0,2})(['\"])([^'\"\s]{1,300})\1")


def program_language(head):
    if head.startswith("python"):
        return "python"
    if head in ("node", "nodejs", "deno", "bun"):
        return "node"
    return head


def protected_literal(text, root, cwd, patterns):
    """The first string literal in `text` that is itself a protected path (as written, or any
    tail of it after a slash, so a worktree's absolute path counts), or None. A path inside a
    sentence is prose, not a target, and does not count."""
    bases = [b.lower() for b in protected_bases(patterns)]
    for m in STRING_LITERAL.finditer(text):
        lit = m.group(2)
        if "/" not in lit and "." not in lit:
            continue  # a word or a number, not a path
        rel = relative_to_root(os.path.expanduser(lit), root, cwd) if lit.startswith(("/", "~", ".")) else None
        candidates = [norm_rel(rel)] if rel else []
        tail = lit.lstrip("/")
        while tail:
            candidates.append(norm_rel(tail))
            cut = tail.find("/")
            if cut < 0:
                break
            tail = tail[cut + 1 :]
        for c in candidates:
            if is_protected(c, patterns) or c.lower().rstrip("/") in bases:
                return lit
    return None


def check_programs(command, root, patterns, state):
    """A program a command runs through an interpreter (a heredoc, -c or -e text, or a script file
    named on the line) that writes files and names a protected path is judged as a shell write to
    it (11 October 2026: a python heredoc changed a protected file with no UNLOCK). The guard reads
    the program, not what it computes: a path built at run time from pieces is not seen."""
    texts = []
    for seg, stages in pipelines(strip_heredocs(command)):
        for st in stages:
            toks = tokens_of(st)
            if not toks:
                continue
            i = 0
            while i < len(toks) and (toks[i] in SHELL_WORDS or re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", toks[i])):
                i += 1
            if i >= len(toks):
                continue
            head = os.path.basename(toks[i])
            if not PROGRAM_HEAD.match(head):
                continue
            lang = program_language(head)
            texts.append((lang, command))  # heredoc bodies and inline text
            for t in toks[i + 1 :]:
                if t.startswith("-"):
                    continue
                path = os.path.join(state["cwd"], os.path.expanduser(t)) if not os.path.isabs(os.path.expanduser(t)) else os.path.expanduser(t)
                if os.path.isfile(path) and os.path.getsize(path) < 1_000_000:
                    try:
                        with open(path, errors="replace") as fh:
                            texts.append((lang, fh.read()))
                    except OSError:
                        pass
                break
    for lang, text in texts:
        writes = PROGRAM_WRITES.get(lang)
        if not writes or not writes.search(text):
            continue
        lit = protected_literal(text, root, state["cwd"], patterns)
        if not lit:
            continue
        card = unlock_card(root)
        if card:
            log(root, "ALLOWED protected-program card=" + card, command[:500])
            return
        refuse(
            root,
            "protected-path",
            command[:500],
            f"This program writes files and names {lit}, a protected path. Changes to it need a card that names "
            "the change and Matt's approval on the pull request: ask Matt to write the card number into "
            ".claude/hooks/UNLOCK for this session, then retry. Reading it is open to you.",
        )


def shell_heredoc_bodies(command):
    """The bodies of heredocs fed to a shell (bash <<EOF ... EOF): commands, so they are judged."""
    bodies = []
    lines = command.split("\n")
    i = 0
    while i < len(lines):
        marker = heredoc_marker(lines[i])
        if marker:
            opening = lines[i]
            body = []
            i += 1
            while i < len(lines) and lines[i].strip() != marker:
                body.append(lines[i])
                i += 1
            if re.search(r"(?:^|[\s;&|(])(?:\S*/)?(?:bash|sh|zsh|dash|ksh)\b[^|;&]*<<", opening):
                bodies.append("\n".join(body))
        i += 1
    return bodies


def run_bash_checks(command, root, patterns, state, depth=0):
    if depth > 3:
        refuse(
            root,
            "nesting",
            command,
            "Nested more deeply than the guard reads (bash -c inside eval inside bash -c). Flatten the command so each step is visible; push your branch and open a pull request as plain steps.",
        )
    check_programs(command, root, patterns, state)
    for body in shell_heredoc_bodies(command):
        run_bash_checks(body, root, patterns, state, depth + 1)
    command = strip_heredocs(command)
    for seg, stages in pipelines(command):
        check_script_from_url(seg, root, stages)
        for st in stages:
            toks = tokens_of(st)
            if not toks:
                continue
            if apply_cd(toks, state, root):
                continue
            head = os.path.basename(toks[0])
            if head in INTERPRETERS[:5] and len(toks) >= 3 and toks[1] == "-c":
                run_bash_checks(toks[2], root, patterns, state, depth + 1)
                continue
            if head == "eval" and len(toks) >= 2:
                run_bash_checks(" ".join(toks[1:]), root, patterns, state, depth + 1)
                continue
            if head in ("npx", "pnpx", "bunx", "npm", "pnpm", "yarn", "bun"):
                for i, t in enumerate(toks[1:], 1):
                    if t in ("-c", "--call") and i + 1 < len(toks):
                        run_bash_checks(toks[i + 1], root, patterns, state, depth + 1)
                    elif t.startswith("--call="):
                        run_bash_checks(t.split("=", 1)[1], root, patterns, state, depth + 1)
            state["assignments"] = leading_assignments(st)
            if head == "git":
                check_git(toks, root, state)
            elif head == "gh":
                check_gh(toks, root)
            check_deploy(toks, root, state)
            check_install(toks, root, st)
            check_shell_writes(toks, st, root, patterns, state)
            if head == "export" and any(
                a.upper().startswith(("GIT_CONFIG", "GIT_DIR", "GIT_WORK_TREE", "GIT_SSH"))
                for a in toks[1:]
            ):
                refuse(
                    root,
                    "config",
                    st,
                    "Configuring git through the environment is not done by an agent. Use plain git commands on your branch.",
                )


def pre_bash(payload, root):
    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str) or not command.strip():
        return
    cwd = payload.get("cwd") or root
    state = {
        "cwd": os.path.realpath(cwd),
        "base_cwd": os.path.realpath(cwd),
        "branch_override": None,
        "stack": [],
        "prev": None,
    }
    _STATE["cwd"] = state["cwd"]
    patterns = load_protected(root)
    run_bash_checks(command, root, patterns, state)


# --------------------------------------------------------------------------- the edit pass


def pre_edit(payload, root):
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not isinstance(path, str) or not path:
        return
    cwd = payload.get("cwd") or root
    rel = relative_to_root(path, root, cwd)
    if rel is None:
        log(root, "NOTE outside-project edit", path)
        return
    patterns = load_protected(root)
    hit = is_protected(rel, patterns)
    if hit is None:
        return
    card = unlock_card(root)
    if card:
        log(root, "ALLOWED protected-edit card=" + card, rel)
        return
    refuse(
        root,
        "protected-path",
        rel,
        f"{rel} is a protected path ({hit}). Edits to it need a card that names the change and Matt's approval on the "
        "pull request: ask Matt to write the card number into .claude/hooks/UNLOCK for this session, then retry. "
        "Say on the card what you wanted to change and why.",
    )


# --------------------------------------------------------------------------- main


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pre-bash"
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    root = project_dir(payload)
    if not raw.strip() or payload == {}:
        log(root, "NOTE", f"no usable hook payload for {mode}; allowed")
        return
    try:
        if mode == "pre-edit":
            pre_edit(payload, root)
        else:
            pre_bash(payload, root)
    except SystemExit:
        raise
    except Exception as exc:
        log(root, "FAULT", f"{mode}: {exc!r}")
        sys.stderr.write(
            "MilUX guard: internal fault, logged to .claude/hooks/guard.log; the call was allowed. Tell Matt.\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
