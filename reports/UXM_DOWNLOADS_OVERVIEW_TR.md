# UXM — Downloads Klasörü Genel Durum Raporu (TR)

Amaç: `C:\Users\mete\Downloads` içindeki UXM / uxm türevli projeleri tarayıp tek bir Türkçe özet hazırlamak; hangi kök dizinlerde hangi projeler var, durumları, mimarileri, komut türleri, örnek kullanım ve CSV raporlarından çıkan bulgular.

Özet (kısa):
- Proje ailesi: Brainfuck-benzeri, tape/stack/data/FIFO tabanlı deneysel dil seti (uygulama adları: UXM, UX-MINIMA, UXM-A, V33 vb.).
- En gelişkin kökler (öncelik/bitmeye yakınlık sıralaması):
  1. `C:\Users\mete\Downloads\UXMC\UXM_A_64K_COMPILER` — Derleyici paketi, test suiti, final release gate; çalıştırılabilir derleyici ve kapsamlı sınama verisi mevcut.
  2. `C:\Users\mete\Downloads\toplu dosyalar\uxm_3_kardes_ayri_dunyalar` — Dil spesifikasyonu, VSCode eklentisi dokümanları, FreeBASIC runtime kaynakları; IDE ve dil tanımı tam görünüyor.
  3. `C:\Users\mete\Downloads\1\UXMv33` — Aktif geliştirme dalı; çok sayıda aşama/betik, optimizasyon araçları ve sınama/iş akışı betikleri bulunuyor.
  4. `C:\Users\mete\Downloads\UXMC\ucma\_forensic\strongest2_src` — Analiz/forensic depo; raporlar (`reports/`) ve `uxm_s` görev matrisleri burada.
  5. Diğer küçük paketler: `uxminima`, çeşitli sıkıştırılmış paketler ve eski sürüm ağaçları (arşiv, deneysel kaynaklar).

Bulunan ana dosyalar ve nerede oldukları (temel örnekler):
- `C:\Users\mete\Downloads\UXM_A64_DURUM_VE_HOTFIX3_NOTU.md` — Hotfix ve derleme notları (çalışma zamanı/derleme akışı düzeltmeleri).
- `C:\Users\mete\Downloads\UXMC\UXM_A_64K_COMPILER\UXM_A_64K_STATIC_AUDIT.md` — Statik denetim özeti (çalışma zamanı eksikleri, derleyici araç gereksinimleri).
- `C:\Users\mete\Downloads\toplu dosyalar\uxm_3_kardes_ayri_dunyalar\...\docs\UXM_LANGUAGE_SPEC.md` — Dil spesifikasyonu (komut listesi, adresleme, meta servisler).
- `C:\Users\mete\Downloads\UXMC\ucma\_forensic\strongest2_src\reports\UXM_COMMAND_CATALOG.csv` — Taranmış komut katalogu (OP_*, semboller vb.).
- `C:\Users\mete\Downloads\UXMC\ucma\_forensic\strongest2_src\reports\UXM_EXEC_KEYS_CATALOG.csv` — Betik/anahtar (arg/flag) katalogu.
- `C:\Users\mete\Downloads\UXMC\ucma\_forensic\strongest2_src\reports\uxm_s_task_key_matrix.csv` — `uxm_s` görev/anahtar matrisi.

Mimari: ortak noktalar
- Dil çekirdeği: tape (bant) + stack (yığın) + data bölgesi, hücre büyüklüğü varyantlara göre değişiyor (ör: A-64K paketinde 64KB sınırı).
- Bellek modelasyonu: adresleme biçimleri `(T)`, `(D:0)`, `(S:0)` gibi kuralcı ifadeler; meta-frame argüman konvansiyonları (`T-2`, `T-1`, `T`, `T+1`).
- Komut katmanları: sembolik tek-karakter komutlar (Brainfuck kökenli) + OP_ sabitleri (derleyicide enum/const olarak tanımlı) + meta servis çağrıları (`@N`, `@#` vb.).
- Derleyici hattı: kaynak -> HIR/MIR -> native emit (FreeBASIC / NASM hedefleri) -> çalışma zamanı nesneleri; iş akışı betikleri aşama bazlı (`stage runner`) ve release gate mekanizması mevcut.
- Çalışma zamanı: FreeBASIC tabanlı runtime kaynakları (`uxm31_runtime_fb_full.bas`) ve bazı native exe örnekleri (`uxm31_compiler.exe`, `uxm.exe`) bulunuyor.
- Sınama altyapısı: büyük bir `final_expected_suite` dizini ile `.uxm` testleri ve `.expect` beklenen çıktıları; `stage runner` ve `expect runner` betikleri Python ile yazılmış.

Komutlar (özet ve örnekler)
- Sembol tabanlı (tek karakterler): `> < + - 0 . , [ ] $ % ? ! ; & | ^ ~ { } @N @#` (kullanım: hücre-değiştir, döngü, yığın işlemleri, meta servis çağrıları).
- OP_* sabitleri (örnek kısım): `OP_AND, OP_BRANCH, OP_CLEAR, OP_DEC, OP_EQ, OP_GETC, OP_GT, OP_INC, OP_LEFT, OP_LOOP_BEG, OP_LOOP_END, OP_LT, OP_META, OP_NOP, OP_NOT, OP_OR, OP_POP, OP_PRINT_STRING, OP_PUSH, OP_PUTC, OP_RIGHT, OP_SHL, OP_SHR, OP_STATUS, OP_XOR` — bu isimler `reports/UXM_COMMAND_CATALOG.csv` içinde listelenmiştir.
- Matematik fonksiyonları/keywordler: `sin, cos, tan, sqrt, exp, log, pow, abs, neg` — compiler extension içinde parse edilip native çağrı üretiliyor.

