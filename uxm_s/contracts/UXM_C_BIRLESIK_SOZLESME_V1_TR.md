# UXM-C Birlesik Sozlesme V1 (TR)

Tarih: 15 Mayis 2026
Durum: Asama-3 kilit sozlesmesi

## 1) Komut Sozlesmesi (Tek Merkez)

Komut semantigi tek merkezden yonetilir:

- `src/core/service_registry/uxm_v20_commands.bi`
- `src/frontend/uxm_s_frontend_entry.bas`
- `src/backends/*`

Kural:

1. Komut adlari ve opcode esitligi tek kaynakta tutulur.
2. Komut parser davranisi bu tabloya aykiri olamaz.
3. Runtime ve backend komut davranislari ayni sozlesmeyi izler.

## 2) Adresleme Modu Sozlesmesi (Tek Merkez)

Adresleme resmi listesi:

- `contracts/ADRESLEME_STANDARTI_TR.md`
- `src/frontend/address_resolver/uxm_v20_addressing_modes.bas`

Kural:

1. Lexer/parser adresleme bicimlerini bu listedeki tiplerle sinirlar.
2. Gecersiz bicimler kaynak konumu ile raporlanir.
3. Adresleme cozum sonucu tek UIR alan modeline yazilir.

## 3) Branch Sozlesmesi (Parse/Validate/Emit)

Branch akisi tek zincirdir:

1. Parse
2. Validate
3. Emit

Kural:

1. Eslesmeyen loop ve branch hedefleri derleme asamasinda reddedilir.
2. Runtime'a hatali branch sarkmasi engellenir.
3. Branch negatif testleri zorunludur.

## 4) Servis Sozlesmesi ve Ust Sinir

Servis ID araligi:

- Min: 0
- Max: 65535

Kod kilidi:

- `src/core/service_registry/uxm_v20_service_registry.bi`

Kural:

1. 65535 ustu servis kimligi gecersizdir.
2. Registry-dispatch uyumu gate tarafinda test edilir.
3. Servis durumu: tanimli / tanimsiz / karantinada.

## 5) Para Komutlari (Branch Baglamli)

Para (akisi yoneten) komutlar su gruba dahildir:

- Loop ac/kapat: `[` `]`
- Branch/akisi degistiren dallar

Kural:

1. Para komutlari parser tarafinda yapisal dengeye zorlanir.
2. Validate asamasi gecmeyen para akisi emit edilmez.

## 6) CLI Secenek Sozlesmesi

CLI secenekleri su ana hatlari kapsar:

1. Kaynak girisi
2. Cikti tipi secimi
3. Derleme modu
4. Rapor/gate secenekleri

Kural:

1. CLI secenekleri belgede yazili adlar disina cikamaz.
2. Cikti tipi secimi `json/asm/obj/exe` hatlariyla uyumlu olmak zorundadir.

## 7) Cikti Hatlari Sozlesmesi

Desteklenen cikti hatlari:

1. JSON
2. ASM
3. OBJ
4. EXE

Kural:

1. Her hatta standart envelope kullanilir.
2. Basari/hata durumu tek formatla raporlanir.
3. Test runner ciktilari JSON envelope ile kaydedilir.

## 8) Asama-3 Kabul Kriteri

Asagidaki maddeler saglandiginda Asama-3 tamam sayilir:

1. Komut/adresleme/branch/servis/cikti sozlesmeleri tek merkezde.
2. Servis 65535 ust siniri kodda kilitli.
3. Gate komutu tek dosyadan calisiyor.
4. Asama-3 giris-cikis kriter raporu guncel.
