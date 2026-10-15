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
| Update | `/foothold-update`, the vault-bundled skill that compares the vault with `main` on GitHub and pulls changed template files without overwriting the user's own work. |
| `last_known_shas` | The update skill's record of each template file's git blob SHA at the last install or update, used to tell a user's edit from an upstream change. |
| `{{pack_owner}}` | The placeholder replaced with the user's name at setup. Files carrying it are listed by hand in the update skill. |
| Guide file | The `<Folder> Guide.md` page in every template folder, saying what goes there. |
| Skill | A `SKILL.md` folder under `Skills/` that Claude runs inside the vault. |
| Cowork | Anthropic's desktop app in which the pack is designed to run alongside Obsidian. |
| Release | A version heading in `CHANGELOG.md`, matched in `plugin.json` (the version file the update skill reads). What users receive is whatever is on `main`. |
