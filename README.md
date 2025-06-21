# SourceRoot Labs Terraform Modules

SourceRoot Labs Terraform modules

## Module Release & Changelog Automation

This repository uses [Google's Release Please](https://github.com/googleapis/release-please) to automate versioning and changelog generation for each Terraform module.

Each module is versioned and released independently using tags like `random-pet-v1.0.0`. The process is fully automated using [GitHub Actions](https://github.com/marketplace/actions/release-please-action) and is driven by **Conventional Commit** messages.

---

### How It Works

1. You make commits to a module using [Conventional Commit syntax](https://www.conventionalcommits.org/):
   ```bash
   feat(random-pet): Add name_prefix option
   fix(random-pet): Fix typo in variable default
   chore(random-pet): Update README
   feat(random-pet)!: Remove deprecated variable
   ```

2. When a PR is merged to `main`, Release Please will:
   - Parse commits to determine the version bump (major, minor, patch)
   - Update or create `CHANGELOG.md` under the module folder (e.g., `random-pet/CHANGELOG.md`)
   - Tag the release with the appropriate version (e.g., `random-pet-v1.2.0`)
   - Open a release PR with all updates. This PR must be merged to complete the release.
   - Publish a GitHub Release

---

### Release Strategy

| Situation                                        | Strategy                |
|--------------------------------------------------|-------------------------|
| Production-ready module, first release           | Use `release-as: 1.0.0` |
| Experimental or evolving module                  | Start at `0.1.0`        |
| Breaking changes after initial release           | Use `!` in commit       |

**Note:** For modules using the [`terraform-module`](https://github.com/googleapis/release-please/blob/main/src/strategies/terraform-module.ts) release strategy, even a `!` in the initial commit will not trigger a `1.0.0` release. The strategy defaults the first release version to `0.1.0`. To start at `1.0.0`, you must explicitly include `release-as: 1.0.0` in your commit message.


#### Example for Initial Release:

```bash
git commit -m "feat(random-pet): Initial release." -m "release-as: 1.0.0"
```

> The `release-as` directive in the commit body forces the version bump to `1.0.0`.

### Adding a New Module

To add a new module (e.g., `awesome-module`):

1. Create a new directory: `awesome-module/`
2. Add Terraform code and a `README.md`
3. Add an entry to `release-please-config.json`:

```json
{
  "packages": {
    "awesome-module": {
      "release-type": "terraform-module",
      "package-name": "awesome-module",
      "changelog-path": "CHANGELOG.md",
      "include-component-in-tag": true
    }
  }
}
```

4. Add the starting version to `.release-please-manifest.json`:
   - Use `"0.9.9"` if releasing as stable immediately (forces `1.0.0`)
   - Use `"0.0.0"` to start from scratch (will bump to `0.1.0`)

```json
{
  "awesome-module": "0.9.9"
}
```

5. Merge to `main` with a conventional commit to trigger the process.

### Commit Message Tips

| Commit Type            | Example                                         | Release Effect |
|------------------------|--------------------------------------------------|----------------|
| `feat`                 | `feat(mod): Add resource for X`                 | Minor          |
| `fix`                  | `fix(mod): Correct logic for Y`                 | Patch          |
| `feat!` or `fix!`      | `feat(mod)!: Rename variable Z`                 | Major          |
| `release-as` (initial) | `feat(mod): Initial release release-as: 1.0.0`  | Forces version |

**Note:** Use your module name as the scope to trigger versioning for the right module.

### Other Commit Types & When They Matter

In addition to `feat` and `fix`, the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification allows a variety of other commit types to help clarify the purpose of changes. Some common examples include:

- `docs`: For documentation changes (e.g., updating the README or inline comments)
- `refactor`: For code changes that neither fix a bug nor add a feature
- `chore`: For maintenance or tooling updates

By default, these commit types **do not trigger a version bump or changelog entry** when used alone. However:

- ✅ If the commit **also includes a `!`** or a `BREAKING CHANGE:` footer, it **will trigger a major version bump**
- ✅ If such commits are **mixed in a PR alongside `feat` or `fix` commits**, they will appear in the generated changelog

This ensures semantic versioning stays accurate while still allowing granular tracking of work.

#### Examples

```bash
# No release triggered
docs(readme): Update usage section.

# No release triggered
refactor(module): Simplify internal logic.

# No release triggered
chore(ci): Update GitHub Actions versions.

# Triggers MAJOR release due to breaking change
refactor!: Change module output structure.

# Triggers MINOR release, both commits show in changelog
docs(module): Document new variable.
feat(module): Add support for tags.
```

### Conventional Commit Linting

We enforce commit message linting on pull requests using GitHub Actions.

PRs that do not follow the [Conventional Commit](https://www.conventionalcommits.org/) format will fail CI and be blocked from merging.

### Merging Strategy

**Recommended:** Use **squash and merge**.

- ✅ It keeps the `main` branch history clean.
- ✅ The final squash commit message is the **one that determines version bump**.
- ❗ Make sure to edit the squash message to follow Conventional Commit format, even if PR contributors didn’t.

If using **merge commits** instead, ensure all commits in the PR follow the format — otherwise Release Please may skip versioning or behave unexpectedly.

---

### Useful References

- [Release Please Documentation](https://github.com/googleapis/release-please)
- [release-please-action GitHub Action](https://github.com/google-github-actions/release-please-action)
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [Semantic Versioning (SemVer)](https://semver.org/)
- [release-as directive usage](https://github.com/googleapis/release-please#release-as-commits)
