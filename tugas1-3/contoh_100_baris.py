"""Contoh modul pengelolaan pesanan untuk uji penjelajah node (lebih dari 100 baris)."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Item:
    kode: str
    nama: str
    harga: int
    stok: int

    def tersedia(self, jumlah: int) -> bool:
        return jumlah > 0 and self.stok >= jumlah

    def kurangi_stok(self, jumlah: int) -> None:
        if not self.tersedia(jumlah):
            raise ValueError("Stok tidak mencukupi")
        self.stok -= jumlah


@dataclass
class BarisPesanan:
    item: Item
    jumlah: int

    def subtotal(self) -> int:
        return self.item.harga * self.jumlah


class Keranjang:
    def __init__(self, pemilik: str):
        self.pemilik = pemilik
        self.baris: list[BarisPesanan] = []
        self.dibuat_pada = datetime.now()

    def tambah(self, item: Item, jumlah: int) -> None:
        if jumlah <= 0:
            raise ValueError("Jumlah harus positif")
        if not item.tersedia(jumlah):
            raise ValueError("Stok tidak mencukupi")
        for baris in self.baris:
            if baris.item.kode == item.kode:
                baris.jumlah += jumlah
                return
        self.baris.append(BarisPesanan(item, jumlah))

    def hapus(self, kode_item: str) -> bool:
        for indeks, baris in enumerate(self.baris):
            if baris.item.kode == kode_item:
                del self.baris[indeks]
                return True
        return False

    def kosongkan(self) -> None:
        self.baris.clear()

    def total_item(self) -> int:
        return sum(baris.jumlah for baris in self.baris)

    def total_harga(self) -> int:
        return sum(baris.subtotal() for baris in self.baris)

    def valid(self) -> bool:
        return bool(self.baris) and all(baris.jumlah > 0 for baris in self.baris)

    def ringkasan(self) -> dict[str, int | str]:
        return {
            "pemilik": self.pemilik,
            "jumlah_baris": len(self.baris),
            "total_item": self.total_item(),
            "total_harga": self.total_harga(),
        }


class LayananPesanan:
    def __init__(self):
        self.pesanan: dict[str, Keranjang] = {}
        self.nomor_berikutnya = 1

    def buat_keranjang(self, pemilik: str) -> str:
        kode = f"ORD-{self.nomor_berikutnya:04d}"
        self.nomor_berikutnya += 1
        self.pesanan[kode] = Keranjang(pemilik)
        return kode

    def ambil(self, kode: str) -> Optional[Keranjang]:
        return self.pesanan.get(kode)

    def hapus_pesanan(self, kode: str) -> bool:
        if kode not in self.pesanan:
            return False
        del self.pesanan[kode]
        return True

    def hitung_semua_pesanan(self) -> int:
        return sum(keranjang.total_harga() for keranjang in self.pesanan.values())

    def daftar_kode(self) -> list[str]:
        return sorted(self.pesanan.keys())


def format_rupiah(nilai: int) -> str:
    teks = f"{nilai:,}".replace(",", ".")
    return f"Rp{teks}"


def validasi_kode(kode: str) -> bool:
    if not kode:
        return False
    if not kode.startswith("ORD-"):
        return False
    bagian = kode.split("-")
    return len(bagian) == 2 and bagian[1].isdigit()


def cari_item(katalog: list[Item], kata_kunci: str) -> list[Item]:
    kata = kata_kunci.casefold()
    hasil = []
    for item in katalog:
        if kata in item.nama.casefold() or kata in item.kode.casefold():
            hasil.append(item)
    return hasil


def ringkas_katalog(katalog: list[Item]) -> dict[str, int]:
    jumlah_produk = len(katalog)
    total_stok = sum(item.stok for item in katalog)
    nilai_stok = sum(item.stok * item.harga for item in katalog)
    return {
        "jumlah_produk": jumlah_produk,
        "total_stok": total_stok,
        "nilai_stok": nilai_stok,
    }


def contoh_data() -> list[Item]:
    return [
        Item("BRG-01", "Keyboard", 150000, 12),
        Item("BRG-02", "Mouse", 75000, 20),
        Item("BRG-03", "Monitor", 1800000, 5),
    ]


def main() -> None:
    katalog = contoh_data()
    layanan = LayananPesanan()
    kode = layanan.buat_keranjang("Budi")
    keranjang = layanan.ambil(kode)
    if keranjang is not None:
        keranjang.tambah(katalog[0], 2)
        keranjang.tambah(katalog[1], 1)
        print(keranjang.ringkasan())
        print(format_rupiah(keranjang.total_harga()))
    print(ringkas_katalog(katalog))


if __name__ == "__main__":
    main()
