# 10. hafta: parola gücü — zayıf, orta ve güçlü örnekler.
# Üç kart: güç düzeyi, ikişer örnek parola (sabit genişlikli, kalın) ve kısa açıklama.
#
# Kullanım:
#   python3 diyagram_betikleri/diagram-parola.py            # PNG üretir
#   python3 diyagram_betikleri/diagram-parola.py --kontrol  # yazı taşması denetimi
#
# Çıktı: hafta-10-bilgi-guvenligi/gorseller/diagram-parola.png
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
GRI = "#595959"

plt.rcParams["font.family"] = "DejaVu Sans"

G, Y = 17.4, 5.9
M, ARA = 0.35, 0.5
KUTU_W = (G - 2 * M - 2 * ARA) / 3
KUTU_H = 5.2
Y0 = (Y - KUTU_H) / 2

# (başlık, başlık rengi, kenar rengi, zemin rengi, [iki örnek parola], açıklama)
KARTLAR = [
    ("ZAYIF", "#8C1C1C", "#A93A3A", "#F7E3E3",
     ["123456", "Ahmet2010!"], "tahmin edilebilir kalıplar"),
    ("ORTA", LAC, LAC, "#E8EFF8",
     ["k7#Lp2g", "M3v*Qr8"], "kısa ama rastgele"),
    ("GÜÇLÜ", "#1E5A31", "#2E6B3E", "#E3F2E6",
     ["mavi-tohum-sandalye-41!", "kahve-bulut-pencere-91!"], "uzun ve özgün söz öbeği"),
]

BASLIK_FS, MONO_FS, ACIKLAMA_FS = 12, 9, 9
IC_PAY = 0.3


def gen_olc(fig, ax, metin, fs, bold, mono=False):
    aile = "monospace" if mono else "sans"
    t = ax.text(0, 0, metin, fontsize=fs, fontweight="bold" if bold else "normal",
                family=aile)
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
    for i, (baslik, renk, kenar, zemin, ornekler, aciklama) in enumerate(KARTLAR):
        x = M + i * (KUTU_W + ARA)
        ax.add_patch(FancyBboxPatch((x, Y0), KUTU_W, KUTU_H,
                     boxstyle="round,pad=0.02,rounding_size=0.16",
                     linewidth=1.6, edgecolor=kenar, facecolor=zemin, zorder=2))
        ax.text(x + KUTU_W / 2, Y0 + KUTU_H - 0.7, baslik, ha="center", va="center",
                fontsize=BASLIK_FS, color=renk, fontweight="bold", zorder=3)
        for j, ornek in enumerate(ornekler):
            ax.text(x + KUTU_W / 2, Y0 + KUTU_H - 2.0 - j * 0.72, ornek,
                    ha="center", va="center", fontsize=MONO_FS, color=renk,
                    fontweight="bold", family="monospace", zorder=3)
        ax.text(x + KUTU_W / 2, Y0 + 0.75, aciklama, ha="center", va="center",
                fontsize=ACIKLAMA_FS, color=GRI, zorder=3)
    return fig, ax


def kontrol(fig, ax):
    sorun = 0
    sinir = KUTU_W - 2 * IC_PAY
    for baslik, _, _, _, ornekler, aciklama in KARTLAR:
        g = gen_olc(fig, ax, baslik, BASLIK_FS, True)
        if g > sinir:
            print(f"TAŞIYOR  başlık: {g:.2f} > {sinir:.2f}  ({baslik})")
            sorun += 1
        for ornek in ornekler:
            g = gen_olc(fig, ax, ornek, MONO_FS, True, mono=True)
            if g > sinir:
                print(f"TAŞIYOR  parola: {g:.2f} > {sinir:.2f}  ({ornek})")
                sorun += 1
        g = gen_olc(fig, ax, aciklama, ACIKLAMA_FS, False)
        if g > sinir:
            print(f"TAŞIYOR  açıklama: {g:.2f} > {sinir:.2f}  ({aciklama})")
            sorun += 1
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


fig, ax = kur()
if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-parola.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
