# Asama-3 Giris Cikis Kriterleri (TR)

Tarih: 15 Mayis 2026

## 1) Giris Kriterleri

1. Asama-2 frontend entegrasyonu derlenebilir durumda olmali.
2. Komut/adresleme/meta sozlesmeleri mevcut olmali.
3. UIR giris kapisi tek fonksiyon uzerinden calismali.

## 2) Asama-3 Uygulama Kapsami

1. Tek merkezli UXM-C birlesik sozlesme olusturma.
2. Servis sinirini 0..65535 kod seviyesinde kilitleme.
3. Test ve cikti hatlarinda standart JSON envelope kullanma.
4. Tek komutlu Asama-3 gate betigiyle derleme dogrulama.

## 3) Cikis Kriterleri

1. `uxm_s/contracts/UXM_C_BIRLESIK_SOZLESME_V1_TR.md` mevcut ve guncel.
2. `uxm_s/src/core/service_registry/uxm_v20_service_registry.bi` icinde 65535 siniri aktif.
3. `uxm_s/src/backends/test_runner/uxm_s_test_runner.bas` JSON cikti uretiyor.
4. `uxm_s/src/backends/ide_json/uxm_s_ide_json_backend.bas` envelope fonksiyonunu sagliyor.
5. `uxm_s/run_asama3_gate.ps1` ile gate raporu olusuyor.

## 4) Dogrulama Komutlari

1. `fbc -c uxm_s/src/uxm_s_pipeline.bas`
2. `pwsh -File uxm_s/run_asama3_gate.ps1`

## 5) Sonuc

Bu kriterler karsilanirsa Asama-3 tamamlanmis kabul edilir ve Asama-4 sikilastirma fazina gecilir.
