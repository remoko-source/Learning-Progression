# Phase 5 — Day 4: Conversation History

**Status:** SELESAI ✅
**Capstone terkait:** Mp-04 "Context Keeper CLI" (`konsul_market_CLI.py`) — level 🔴🔴 hard mode

---

## 1. Kenapa Conversation History Dibutuhkan

LLM itu **stateless** — server tidak menyimpan apa-apa dari request sebelumnya. Tiap `generate_content()` adalah kejadian baru yang kosong.

Supaya AI *terasa* "inget" percakapan sebelumnya, solusinya bukan bikin server nyimpen, tapi **kita yang kirim ulang SELURUH percakapan** tiap kali request baru — sebagai list.

> Analogi: ngobrol sama orang yang short-term memory loss tiap 5 detik. Supaya dia tetap nyambung, kita harus baca ulang seluruh transkrip chat ke dia sebelum dia jawab pertanyaan baru.

---

## 2. Format History Gemini API

Tiap giliran bicara = 1 `dict` di dalam list:

```python
history = [
    {"role": "user", "parts": [{"text": "Harga BTC berapa?"}]},
    {"role": "model", "parts": [{"text": "BTC saat ini $65,000"}]}
]
```

- `"role"` → `"user"` atau `"model"` (bukan `"assistant"`)
- `"parts"` → **list**, karena secara desain API bisa nampung lebih dari teks (misal gambar). Kita cuma pakai teks, tapi strukturnya tetap wajib list.

**Kenapa harus list of dict, bukan 1 string gabungan?**
Supaya AI tau siapa ngomong apa. Kalau digabung jadi 1 string panjang, AI harus nebak-nebak sendiri mana bagian user, mana bagian model — rawan salah paham.

---

## 3. Alur Pemakaian di Dalam Function

```python
def tanya_ai(chat, history, instructions="default"):
    # 1. Tulis pesan user ke history SEBELUM kirim
    history.append({"role": "user", "parts": [{"text": chat}]})

    # 2. Kirim SELURUH history (bukan cuma chat) ke API
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=history,   # <- bedanya dari Mp-03 (dulu contents=chat)
        config=config
    )

    # 3. Tulis balasan AI ke history SETELAH dapat response
    history.append({"role": "model", "parts": [{"text": response.text}]})

    return response.text
```

`history = []` didefinisikan **sekali**, di luar loop utama — bukan di dalam function, bukan di dalam `while`.

---

## 4. `types.GenerateContentConfig` — Alternatif Dict untuk Config

Dict biasa (yang dipakai sejak Mp-03):
```python
config = {"temperature": 0.7, "max_output_tokens": 1000}
```

Alternatif pakai `types.GenerateContentConfig`:
```python
from google.genai import types

config = types.GenerateContentConfig(
    system_instruction="...",
    temperature=0.7,
    max_output_tokens=1000
)
```

**Bedanya:**
- Dict: akses pakai `config["temperature"]`, typo nama field tidak langsung ketahuan (bisa diam-diam diabaikan API, buang token percuma)
- `types.GenerateContentConfig`: akses pakai titik `config.temperature`, typo field langsung kasih error SEBELUM request terkirim → hemat token kalau salah ketik

Dua-duanya valid, ini soal tradeoff (fleksibel vs validasi lebih awal).

---

## 5. Mutable List: Kenapa `.append()` di Dalam Function Kebawa Keluar

Waktu `history` dioper sebagai argumen ke function, yang dioper itu **referensi/alamat ke objek list yang sama**, bukan salinan/copy baru. Jadi `.append()` di dalam function mengubah objek fisik yang sama dengan yang di luar — ini disebut **reference/mutable passing**.

Bandingkan dengan int/str (immutable) — assignment ulang di dalam function TIDAK mengubah variabel di luar, karena itu bikin objek baru.

**Kenapa tetap dioper sebagai parameter, bukan langsung dibaca dari global (walau secara teknis bisa)?**
1. **Predictability** — orang yang baca function langsung tau dependency-nya tanpa buka isi function
2. **Konsisten** dengan pola `scanner.py` di Capstone Phase 4 (`baseline`, `cooldown_until` juga dioper sebagai parameter)
3. **Fleksibilitas** — bisa punya lebih dari 1 `history` (misal beda user/sesi) pakai function yang sama

---

## 6. Error Handling `google.genai.errors`

Hierarki:
```
APIError               (base — payung paling luas)
├── ClientError         (4xx — salah di request kita, JANGAN retry)
└── ServerError         (5xx — salah di server Google, LAYAK retry)

UnknownApiResponseError  (terpisah — response datang tapi bentuknya aneh)
```

Ditambah, terpisah dari SDK (level koneksi mentah):
- `ConnectionError` — koneksi putus
- `TimeoutError` — request kelamaan

