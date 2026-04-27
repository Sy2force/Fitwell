"""
Applique les traductions FR\u2192EN au fichier .po EN avec polib (parser robuste).
Importe le dictionnaire depuis translate_po_v2 pour rester DRY.
"""
import sys
from pathlib import Path

import polib

sys.path.insert(0, str(Path(__file__).parent))
from translate_po_v2 import TRANSLATIONS  # noqa: E402


def main():
    base = Path(__file__).resolve().parent.parent
    en_po = base / "locale" / "en" / "LC_MESSAGES" / "django.po"
    if not en_po.exists():
        print(f"ERROR: {en_po} not found")
        return 1

    po = polib.pofile(str(en_po))
    filled = 0
    still_empty = []

    for entry in po:
        if entry.obsolete:
            continue
        if not entry.msgid:
            continue  # header
        if entry.msgstr.strip():
            continue  # already translated
        if entry.msgid in TRANSLATIONS:
            entry.msgstr = TRANSLATIONS[entry.msgid]
            # Remove fuzzy flag if any
            if "fuzzy" in entry.flags:
                entry.flags.remove("fuzzy")
            filled += 1
        else:
            still_empty.append(entry.msgid)

    po.save(str(en_po))

    print(f"\u2705 EN: {filled} translations filled")
    print(f"   Still empty: {len(still_empty)}")
    if still_empty:
        print("\n   Remaining missing:")
        for s in still_empty:
            display = s if len(s) < 120 else s[:117] + "..."
            print(f"     {repr(display)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
