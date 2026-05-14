#!/usr/bin/env python3
import csv
import os
import re
from collections import defaultdict

CMD_CSV = os.path.join('reports','UXM_COMMAND_CATALOG.csv')
KEY_CSV = os.path.join('reports','UXM_EXEC_KEYS_CATALOG.csv')
OUT_MD = os.path.join('reports','UXM_V33_UXM_S_HAT_KARSI_TR.md')
UXM_S_CSV = os.path.join('reports','uxm_s_task_key_matrix.csv')

def read_csv(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for r in reader:
            rows.append(r)
    return rows

cmd_rows = read_csv(CMD_CSV)
key_rows = read_csv(KEY_CSV)

# normalize lane values
v33_cmds = set()
v33_keys = set()

hat5_cmds = set()
hat8_cmds = set()

# columns in CMD_CSV: lane,file,command_type,command_value,detail
for r in cmd_rows:
    if len(r) < 4:
        continue
    lane = r[0].strip().lower()
    cmd_val = r[3].strip()
    if lane == 'v33' or lane == 'v33'.lower():
        if cmd_val:
            v33_cmds.add(cmd_val)
    if 'hat5' in lane:
        if cmd_val:
            hat5_cmds.add(cmd_val)
    if 'hat8' in lane:
        if cmd_val:
            hat8_cmds.add(cmd_val)

# columns in KEY_CSV: lane,file,key_type,key,detail
for r in key_rows:
    if len(r) < 4:
        continue
    lane = r[0].strip().lower()
    key = r[3].strip()
    if lane == 'v33':
        if key:
            v33_keys.add(key)

# find uxm_s tasks by scanning files under uxm_s folder for UXS_ tokens
uxs_tasks = set()
uxm_s_keys = set()
uxm_s_sources = set()
pattern = re.compile(r"\bUXS_[A-Za-z0-9_]+\b")
if os.path.isdir('uxm_s'):
    for root,dirs,files in os.walk('uxm_s'):
        for fn in files:
            fp = os.path.join(root,fn)
            try:
                with open(fp,encoding='utf-8',errors='replace') as f:
                    txt = f.read()
                for m in pattern.findall(txt):
                    uxs_tasks.add(m)
            except Exception:
                continue

# collect exec keys related to uxm_s by matching file path in key_rows
for r in key_rows:
    if len(r) < 4:
        continue
    file_path = r[1]
    key = r[3].strip()
    if 'uxm_s' in file_path.replace('\\','/').lower() or 'uxm_s' in os.path.basename(file_path).lower():
        if key:
            uxm_s_keys.add(key)
        uxm_s_sources.add(file_path)

# fallback: include keys that appear in repo scripts mentioning run_asama3_gate or uxm_s
# create CSV for uxm_s matrix: task,keys,searched_sources
with open(UXM_S_CSV,'w',encoding='utf-8',newline='') as outf:
    w = csv.writer(outf)
    w.writerow(['task','keys_semicolon_separated','sources_semicolon_separated'])
    if uxs_tasks:
        for t in sorted(uxs_tasks):
            w.writerow([t,';'.join(sorted(uxm_s_keys)), ';'.join(sorted(uxm_s_sources))])
    else:
        # if no tasks detected, add a best-effort set based on known names
        known = ['UXS_FrontendBuildUIR','UXS_RunPipeline']
        for t in known:
            w.writerow([t,';'.join(sorted(uxm_s_keys)), ';'.join(sorted(uxm_s_sources))])

# HAT comparison: compute sizes and set diffs
hat5 = hat5_cmds
hat8 = hat8_cmds
v33 = {c for c in v33_cmds}

hat5_only = sorted(hat5 - hat8 - v33)
hat8_only = sorted(hat8 - hat5 - v33)
v33_only = sorted(v33 - hat5 - hat8)
common_all = sorted(hat5 & hat8 & v33)

# write combined markdown
with open(OUT_MD,'w',encoding='utf-8') as md:
    md.write('# V33 — Komutlar & Anahtarlar; uxm_s matris ve HAT karşılaştırması (TR)\n\n')
    md.write('## 1) Sadece V33 — Tam Komut ve Anahtar Listesi\n\n')
    md.write('- Kaynak CSV: `reports/UXM_COMMAND_CATALOG.csv` ve `reports/UXM_EXEC_KEYS_CATALOG.csv`\n')
    md.write('- Özet: benzersiz komut sayısı: {}\n\n'.format(len(v33_cmds)))
    md.write('### A) V33 — Benzersiz komutlar (alfabetik)\n\n')
    for c in sorted(v33_cmds):
        md.write('- {}\n'.format(c))
    md.write('\n')
    md.write('### B) V33 — Çalıştırılabilir anahtarlar (alfabetik)\n\n')
    for k in sorted(v33_keys):
        md.write('- {}\n'.format(k))
    md.write('\n---\n\n')

    md.write('## 2) Sadece `uxm_s` — Görev/Anahtar Matris (CSV ve MD)\\n\n')
    md.write('- CSV: `reports/uxm_s_task_key_matrix.csv`\n\n')
    md.write('### A) Bulunan görevler (kod tabanından `UXS_` önekli isimler)\n\n')
    if uxs_tasks:
        for t in sorted(uxs_tasks):
            md.write('- {}\n'.format(t))
    else:
        md.write('- Uygun kod taramasıyla `UXS_` önekli görev bulunamadı; varsayılan: `UXS_FrontendBuildUIR`, `UXS_RunPipeline`\n')
    md.write('\n')
    md.write('### B) uxm_s ile ilişkili anahtarlar (CSV kaynaklarından)\n\n')
    if uxm_s_keys:
        md.write('`{}`\n\n'.format(', '.join(sorted(uxm_s_keys))))
    else:
        md.write('- Bu repoda `uxm_s` için CSV kaynaklarında doğrudan anahtar bulunamadı.\n\n')

    md.write('### C) Görev-Anahtar Tablosu (kısa gösterim)\n\n')
    md.write('| Görev | Anahtarlar | Kaynak dosyalar |\n')
    md.write('|---|---:|---|\n')
    # read uxms csv to show entries
    try:
        with open(UXM_S_CSV,encoding='utf-8') as f:
            r = csv.reader(f)
            next(r,None)
            for row in r:
                md.write('| {} | {} | {} |\n'.format(row[0], row[1], row[2]))
    except Exception:
        md.write('| - | - | - |\n')

    md.write('\n---\n\n')
    md.write('## 3) HAT Bazlı Karşılaştırma: HAT5 vs HAT8 vs V33\n\n')
    md.write('- Kaynak: `reports/UXM_COMMAND_CATALOG.csv` (lane sütunu)\n\n')
    md.write('| Ölçüt | HAT5 | HAT8 | V33 |\n')
    md.write('|---:|---:|---:|---:|\n')
    md.write('| Benzersiz komut sayısı | {} | {} | {} |\n'.format(len(hat5), len(hat8), len(v33)))
    md.write('| Tümünde ortak komut sayısı | {} | {} | {} |\n'.format(len(common_all), len(common_all), len(common_all)))
    md.write('| Sadece HAT5’de olan (örnek 10) | {} | - | - |\n'.format(len(hat5_only)))
    md.write('| Sadece HAT8’de olan (örnek 10) | - | {} | - |\n'.format(len(hat8_only)))
    md.write('| Sadece V33’te olan (örnek 10) | - | - | {} |\n'.format(len(v33_only)))
    md.write('\n')
    md.write('### A) Sadece HAT5 örnekleri (ilk 10)\n\n')
    for c in hat5_only[:10]:
        md.write('- {}\n'.format(c))
    md.write('\n')
    md.write('### B) Sadece HAT8 örnekleri (ilk 10)\n\n')
    for c in hat8_only[:10]:
        md.write('- {}\n'.format(c))
    md.write('\n')
    md.write('### C) Sadece V33 örnekleri (ilk 10)\n\n')
    for c in v33_only[:10]:
        md.write('- {}\n'.format(c))
    md.write('\n')

print('\nOutputs written:')
print(' -', OUT_MD)
print(' -', UXM_S_CSV)
print('\nSummary: V33 commands={}, V33 keys={}, uxm_s tasks={}, uxm_s_keys={}'.format(len(v33_cmds), len(v33_keys), len(uxs_tasks), len(uxm_s_keys)))
