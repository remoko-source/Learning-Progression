# Phase 5 Day 2 — Token Management & Cost Awareness

## Kenapa Materi Ini Penting

LLM tidak membaca teks seperti manusia — dia membaca **token** (potongan kecil dari teks). Ini punya dua konsekuensi langsung buat AI Trading Agent:

- **Biaya**: API dibayar per token (input + output). Kalau bot jalan tiap 60-120 detik dan generate reasoning tiap kali trigger, tagihan bisa membengkak tanpa disadari kalau tidak dikontrol.
- **Context window**: tiap model punya batas token yang bisa diproses sekaligus. Kelebihan batas = request gagal atau data kepotong tanpa peringatan.

Token awareness ini kontrol biaya dan reliability, bukan sekadar syntax baru.

---

## 1. Estimasi Kasar (Sanity Check)

```python
def estimasi_token(teks: str) -> int:
    return len(teks) // 4
```

Aturan jempol: **1 token ≈ 4 karakter**. Ini bukan hasil akurat — cuma buat cek cepat "kira-kira masuk akal atau tidak" sebelum manggil API beneran. Gratis, instan, tidak makan kuota.

## 2. Hitung Akurat — `count_tokens()`

```python
from google import genai

client = genai.Client()

def hitung_token_akurat(teks: str, model: str = "gemini-flash-latest") -> int:
    hasil = client.models.count_tokens(model=model, contents=teks)
    return hasil.total_tokens
```

Ini yang beneran dipakai buat validasi — pakai tokenizer asli dari server Gemini, bukan estimasi. Method ini cuma **menghitung**, tidak menghasilkan jawaban AI apapun.

Catatan soal `model: str = "gemini-flash-latest"` — ini parameter dengan **default value**. Kalau tidak diisi saat manggil fungsi, otomatis pakai nilai itu. Kalau mau pakai model lain, tinggal override: `hitung_token_akurat(teks, model="model-lain")`.

## 3. Baca `usage_metadata` — Token yang Beneran Kepake

```python
response = client.models.generate_content(model="gemini-flash-latest", contents=prompt)
print(response.usage_metadata)
# prompt_token_count      -> token dari input yang dikirim
# candidates_token_count  -> token dari jawaban LLM
# total_token_count       -> jumlah keduanya
```

Beda dengan `count_tokens()` (cek SEBELUM kirim), `usage_metadata` ini laporan SETELAH LLM beneran menjawab. Berguna buat logging/audit — nanti di Phase 6.5 (SQLite) bisa disimpan buat lihat tren pemakaian dari waktu ke waktu.

---

## Troubleshooting yang Ditemui

| Error | Penyebab | Solusi |
|---|---|---|
| `503 UNAVAILABLE` | Server Gemini sibuk (transient, bukan salah kode) | Tunggu, coba lagi — sama seperti pola retry logic Phase 3 (error sementara ≠ kode salah) |
| `404 NOT_FOUND: models/gemini-2-flash-lite` | Salah nama model (harusnya `gemini-2.5-flash-lite`) — ternyata juga tidak kompatibel API key gratis | Tetap pakai `gemini-flash-latest` yang sudah terbukti valid |

---

## Mini Project: Mp-02 "Token Budget Guard"

**Tujuan:** cek narasi market SEBELUM dikirim ke LLM. Kalau kepanjangan, potong otomatis atau reject, sambil dicatat ke log.

### Struktur Logika

```python
class TokenBudgetExceededError(Exception):
    pass

def cek_token(text: str, model: str = "gemini-flash-latest"):
    hitung = client.models.count_tokens(model=model, contents=text)
    
    if hitung.total_tokens <= 10:
        pass  # aman, tidak perlu apa-apa
    
    elif hitung.total_tokens > 10 and hitung.total_tokens <= 15:
        # toleransi kecil -> potong bertahap kata per kata
        potong = text.split()
        kali = []
        for i in potong:
            kali.append(i)
            hitung = client.models.count_tokens(model=model, contents=" ".join(kali))
            if hitung.total_tokens <= 10:
                continue
            else:
                kali.remove(i)
                text = " ".join(kali)
                logger.warning("TEKS DIPOTONG")
    
    else:
        # kelewat jauh -> jangan dipaksa potong, konteks bisa rusak
        raise TokenBudgetExceededError("Token melebihi batas, Operasi gagal")
    
    logger.info("AMAN")
    return text
```

### Kenapa Ada 3 Cabang, Bukan Cuma "potong kalau lewat batas"

Ini poin desain paling penting di Mp-02: **kalau input jauh melebihi batas** (misal batas 10 token tapi input 40 token), potong paksa sampai muat bisa menghasilkan teks yang kehilangan konteks penting — cuma sepotong kalimat awal yang menggantung.

Solusinya dipisah jadi dua level:
- **Toleransi kecil** (10-15 token) → masih masuk akal dipotong, konteks kemungkinan besar aman
- **Kelewat jauh** (>15 token) → langsung `raise` error, JANGAN dipotong paksa. Mending gagal total daripada hasilnya rusak.

### Kenapa Potong Kata Butuh Loop, Bukan Hitung Matematis Langsung

Token tidak proporsional 1:1 ke jumlah kata atau karakter — kata pendek seperti "di" mungkin 1 token, tapi kata seperti "$65,000" bisa jadi 3-4 token karena angka dan simbol sering dipecah tokenizer. Tidak ada rumus pasti buat nebak "berapa kata = berapa token" tanpa manggil `count_tokens()`.

Makanya prosesnya **coba-cek-ulang**:
1. Split teks jadi list kata (`.split()` — defaultnya belah berdasarkan spasi, koma/simbol tetap nempel ke kata, tidak pernah hilang)
2. Tambahkan kata satu-satu ke list sementara
3. Tiap nambah, gabung ulang (`" ".join(...)`) dan cek token-nya
4. Begitu lewat batas, buang kata terakhir yang bikin kelebihan, berhenti

### Detail Teknis yang Sempat Bikin Bingung

- **Slicing list** — `list[start:stop]` pakai titik dua, bukan koma. Konsepnya sama seperti slicing string yang sudah dikuasai sebelumnya, cuma sekarang dipakai di list.
- **`.split()` vs `.join()`** — `.split()` membelah string jadi list (default di spasi), `.join()` kebalikannya, gabung list jadi string dengan pemisah yang kita tentukan sendiri (`" ".join(...)` = gabung pakai spasi).
- **Kenapa koma tidak pernah hilang** — `.split()` cuma peduli spasi sebagai titik potong. Koma yang nempel di kata seperti `"$65,000"` atau `"tajam,"` tetap ikut sebagai satu kesatuan dengan kata itu.

---

## Ringkasan Materi yang Dikuasai

- [x] Estimasi token kasar (`len(teks) // 4`)
- [x] Hitung token akurat (`count_tokens()`)
- [x] Baca `usage_metadata` dari response
- [x] Custom exception untuk kasus token melebihi batas
- [x] Logic potong teks bertahap berbasis loop + validasi berulang
- [x] Integrasi logging 3 level (info/warning/critical) di satu alur validasi

## Next: Phase 5 Day 3-4 — LLM API

Cara manggil Gemini API lebih terstruktur — system instruction, parameter seperti temperature, dll. Modal dasar sudah ada: API key, `generate_content()` dasar, `count_tokens()`, konsep statelessness LLM.