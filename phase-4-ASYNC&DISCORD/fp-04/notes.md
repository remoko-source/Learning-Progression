# Phase 4 — Async & Discord — Ringkasan Lengkap

**Status:** SELESAI ✓
**Fokus:** Asyncio dasar, Discord Webhooks, discord.py full bot, Embed, integrasi jadi Auto Signal Bot

---

## Daftar Project yang Dibangun

| Hari | Nama Project | Konsep Utama |
|---|---|---|
| Day 1-2 | Asyncio Dasar | `async/await`, `asyncio.sleep()`, `create_task()`, blocking vs non-blocking |
| Day 3 | Signal Relay (Mp-03) | Discord Webhooks, `requests.post()`, custom exception untuk fetch & delivery |
| Day 4-5 | Live Price Bot (Mp-04) | `discord.py` full bot, intents, event handler, prefix command |
| Day 6 | Refactor ke Embed (Mp-05) | `discord.Embed`, `add_field`, refactor presentasi tanpa ubah fetch logic |
| Capstone | Auto Signal Bot | Integrasi semua skill Phase 4 jadi bot notifikasi trading real-time |

---

## Ringkasan Materi per Hari

### Day 1-2 — Asyncio Dasar
- `async def` + `await` untuk coroutine, `asyncio.sleep()` untuk simulasi jeda tanpa blocking
- `asyncio.create_task()` dipakai bukan "karena ada loop", tapi karena ada 2+ hal yang harus jalan **bersamaan** tanpa saling blocking
- `await task_variable` di akhir untuk memastikan background task selesai sebelum program keluar
- Exception handling per-coroutine — error di satu task nggak otomatis menghentikan task lain

### Day 3 — Signal Relay (Webhooks)
- Webhook = endpoint pasif (bukan bot penuh) — cukup satu `requests.post(url, json=payload)`, nggak perlu bot online 24 jam
- `payload` wajib berupa dict/JSON — itu kontrak API Discord, bukan pilihan format bebas
- Rate limit Discord ±30 request/menit → response 429 + `retry_after`
- Dua custom exception: `CoinDataError`, `SignalDeliveryError`, menangkap `requests.exceptions.RequestException`
- Bug format: tabel `tabulate` berantakan di Discord karena font monospace Notepad++ beda dari font proporsional Discord — fix pakai code block markdown Discord (```` ```\n{message}\n``` ````), bukan diatur dari sisi Python

### Day 4-5 — discord.py Full Bot
- Setup bot via Discord Developer Portal, `intents`, `commands.Bot(command_prefix=...)`
- `bot.process_commands(message)` **wajib** dipanggil manual di dalam `on_message` kalau `on_message` di-override
- `on_command_error` sebagai satu handler global untuk banyak jenis error command
- `aiohttp` sebagai pengganti non-blocking untuk `requests` di konteks bot async

### Day 6 — Embed & Formatting
- `discord.Embed` + `add_field()` — `title`/`description` diisi sekali di level konstruktor, `add_field()` bisa dipanggil berkali-kali
- `inline=True` cuma sejajar kalau field-field di sekitarnya juga `inline=True` dan bersebelahan langsung
- `set_footer(text=...)` butuh keyword argument, bukan positional
- `timestamp` wajib timezone-aware: `datetime.now(timezone.utc)`
- Prinsip refactor: pertahankan fetch logic lama, ganti presentasi `tabulate` → `Embed` — refactor lebih baik daripada rewrite dari nol

---

## Capstone — Auto Signal Bot

### Arsitektur & Pembagian Tanggung Jawab
- **`scanner.py`** — synchronous murni, tidak ada `async def` sama sekali. Berisi *pure functions* tanpa state tersembunyi: `fetch_prices()`, `hitung_persen()`, `cek_trigger()`, `update_state()`. `baseline` dan `cooldown_until` dioper sebagai parameter, bukan disimpan sebagai variabel global di file ini.
- **`bot.py`** — async, memegang semua state yang harus "diingat" antar-iterasi (`baseline`, `cooldown_until`, `config`, `i`) sebagai variabel **global**, karena `tasks.loop` memanggil fungsinya otomatis tanpa argumen tiap iterasi.
- `asyncio.to_thread()` **wajib** dipakai untuk memanggil `fetch_prices()` dari `bot.py` — karena fungsi itu pakai `time.sleep()` (synchronous), memanggilnya langsung tanpa `to_thread()` akan membuat `time.sleep()` blocking **seluruh** event loop bot, bukan cuma satu iterasi.

