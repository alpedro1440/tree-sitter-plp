# Tugas 4-5 - Grammar dan highlight DSL filter

## Generate dan uji grammar

Dari folder ini:

```powershell
tree-sitter generate
tree-sitter parse .\contoh.filter
tree-sitter test
```

Grammar mendukung perbandingan, prioritas `and`/`or`, `not`, ekspresi bertanda kurung, string, angka, boolean, `in` dengan daftar nilai, dan `contains`.

## Highlight

Jalankan `tree-sitter init-config`, lalu tambahkan folder induk direktori `tree-sitter-filter` ke `parser-directories` di konfigurasi CLI. Pastikan `tree-sitter.json` menunjuk ke `queries/highlights.scm` dan mencantumkan ekstensi `filter`.

```powershell
tree-sitter highlight .\contoh.filter
```

Corpus berisi tujuh kasus uji pada `test/corpus/dasar.txt`. Jangan memakai `tree-sitter test --update` sebelum memeriksa bahwa pohon hasil parse memang sesuai dengan input dan prioritas operator.
