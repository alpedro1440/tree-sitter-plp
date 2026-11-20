"""File contoh untuk Tugas 1 dan Tugas 3."""

import os
from pathlib import Path


def sapa(nama, gelar="Mahasiswa"):
    """Mengembalikan salam sederhana."""
    pesan = f"Halo {gelar} {nama}"
    print(pesan)
    return pesan


def hitung_total(harga, jumlah):
    total = harga * jumlah
    if total >= 100000:
        print("Diskon dapat dipertimbangkan")
    else:
        print("Harga normal")
    return total


class Pesanan:
    def __init__(self, kode, pemilik):
        self.kode = kode
        self.pemilik = pemilik

    def tampilkan(self):
        print(f"Pesanan {self.kode} milik {self.pemilik}")


if __name__ == "__main__":
    sapa("Budi")
    pesanan = Pesanan("ORD-01", "Budi")
    pesanan.tampilkan()
