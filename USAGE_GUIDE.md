# 🚀 Module Release & Changelog Guide

## ✅ How to Use

1. Make commits using [Conventional Commit](https://www.conventionalcommits.org/) syntax:
   - `feat(random-pet): add name_prefix option`
   - `fix(random-pet): correct variable type`
   - `chore(random-pet): update docs`
   - Use `!` for breaking changes: `feat(random-pet)!: remove deprecated var`

2. Run the script to bump version & generate changelog:

```bash
python scripts/bump_and_changelog.py random-pet
```

3. The script will:
   - Determine version bump (major/minor/patch)
   - Update `random-pet/version.txt`
   - Update `random-pet/CHANGELOG.md`
   - Create Git tag `random-pet/vX.Y.Z`
   - Commit & push the changes and tag

## 📦 Requirements
- Git must be initialized
- Each module must have:
  - `version.txt` (e.g. `0.1.0`)
  - Committed files under its folder (e.g. `random-pet/`)

## 🔄 Versioning Rules

| Commit Example                                   | Resulting Bump |
|--------------------------------------------------|----------------|
| `fix(random-pet): fix typo`                     | Patch          |
| `feat(random-pet): add name`                    | Minor          |
| `feat(random-pet)!: remove critical variable`   | Major          |

Happy versioning!