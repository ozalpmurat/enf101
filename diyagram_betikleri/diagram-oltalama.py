# 10. hafta: oltalama (phishing) saldırısının belirtileri.
# Dört kart: acele ettirme, beklenmedik ek, adres uyuşmazlığı, bilgi/parola isteme.
#
# Kullanım:
#   python3 diyagram_betikleri/diagram-oltalama.py            # PNG üretir
#   python3 diyagram_betikleri/diagram-oltalama.py --kontrol  # yazı taşması denetimi
#
# Çıktı: hafta-10-bilgi-guvenligi/gorseller/diagram-oltalama.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8): başlık ders notunda şekil
# altyazısı, sunuda slayt başlığıdır. Eski PNG'de "OLTALAMA (PHISHING)
# İŞARETLERİ" başlığı gömülüydü ve kaynak betiği kayıptı; şema başlıksız olarak
# yeniden çizildi.

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

G, Y = 17.4, 4.1
M, ARA = 0.45, 0.55
KUTU_W = (G - 2 * M - 3 * ARA) / 4
KUTU_H = 2.7
Y0 = (Y - KUTU_H) / 2

KARTLAR = [
    "Acele ettirir",
    "Beklenmedik\nek",
    "Adres\nuyuşmazlığı",
    "Bilgi/parola\nister",
]
FS = 10.5
IC_PAY = 0.35


def metin_olc(fig, ax, metin, fs):
    t = ax.text(0, 0, metin, fontsize=fs, fontweight="bold")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x1, _), (x2, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    t.remove()
    return x2 - x1


def en_uzun(metin, fs, fig, ax):
    return max(metin_olc(fig, ax, s, fs) for s in metin.split("\n"))


def kur():
    fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, G)
    ax.set_ylim(0, Y)
    ax.axis("off")
    for i, metin in enumerate(KARTLAR):
        x = M + i * (KUTU_W + ARA)
        ax.add_patch(FancyBboxPatch((x, Y0), KUTU_W, KUTU_H,
                     boxstyle="round,pad=0.02,rounding_size=0.16",
                     linewidth=1.6, edgecolor=LAC, facecolor=ZEMIN, zorder=2))
        ax.text(x + KUTU_W / 2, Y0 + KUTU_H / 2, metin, ha="center", va="center",
                fontsize=FS, color=GRI, fontweight="bold", linespacing=1.5, zorder=3)
    return fig, ax


def kontrol(fig, ax):
    sorun = 0
    sinir = KUTU_W - 2 * IC_PAY
    for metin in KARTLAR:
        g = en_uzun(metin, FS, fig, ax)
        if g > sinir:
            print(f"TAŞIYOR: {g:.2f} > {sinir:.2f}  ({metin.splitlines()[0]})")
            sorun += 1
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


fig, ax = kur()
if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-oltalama.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
