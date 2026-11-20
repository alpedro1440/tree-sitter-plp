# Prediksi pohon - Tugas 1

Baca bagian ini sebelum menjalankan `t1.py`, lalu bandingkan dengan hasil parser. Ini adalah prediksi struktur, bukan pengganti output Tree-sitter yang sebenarnya.

## 1. Fungsi

Kode:

```python
def sapa(nama):
    return nama
```

Prediksi S-expression:

```scheme
(module
  (function_definition
    name: (identifier)
    parameters: (parameters (identifier))
    body: (block
      (return_statement (identifier))))
```

Node bernama yang terlihat: `module`, `function_definition`, `identifier`, `parameters`, `block`, `return_statement`. Token seperti `def`, `(`, `)`, dan `:` adalah node anonim.

## 2. If/else

Kode menggunakan assignment `nilai = 75`, lalu `if nilai >= 70` dengan blok `hasil = 'Lulus'`, dan cabang `else` berisi `hasil = 'Remedial'`.

Prediksi struktur: root `module` memiliki assignment dan `if_statement`. Di dalam `if_statement` terdapat kondisi perbandingan, blok consequence, dan blok alternatif/else. Cocokkan nama node dan field pastinya dengan output parser karena bentuk detailnya mengikuti grammar Python yang digunakan.

## 3. Kelas dengan satu method

Kode:

```python
class Mahasiswa:
    def __init__(self, nama):
        self.nama = nama
```

Prediksi struktur: `module` berisi `class_definition`; kelas memiliki nama `Mahasiswa` dan `block` body. Body berisi `function_definition` untuk `__init__`, parameter, dan assignment atribut `self.nama = nama`.

## Perbandingan yang harus ditulis

1. Catat node bernama dan node anonim yang benar-benar muncul dari output `t1.py`.
2. Hapus tanda `:` pada definisi fungsi, jalankan ulang, lalu catat apakah parser menandai `ERROR`, `MISSING`, atau keduanya.
3. Jelaskan bahwa `children` mengandung node bernama dan anonim, sedangkan `named_children` hanya mengandung node bernama.
