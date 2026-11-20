"""Aplikasi kecil untuk menguji detektor TODO dan fungsi panjang."""


def hitung_diskon(harga, persen):
    # TODO: tambahkan validasi bahwa harga tidak negatif.
    if harga < 0:
        return 0
    if persen < 0:
        persen = 0
    if persen > 100:
        persen = 100
    diskon = harga * persen / 100
    hasil = harga - diskon
    return round(hasil)


def proses_laporan_harian(data):
    """Fungsi sengaja dibuat panjang untuk menguji batas lebih dari 30 baris."""
    jumlah = 0
    total = 0
    berhasil = 0
    gagal = 0
    menunggu = 0
    nilai_tidak_valid = 0
    for entri in data:
        jumlah += 1
        nilai = entri.get("nilai", 0)
        status = entri.get("status", "baru")
        if not isinstance(nilai, (int, float)):
            nilai_tidak_valid += 1
            continue
        if status == "selesai":
            berhasil += 1
            total += nilai
        elif status == "gagal":
            gagal += 1
        elif status == "menunggu":
            menunggu += 1
        else:
            total += 0
    rata_rata = total / berhasil if berhasil else 0
    ringkasan = {
        "jumlah": jumlah,
        "berhasil": berhasil,
        "gagal": gagal,
        "menunggu": menunggu,
        "nilai_tidak_valid": nilai_tidak_valid,
        "total": total,
        "rata_rata": rata_rata,
    }
    label = "baik" if gagal == 0 else "perlu diperiksa"
    ringkasan["label"] = label
    return ringkasan


def format_ringkasan(ringkasan):
    return (
        f"Jumlah: {ringkasan['jumlah']}, "
        f"berhasil: {ringkasan['berhasil']}, "
        f"gagal: {ringkasan['gagal']}"
    )


if __name__ == "__main__":
    contoh = [
        {"nilai": 100, "status": "selesai"},
        {"nilai": 50, "status": "gagal"},
    ]
    print(format_ringkasan(proses_laporan_harian(contoh)))
