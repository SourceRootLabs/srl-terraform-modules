#!/usr/bin/env python3
import subprocess
import sys
import re
from pathlib import Path
from datetime import datetime
import os

# Commit types and their changelog sections
SECTIONS = {
    "feat": "### Features",
    "fix": "### Fixes",
    "chore": "### Chores",
    "refactor": "### Refactors",
}


def run_git(cmd):
    return subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()


def get_last_tag(module):
    tags = run_git(["git", "tag"]).splitlines()
    pattern = re.compile(rf"^{module}/v(\d+\.\d+\.\d+)$")
    versions = [tag for tag in tags if pattern.match(tag)]
    if not versions:
        return None
    return sorted(
        versions, key=lambda x: list(map(int, x.split("/")[-1][1:].split(".")))
    )[-1]


def get_commits_since(tag, module):
    path_filter = f"{module}/"
    if tag:
        cmd = ["git", "log", f"{tag}..HEAD", "--pretty=format:%s", "--", path_filter]
    else:
        cmd = ["git", "log", "--pretty=format:%s", "--", path_filter]
    return run_git(cmd).splitlines()


def determine_bump(commits):
    level = "patch"
    for msg in commits:
        if "BREAKING CHANGE" in msg or re.match(r"^.*!:.*", msg):
            return "major"
        if msg.startswith("feat("):
            level = "minor"
    return level


def bump_version(current, level):
    major, minor, patch = map(int, current.split("."))
    if level == "major":
        return f"{major+1}.0.0"
    elif level == "minor":
        return f"{major}.{minor+1}.0"
    return f"{major}.{minor}.{patch+1}"


def parse_changelog(commits, module):
    sections = {v: [] for v in SECTIONS.values()}
    for msg in commits:
        for ctype, header in SECTIONS.items():
            if msg.startswith(f"{ctype}({module}):"):
                clean_msg = msg.split("):", 1)[1].strip()
                sections[header].append(f"- {clean_msg}")
                break
    return sections


def update_changelog(module, new_version, sections):
    changelog_path = Path(module) / "CHANGELOG.md"
    date = datetime.today().strftime("%Y-%m-%d")
    version_header = f"# {new_version} ({date})"

    # Build changelog body from sections
    body = "".join(
        f"{header}{chr(10).join(lines)}" for header, lines in sections.items() if lines
    )
    new_entry = f"{version_header}{body}"

    # Ensure changelog has a main heading
    if changelog_path.exists():
        content = changelog_path.read_text()
        if not content.startswith(f"# Change Log - {module}"):
            content = f"# Change Log - {module}" + content
    else:
        content = f"# Change Log - {module}"

    changelog_path.write_text(f"{content}{new_entry}")
    date = datetime.today().strftime("%Y-%m-%d")
    header = f"# {new_version} ({date})\n"
    body = "\n".join(
        f"{header}\n{chr(10).join(lines)}"
        for header, lines in sections.items()
        if lines
    )
    existing = changelog_path.read_text() if changelog_path.exists() else ""
    changelog_path.write_text(f"{header}\n{body}\n\n{existing}")


def write_version(module, version):
    version_path = Path(module) / "version.txt"
    version_path.write_text(version + "\n")


def tag_module(module, version):
    run_git(["git", "add", f"{module}/CHANGELOG.md", f"{module}/version.txt"])
    run_git(["git", "commit", "-m", f"chore({module}): release v{version}"])
    run_git(["git", "tag", f"{module}/v{version}"])
    run_git(["git", "push"])
    run_git(["git", "push", "--tags"])


def main():
    if len(sys.argv) != 2:
        print("Usage: bump_and_changelog.py <module>")
        sys.exit(1)

    module = sys.argv[1]
    version_file = Path(module) / "version.txt"

    if not version_file.exists():
        print(f"Missing version.txt in {module}")
        sys.exit(1)

    current_version = version_file.read_text().strip()
    last_tag = get_last_tag(module)
    commits = get_commits_since(last_tag, module)

    if not commits:
        print("No new commits to release.")
        sys.exit(0)

    bump_type = determine_bump(commits)
    new_version = bump_version(current_version, bump_type)
    changelog_sections = parse_changelog(commits, module)

    write_version(module, new_version)
    update_changelog(module, new_version, changelog_sections)
    tag_module(module, new_version)
    print(f"✅ Released {module}/v{new_version}")


if __name__ == "__main__":
    main()
