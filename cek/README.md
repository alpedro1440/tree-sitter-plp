# Tugas 6 - CLI pemeriksa kode Python

## Instalasi

Dari folder utama proyek:

```powershell
py -m pip install tree-sitter tree-sitter-python
```

## Menjalankan

```powershell
py .\cek\cek.py .\cek\uji
```

Program melaporkan:

1. Komentar yang mengandung `TODO` atau `FIXME`, dengan nama file dan baris.
2. Fungsi yang rentang definisinya lebih dari 30 baris.
3. File yang syntax tree-nya mengandung error, beserta lokasi node `ERROR`/`MISSING` pertama.

Direktori `.git`, `.venv`, `venv`, `env`, `node_modules`, `__pycache__`, `.mypy_cache`, dan
`.pytest_cache` dilewati agar pemindaian tidak membuang waktu pada lingkungan atau cache.



