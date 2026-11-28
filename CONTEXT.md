# Foothold: words and what they mean

The glossary for this repository.

| Word | Meaning here |
|---|---|
| Foothold | The pack: this repository, and the vault it installs. Named for a secure initial position in hostile territory. |
| Pack | The installable whole: template, skills and setup. Foothold and Footing are sibling packs. |
| Footing | The sibling pack for established businesses outside defence (`MilUX-Ltd/footing`). Changes to shared skills usually land in both. |
| Tally | MilUX's public directory of defence companies (`MilUX-Ltd/tally`). Foothold users may read it; Foothold does not depend on it. |
| Template | `foothold/template/`: the files a user's vault receives at setup and update. |
| Vault | The user's installed copy of the template, a folder of Markdown opened in Obsidian. |
| Setup | `foothold-setup`: lays the vault down from the template and runs onboarding. The README says how to start it. |
| Update | `/foothold-update`, the vault-bundled skill that compares the vault with the latest release and applies changed template files only with the user's yes, never overwriting their own work. |
| `release_hashes`, `vault_hashes` | The update skill's record, in the vault's `.foothold/config.yml`, of each file's SHA-256: as in the release it came from, and as written into the vault. Used to tell a user's edit from a release's change. |
| `declined_by_person` | The update's record of the changes the person said no to, with `release_hashes` holding the release they said no to. Not asked again for that release; asked about singly when a later release changes the file. |
| `last_known_shas` | The record vaults set up before 2.5.0 hold instead: git blob SHA-1s. The update reads it once and records SHA-256 from then on. |
| `{{pack_owner}}` | The placeholder replaced with the user's name at setup. Files carrying it are listed by hand in the update skill. One of setup's placeholders. |
| Guide file | The `<Folder> Guide.md` page in every template folder, saying what goes there. |
| Skill | A `SKILL.md` folder under `Skills/` that Claude runs inside the vault. |
| Cowork | Anthropic's desktop app in which the pack is designed to run alongside Obsidian. |
| Release | A tag `vX.Y.Z` on `main`, matching the version in `CHANGELOG.md`, `plugin.json`, `marketplace.json` and `data/foothold-map.json`. The release workflow publishes it as a GitHub release with three files: the zip, `SHA256SUMS.txt` and `release-files.txt` (ADR 003). Users receive only releases. |
| `release-files.txt` | The list of every file in a release zip with its SHA-256, other than itself. Published beside the zip and carried at the top of the zip's folder, the same bytes. The copy inside the zip lets the update check an unzipped folder and do its bookkeeping; it shows damage, not who made the zip. |
| Folder's own list | The `release-files.txt` inside an unzipped release folder the person vouched for. The update's helper uses it when there is no downloaded list, and refuses the folder if any file in it is missing, extra or different. |
| File-name form | The form of the person's name and of their organisation's name used in file names (`pack_owner_file`, `pack_org_file` in the record): accents dropped, every character the path rule refuses replaced by a space, trimmed. The value itself stays as given in page text. |
| Setup's placeholders | The fixed list, in the setup skill, of the placeholders setup fills at install (`{{pack_owner}}`, `{{install_date}}` and the rest). Placeholders other skills fill, such as mobilise-engagement's and write-sow's, are listed there as not setup's. `tools/check.py` fails on a template placeholder that is on neither list. |
| Start Here | `foothold/Start Here.md`, the entry point in every release zip, for the person and for their AI tool. It names the version. |
| Release zip | `foothold-X.Y.Z.zip`, built by `tools/build_release.py`. Only zips the release workflow builds from a tag may be offered to users. |
