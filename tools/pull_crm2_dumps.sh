#!/bin/sh
set -eu

OUT="${1:-/Users/peach/Documents/Poke/project/cookierun_readable_db/database/crm2_dumps}"
mkdir -p "$OUT"
adb pull /sdcard/Download/cookierun_crm2_dumps "$OUT"
