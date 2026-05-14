# Asama-3 Plan Eksikleri ve 5 Hamle Planı

Tarih: 15 Mayıs 2026
Kapsam: strongest2_src + bağlı plan klasörleri

## 1) Ana Plan Kaç Aşamadan Oluşuyor?

Ana faz haritası 4 aşamalıdır.

- Asama-1: Uyumluluk modu varsayılan
- Asama-2: Çift-yol doğrulama
- Asama-3: Yönlendirmeli geçiş
- Asama-4: Sıkılaştırma

Kaynak plan belgesi:
- `BasicOyunSource/uXBasic_repo/spec/IR_RUNTIME_MASTER_PLAN.md`

İlgili giriş kriterleri ve sonraki faz kapıları:
- `BasicOyunSource/uXBasic_repo/spec/NEXT_PHASE_ENTRY_CRITERIA.md`

strongest2_src içindeki otoriter plan klasörü:
- `strongest2_src/README.md`
- `strongest2_src/reports/`
- `strongest2_src/uxm_s/docs/`
- `strongest2_src/uxm_s/contracts/`
- `strongest2_src/uxm_s/reports/`

## 2) Taranan Plan Belgelerinden Çıkan Eksikler

Taranan klasörler:

- `UXMC/ucma/_forensic/strongest2_src`
- `UXM XMX`
- `BasicOyunSource/uXBasic_repo`
- `toplu dosyalar/lapaci_uxm_compiler_pack_v2/uxm`

En güncel ve tekrar eden eksik başlıklar:

1. Komut sözleşmesi tek merkezde kilitli değil.
2. Adresleme modu sözleşmesi farklı klasörlere dağılmış durumda.
3. Branch parse/validate/emit zinciri için tek resmi plan dokümanı eksik.
4. Servis katmanı için 65535 üst sınırını açıkça bağlayan merkezi sözleşme eksik.
5. JSON / ASM / OBJ / EXE çıktı hatlarının tek bir üretim sözleşmesi eksik.
6. `.plan.md` append-only kayıt akışı tek yerde toplanmamış.
7. Asama-3 için net giriş-çıkış kriterleri birleştirilmemiş.

Lapaci paketinden çıkan kritik not:

- Tamamlanmayan büyük iş fiziksel modül parçalama.
- Riskli kaynaklar aktif pakete alınmamalı: `uxm31_full_tool_fb.bas`, `uxm31_full_tool_fb_2.bas`.

## 3) Asama-3 İçin 5 Hamlelik Profesyonel Plan

Bu plan 5 hamleyi geçmez.

### Hamle 1 - Kanonik Plan Kilidi

- Tüm plan md dosyalarını tek indeks altında topla.
- Ana referansları `strongest2_src/reports/` içine bağla.
- `README.md` içindeki plan klasörü sözleşmesini koru.

### Hamle 2 - Dil Sözleşmesi Kilidi

- Komut listesi, adresleme modları ve branch semantiğini tek belgeye bağla.
- `src/shared/uxm_v20_addressing_modes.bas` ve parser kayıtlarını aynı referansla eşle.
- Komut sözlüğü ve meta servis haritasını tek tablo halinde kilitle.

### Hamle 3 - Servis Sınırı ve Registry Kilidi

- Servis sayısını 65535 üst sınırıyla açıkça sınırla.
- `runtime_meta_dispatch.bas` ile registry dosyalarını aynı kontrata bağla.
- Servisler için “tanımlı / tanımsız / karantinada” durum modeli uygula.

### Hamle 4 - Çıktı Hattı Kilidi

- JSON, ASM, OBJ ve EXE hatlarını tek çıktı sözleşmesine bağla.
- Her çıktı için giriş-çıkış ölçütlerini yaz.
- Hata raporu ve başarı raporunu aynı pipeline’a bağla.

### Hamle 5 - Gate ve Yayın Kilidi

- Build, test ve parity kapılarını tek komutlu çalıştır.
- Asama-3 raporunu ve sonraki faz kriterlerini güncelle.
- Push öncesi yalnız seçili dosyaları sahaya al.

## 4) Asama-3 İçin Uygulanacak Kodlama Önceliği

1. Önce sözleşme ve plan belgeleri kilitlenecek.
2. Sonra parser/adresleme/branch zinciri aynı sözleşmeye bağlanacak.
3. Sonra servis ve çıktı hatları tek pipeline’da birleştirilecek.
4. En sonda gate ve yayın komutları standartlaştırılacak.

## 5) Kısa Sonuç

Bu proje 4 aşamalı ana plana sahip. Şu an Asama-3 için en kritik ihtiyaç, komut-adresleme-branch-servis-çıktı zincirlerini tek bir resmi plan ve tek bir teknik sözleşmede toplamak. Böylece kalan kodlama işleri 5 hamlede yürütülebilir hale gelir.