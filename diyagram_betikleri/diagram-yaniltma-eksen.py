#!/usr/bin/env python3
"""Eksen kaynaklı yanıltma örneği — her sütunda doğru ve yanıltıcı grafik,
aralarında siyah ayırıcı çizgi; yanıltıcının altında ipucu yazıyor.

Çıktı: hafta-08-hesap-tablosu/gorseller/diagram-yaniltma-eksen.png
"""

from pathlib import Path

from _yaniltma_ortak import ciz

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "hafta-08-hesap-tablosu" / "gorseller" / "diagram-yaniltma-eksen.png"

if __name__ == "__main__":
    ciz(5, CIKTI, olcu=(13.4, 6.2))