```python
try:
    response = client.models.generate_content(...)
except errors.ClientError as e:
    if e.code in (400, 401, 403, 404):
        # fatal, stop — jangan retry
        ...
except errors.ServerError as e:
    # sementara, layak retry
    ...
except (ConnectionError, TimeoutError):
    # koneksi/jaringan bermasalah, layak retry
    ...
```

**Retry** (masalah sementara): 429, 5xx (500/502/503/504), `ConnectionError`, `TimeoutError`
**Stop/raise langsung** (masalah permanen): 400, 401, 403, 404

> 429 itu pengecualian — statusnya 4xx tapi tetap layak retry, karena bukan salah format, cuma kebanyakan request.

---

## 7. `finish_reason` — Cek Manual, Bukan Except

`finish_reason` bukan exception yang otomatis di-raise. Dia field biasa di `response` yang harus dicek pakai `if`, SETELAH response berhasil didapat — karena dari sudut pandang API, request itu tetap **sukses** (200 OK) walau isinya kepotong.

```python
if response.candidates[0].finish_reason == types.FinishReason.MAX_TOKENS:
    raise AITokenBudgetExceeded("Jawaban AI terpotong")
```

Custom exception dibuat manual (pola sama seperti `SaldoTidakCukupError`/`PathNotFoundError` Phase 2):
```python
class AITokenBudgetExceeded(Exception):
    pass
```

---

## 8. Observasi Nyata: Thinking Budget

Dari `response.usage_metadata` (Mp-04, `max_output_tokens=1000`):
- `thoughts_token_count` bisa makan 500–700 dari total 1000
- Sisanya baru buat jawaban aktual (`candidates_token_count`)
- Thinking budget itu **adaptif**, bukan angka tetap — pertanyaan lebih kompleks bisa makan thinking jauh lebih besar

Implikasi: `max_output_tokens` adalah pagar gabungan thinking + jawaban, bukan cuma jawaban.

---

## 9. Mini Project — Mp-04 "Context Keeper CLI"

**File:** `konsul_market_CLI.py`
**Level:** 🔴🔴 (hard mode — tanpa skeleton, dikerjakan mandiri)

### Fitur yang diimplementasikan
- Validasi input: `chat` kosong → `ValueError`, `history` bukan list → `TypeError`
- Logging 2-layer: `StreamHandler` (level ERROR+, tampil di terminal) + `FileHandler` (level INFO+, ke file log)
- Custom exception `AITokenBudgetExceeded`
- Error handling lengkap: `ClientError` (fatal 400/401/403/404 vs recoverable), `ServerError`, `ConnectionError`/`TimeoutError`
- History trimming `history[-6:]` tiap 5 iterasi
- Warning log saat total token mendekati batas `max_output_tokens`

### Bug substansial yang ditemukan & diperbaiki sendiri

**1. Trimming ke-skip kalau exception nyangkut di tengah for-loop**
Baris `history = history[-6:]` ada di dalam `try`, setelah `for`. Kalau exception terjadi di tengah iterasi `for`, program lompat ke `except` dan baris trimming itu tidak pernah kejalan.
→ Solusi: pindahkan trimming ke blok `finally`, supaya pasti jalan apapun hasil `for`-nya.

**2. Perbandingan token yang tidak sepadan**
Awalnya membandingkan `max_output_tokens` (cuma mengatur OUTPUT: jawaban + thinking) dengan `total_token_count` (gabungan input + output + thinking). Dua angka ini tidak dari "kantong" yang sama.
→ Diperbaiki ke field yang sepadan.

---

## 10. Ringkasan Konsep Kunci

| Konsep | Poin Penting |
|---|---|
| Stateless LLM | Server tidak inget apa-apa, history harus dikirim ulang penuh tiap request |
| Format history | List of dict, `role` + `parts` (list, walau isinya 1 teks) |
| `contents=history` | Menggantikan `contents=chat` — kirim SEMUA, bukan cuma pesan baru |
| `types.GenerateContentConfig` | Alternatif dict, validasi field lebih awal sebelum buang token |
| Mutable passing | `.append()` di dalam function kebawa keluar karena reference ke objek sama |
| State sebagai parameter | Predictability + konsisten pola `scanner.py` + fleksibilitas multi-sesi |
| `finish_reason` | Dicek manual pakai `if`, bukan `except` — request tetap sukses walau kepotong |
| Thinking budget | Adaptif, ikut makan `max_output_tokens` — cek pakai `usage_metadata` |

---

## 11. Next: Phase 5 Day 5+

Belum ditentukan detailnya — kemungkinan lanjut ke integrasi data market dengan LLM, structured outputs/JSON mode, menuju Capstone Phase 5 "AI Setup Generator".