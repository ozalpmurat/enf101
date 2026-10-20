# 7. hafta: akademik dürüstlük — kaynak ile metin arasındaki bağ (kavramsal şema).
# Kullanım: python3 diyagram_betikleri/diagram-intihal.py [--kontrol]
#           --kontrol : yazıların kutulara sığıp sığmadığını ölçer, PNG üretmez
# Çıktı:    hafta-07-kelime-islemci/gorseller/diagram-intihal.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8); başlık slaytta/ders notunda
# altyazıdır. Şema, intihal biçimlerini ve kaynak künyesi unsurlarını LİSTELEMEZ
# — o bilgiler sunumun s.30 ve s.31'inde, ders notunda §9.1–9.2'de anlatılır.

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-07-kelime-islemci" / "gorseller"

LAC = "#1F3864"     # lacivert
MAVI = "#2E74B5"    # vurgu, ok
ACIK = "#DCE7F5"    # kutu zemini
ZEMIN = "#EDF2F9"   # zemin bandı
GRI = "#595959"     # açıklama metni
KIRMIZI = "#9E2B2B"     # intihal vurgusu
ACIK_KIRMIZI = "#E3C9C9"

plt.rcParams["font.family"] = "DejaVu Sans"

# birim = cm
G, Y = 17.4, 5.9

KUTU_W, KUTU_H, KUTU_Y = 6.2, 2.5, 2.1
SOL_X, SAG_X = 0.8, G - 0.8 - KUTU_W
OK_Y = KUTU_Y + KUTU_H / 2

ETIKET_FS = 12.5      # kutu başlığı
ALT_FS = 9.5          # kutu altı açıklama
OK_FS = 10.5          # ok etiketi
SONUC_FS = 10.5       # alt sonuç satırı

SOL = ("KAYNAK", "başkasının fikri, cümlesi\nveya görseli")
SAG = ("SENİN METNİN", "alıntı ya da kendi\ncümlelerinle")
OK_METIN = "kaynak göster"
SONUC = "Kaynak gösterilmezse: İNTİHAL"


def metin_olc(fig, ax, metin, fs, bold):
    t = ax.text(0, 0, metin, fontsize=fs, fontweight="bold" if bold else "normal")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x1, _), (x2, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    t.remove()
    return x2 - x1


def en_uzun(metin, fs, bold, fig, ax):
    return max(metin_olc(fig, ax, s, fs, bold) for s in metin.split("\n"))


def kontrol(fig, ax):
    sorun = 0
    sinir = KUTU_W - 0.6
    for baslik, alt in (SOL, SAG):
        for metin, fs, bold in ((baslik, ETIKET_FS, True), (alt, ALT_FS, False)):
            g = en_uzun(metin, fs, bold, fig, ax)
            if g > sinir:
                print(f"TAŞIYOR  kutu: {g:.2f} > {sinir:.2f}  ({metin.splitlines()[0]})")
                sorun += 1
    for metin, fs, bold in ((OK_METIN, OK_FS, True), (SONUC, SONUC_FS, True)):
        if metin_olc(fig, ax, metin, fs, bold) > G - 1.0:
            print(f"TAŞIYOR  {metin}")
            sorun += 1
    print(f"şema: kutular {SOL_X:.1f}–{SOL_X + KUTU_W:.1f} ve "
          f"{SAG_X:.1f}–{SAG_X + KUTU_W:.1f}, eksen {G} cm")
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


def kutu(ax, x, y, w, h, fc, renk=LAC, kalinlik=1.6, yuvarlak=0.10):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.02,rounding_size={yuvarlak}",
                 linewidth=kalinlik, edgecolor=renk, facecolor=fc, zorder=2))


def kaynak_kutusu(ax, x, baslik, alt):
    kutu(ax, x, KUTU_Y, KUTU_W, KUTU_H, "#FFFFFF")
    ax.text(x + KUTU_W / 2, KUTU_Y + KUTU_H - 0.55, baslik, ha="center", va="center",
            fontsize=ETIKET_FS, color=LAC, fontweight="bold", zorder=3)
    ax.text(x + KUTU_W / 2, KUTU_Y + 0.75, alt, ha="center", va="center",
            fontsize=ALT_FS, color=GRI, linespacing=1.5, zorder=3)


fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, G)
ax.set_ylim(0, Y)
ax.axis("off")

# zemin bandı
ax.add_patch(FancyBboxPatch((0.15, 0.15), G - 0.3, Y - 0.3,
             boxstyle="round,pad=0.02,rounding_size=0.14",
             linewidth=0, facecolor=ZEMIN, zorder=0))

kaynak_kutusu(ax, SOL_X, *SOL)
kaynak_kutusu(ax, SAG_X, *SAG)

# kaynak -> metin oku
ax.add_patch(FancyArrowPatch((SOL_X + KUTU_W + 0.15, OK_Y), (SAG_X - 0.15, OK_Y),
                             arrowstyle="-|>", mutation_scale=18,
                             linewidth=2.0, color=MAVI, zorder=3))
ax.text((SOL_X + KUTU_W + SAG_X) / 2, OK_Y + 0.55, OK_METIN, ha="center", va="center",
        fontsize=OK_FS, color=MAVI, fontweight="bold", zorder=3)

# alt sonuç satırı
kutu(ax, 2.4, 0.55, G - 4.8, 0.95, ACIK_KIRMIZI, renk=ACIK_KIRMIZI,
     kalinlik=0, yuvarlak=0.12)
ax.text(G / 2, 1.02, SONUC, ha="center", va="center", fontsize=SONUC_FS,
        color=KIRMIZI, fontweight="bold", zorder=3)

if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-intihal.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
