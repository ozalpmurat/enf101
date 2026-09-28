#!/usr/bin/env python3
"""BASLIKLAR.qmd dosyasını hafta-*/ders-notu.qmd dosyalarından üretir.

Kullanım (depo kökünde):
    python3 araclar/basliklari-uret.py

Bağımlılık yoktur; yalnızca standart kütüphane kullanılır.
Çıktı dosyasını elle düzenlemeyin — her çalıştırmada baştan yazılır.
"""

import glob
import os
import re

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASLIK_ISARETI = "<!-- Bu dosya araclar/basliklari-uret.py ile üretilir; elle düzenlemeyin. -->"


def onyuz_ve_basliklar(yol):
    """(title, [(seviye, metin), ...]) döndürür.

    Yalnızca içerik dışındaki # ve ## başlıkları alınır:
    ön yüz, kod blokları ve kutu (callout) gövdeleri atlanır.
    """
    satirlar = open(yol, encoding="utf-8").read().split("\n")
    baslik, cikti = "", []
    i = 0
    if satirlar and satirlar[0].strip() == "---":          # ön yüz
        i = 1
        while i < len(satirlar) and satirlar[i].strip() != "---":
            m = re.match(r'^title:\s*"?(.*?)"?\s*$', satirlar[i])
            if m:
                baslik = m.group(1)
            i += 1
        i += 1
    kod, kutu = False, 0
    while i < len(satirlar):
        s = satirlar[i].strip()
        if s.startswith("```"):                            # kod bloğu
            kod = not kod
        elif not kod:
            if s.startswith(":::") and len(s) > 3:
                kutu += 1
            elif s == ":::":
                kutu = max(0, kutu - 1)
            elif kutu == 0:
                m = re.match(r'^(#{1,2}) (.+)$', satirlar[i])
                if m:
                    cikti.append((len(m.group(1)), m.group(2).strip()))
        i += 1
    return baslik, cikti


def sunum_slaytlari(yol):
    """Sunumdaki ## slayt başlıklarının sayısı (kutu başlıkları hariç)."""
    _, basliklar = onyuz_ve_basliklar(yol)
    return sum(1 for s, _ in basliklar if s == 2)


def soru_sayisi(yol):
    """Alıştırmadaki soru sayısı."""
    metin = open(yol, encoding="utf-8").read()
    return len(re.findall(r'^\*\*\d+\.\*\*', metin, re.M))


def main():
    parcalar = [
        "---",
        'title: "Ders İçeriği Başlıkları"',
        'subtitle: "ENF101 Temel Bilgi Teknolojileri · 14 Hafta"',
        "format:",
        "  pdf:",
        "    toc: true",
        "    toc-depth: 1",
        "---",
        "",
        BASLIK_ISARETI,
        "",
        "::: {.callout-note}",
        "## Bu belge nedir?",
        "",
        "14 haftanın **ders notlarındaki** bölüm başlıklarının bir arada görünümüdür; dersin içerik haritası olarak kullanılır. Sunum ve alıştırma için hafta başına yalnızca sayı verilir. Notlardaki kutu (callout) başlıkları bölüm sayılmadığı için buraya alınmaz.",
        "",
        "**Otomatik üretilir, elle düzenlenmez.** İçerikte ekleme, çıkarma ya da yer değişikliği yaptıktan sonra betiği çalıştırıp belgeyi yeniden derleyin: `python3 araclar/basliklari-uret.py` ve `quarto render BASLIKLAR.qmd`.",
        ":::",
        "",
    ]
    sayac = 0
    for klasor in sorted(glob.glob(os.path.join(KOK, "hafta-*"))):
        not_ = os.path.join(klasor, "ders-notu.qmd")
        if not os.path.exists(not_):
            continue
        sayac += 1
        no = os.path.basename(klasor).split("-")[1]
        baslik, basliklar = onyuz_ve_basliklar(not_)
        parcalar.append(f"# {int(no)}. Hafta — {baslik}")
        parcalar.append("")
        sl = sunum_slaytlari(os.path.join(klasor, "sunum.qmd"))
        al = soru_sayisi(os.path.join(klasor, "alistirma.qmd"))
        parcalar.append(f"*Sunum: {sl} slayt başlığı · Alıştırma: {al} soru*")
        parcalar.append("")
        for seviye, metin in basliklar:
            parcalar.append(("  " * (seviye - 1)) + "- " + metin)
        parcalar.append("")
    parcalar.append(BASLIK_ISARETI)
    parcalar.append("")

    hedef = os.path.join(KOK, "BASLIKLAR.qmd")
    open(hedef, "w", encoding="utf-8").write("\n".join(parcalar))
    print(f"yazıldı: {hedef}")
    print(f"hafta: {sayac}, satır: {len(parcalar)}")


if __name__ == "__main__":
    main()
