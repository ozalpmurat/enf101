# 10. hafta: iki adımlı doğrulama akışı.
# Üç kutu: parola → tek kullanımlık kod → giriş onayı.
#
# Kullanım:
#   python3 diyagram_betikleri/diagram-2fa.py            # PNG üretir
#   python3 diyagram_betikleri/diagram-2fa.py --kontrol  # yazı taşması denetimi
#
# Çıktı: hafta-10-bilgi-guvenligi/gorseller/diagram-2fa.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8): başlık ders notunda şekil
# altyazısı, sunuda slayt başlığıdır.

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-10-bilgi-guvenligi" / "gorseller"

LAC = "#1F3864"
MAVI = "#2E74B5"
ZEMIN = "#EDF2F9"
GRI = "#595959"
YESIL_K = "#2E6B3E"
YESIL_Z = "#E3F2E6"

plt.rcParams["font.family"] = "DejaVu Sans"

G, Y = 20.0, 6.2
M = 0.6
KUTU_W, KUTU_H = 5.3, 3.4
ARA = (G - 2 * M - 3 * KUTU_W) / 2
Y0 = (Y - KUTU_H) / 2

KARTLAR = [
    ("1. Adım\nParola", "bildiğiniz bir şey", LAC, ZEMIN),
    ("2. Adım\nTek kullanımlık kod", "sahip olduğunuz bir şey", LAC, ZEMIN),
    ("Giriş onaylandı", "hesabınız korunur", YESIL_K, YESIL_Z),
]

BASLIK_FS, GOVDE_FS = 12, 10
IC_PAY = 0.35


def metin_olc(fig, ax, metin, fs, bold):
    t = ax.text(0, 0, metin, fontsize=fs, fontweight="bold" if bold else "normal")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x1, _), (x2, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    t.remove()
    return x2 - x1


def kur():
    fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, G)
    ax.set_ylim(0, Y)
    ax.axis("off")
    for i, (baslik, govde, kenar, zemin) in enumerate(KARTLAR):
        x = M + i * (KUTU_W + ARA)
        ax.add_patch(FancyBboxPatch((x, Y0), KUTU_W, KUTU_H,
                     boxstyle="round,pad=0.02,rounding_size=0.16",
                     linewidth=1.6, edgecolor=kenar, facecolor=zemin, zorder=2))
        ax.text(x + KUTU_W / 2, Y0 + KUTU_H / 2 + 0.45, baslik, ha="center", va="center",
                fontsize=BASLIK_FS, color=kenar, fontweight="bold", zorder=3,
                linespacing=1.35)
        ax.text(x + KUTU_W / 2, Y0 + KUTU_H / 2 - 0.75, govde, ha="center", va="center",
                fontsize=GOVDE_FS, color=GRI, zorder=3)
        if i < len(KARTLAR) - 1:
            ax.text(x + KUTU_W + ARA / 2, Y / 2, "→", ha="center", va="center",
                    fontsize=20, color=MAVI, zorder=3)
    return fig, ax


def kontrol(fig, ax):
    sorun = 0
    sinir = KUTU_W - 2 * IC_PAY
    for baslik, govde, _, _ in KARTLAR:
        for satir in baslik.split("\n"):
            g = metin_olc(fig, ax, satir, BASLIK_FS, True)
            if g > sinir:
                print(f"TAŞIYOR  başlık: {g:.2f} > {sinir:.2f}  ({satir})")
                sorun += 1
        g = metin_olc(fig, ax, govde, GOVDE_FS, False)
        if g > sinir:
            print(f"TAŞIYOR  gövde: {g:.2f} > {sinir:.2f}  ({govde})")
            sorun += 1
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


fig, ax = kur()
if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-2fa.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
