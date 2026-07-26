# Phase 5 — Day 3: LLM API Dasar

## Materi
1. System Instruction
2. Generation Parameters (`temperature`, `max_output_tokens`)

---

## 1. System Instruction

**Apa itu:** aturan/peran permanen yang berlaku ke SEMUA prompt selama sesi, ditulis terpisah dari pertanyaan user.

**Kenapa penting:** tanpa ini, tiap prompt harus nulis ulang instruksi manual — boros token dan gampang inkonsisten.

**Analogi:** SOP yang ditempel di dinding — dibaca sekali, berlaku terus. Tapi LLM itu stateless, jadi tiap request dia "baca ulang" SOP itu dan tetap kena token.

```python
response = client.models.generate_content(
    model="gemini-flash-latest",
    config={
        "system_instruction": "Kamu adalah asisten analisis crypto. Jawab singkat."
    },
    contents="Bagaimana kondisi BTC hari ini?"
)
```

**Aturan pembeda system_instruction vs instruksi di contents:**
- Berlaku selalu, apapun pertanyaannya → `system_instruction`
- Cuma buat request itu doang (misal "buat dalam bentuk list") → gabung ke `contents`

**Catatan penting:** system_instruction TETAP kena hitungan token (`prompt_token_count`) setiap kali dipanggil — bukan gratis, bukan sekali bayar di awal.

---

## 2. Temperature

**Apa itu:** ngatur seberapa "berani" LLM milih kata yang bukan pilihan probabilitas tertinggi.

| Temperature | Karakteristik | Cocok untuk |
|---|---|---|
| 0.0–0.3 | Konsisten, predictable | Analisis data, trading, output terstruktur |
| 0.7–1.0 | Balance | Chat umum |
| 1.5–2.0 | Sangat variatif | Brainstorming, cerita |

**Penting untuk project:** Setup Generator nanti WAJIB pakai temperature rendah (0.2–0.3) — LLM nggak boleh "kreatif" dalam analisis market, harus konsisten. Selaras dengan prinsip risk management yang deterministic.

**Insight dari eksperimen (temp 0.3 vs 1.5, sama-sama max_token 1000):** temperature tinggi nggak selalu bikin jawaban lebih panjang/detail. Kadang malah lebih cepat "memutuskan berhenti" karena random-nya juga mempengaruhi kapan model berhenti generate, bukan cuma kata apa yang dipilih.

---

## 3. max_output_tokens

**Apa itu:** batas maksimal panjang token yang boleh di-generate.

**PENTING — max_output_tokens itu PAGAR, bukan target:**
- LLM generate token satu-per-satu, TIDAK tahu sebelumnya kalau bakal kena limit
- Begitu nyampe batas → dipotong paksa, di mana pun posisinya (bisa di tengah kalimat/JSON)
- LLM TIDAK "improv" atau menyesuaikan gaya bahasa saat mendekati limit — itu bukan cara kerjanya

**Gemini Flash punya proses thinking internal** yang ikut makan jatah max_output_tokens sebelum sampai ke teks output. Jadi angka kecil (300) bisa kepotong padahal kelihatannya cukup.

**Cara debug:** cek `response.candidates[0].finish_reason`
- `STOP` → selesai normal
- `MAX_TOKENS` → kepotong karena limit, perlu dinaikkan

```python
config={
    "system_instruction": "...",
    "temperature": 0.3,
    "max_output_tokens": 1000
}
```

### Kasus nyata yang dialami:
`max_output_tokens=300` → response kepotong ("Level Kunci:**" doang, atau kalimat putus di tengah). Cek `finish_reason` → `MAX_TOKENS`. Solusi: naikkan ke `1000` → `finish_reason` jadi `STOP`, lengkap.

**Tradeoff:**
| Setting | Resiko |
|---|---|
| Kekecilan | Kepotong, output rusak (bahaya kalau JSON) |
| Cukup besar | Aman, tapi boros kalau nggak perlu sepanjang itu |
| Kegedean tanpa alasan | Boros signifikan tanpa manfaat |

---

## Mini Project: Market Advisor CLI (Mp-03)

Function `tanya_ai(chat, instructions="default")`:
- Default parameter + type hint untuk system instruction fleksibel
- `temperature=0.3`, `max_output_tokens=1000`
- Loop `while True` dengan exit command

**Fitur tambahan (eksplorasi pribadi):** command parser untuk ganti instruction on-the-fly via keyword `instruksi:` / `instruction:` di awal kalimat.

**Refactor yang dipelajari — `.partition(":")` vs `.split()[n:]`:**

Masalah awal: pakai `.split()` lalu ambil index tertentu, butuh 2 blok berbeda untuk handle `"instruksi : x"` vs `"instruksi: x"` (beda posisi titik dua bikin beda index).

Solusi lebih tepat:
```python
_, _, sisa = ask.partition(":")
ask = sisa.strip()
```
`.partition(":")` motong string jadi 3 bagian berdasarkan karakter `:` itu sendiri — konsisten untuk kedua format spasi, nggak perlu nebak index.

**`.strip()`** — buang spasi (atau karakter lain) di awal & akhir string saja. Variannya: `.lstrip()` (kiri saja), `.rstrip()` (kanan saja).

**Prinsip yang didapat:** kalau butuh banyak percabangan if-elif buat handle variasi format input, itu biasanya tanda ada method yang lebih tepat — bukan nambah lebih banyak percabangan.

**Edge case dibahas:** keyword `instruksi` di TENGAH kalimat (misal `"gak penting instruksi : blabla"`) tidak kedeteksi, karena logic cuma cek kata pertama (`ask.split()[0]`). Ini desain yang benar (command harus di awal, sama seperti command Discord `!price`), bukan bug — selama itu memang niatnya.

---

## Key Takeaway Hari Ini
- `system_instruction` = permanen, kena token tiap call. Instruksi ad-hoc = ikut di `contents`.
- `temperature` mengatur gaya pemilihan token, TIDAK mempengaruhi jumlah token dipakai.
- `max_output_tokens` = pagar keras, bukan target — LLM tidak beradaptasi mendekati limit.
- `finish_reason` adalah tool debug utama untuk kasus output kepotong.
- Kalau logic butuh banyak percabangan untuk variasi format input → cari method yang lebih tepat dulu, sebelum nambah percabangan.

---

**Status: Phase 5 Day 3 SELESAI ✅**
**Next: Phase 5 Day 4 — Conversation History (LLM stateless, cara "menyambung" percakapan) + struktur function reusable**