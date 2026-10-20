# 7. hafta: atıf sistemleri — APA, MLA ve IEEE arasındaki temel fark (infografik).
# Kullanım: python3 diyagram_betikleri/diagram-atif-sistemleri.py [--kontrol]
#           --kontrol : yazıların hücrelere sığıp sığmadığını ölçer, PNG üretmez
# Çıktı:    hafta-07-kelime-islemci/gorseller/diagram-atif-sistemleri.png
#
# Amaç yalnızca fikir vermektir: sistemlerin ayrıntılı kuralları değil, hangi
# alanda yaygın oldukları ve metin içi atfın nasıl göründüğü gösterilir
# (AGENTS.md §8: şemaya başlık gömülmez).

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-07-kelime-islemci" / "gorseller"

LAC = "#1F3864"
MAVI = "#2E74B5"
ACIK = "#DCE7F5"
ZEMIN = "#EDF2F9"
GRI = "#595959"

plt.rcParams["font.family"] = "DejaVu Sans"

G, Y = 18.0, 7.0

ETIKET_X, ETIKET_W = 0.6, 3.0
KOLON_X = [3.8, 8.4, 13.0]
KOLON_W = 4.4

BASLIK_Y, BASLIK_H = 5.6, 1.0
SATIR_Y = [4.3, 3.0, 1.7]
SATIR_H = 1.2
NOT_Y, NOT_H = 0.45, 0.95

BASLIK_FS = 12
ETIKET_FS = 9.5
DEGER_FS = 10
NOT_FS = 9.5

SISTEMLER = ["APA", "MLA", "IEEE"]
SATIRLAR = [
    ("Alan", ["Sosyal bilimler", "Beşeri bilimler", "Mühendislik, bilişim"]),
    ("Metin içi", ["(Yılmaz, 2024)", "(Yılmaz 45)", "[1]"]),
    ("Kaynakça", ["Alfabetik", "Alfabetik", "Numaralı"]),
]
NOT = "Hangi biçimin kullanılacağını bölümünüz belirler; önemli olan tutarlılık."


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

    def olc(metin, fs, bold, sinir, ad):
        nonlocal sorun
        g = metin_olc(fig, ax, metin, fs, bold)
        if g > sinir:
            print(f"TAŞIYOR  {ad}: {g:.2f} > {sinir:.2f}  ({metin})")
            sorun += 1

    for s in SISTEMLER:
        olc(s, BASLIK_FS, True, KOLON_W - 0.4, "başlık")
    for etiket, degerler in SATIRLAR:
        olc(etiket, ETIKET_FS, True, ETIKET_W - 0.3, "satır etiketi")
        for d in degerler:
            olc(d, DEGER_FS, False, KOLON_W - 0.4, "değer")
    olc(NOT, NOT_FS, False, G - 2.0, "alt not")
    print(f"şema: {G} × {Y} cm; kolonlar {KOLON_X}, genişlik {KOLON_W} cm")
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, G)
ax.set_ylim(0, Y)
ax.axis("off")

# zemin
ax.add_patch(FancyBboxPatch((0.15, 0.15), G - 0.3, Y - 0.3,
             boxstyle="round,pad=0.02,rounding_size=0.14",
             linewidth=0, facecolor=ZEMIN, zorder=0))

# başlık bantları
for x, s in zip(KOLON_X, SISTEMLER):
    ax.add_patch(Rectangle((x, BASLIK_Y), KOLON_W, BASLIK_H,
                           facecolor=LAC, edgecolor="none", zorder=2))
    ax.text(x + KOLON_W / 2, BASLIK_Y + BASLIK_H / 2, s, ha="center", va="center",
            fontsize=BASLIK_FS, color="white", fontweight="bold", zorder=3)

# satırlar
for i, (etiket, degerler) in enumerate(SATIRLAR):
    y = SATIR_Y[i]
    if i > 0:
        ax.plot([ETIKET_X, KOLON_X[-1] + KOLON_W], [y + SATIR_H + 0.05] * 2,
                color="#C9D6E8", linewidth=0.9, zorder=2)
    ax.text(ETIKET_X, y + SATIR_H / 2, etiket, ha="left", va="center",
            fontsize=ETIKET_FS, color=GRI, fontweight="bold", zorder=3)
    for x, d in zip(KOLON_X, degerler):
        ax.text(x + 0.15, y + SATIR_H / 2, d, ha="left", va="center",
                fontsize=DEGER_FS, color=LAC, zorder=3)

# alt not
ax.add_patch(FancyBboxPatch((0.6, NOT_Y), G - 1.2, NOT_H,
             boxstyle="round,pad=0.02,rounding_size=0.10",
             linewidth=0, facecolor=ACIK, zorder=2))
ax.text(G / 2, NOT_Y + NOT_H / 2, NOT, ha="center", va="center",
        fontsize=NOT_FS, color=LAC, zorder=3)

if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-atif-sistemleri.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
