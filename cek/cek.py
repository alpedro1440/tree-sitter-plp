"""Tugas 6 - CLI pendeteksi TODO/FIXME, fungsi panjang, dan syntax error."""

import sys
from pathlib import Path

import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor


PY_LANGUAGE = Language(tspython.language())
PARSER = Parser(PY_LANGUAGE)

Q_TODO = Query(PY_LANGUAGE, '((comment) @komentar (#match? @komentar "TODO|FIXME"))')
Q_FUNCTION = Query(
    PY_LANGUAGE,
    "(function_definition name: (identifier) @nama) @fungsi",
)

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
}


def node_error_pertama(node):
    """Cari node ERROR/MISSING pertama dengan traversal preorder."""
    if node.is_error or node.is_missing or node.type == "ERROR":
        return node
    for child in node.children:
        hasil = node_error_pertama(child)
        if hasil is not None:
            return hasil
    return None


def cek_file(path: Path) -> int:
    """Periksa satu file dan kembalikan jumlah temuan yang dilaporkan."""
    try:
        source = path.read_bytes()
    except OSError as exc:
        print(f"[GAGAL BACA] {path}: {exc}")
        return 0

    tree = PARSER.parse(source)
    jumlah_temuan = 0

    # Fitur 1: komentar yang mengandung TODO atau FIXME.
    todo_captures = QueryCursor(Q_TODO).captures(tree.root_node)
    for node in todo_captures.get("komentar", []):
        baris = node.start_point[0] + 1
        teks = node.text.decode("utf-8", errors="replace").strip()
        print(f"[TODO/FIXME] {path}:{baris}: {teks}")
        jumlah_temuan += 1

    # Fitur 2: fungsi yang rentang definisinya lebih dari 30 baris.
    # Perhitungan mengikuti instruksi tugas: end_row - start_row + 1.
    function_matches = QueryCursor(Q_FUNCTION).matches(tree.root_node)
    for _, captures in function_matches:
        node_nama = captures["nama"][0]
        node_fungsi = captures["fungsi"][0]
        nama = node_nama.text.decode("utf-8", errors="replace")
        jumlah_baris = node_fungsi.end_point[0] - node_fungsi.start_point[0] + 1
        if jumlah_baris > 30:
            baris_awal = node_fungsi.start_point[0] + 1
            print(
                f"[FUNGSI PANJANG] {path}:{baris_awal}: "
                f"{nama} ({jumlah_baris} baris)"
            )
            jumlah_temuan += 1

    # Fitur 3: file dengan pohon yang memiliki ERROR atau MISSING.
    if tree.root_node.has_error:
        error = node_error_pertama(tree.root_node)
        if error is not None:
            baris = error.start_point[0] + 1
            kolom = error.start_point[1] + 1
            teks = error.text.decode("utf-8", errors="replace")
            print(
                f"[SYNTAX ERROR] {path}:{baris}:{kolom}: "
                f"node={error.type}, teks={teks!r}"
            )
        else:
            print(f"[SYNTAX ERROR] {path}: root_node.has_error=True")
        jumlah_temuan += 1

    return jumlah_temuan


def kumpulkan_file(target: Path):
    if target.is_file():
        if target.suffix == ".py":
            yield target
        return

    for path in sorted(target.rglob("*.py")):
        if any(bagian in SKIP_DIRS for bagian in path.parts):
            continue
        yield path


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Pemakaian: python cek.py <folder-atau-file.py>")

    target = Path(sys.argv[1]).resolve()
    if not target.exists():
        raise SystemExit(f"Target tidak ditemukan: {target}")

    files = list(kumpulkan_file(target))
    if not files:
        print("Tidak ditemukan file Python untuk diperiksa.")
        return

    print(f"Memeriksa {len(files)} file Python di: {target}\n")
    total_temuan = 0
    for path in files:
        total_temuan += cek_file(path)

    print(f"\nSelesai. Total temuan: {total_temuan}")


if __name__ == "__main__":
    main()
