# 🚀 Module Release & Changelog Guide

## ✅ How to Use

1. Make commits using [Conventional Commit](https://www.conventionalcommits.org/) syntax:
   - `feat(random-pet): Add name_prefix option.`
   - `fix(random-pet): Correct variable type.`
   - `chore(random-pet): Update docs.`
   - Use `!` for breaking changes: `feat(random-pet)!: Remove deprecated var.`


3. The script will:
   - Determine version bump (major/minor/patch)
   - Update `random-pet/version.txt`
   - Update `random-pet/CHANGELOG.md`
   - Create Git tag `random-pet/vX.Y.Z`
   - Commit & push the changes and tag

## 📦 Requirements
- Git must be initialized
- Each module must have:
  - Committed files under its folder (e.g. `random-pet/`)

## 🔄 Versioning Rules

| Commit Example                                   | Resulting Bump |
|--------------------------------------------------|----------------|
| `fix(random-pet): Fix typo.`                      | Patch          |
| `feat(random-pet): Add name.`                     | Minor          |
| `feat(random-pet)!: Remove critical variable.`    | Major          |

Happy versioning!