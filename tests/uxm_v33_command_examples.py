#!/usr/bin/env python3
"""
tests/uxm_v33_command_examples.py

Bu betik `reports/UXM_V33_UXM_S_HAT_KARSI_TR.md` içindeki V33 komut listesini okur
ve her komut için "anlamlı" ve "anlamsız" örnek çağrı/işlem satırı üretir.
Amaç: komutların kullanım örneklerini görsel olarak sunmak (gerçek çağrı yapmaz).

Çalıştırma:
    py -3 tests/uxm_v33_command_examples.py
"""

import re
import argparse
from pathlib import Path

MD = Path('reports/UXM_V33_UXM_S_HAT_KARSI_TR.md')
if not MD.exists():
    print('Rapor bulunamadı:', MD)
    raise SystemExit(1)

text = MD.read_text(encoding='utf-8', errors='replace')
# Bölümü yakala
m = re.search(r"### A\) V33 — Benzersiz komutlar.*?\n\n(.*?)(?:\n### B\) V33 — Çalıştırılabilir anahtarlar|\Z)", text, re.S)
if not m:
    print('V33 komut bölümü bulunamadı.')
    raise SystemExit(1)

commands_block = m.group(1)
commands = [line.strip()[2:] for line in commands_block.splitlines() if line.strip().startswith('- ')]

# Basit simülasyon: komut türüne göre iki örnek çağrı üret
import re

def simulate(cmd):
    if cmd.startswith('OP_'):
        return f"uxm --op {cmd} --src sample.bin --dst out.bin"
    if cmd.startswith('UXS_'):
        return f"uxm_s --task {cmd} --json state.json"
    if cmd in ('sin','cos','tan','sqrt','exp','log','pow','abs','neg'):
        return f"math_eval --fn {cmd} --arg 3.14"
    if re.match(r'^(r|r[0-9]+|rax|rbx|rcx|rdx|rsi|rdi|r8|r9|r10|r11|r12|r13|r14|r15)$', cmd, re.I):
        return f"regtool --set {cmd} 0x12345678"
    # tek karakterli semboller
    if len(cmd) == 1 and not cmd.isalnum():
        esc = cmd.replace('\\', '\\\\')
        return f"eval --expr '1 {esc} 2'"
    return f"uxm --cmd {cmd} --help"


def main():
    parser = argparse.ArgumentParser(description='Generate examples for V33 commands and optionally write meaningful ones to a file.')
    parser.add_argument('-o', '--out', default='uxm', help='Output file to write (default: uxm)')
    parser.add_argument('--mode', choices=['meaningful', 'both'], default='meaningful', help='Write only meaningful commands or both meaningful and nonsense')
    args = parser.parse_args()

    out_path = Path(args.out)
    lines_to_write = []

    for cmd in commands:
        safe = re.sub(r'[^0-9A-Za-z_]', '_', cmd)
        meaningful = simulate(cmd)
        nonsense = f"run_random --{safe} foo bar"

        print('===', cmd)
        print('Meaningful:', meaningful)
        print('Nonsense:  ', nonsense)
        print()

        if args.mode in ('meaningful', 'both'):
            lines_to_write.append(meaningful)
        if args.mode == 'both':
            lines_to_write.append(nonsense)

    if lines_to_write:
        out_path.write_text('\n'.join(lines_to_write), encoding='utf-8')
        print(f"Wrote {len(lines_to_write)} lines to {out_path}")

if __name__ == '__main__':
    main()
