# 7. hafta: doğru yol — alıntı ve özet, ikisi de kaynak göstermeye çıkar.
# Kullanım: python3 diyagram_betikleri/diagram-dogru-yol.py [--kontrol]
#           --kontrol : yazıların kutulara sığıp sığmadığını ölçer, PNG üretmez
# Çıktı:    hafta-07-kelime-islemci/gorseller/diagram-dogru-yol.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8); başlık slaytta/ders notunda
# altyazıdır.

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-07-kelime-islemci" / "gorseller"

LAC = "#1F3864"
MAVI = "#2E74B5"
ACIK = "#DCE7F5"
ZEMIN = "#EDF2F9"
GRI = "#595959"

plt.rcParams["font.family"] = "DejaVu Sans"

# birim = cm
G, Y = 17.4, 7.0

SOL_W = 4.4
ORTA_W = 4.9
SAG_W = 5.0
SOL_X = 0.8
ORTA_X = 6.4
SAG_X = 12.2

UST_Y, UST_H = 3.9, 2.1        # 1. yol
ALT_Y, ALT_H = 0.9, 2.1        # 2. yol
SAG_Y, SAG_H = 0.9, 5.1        # birleşen kutu

BASLIK_FS = 10.5
ALT_FS = 10
SAG_FS = 12.5

YOLLAR = [
    (UST_Y, UST_H, "DOĞRUDAN\nALINTI", "tırnak içinde göster"),
    (ALT_Y, ALT_H, "KENDİ\nCÜMLELERİNLE\n(ÖZET)", "anlamı koruyarak yaz"),
]
SAG_METIN = "KAYNAK GÖSTER"


def metin_olc(fig, ax, metin, fs, bold):
    t = ax.text(0, 0, metin, fontsize=fs, fontweight="bold" if bold else "normal")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x1, _), (x2, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    t.remove()
    return x2 - x1


def kontrol(fig, ax):
    sorun = 0
    for _, _, baslik, eylem in YOLLAR:
        for metin, fs, bold, sinir in ((baslik, BASLIK_FS, True, SOL_W - 0.5),
                                       (eylem, ALT_FS, False, ORTA_W - 0.5)):
            g = metin_olc(fig, ax, metin, fs, bold)
            if g > sinir:
                print(f"TAŞIYOR  {metin}: {g:.2f} > {sinir:.2f}")
                sorun += 1
    g = metin_olc(fig, ax, SAG_METIN, SAG_FS, True)
    if g > SAG_W - 0.5:
        print(f"TAŞIYOR  {SAG_METIN}: {g:.2f} > {SAG_W - 0.5:.2f}")
        sorun += 1
    print(f"şema: {G} × {Y} cm; kutular x {SOL_X:.1f}, {ORTA_X:.1f}, {SAG_X:.1f}")
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


def kutu(ax, x, y, w, h, fc, renk=LAC, kalinlik=1.6, yuvarlak=0.10):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.02,rounding_size={yuvarlak}",
                 linewidth=kalinlik, edgecolor=renk, facecolor=fc, zorder=2))


def ok(ax, x0, x1, y):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>",
                                 mutation_scale=16, linewidth=1.8,
                                 color=MAVI, zorder=3))


fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, G)
ax.set_ylim(0, Y)
ax.axis("off")

ax.add_patch(FancyBboxPatch((0.15, 0.15), G - 0.3, Y - 0.3,
             boxstyle="round,pad=0.02,rounding_size=0.14",
             linewidth=0, facecolor=ZEMIN, zorder=0))

for y, h, baslik, eylem in YOLLAR:
    kutu(ax, SOL_X, y, SOL_W, h, "#FFFFFF")
    ax.text(SOL_X + SOL_W / 2, y + h / 2, baslik, ha="center", va="center",
            fontsize=BASLIK_FS, color=LAC, fontweight="bold", zorder=3)

    kutu(ax, ORTA_X, y, ORTA_W, h, "#FFFFFF")
    ax.text(ORTA_X + ORTA_W / 2, y + h / 2, eylem, ha="center", va="center",
            fontsize=ALT_FS, color=GRI, zorder=3)

    ok(ax, SOL_X + SOL_W + 0.15, ORTA_X - 0.15, y + h / 2)
    ok(ax, ORTA_X + ORTA_W + 0.15, SAG_X - 0.15, y + h / 2)

kutu(ax, SAG_X, SAG_Y, SAG_W, SAG_H, ACIK, kalinlik=2.0)
ax.text(SAG_X + SAG_W / 2, SAG_Y + SAG_H / 2, "KAYNAK\nGÖSTER", ha="center",
        va="center", fontsize=SAG_FS, color=LAC, fontweight="bold",
        linespacing=1.6, zorder=3)

if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-dogru-yol.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
