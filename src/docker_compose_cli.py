"""A command-line utility to run Docker Compose with specific profiles"""

import subprocess
import sys

PROFILES = {
    "deps": "dependencies",
    "db": "db",
    "all": "all",
}


def main():
    if len(sys.argv) < 2:
        print("Usage: dc [deps|db|all] [compose-args...]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode not in PROFILES:
        print(f"Invalid mode '{mode}'. Use: deps, db, or all")
        sys.exit(1)

    profile = PROFILES[mode]
    args = sys.argv[2:]

    cmd = ["docker", "compose", "--profile", profile] + args
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


if __name__ == "__main__":
    sys.exit(main())
