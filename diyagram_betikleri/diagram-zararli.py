# 10. hafta: zararlı yazılımların yaygın davranışları.
# İki grup: "Nasıl bulaşır?" (virüs, solucan, truva atı) ve "Ne yapar?"
# (fidye yazılımı, casus yazılım). Adlar kesin türler değil, davranışlardır.
#
# Kullanım:
#   python3 diyagram_betikleri/diagram-zararli.py            # PNG üretir
#   python3 diyagram_betikleri/diagram-zararli.py --kontrol  # yazı taşması denetimi
#
# Çıktı: hafta-10-bilgi-guvenligi/gorseller/diagram-zararli.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8).

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

G, Y = 18.0, 10.4
M, ARA = 0.4, 0.5
KUTU_W = (G - 2 * M - 2 * ARA) / 3
KUTU_H = 3.1

BASLIK_FS, GOVDE_FS, GRUP_FS = 12, 9.5, 12.5
IC_PAY = 0.3

# (grup başlığı y, kartların y0, grup başlığı, kartlar)
GRUPLAR = [
    (9.75, 6.25, "Nasıl bulaşır?", [
        ("VİRÜS", "başka bir dosyaya eklenir;\no dosyayla yayılır"),
        ("SOLUCAN", "bir dosyaya ihtiyaç\nduymadan ağda yayılır"),
        ("TRUVA ATI", "yararlı görünür;\naçılınca kapı açar"),
    ]),
    (5.05, 1.55, "Ne yapar?", [
        ("FİDYE YAZILIMI", "dosyaları şifreler,\npara ister"),
        ("CASUS YAZILIM", "izler; parola ve\nbilgi toplar"),
    ]),
]


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
    ax.text(x + KUTU_W / 2, y + KUTU_H - 0.6, baslik, ha="center", va="center",
            fontsize=BASLIK_FS, color=LAC, fontweight="bold", zorder=3)
    ax.text(x + KUTU_W / 2, y + KUTU_H / 2 - 0.3, govde, ha="center", va="center",
            fontsize=GOVDE_FS, color=GRI, linespacing=1.55, zorder=3)


def kur():
    fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, G)
    ax.set_ylim(0, Y)
    ax.axis("off")
    for gy, y0, grup, kartlar in GRUPLAR:
        ax.text(M, gy, grup, ha="left", va="center", fontsize=GRUP_FS,
                color=LAC, fontweight="bold", zorder=3)
        n = len(kartlar)
        toplam = n * KUTU_W + (n - 1) * ARA
        x0 = (G - toplam) / 2
        for i, (baslik, govde) in enumerate(kartlar):
            kart(ax, x0 + i * (KUTU_W + ARA), y0, baslik, govde)
    return fig, ax


def kontrol(fig, ax):
    sorun = 0
    sinir = KUTU_W - 2 * IC_PAY
    for _, _, grup, kartlar in GRUPLAR:
        g = metin_olc(fig, ax, grup, GRUP_FS, True)
        if g > G - M - 0.3:
            print(f"TAŞIYOR  grup: {g:.2f} > {G - M - 0.3:.2f}  ({grup})")
            sorun += 1
        for baslik, govde in kartlar:
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