### Desain Konfigurasi (`config.json`)
Field: `coins`, `currencies`, `threshold_percent`, `interval_seconds`, `cooldown_minutes`, `max_retry_attempts`.

### Baseline — Rolling (bukan tetap)
`update_state()` dipanggil untuk **semua** coin tiap iterasi (kecuali iterasi pertama, yang cuma mengisi baseline awal tanpa cek trigger), terlepas dari hasil trigger-nya. Ini supaya baseline nggak "basi" walau ada coin yang sedang cooldown. Konsekuensinya: harga yang dibandingkan selalu "harga sekarang vs harga di iterasi sebelumnya", bukan vs harga di titik waktu tetap.

### Cooldown — Per-Coin, Berbasis Datetime
`cooldown_until` adalah dict `{coin: datetime}`, bukan boolean dan bukan global untuk semua coin. Coin yang belum pernah trigger sama sekali **absen** dari dict ini (bukan `None`, bukan `False` — key-nya memang tidak ada).

Logika cek status cooldown di `cek_trigger()`:
```python
cooldown_time = cooldown_until.get(coin)
sedang_cooldown = cooldown_time is not None and datetime.now(timezone.utc) < cooldown_time
```
`cooldown_until[coin]` **hanya** ditambahkan untuk coin yang trigger-nya `True`, di `scanner_loop`, di loop terpisah **setelah** proses kirim embed selesai — bukan di dalam `cek_trigger()` itu sendiri (fungsi itu cuma boleh *membaca* state, bukan menulisnya, supaya tetap predictable dan gampang di-test).

### Trigger — Logika AND, Bukan OR
```python
if abs(persen) >= threshold_percent and not sedang_cooldown:
```
Kirim ke Discord **hanya** kalau perubahan harga melewati threshold **dan** coin itu tidak sedang cooldown — cuma 1 dari 4 kombinasi yang menghasilkan post. Wajar dan sehat kalau bot jarang trigger; itu tanda threshold representatif, bukan bug.

### Error Handling di `fetch_prices()` — Dibedakan Berdasarkan Sifat Error
| Error | Sifat | Perlakuan |
|---|---|---|
| 429 (rate limit) | Sementara | Retry dengan `time.sleep(i*interval)`, ditangani internal, `bot.py` tidak perlu tahu |
| 500/502/503 | Sementara | Retry sama seperti di atas |
| Timeout/ConnectionError | Sementara | Retry sama seperti di atas |
| 400/404 | **Permanen** (config salah) | `raise ValueError` — diteruskan ke `bot.py`, karena retry tidak akan mengubah hasil |
| Coin hilang dari response sukses (200 tapi ID tidak dikenali) | **Permanen** | `raise ValueError` menyebut coin spesifik yang hilang |
| InvalidURL | Bug programmer, bukan human-input-error | `logger.critical()` + `return None`, bukan `raise` |
| Retry habis tanpa 400/404 | Sementara tapi berkepanjangan | `return None` |

Prinsip di balik pembagian ini: *"fail loud untuk bug permanen, fail silent-dengan-retry untuk gangguan sementara"*. Kalau semua error di-`return None` tanpa dibedakan, bot akan terlihat "jalan normal" padahal diam-diam gagal terus — sulit di-debug.

Di `scanner_loop`, exception `ValueError` ditangani beda dari hasil `None`:
- **`ValueError`** → `logger.critical()` + kirim pesan ke channel Discord + `scanner_loop.stop()` (permanen, config perlu diperbaiki manual)
- **`None`** → `logger.warning()` + `return` (skip iterasi ini saja), **tidak** `stop()` — karena sifatnya sementara dan kemungkinan pulih di iterasi berikutnya

### `off_by_one` & Bug Kecil yang Sempat Terjadi
- `range(1, max_retry)` → seharusnya `range(1, max_retry + 1)`, supaya `max_retry` beneran menghasilkan jumlah percobaan yang sesuai
- `abs()` sempat lupa ditambahkan di `cek_trigger()`, sehingga penurunan harga tajam tidak terdeteksi sebagai trigger

### Command Manual: `!price` dan `!status`
Dua command ini punya sumber data yang **sengaja berbeda**:

