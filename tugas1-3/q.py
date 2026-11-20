"""Tugas 3 - Menjalankan query Tree-sitter pada file Python."""

import sys
from pathlib import Path

import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor


PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)
QUERY_DIR = Path(__file__).parent / "queries"

QUERIES = {
    "fungsi": "fungsi.scm",
    "print": "print.scm",
    "import": "imports.scm",
}


def baca_query(nama):
    return Query(PY_LANGUAGE, (QUERY_DIR / QUERIES[nama]).read_text(encoding="utf-8"))


def cetak_fungsi(root):
    query = baca_query("fungsi")
    matches = QueryCursor(query).matches(root)
    print("== Nama fungsi dan jumlah parameter ==")
    for _, captures in matches:
        nama = captures["nama"][0].text.decode("utf-8", errors="replace")
        params = captures["params"][0]
        jumlah = params.named_child_count
        print(f"{nama}: {jumlah} parameter")


def cetak_print(root):
    query = baca_query("print")
    captures = QueryCursor(query).captures(root)
    print("== Pemanggilan print(...) ==")
    nodes = captures.get("panggilan", [])
    if not nodes:
        print("Tidak ada pemanggilan print yang ditemukan.")
    for node in nodes:
        baris = node.start_point[0] + 1
        print(f"baris {baris}: {node.text.decode('utf-8', errors='replace')}")


def nama_modul_import(node):
    """Ambil modul dari import biasa atau from-import tanpa menebak teks mentah."""
    if node.type == "future_import_statement":
        return ["__future__"]

    if node.type == "import_from_statement":
        modul = node.child_by_field_name("module_name")
        if modul is not None:
            return [modul.text.decode("utf-8", errors="replace")]
        return ["(modul relatif tidak terdeteksi dari field module_name)"]

    hasil = []
    for child in node.named_children:
        # Pada import biasa, grammar dapat membungkus alias dalam aliased_import.
        if child.type == "aliased_import":
            nama = child.child_by_field_name("name")
            if nama is None and child.named_children:
                nama = child.named_children[0]
        else:
            nama = child
        if nama is not None:
            hasil.append(nama.text.decode("utf-8", errors="replace"))
    return hasil


def cetak_import(root):
    query = baca_query("import")
    captures = QueryCursor(query).captures(root)
    print("== Pernyataan import dan nama modul ==")
    nodes = captures.get("pernyataan_import", [])
    if not nodes:
        print("Tidak ada pernyataan import yang ditemukan.")
    for node in nodes:
        baris = node.start_point[0] + 1
        for modul in nama_modul_import(node):
            print(f"baris {baris}: {modul}")


def main():
    if len(sys.argv) not in (2, 3):
        raise SystemExit("Pemakaian: python q.py <file.py> [fungsi|print|import|all]")

    path = Path(sys.argv[1])
    if not path.is_file():
        raise SystemExit(f"File tidak ditemukan: {path}")

    mode = sys.argv[2] if len(sys.argv) == 3 else "all"
    if mode not in {"fungsi", "print", "import", "all"}:
        raise SystemExit("Mode harus: fungsi, print, import, atau all")

    tree = parser.parse(path.read_bytes())
    print(f"File: {path}")
    print(f"Mengandung error: {tree.root_node.has_error}\n")

    if mode in ("fungsi", "all"):
        cetak_fungsi(tree.root_node)
    if mode in ("print", "all"):
        cetak_print(tree.root_node)
    if mode in ("import", "all"):
        cetak_import(tree.root_node)


if __name__ == "__main__":
    main()
