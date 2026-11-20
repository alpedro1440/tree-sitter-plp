# Pengumpulan Tugas Awal: Memahami Tree-sitter (Tugas 1-6)

Paket ini berisi skrip, grammar DSL, query, test corpus, hasil pengujian, bukti screenshot, laporan, dan draf proposal sesuai format pengumpulan pada materi.

## Struktur pengumpulan

```text
 tree-sitter-pengumpulan/
 ├── tugas1-3/
 │   ├── t1.py
 │   ├── jelajah.py
 │   ├── q.py
 │   ├── queries/                 # fungsi, print, imports
 │   ├── outputs/                 # hasil pengujian .txt
 │   ├── contoh.py
 │   ├── contoh_100_baris.py
 │   ├── kecil.py
 │   └── prediksi_pohon.md
 ├── tree-sitter-filter/
 │   ├── grammar.js
 │   ├── tree-sitter.json
 │   ├── queries/highlights.scm
 │   ├── test/corpus/dasar.txt
 │   └── contoh.filter
 ├── cek/
 │   ├── cek.py
 │   ├── README.md
 │   ├── uji/                     # fixture lokal valid dan rusak
 │   └── verifikasi_manual_itsdangerous.txt
 ├── bukti/                       # screenshot hasil uji aktual
 ├── hasil-pengujian/             # transkrip Tugas 4-6
 ├── requirements.txt
 ├── capture_outputs.ps1
 ├── laporan.pdf                  # maksimal 3 halaman
 └── proposal-draf.pdf            # maksimal 1 halaman
```

## Lingkungan pengujian

Pengujian dilakukan pada Windows PowerShell. Pada komputer pengujian:
- Python digunakan melalui perintah `py`.
- Tree-sitter CLI telah dipasang melalui Cargo (`cargo install tree-sitter-cli`).
- Node.js dikelola dengan FNM; saat pengujian versinya `v26.13.1`, npm `11.20.0`.
- `node` harus tersedia pada PATH terminal yang menjalankan `tree-sitter generate`, karena CLI menjalankan `grammar.js` melalui Node.js.
- Binding Python dipasang dengan `py -m pip install -r requirements.txt`.

Inisialisasi FNM untuk PowerShell (cukup sekali di `$PROFILE`):

```powershell
fnm env --use-on-cd --shell powershell | Out-String | Invoke-Expression
```

Setelah membuka terminal baru, verifikasi `node -v`, `npm.cmd -v`, dan `tree-sitter --version`. Jika kebijakan PowerShell memblokir `npm.ps1`, gunakan `npm.cmd` untuk perintah npm; paket ini tidak memerlukan instalasi CLI lewat npm karena CLI sudah dipasang melalui Cargo.

## Menjalankan tugas

### Tugas 1-3

```powershell
cd .\tugas1-3
py .\t1.py
py .\jelajah.py .\kecil.py
py .\jelajah.py .\contoh_100_baris.py
py .\q.py .\contoh.py all
```

Mode `q.py`: `fungsi`, `print`, `import`, atau `all`. Argumen ketiga adalah mode, bukan nama file `.scm`; query yang dipakai disimpan di folder `queries/`.

Untuk membuat ulang log dari mesin Windows, jalankan dari folder utama proyek:

```powershell
.\capture_outputs.ps1
```

### Tugas 4-5

```powershell
cd ..\tree-sitter-filter
tree-sitter generate
tree-sitter parse .\contoh.filter
tree-sitter test
tree-sitter highlight .\contoh.filter
```

Hasil uji pada mesin pengujian: **7/7 corpus tests lulus**. Highlight terlihat pada nama field, string, keyword, operator, dan angka. File `tree-sitter.json` sudah menempatkan `highlights` di dalam entri grammar.

### Tugas 6

```powershell
cd ..\cek
py .\cek.py .\uji
py .\cek.py .\repo-itsdangerous
```

Perintah kedua dijalankan pada clone lokal repositori publik `pallets/itsdangerous` (clone tersebut tidak disertakan di paket). Hasil aktual: 15 file Python diperiksa, 7 temuan; 1 TODO/FIXME dan 6 fungsi panjang. Tidak ada syntax error yang dilaporkan.

## Ringkasan hasil aktual

| Tugas | Hasil |
|---|---|
| 1 | Tiga contoh (fungsi, if/else, kelas) berhasil di-parse; input tanpa `:` menghasilkan `ERROR` dan `root_node.has_error=True`. |
| 2 | Penjelajah rekursif menghasilkan indentasi, tipe, posisi, dan field; diuji pada file contoh 161 baris. |
| 3 | Query nama fungsi/jumlah parameter, `print(...)`, dan import berhasil pada `contoh.py`. |
| 4 | `tree-sitter test`: 7 berhasil, 0 gagal. |
| 5 | `tree-sitter highlight` berjalan tanpa warning konfigurasi dan menampilkan warna token. |
| 6 | Fixture lokal: 3 temuan. ItsDangerous: 15 file, 7 temuan; dua temuan dicocokkan manual. |

Lihat `tugas1-3/outputs/` untuk transkrip Tugas 1-3, `hasil-pengujian/` untuk Tugas 4-6, dan `bukti/` untuk screenshot. Petikan Tugas 2 untuk file 161 baris hanya menampilkan 30 baris pertama sesuai tampilan terminal; jalankan `capture_outputs.ps1` untuk menyimpan output lengkap.

