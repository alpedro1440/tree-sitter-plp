"""Tugas 1 - Membaca pohon syntax Python dengan Tree-sitter."""

import tree_sitter_python as tspython
from tree_sitter import Language, Parser


PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

SAMPLES = {
    "fungsi": b"def sapa(nama):\n    return nama\n",
    "if_else": (
        b"nilai = 75\n"
        b"if nilai >= 70:\n"
        b"    hasil = 'Lulus'\n"
        b"else:\n"
        b"    hasil = 'Remedial'\n"
    ),
    "kelas_dengan_method": (
        b"class Mahasiswa:\n"
        b"    def __init__(self, nama):\n"
        b"        self.nama = nama\n"
    ),
}


def tampilkan_semua_node(node, kedalaman=0):
    """Cetak node bernama dan anonim agar token seperti ':' terlihat."""
    indentasi = "  " * kedalaman
    status = "named" if node.is_named else "anonymous"
    teks = node.text.decode("utf-8", errors="replace").replace("\n", "\\n")
    print(f"{indentasi}{node.type} [{status}] -> {teks!r}")

    for child in node.children:
        tampilkan_semua_node(child, kedalaman + 1)


def temukan_error(node):
    """Cari node ERROR atau MISSING pertama secara preorder."""
    if node.is_error or node.is_missing or node.type == "ERROR":
        return node

    for child in node.children:
        hasil = temukan_error(child)
        if hasil is not None:
            return hasil
    return None


def main():
    for nama, kode in SAMPLES.items():
        print(f"\n{'=' * 18} {nama} {'=' * 18}")
        tree = parser.parse(kode)
        print("S-expression:")
        print(tree.root_node)
        print("Semua node (named dan anonymous):")
        tampilkan_semua_node(tree.root_node)

    print("\n================ UJI KODE RUSAK ================")
    kode_rusak = b"def sapa(nama)\n    return nama\n"  # ':' sengaja dihapus
    tree_rusak = parser.parse(kode_rusak)
    print(tree_rusak.root_node)
    print("root_node.has_error:", tree_rusak.root_node.has_error)
    error = temukan_error(tree_rusak.root_node)
    if error is None:
        print("Tidak ditemukan node ERROR/MISSING pada input ini.")
    else:
        baris = error.start_point[0] + 1
        print(f"Node pertama: {error.type}, baris {baris}, teks={error.text!r}")


if __name__ == "__main__":
    main()