- **`!price <coin>`** — fetch **baru**, bukan ambil dari `baseline`. Alasan: user mau tahu harga *sekarang*, bukan harga di iterasi terakhir `scanner_loop` yang bisa saja beberapa menit lalu. Tidak menyentuh `baseline` maupun `cooldown_until` — murni "tanya harga", terpisah dari alur auto-scan. `coin.lower()` dipakai supaya input case-insensitive, karena CoinGecko ID selalu lowercase. `ValueError` dari `fetch_prices()` (coin tidak dikenali) ditangkap lokal di command ini, bukan dilempar ke `on_command_error`, supaya pesannya bisa spesifik ("Coin X tidak dikenali").
- **`!status`** — **tidak** fetch baru, murni membaca variabel global (`baseline`, `cooldown_until`, `config["coins"]`) yang sudah ada. Loop dari `config["coins"]` (bukan `cooldown_until.items()` langsung), karena tidak semua coin yang dipantau tentu ada di `cooldown_until` — yang belum pernah trigger memang absen dari dict itu.

Perhitungan "waktu tersisa" cooldown:
```python
sisa = waktu_cooldown - datetime.now(timezone.utc)
menit, detik = divmod(int(sisa.total_seconds()), 60)
```
`timedelta` (hasil pengurangan dua `datetime`) **tidak** punya method `.strftime()` — itu cuma dimiliki `datetime`. `strftime()` langsung ke `waktu_cooldown` tanpa dikurangi dulu akan menampilkan jam absolut, bukan durasi (ini bug nyata yang sempat terjadi: cooldown 5 menit tampil sebagai "44 menit" karena `strftime("%M:%S")` membaca bagian menit dari jam absolut, bukan hasil selisih).

### `on_command_error` — `elif`, Bukan `if` Terpisah
```python
if isinstance(error, commands.MissingRequiredArgument):
    ...
elif isinstance(error, commands.CommandNotFound):
    ...
elif isinstance(error, commands.BadArgument):
    ...
else:
    logger.error(...)
    ...
```
Kalau ditulis pakai `if` terpisah (bukan `elif`), `else` di akhir akan **selalu** menempel ke kondisi `if` terakhir sebelumnya, bukan ke keseluruhan rangkaian — menyebabkan dua pesan error terkirim sekaligus untuk satu kejadian error (bug nyata yang sempat terjadi: `CommandNotFound` dan pesan generic muncul bersamaan). Pola bug yang sama juga sempat terjadi di logika pemilihan warna embed (`if`/`if`/`else` alih-alih `if`/`elif`/`else`) — kondisi "harga naik semua" tertimpa warna default karena `if` kedua tetap dievaluasi.

### Bug Non-Obvious yang Ditemukan Selama Proses
- **Logger duplikat** — `scanner.py` sempat punya `get_logger()` sendiri yang setup handler lagi, sehingga log tercetak dua kali. Fix: `scanner.py` cukup `logging.getLogger(__name__)` tanpa setup ulang, mewarisi konfigurasi dari `bot.py` yang setup lebih dulu (karena `bot.py` yang jadi entry point dan meng-`import scanner`, bukan sebaliknya).
- **`NameError` diam-diam mematikan loop** — `datetime`/`timezone` sempat lupa di-`import` di `scanner.py`. Errornya bukan `ValueError`, jadi tidak tertangkap oleh `except ValueError` di `scanner_loop`, dan `tasks.loop` berhenti diam-diam tanpa pesan apa pun. Ini akar dari gejala "fetch cuma jalan sekali".
- **`await scanner_loop.start()` salah** — `.start()` bukan sesuatu yang perlu di-`await` sampai selesai (dia mulai loop *di background*, bukan tugas yang selesai sekali panggil). Memakai `await` di depannya membuat `on_ready` "menunggu" sesuatu yang tidak pernah selesai secara wajar.
- **`tasks.loop` tidak menerima parameter seperti fungsi biasa** — fungsi yang didekorasi `@tasks.loop` dipanggil otomatis tanpa argumen tiap iterasi, sehingga state apa pun yang perlu "diingat" antar-panggilan (`baseline`, `cooldown_until`, `config`, `i`) harus jadi variabel global, bukan parameter fungsi.

