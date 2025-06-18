#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def run(cmd):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def release_module(module):
    os.chdir(module)
    print(f"🚀 Releasing module: {module}")

    # Ensure CHANGELOG.md exists
    Path("CHANGELOG.md").touch()

    # Run commitizen bump (generates changelog and tag)
    run([
        "cz", "bump",
        "--yes",
        "--changelog",
        "--tag-format", f"{module}/v$version"
    ])

    os.chdir("..")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: release_module.py <module>")
        sys.exit(1)

    release_module(sys.argv[1])
    print("Module released successfully!")