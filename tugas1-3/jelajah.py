"""Tugas 2 - Menjelajahi named node pada syntax tree Python."""

import sys
from pathlib import Path

import tree_sitter_python as tspython
from tree_sitter import Language, Parser


PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)


def jelajah(node, kedalaman=0, field=None):
    """Cetak node bernama, posisi 1-based, dan nama field child bila ada."""
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")

    # Gunakan children agar indeks sesuai dengan field_name_for_child(i).
    # Node anonim dilewati, tetapi indeksnya tetap dihitung.
    for i, child in enumerate(node.children):
        if child.is_named:
            nama_field = node.field_name_for_child(i)
            jelajah(child, kedalaman + 1, nama_field)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Pemakaian: python jelajah.py <file.py>")

    path = Path(sys.argv[1])
    if not path.is_file():
        raise SystemExit(f"File tidak ditemukan: {path}")

    tree = parser.parse(path.read_bytes())
    print(f"File: {path}")
    print(f"Mengandung error: {tree.root_node.has_error}")
    jelajah(tree.root_node)


if __name__ == "__main__":
    main()