Örnek komut yazımları (kullanım formatı):
- Derleyici/işleyici çağrısı: `uxm --op OP_PUSH --src sample.bin --dst out.bin`
- Matematik servis çağrısı (örnek araç): `math_eval --fn sin --arg 3.14`
- Betik/iş akışı çağrısı: Python betikleri için `python UXM_STAGE_RUNNER.py --root <kök> --stage 13 --no-build` (argüman örnekleri `reports/UXM_EXEC_KEYS_CATALOG.csv` içinde listelenmiştir).
- UXM kaynak örneği: `0(T-2)+k10.` (adresleme + hücre işlem + çıktı kombinasyonu, `UXM_LANGUAGE_SPEC.md` referansı).

CSV’lerden çıkarımlar (kısa):
- `UXM_COMMAND_CATALOG.csv` birçok `OP_` sabitini ve tek-karakter sembolleri içeriyor; hem `OP_CONST` hem `OP_REF` hem de `ADDINSTR` tipi kayıtlar var — yani komutlar derleyicide sabit tanımı, referans kullanımı ve emit edilme aşamalarında izlenmiş.
- `UXM_EXEC_KEYS_CATALOG.csv` betik ve çalıştırma anahtarlarının kapsamını verdi; `--root`, `--stage`, `--no-build`, `-o`, `-m`, `-3` gibi flag'ler iş akışı otomasyonunda yoğun kullanılıyor.
- `uxm_s_task_key_matrix.csv` `uxm_s` görevleri için hangi betiklerin hangi anahtarları kullandığını gösteriyor (ör: `UXS_AddToken` gibi görevlerin çok geniş argüman seti var).

Hangi servisler/komutlar hangi ortamda çalışıyor
- Derleyici hedefleri: FreeBASIC (bas), NASM (asm), Python araç zinciri; bazı hazır exe'ler de mevcut.
- Sınama ortamı: Python tabanlı `stage runner` + betikler; gerçek derleme için `fbc` ve `nasm` gereksinimi var (statik denetim `UXM_A_64K_STATIC_AUDIT.md` bunu vurguluyor).
- IDE entegrasyonu: VSCode dil desteği dosyaları (`syntaxes/uxm.tmLanguage.json`, `snippets/uxm.json`) mevcut; bu IDE eklentisi dil sözdizimi ve örnek dokümantasyon sağlıyor.

En gelişkin / bitmeye yakın projeler (detaylı neden)
1. `C:\Users\mete\Downloads\UXMC\UXM_A_64K_COMPILER` — içeride `tests/final_expected_suite` ile geniş sınama vakaları, `final_release_gate_v20` araçları ve `UXM_A64_DURUM_VE_HOTFIX3_NOTU.md` gibi yayın/patch notları; ayrıca `uxm.exe`/derleyici örnekleri görüldü. Son aşama: derleme betiklerinin (gate) runtime dispatch temizliği ile finalleşmesi gerekiyor.
2. `C:\Users\mete\Downloads\toplu dosyalar\uxm_3_kardes_ayri_dunyalar` — dil tanımı, bellek modeli dökümü ve IDE belgeleri hazır; runtime kaynakları ve native derleyici kaynak dizinleri bulunuyor. Son aşama: birleştirme ve paketleme (release gate) adımları.
3. `C:\Users\mete\Downloads\1\UXMv33` — en aktif geliştirme; çok sayıda aşama betiği, optimizasyon aracı ve test koşucu var; bu nedenle hem kapsamlı hem halen değişim altında.
4. `C:\Users\mete\Downloads\UXMC\ucma\_forensic\strongest2_src` — analiz/raporlama, `uxm_s` görev matrisi ve CSV raporları burada; proje değil ama geliştirme/analiz için ana kaynak deposu olarak kullanılıyor.

Kısa aksiyon önerileri (ne yapılabilir)
- Derlemeyi yerel doğrulamak için `fbc` ve `nasm` kurun, ardından `C:\Users\mete\Downloads\UXMC\UXM_A_64K_COMPILER` içindeki `build_a64_gate.bat` adımlarını izleyin.
- `uxm_a64_hotfix_runtime_v3.py` çalıştırılarak `runtime_meta_dispatch.bas` temizlenmeli (hotfix yönergesi dosyada açık).
- Testleri koşmak için `python UXM_STAGE_RUNNER.py --root <kök> --stage <n>` kullanın; `--no-build` ile sadece sınama çalıştırılabilir.

Kaynaklar (okumanız için ilk adreste):
- `C:\Users\mete\Downloads\UXM_A64_DURUM_VE_HOTFIX3_NOTU.md`
- `C:\Users\mete\Downloads\UXMC\UXM_A_64K_COMPILER\UXM_A_64K_STATIC_AUDIT.md`
- `C:\Users\mete\Downloads\toplu dosyalar\uxm_3_kardes_ayri_dunyalar\D_VSCODE_IDE_EXTENSION\uxm-ide-vscode\docs\UXM_LANGUAGE_SPEC.md`
- `C:\Users\mete\Downloads\UXMC\ucma\_forensic\strongest2_src\reports\UXM_COMMAND_CATALOG.csv`
- `C:\Users\mete\Downloads\UXMC\ucma\_forensic\strongest2_src\reports\UXM_EXEC_KEYS_CATALOG.csv`
- `C:\Users\mete\Downloads\UXMC\ucma\_forensic\strongest2_src\reports\uxm_s_task_key_matrix.csv`

Not: tarama geniş bir alanı (binlerce dosya) kapsıyor; isterseniz hangi alanı derinleştireceğimi belirtin (ör: `UXM_A_64K_COMPILER` içinde derlemeyi doğrulama, veya `1\UXMv33` içindeki optimizasyon araçlarını analiz etme). 
