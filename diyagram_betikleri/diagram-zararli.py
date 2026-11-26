# 10. hafta: zararlı yazılım türleri.
# Beş kart: virüs, truva atı, fidye yazılımı (üst sıra); casus yazılım,
# solucan (alt sıra, ortalanmış).
#
# Kullanım:
#   python3 diyagram_betikleri/diagram-zararli.py            # PNG üretir
#   python3 diyagram_betikleri/diagram-zararli.py --kontrol  # yazı taşması denetimi
#
# Çıktı: hafta-10-bilgi-guvenligi/gorseller/diagram-zararli.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8). Eski PNG'nin kaynak betiği
# kayıptı; şema bu betikle yeniden çizildi.

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-10-bilgi-guvenligi" / "gorseller"

LAC = "#1F3864"
ZEMIN = "#EDF2F9"
GRI = "#595959"

plt.rcParams["font.family"] = "DejaVu Sans"

G, Y = 17.8, 7.7
M, ARA = 0.35, 0.5
KUTU_W = (G - 2 * M - 2 * ARA) / 3
KUTU_H = 3.2
UST_Y = 4.1     # üst sıra
ALT_Y = 0.35    # alt sıra

UST = [
    ("VİRÜS", "bulaştığı dosyayla\nyayılır"),
    ("TRUVA ATI", "yararlı görünür,\nkapı açar"),
    ("FİDYE YAZILIMI", "dosyaları şifreler,\npara ister"),
]
ALT = [
    ("CASUS YAZILIM", "izler, parola ve\nbilgi toplar"),
    ("SOLUCAN", "kullanıcı bir şey\nyapmadan ağda yayılır"),
]

BASLIK_FS, GOVDE_FS = 12, 9.5
IC_PAY = 0.35


def metin_olc(fig, ax, metin, fs, bold):
    t = ax.text(0, 0, metin, fontsize=fs, fontweight="bold" if bold else "normal")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x1, _), (x2, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    t.remove()
    return x2 - x1


def kart(ax, x, y, baslik, govde):
    ax.add_patch(FancyBboxPatch((x, y), KUTU_W, KUTU_H,
                 boxstyle="round,pad=0.02,rounding_size=0.16",
                 linewidth=1.6, edgecolor=LAC, facecolor=ZEMIN, zorder=2))
    ax.text(x + KUTU_W / 2, y + KUTU_H - 0.65, baslik, ha="center", va="center",
            fontsize=BASLIK_FS, color=LAC, fontweight="bold", zorder=3)
    ax.text(x + KUTU_W / 2, y + KUTU_H / 2 - 0.35, govde, ha="center", va="center",
            fontsize=GOVDE_FS, color=GRI, linespacing=1.6, zorder=3)


def kur():
    fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, G)
    ax.set_ylim(0, Y)
    ax.axis("off")
    for i, (baslik, govde) in enumerate(UST):
        kart(ax, M + i * (KUTU_W + ARA), UST_Y, baslik, govde)
    alt_x0 = (G - (2 * KUTU_W + ARA)) / 2
    for i, (baslik, govde) in enumerate(ALT):
        kart(ax, alt_x0 + i * (KUTU_W + ARA), ALT_Y, baslik, govde)
    return fig, ax


def kontrol(fig, ax):
    sorun = 0
    sinir = KUTU_W - 2 * IC_PAY
    for baslik, govde in UST + ALT:
        g = metin_olc(fig, ax, baslik, BASLIK_FS, True)
        if g > sinir:
            print(f"TAŞIYOR  başlık: {g:.2f} > {sinir:.2f}  ({baslik})")
            sorun += 1
        for satir in govde.split("\n"):
            g = metin_olc(fig, ax, satir, GOVDE_FS, False)
            if g > sinir:
                print(f"TAŞIYOR  satır: {g:.2f} > {sinir:.2f}  ({satir})")
                sorun += 1
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


fig, ax = kur()
if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-zararli.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
