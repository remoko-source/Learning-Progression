# Notes — Phase 4 Day 6 Review

Review 4 topik yang masih bingung setelah Embed selesai secara teknis, sebelum lanjut ke Capstone Auto Signal Bot.

---

## 1. Nested Structure (List of Dict / Dict of List)

**Masalah awal:** sering ketuker antara `.append()` (untuk list) dan `key = value` (untuk dict) — sempat nulis `scan_results["signal"] = "BUY"` padahal maksudnya nambah ke dalam list di key `"BTC"`.

**Yang diperbaiki:**
- `.append()` HANYA untuk list. Dict tidak punya `.append()`, dict pakai assign `dict[key] = value`.
- Cara baca path nested: turun key/index satu-satu dari kiri ke kanan, baru modifikasi di paling ujung.
  ```python
  scan_results["BTC"].append({"signal": "BUY", "confidence": 80})
  data[0]["blabla"][3] = 270
  ```
- Kalau sudah tahu key/index yang dicari → akses langsung, JANGAN loop pakai `.items()` untuk itu.
- `.items()` hanya dipakai kalau mau proses **semua** pasangan key-value tanpa peduli nama key-nya spesifik apa.
- Key integer vs string: kalau data berasal dari JSON (`json.load()`), semua key otomatis jadi string — key integer asli di Python tidak akan match.

---

## 2. List/Dict Comprehension

**Masalah awal:** belum yakin kapan comprehension boleh dipakai, sempat mikir "cuma bisa hasilin 1 variabel".

**Yang diperbaiki:**
- Comprehension = cara singkat bikin **1 collection baru** (list/dict) dari transform/filter sederhana.
- Pola: `[EKSPRESI for ITEM in ITERABLE]` atau `{KEY: VALUE for ITEM in ITERABLE}`.
- Boleh pakai 2+ variabel di loop-nya (misal `for coin, info in data.items()`) — itu soal *unpacking* tuple, beda hal dari jumlah collection yang dihasilkan (selalu 1).
- **Batas pemakaian:** cocok untuk transform/filter 1 langkah. Begitu ada side-effect (`print`, `logger`, `embed.add_field()`, dll) atau logic if-elif berlapis → **wajib** balik ke loop biasa, jangan dipaksa.
- Contoh anti-pattern: memaksa `embed.add_field(...)` masuk comprehension — hasilnya list berisi `None` yang tidak dipakai, cuma buang-buang readability.

---

## 3. JSON — Safe Load & Append yang Benar

**Masalah awal:** bingung apakah nambah data ke JSON selalu butuh loop.

**Yang diperbaiki:**
- File JSON **tidak bisa** di-append langsung seperti file `.txt` — satu file JSON adalah satu struktur utuh.
- Alur wajib: **LOAD** (jadi struktur Python) → **UBAH** di memory → **DUMP ulang** seluruh struktur (mode `"w"`, timpa semua).
- Loop/comprehension hanya dibutuhkan kalau sedang **reshape data mentah** (misal dari `requests.json()`) ke struktur yang diinginkan — bukan untuk sekadar menambah 1 entry baru ke list yang strukturnya sudah sesuai (itu cukup `.append()` satu baris).
- Pola *safe read* yang dipakai:
  ```python
  def load_journal(filepath):
      path = Path(filepath)
      if not path.exists():
          return []
      try:
          with open(path, "r") as f:
              return json.load(f)
      except json.JSONDecodeError:
          return []
  ```
- `save_journal` (dump) tidak butuh `try-except JSONDecodeError` karena itu error khusus proses **baca**, bukan proses **tulis**.

---

## 4. Custom Exception & `on_command_error`

**Masalah awal:** mengira `on_command_error` cuma bisa menangani satu jenis error, dan bingung custom exception ditaruh di mana.

**Yang diperbaiki:**
- Aturan bikin custom exception: kalau errornya berasal dari **aturan bisnis sendiri** (bukan dari Python/library) → bikin custom exception. Kalau sudah ada built-in (`CommandNotFound`, `KeyError`, dll) → pakai itu, jangan bikin ulang.
- `on_command_error` adalah **satu event handler global**, tapi di dalamnya bisa punya banyak cabang `isinstance()` — satu cabang per jenis error. Bukan keterbatasan, ini memang pola production.
- **2 lapis penanganan:**
  - Error **spesifik ke 1 command** (custom exception yang di-`raise` manual di dalam command) → boleh ditangani lokal pakai `try-except` di dalam command itu sendiri, supaya pesannya bisa sangat spesifik.
  - Error **generic lintas command** (`CommandNotFound`, `MissingRequiredArgument` — otomatis di-raise discord.py **sebelum** command body jalan) → **wajib** ditangani di `on_command_error`, tidak bisa ditangkap dengan `try-except` lokal karena command body belum sempat dieksekusi.
- Kalau butuh pesan beda per command untuk error generic (misal `MissingRequiredArgument`), tetap satu cabang `isinstance`, lalu sortir lagi pakai `ctx.command.name` di dalamnya.

---

## 5. `create_task()` vs `asyncio.sleep()`

**Masalah awal:** paham konsep "jalan di background" tapi belum jelas kapan pakai yang mana.

**Yang diperbaiki:**
- `asyncio.sleep(n)`: menjeda **coroutine yang sedang berjalan itu sendiri**, tapi tetap kasih kesempatan coroutine lain jalan selama menunggu. Tetap 1 alur linear.
- `create_task()`: melepas sebuah coroutine jalan **paralel**, tidak menunggu selesai untuk lanjut ke baris berikutnya.
- **Alasan yang tepat pakai `create_task()` bukan "karena ada loop"**, tapi karena ada **2+ hal yang harus berjalan bersamaan tanpa saling blocking**. Contoh: bot harus tetap standby dengar command user SEKALIGUS scanner loop jalan terus di background — kalau `scanner_loop()` (infinite loop) di-`await` biasa, baris setelahnya (`bot.start()`) tidak akan pernah kejalanin.
- Command manual (`!scan`) **tidak** butuh `create_task()` karena memang harus selesai dulu baru reply — itu perilaku yang diinginkan, bukan masalah.
- Kalau `create_task()` hasilnya perlu ditunggu selesai di titik tertentu, simpan ke variabel lalu `await` variabel itu di akhir:
  ```python
  task_backscan = asyncio.create_task(background_scanner())
  await proses_command()
  await task_backscan
  ```
- `bot.get_channel(CHANNEL_ID)` dipakai untuk kirim pesan **tanpa** `ctx` (situasi tanpa trigger user, misal dari background loop). Butuh `await bot.wait_until_ready()` dulu sebelum dipakai, dan `CHANNEL_ID` sebaiknya disimpan di `.env`.

---

## Status

Semua 5 topik di atas sudah divalidasi lewat 10 soal latihan (`review_day6.py`), dikerjakan mandiri tanpa bantuan AI, hasil output sudah sesuai ekspektasi termasuk soal tersulit (Soal 10 — `create_task` + `await` di akhir untuk memastikan background task benar-benar selesai sebelum program keluar).

**Day 6 CLOSED. Siap lanjut ke Capstone Phase 4: Auto Signal Bot.**