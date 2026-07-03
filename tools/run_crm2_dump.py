#!/usr/bin/env python3
"""Attach the CRM2 Frida dumper to Cookie Run."""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "tools" / "crm2_frida_dump.js"
LOCAL_FRIDA = ROOT / ".venv-frida" / "bin" / "frida"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--package", default="com.devsisters.CookieRunForKakao")
    p.add_argument("--no-spawn", action="store_true")
    args = p.parse_args()

    frida = str(LOCAL_FRIDA) if LOCAL_FRIDA.exists() else shutil.which("frida")
    if not frida:
        raise SystemExit("frida not found; run: python3 -m venv .venv-frida && .venv-frida/bin/pip install frida-tools")

    cmd = [frida, "-U", "-l", str(HOOK)]
    cmd += ["-n", args.package] if args.no_spawn else ["-f", args.package]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
