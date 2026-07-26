# Phase 4 — Embed & Formatting

**Tanggal:** 15 Juli 2026
**Level:** 🔴 (Mp-05: Refactor Live Price Bot → Embed)

---

## Konsep yang Dipelajari

### 1. `discord.Embed`

Embed adalah "kartu" tampilan native Discord — bukan teks biasa. Dipakai lewat objek, bukan string:

```python
embed = discord.Embed(
    title="Judul",
    description="Deskripsi (opsional)",
    color=discord.Color.green()
)
```

- `title` dan `description` → level "header", cuma diisi sekali
- `color` bisa pakai built-in (`discord.Color.green()`, `.red()`, dll) atau hex custom

### 2. `embed.add_field(name, value, inline)`

Field = level "konten", bisa dipanggil berkali-kali untuk nambah baris data.

```python
embed.add_field(name="Label", value="Isi", inline=True)
```

**`inline=True` vs `inline=False`:**
- `True` → field *bersedia* dijajarkan horizontal dengan field `True` lain yang **bersebelahan langsung**
- `False` → field selalu ambil satu baris penuh, memutus jajaran field di sekitarnya

⚠️ Insight penting: `inline=True` bukan jaminan mutlak sejajar. Kalau diapit `inline=False` di kedua sisi, field `True` itu tetap jadi baris sendiri secara visual.

### 3. `set_footer()` dan `timestamp`

```python
embed.set_footer(text="Data by CoinGecko")
```

```python
from datetime import datetime, timezone
embed = discord.Embed(
    timestamp=datetime.now(timezone.utc)  # wajib timezone-aware
)
```

- `timestamp` diisi di **constructor**, bukan method terpisah
- Wajib `timezone.utc` — untuk trading signal, ini krusial karena user perlu tahu seberapa segar sinyalnya

---

## Prinsip Refactor (bukan Rewrite)

Mp-05 = refactor Mp-04, bukan project baru dari nol.

- Fetch logic (aiohttp, batching, custom exception, `on_command_error`) **tetap dipakai ulang** — sudah teruji benar di Mp-04
- Yang berubah **hanya layer presentasi**: dari `tabulate` (text table) → `discord.Embed` (structured field)
- Alasan: field per-coin adalah *structured data* asli, bukan teks yang dibungkus kotak. Pola "1 atribut = 1 field" ini akan dipakai lagi di Phase 5 untuk render sinyal AI (entry/SL/TP/confidence)

---

## Mp-05 — Refactor Live Price Bot → Embed

**File:** `Mp-05.py`

**Requirement yang dipenuhi:**
- `!price <coin>` dan `!prices <coin1> <coin2> ...` render sebagai Embed (bukan code block)
- 1 embed berisi banyak field (1 coin = 1 field), bukan 1 field isi tabel teks
- `inline=True` → coin-coin sejajar
- Partial failure tetap jalan: coin invalid tampil sebagai field `$INVALID`, tidak menggagalkan seluruh command
- `footer` = "Data by CoinGecko", `timestamp` = waktu fetch
- Custom exception `SalahFormat1`/`SalahFormat2` tetap dikirim via `ctx.send(embed=...)` di `on_command_error`, sekarang juga pakai Embed (title "[ERROR]", warna merah)

**Verified working di Discord** — screenshot: `!prices blablabla mandor bitcoin ethereum` menghasilkan embed dengan 3 field sejajar + 1 field turun baris (Ethereum), partial invalid tampil benar.

---

## Key Learnings

- `title`/`description` = sekali; `field` = berkali-kali
- `inline=True` cuma "bersedia" sejajar dengan tetangga `inline=True` yang langsung bersebelahan
- `timestamp` di constructor `Embed()`, wajib `datetime.now(timezone.utc)`
- Refactor yang baik = ubah sesedikit mungkin bagian yang sudah terbukti benar; reuse fetch logic, ganti cuma presentasi
- Field terstruktur (name/value pair) > tabel teks dibungkus 1 field — field native lebih mudah dibaca dan jadi pola dasar untuk render sinyal AI di Phase 5

---

## Status Phase 4

| Day | Materi | Status |
|---|---|---|
| Day 1 | Asyncio Dasar | ✅ |
| Day 2 | create_task() + exception handling | ✅ |
| Day 3 | Discord Webhooks | ✅ |
| Day 4 | discord.py Full Bot | ✅ |
| Day 5/6* | Embed & Formatting | ✅ |
| Capstone | Auto Signal Bot | Belum |

*\*Perlu dikonfirmasi ulang ke roadmap — cek apakah ini Day 5 atau Day 6 sesuai urutan resmi sebelum lanjut capstone.*