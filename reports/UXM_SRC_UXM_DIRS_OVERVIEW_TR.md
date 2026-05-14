# UXM — `src`/`uxm` Dizinleri Tarama Özeti (TR)

Amaç: CSV/MD ve yorum dosyalarından elde edilen bilgilerle workspace içinde `src` veya `uxm` adını içeren ana dizinleri tespit etmek ve kısa durum özeti sunmak.

Kısa sonuç
- Tarama tamamlandı; önemli kök dizinler ve içerikleri aşağıda listelenmiştir.
- Kaynak: `uxm_zip_manifest_ozet.csv`, `UXM_COMMAND_CATALOG.csv`, `UXM_EXEC_KEYS_CATALOG.csv`, `uxm_s_task_key_matrix.csv`, mimari dokümanlar ve runner betikleri okundu.

Tespit edilen önemli dizinler

1) UXM_A_64K_COMPILER
- Yol: C:\Users\mete\Downloads\UXMC\UXM_A_64K_COMPILER
- Öne çıkan dosyalar: `tools/final_release_gate_v20/araclar/uxm_stage20_final.py`, `uxm31_runtime_fb_full.bas`, `uxm31_compiler_fb.bas`, test dizinleri (final expected suite).
- Not: Final release gate araçları ve runtime kaynakları var; `fbc` ve `nasm` gereksinimi bekleniyor.

2) 1\UXMv33 (aktif çalışma dalı)
- Yol: C:\Users\mete\Downloads\1\UXMv33
- Öne çıkan dosyalar: `UXM_STAGE_RUNNER.py`, `UXM_EXPECT_RUNNER_V2.py`, çok sayıda `run_stage*.bat` ve `araclar/` Python betikleri.
- Not: Test/iş akışı betiklerinin merkezi; `--stage`, `--no-build` gibi argümanlar yaygın.

3) uxm_s (mimari/forensic depo)
- Yol: C:\Users\mete\Downloads\UXMC\ucma\_forensic\strongest2_src\uxm_s
- Öne çıkan dosyalar: `docs/UXM_S_MIMARI_TASARIM_TR.md`, `run_asama3_gate.ps1`, contracts referansları; `uxm_s/src` referansı (pipeline / FBC hedefleri).
- Not: Mimari kararlar, geçiş planı ve Asama-3 gate betiği burada.

4) `1\uxm dosyalari` içindeki stage paketleri
- Yol örn: C:\Users\mete\Downloads\1\uxm dosyalari\UXM_V33_STAGE13_PATCH\...
- Öne çıkan dosyalar (tekrar eden): `uxm31_compiler_fb.bas`, `native_asm_emit.bas`, `uxm31_runtime_fb_full.bas`, `runtime_meta_dispatch.bas`, `.uxm` testleri ve `.expect` beklenen çıktılar.
- Not: Çok sayıda stage paket ve büyük test arşivleri (final expected suite). Bunlar compiler + test materyali içeriyor.

5) Test/Arşiv paketleri
- `UXM_ALL_TEST_FILES_ARCHIVE`, `UXM_V33_FINAL_EXPECTED_TEST_SUITE` gibi büyük arşivler workspace içinde yer alıyor; binlerce `.uxm`/`.expect` dosyası içeriyor.

Öne çıkan bulgular (CSV/MD/yorumlardan)
- `uxm_zip_manifest_ozet.csv` stage paketlerinin içerik dağılımını gösteriyor (hangi paketlerde kaç `.uxm`, `.bas`, `.bat` bulunduğu).
- `UXM_COMMAND_CATALOG.csv` OP_* sabitlerini ve tek-karakter sembolleri listeliyor (derleyici/emit katmanları için önemli).
- `UXM_EXEC_KEYS_CATALOG.csv` ve `uxm_s_task_key_matrix.csv` runner/iş akışı argümanlarını ve görev-anahtar eşlemelerini veriyor.
- `UXM_S_MIMARI_TASARIM_TR.md` geçiş planı ve hedef klasör yapısını tanımlıyor (frontend/core/backends ayrımı).

Hızlı öneriler — ne yapılabilir
- `1\UXMv33` içinde test çalıştırma: `python UXM_STAGE_RUNNER.py --stage auto --no-build` (yerel test keşfi).
- `uxm_s` Asama-3 gate kontrolü: `powershell run_asama3_gate.ps1` (repo kökünden çalıştırılmalı).
- Hotfix testi: `python uxm_a64_hotfix_runtime_v3.py --target <runtime_meta_dispatch.bas>` (hotfix scriptleri mevcut).
- Derleme doğrulaması için `fbc` ve `nasm` kurun, sonra `UXM_A_64K_COMPILER` içindeki build betiklerini çalıştırın.

Sonraki adım önerisi
- Hangi kökte derin analiz istiyorsunuz? Ör: `UXM_A_64K_COMPILER` derleme doğrulaması, `1\UXMv33` test koşucunun tam çalıştırılması veya `uxm_s` pipeline derleme/gate kontrolü.

Rapor oluşturulma zamanı: 15 Mayıs 2026

---
Rapor dosyası: `reports/UXM_SRC_UXM_DIRS_OVERVIEW_TR.md`
