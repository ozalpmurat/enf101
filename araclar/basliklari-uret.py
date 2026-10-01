#!/usr/bin/env python3
"""BASLIKLAR.qmd dosyasını hafta-*/NN-ders-notu.qmd dosyalarından üretir.

Kullanım (depo kökünde):
    python3 araclar/basliklari-uret.py            # dosyayı üretir
    python3 araclar/basliklari-uret.py --kontrol  # yalnızca denetler (0: güncel, 1: güncellenmeli)

Bağımlılık yoktur; yalnızca standart kütüphane kullanılır.
Çıktı dosyasını elle düzenlemeyin — her çalıştırmada baştan yazılır.
Kontrol kipi, dosyayı kaynaklarla karşılaştırır; commit beklemez.
"""

import glob
import os
import re
import sys

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
        "14 haftanın **ders notlarındaki** bölüm başlıklarının bir arada görünümüdür; dersin içerik haritası olarak kullanılır. Notlardaki kutu (callout) başlıkları bölüm sayılmadığı için buraya alınmaz.",
        "",
        "**Otomatik üretilir, elle düzenlenmez.** İçerikte ekleme, çıkarma ya da yer değişikliği yaptıktan sonra betiği çalıştırıp belgeyi yeniden derleyin: `python3 araclar/basliklari-uret.py` ve `bash araclar/derle.sh BASLIKLAR.qmd`.",
        ":::",
        "",
    ]
    sayac = 0
    for klasor in sorted(glob.glob(os.path.join(KOK, "hafta-*"))):
        no = os.path.basename(klasor).split("-")[1]
        not_ = os.path.join(klasor, f"{no}-ders-notu.qmd")
        if not os.path.exists(not_):
            continue
        sayac += 1
        baslik, basliklar = onyuz_ve_basliklar(not_)
        parcalar.append(f"# {int(no)}. Hafta — {baslik}")
        parcalar.append("")
        for seviye, metin in basliklar:
            parcalar.append(("  " * (seviye - 1)) + "- " + metin)
        parcalar.append("")
    parcalar.append(BASLIK_ISARETI)
    parcalar.append("")

    hedef = os.path.join(KOK, "BASLIKLAR.qmd")
    yeni = "\n".join(parcalar)

    if "--kontrol" in sys.argv:
        eski = open(hedef, encoding="utf-8").read() if os.path.exists(hedef) else None
        if eski == yeni:
            print("BASLIKLAR.qmd güncel")
            return 0
        print("BASLIKLAR.qmd GÜNCELLENMELİ — `python3 araclar/basliklari-uret.py` çalıştırıp derleyin")
        return 1

    open(hedef, "w", encoding="utf-8").write(yeni)
    print(f"yazıldı: {hedef}")
    print(f"hafta: {sayac}, satır: {len(parcalar)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