### CoinGecko API — Realita Cache & Rate Limit
- CoinGecko (termasuk Demo tier) meng-cache data di sisi server sekitar 1-5 menit — request tetap terhitung sebagai pemakaian kuota walau data yang dikembalikan identik dengan request sebelumnya (belum lewat window cache)
- `interval_seconds` yang terlalu pendek (15-30 detik) menyebabkan sebagian besar fetch memboroskan kuota untuk data yang belum berubah di sisi server — disesuaikan ke rentang 60-120 detik supaya lebih selaras dengan siklus cache
- Public/keyless API **bukan** solusi lebih baik dari Demo key — cache-nya sama, sementara rate limit-nya justru lebih ketat, tidak cocok untuk polling terjadwal
- Emoji asli (bukan library-nya) yang jadi kendala — Windows 8 tidak nyaman dipakai mengetik/melihat emoji di editor, bukan soal Discord tidak mendukungnya. Solusi: pakai placeholder teks (`[UP]`/`[DOWN]`/`[FLAT]`) yang tetap terbaca jelas di sisi client Discord manapun

---

## Key Learnings — Asyncio & Discord

- `create_task()` dipakai untuk concurrent execution ketika ada 2+ hal yang harus jalan bersamaan tanpa saling blocking, bukan sekadar "karena ada loop"
- `asyncio.to_thread()` wajib untuk memanggil fungsi synchronous (yang memakai `time.sleep()`) dari konteks async, supaya tidak memblokir seluruh event loop
- `bot.get_channel()` dipakai untuk mengirim pesan ke channel tanpa `ctx` — dibutuhkan karena background loop tidak dipicu oleh command user, jadi tidak punya akses ke `ctx`
- `bot.process_commands(message)` wajib dipanggil manual di `on_message` kalau event itu di-override
- `discord.Embed`: `add_field()` bisa dipanggil berkali-kali, tapi parameternya `name`/`value`/`inline` — bukan `key`/`value`
- Channel ID dan token bot disimpan di `.env`, bukan hardcode — supaya bisa diganti tanpa menyentuh kode

## Key Learnings — Error Handling & State Management

- Pembagian error "sementara vs permanen" menentukan apakah harus retry-diam-diam atau *fail loud* ke level yang lebih tinggi
- Fungsi yang mengecek kondisi (`cek_trigger`) sebaiknya hanya *membaca* state, bukan menulisnya — supaya predictable dan gampang ditest; yang menulis state adalah pemanggilnya (`scanner_loop`)
- `dict.get(key)` mengembalikan `None` untuk key yang tidak ada, dipakai untuk membedakan "belum pernah terjadi" dari "pernah terjadi tapi sudah tidak berlaku lagi"
- `timedelta` (hasil pengurangan dua `datetime`) tidak punya `.strftime()` — hanya `datetime` yang punya; durasi diformat pakai `divmod(int(td.total_seconds()), 60)`
- Urutan `if`/`elif`/`else` yang salah ditulis sebagai `if`/`if`/`else` terpisah adalah sumber bug yang halus — kondisi yang seharusnya eksklusif malah saling menimpa

## Key Learnings — Engineering Mindset

- Refactor (mengganti presentasi, mempertahankan fetch logic) lebih baik daripada rewrite dari nol
- Variabel yang "kebetulan jalan" karena urutan eksekusi program (bukan karena strukturnya memang menjamin itu) tetap perlu disadari sebagai rapuh, meski tidak selalu mendesak untuk segera diperbaiki
- Keputusan desain yang sengaja tidak menyeragamkan dua kondisi berbeda (misal: tabel iterasi pertama vs iterasi berikutnya) adalah pilihan valid selama alasannya jelas dan konsisten dipegang — bukan otomatis dianggap kekurangan

---

## Koneksi ke Roadmap AI Trading Agent

Capstone Phase 4 ini adalah implementasi pertama dari **output layer** — sinyal dari scanner keluar lewat Discord ke channel trader, persis peran yang direncanakan untuk folder `discord/` di arsitektur akhir. Pola `scanner.py` (synchronous, pure functions, state dioper sebagai parameter) adalah cetakan awal untuk `analysis/` dan `tools/` — logic murni yang bisa dipakai ulang lepas dari async/bot. Prinsip *fail loud untuk error permanen* yang dipakai di sini juga jadi dasar penting untuk `risk/` guardrails di Phase 8, di mana kesalahan konfigurasi harus segera menghentikan sistem, bukan diam-diam diabaikan.

---

*Notes ini ringkasan pembelajaran Phase 4 secara keseluruhan.*