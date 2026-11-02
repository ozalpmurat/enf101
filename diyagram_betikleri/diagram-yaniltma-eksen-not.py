#!/usr/bin/env python3
"""Ders notu sürümü: slayttaki üç örneğe (a), (b), (c) etiketi ekler."""

from pathlib import Path

from _not_etiket import etiketle

KOK = Path(__file__).resolve().parent.parent
GORSEL = KOK / "hafta-08-hesap-tablosu" / "gorseller"

if __name__ == "__main__":
    etiketle(GORSEL / "diagram-yaniltma-eksen.png", GORSEL / "diagram-yaniltma-eksen-not.png")
