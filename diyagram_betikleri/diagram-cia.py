# 10. hafta: bilgi güvenliğinin üç temeli (gizlilik, bütünlük, erişilebilirlik).
# Üç kart: ilkenin adı ve kısa açıklaması.
#
# Kullanım:
#   python3 diyagram_betikleri/diagram-cia.py            # PNG üretir
#   python3 diyagram_betikleri/diagram-cia.py --kontrol  # yazı taşması denetimi
#
# Çıktı: hafta-10-bilgi-guvenligi/gorseller/diagram-cia.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8): başlık ders notunda şekil
# altyazısı, sunuda slayt başlığıdır. Eski PNG'de "BİLGİ GÜVENLİĞİNİN ÜÇ TEMELİ"
# başlığı gömülüydü ve kaynak betiği kayıptı; şema bu betikle başlıksız olarak
# yeniden çizildi.

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-10-bilgi-guvenligi" / "gorseller"

LAC = "#1F3864"     # lacivert
ZEMIN = "#EDF2F9"   # açık mavi kutu
GRI = "#595959"     # gövde metni

plt.rcParams["font.family"] = "DejaVu Sans"

# veri birimi = cm
G, Y = 17.4, 4.6
KUTU_W, KUTU_H = 4.95, 3.9
ARA = 0.83
X0 = (G - (3 * KUTU_W + 2 * ARA)) / 2
Y0 = (Y - KUTU_H) / 2

KARTLAR = [
    ("GİZLİLİK", "bilgiye yalnızca\nyetkili kişiler\nerişir"),
    ("BÜTÜNLÜK", "bilgi doğrudur ve\ndeğiştirilmemiştir"),
    ("ERİŞİLEBİLİRLİK", "bilgiye ihtiyaç\nanında ulaşılır"),
]

BASLIK_FS, GOVDE_FS = 11.5, 9.5
IC_PAY = 0.35


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


def kur():
    fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, G)
    ax.set_ylim(0, Y)
    ax.axis("off")
    for i, (baslik, govde) in enumerate(KARTLAR):
        x = X0 + i * (KUTU_W + ARA)
        ax.add_patch(FancyBboxPatch((x, Y0), KUTU_W, KUTU_H,
                     boxstyle="round,pad=0.02,rounding_size=0.16",
                     linewidth=1.6, edgecolor=LAC, facecolor=ZEMIN, zorder=2))
        ax.text(x + KUTU_W / 2, Y0 + KUTU_H - 0.75, baslik, ha="center", va="center",
                fontsize=BASLIK_FS, color=LAC, fontweight="bold", zorder=3)
        ax.text(x + KUTU_W / 2, Y0 + 1.35, govde, ha="center", va="center",
                fontsize=GOVDE_FS, color=GRI, linespacing=1.5, zorder=3)
    return fig, ax


def kontrol(fig, ax):
    sorun = 0
    sinir = KUTU_W - 2 * IC_PAY
    for baslik, govde in KARTLAR:
        g = en_uzun(baslik, BASLIK_FS, True, fig, ax)
        if g > sinir:
            print(f"TAŞIYOR  başlık: {g:.2f} > {sinir:.2f}  ({baslik})")
            sorun += 1
        g = en_uzun(govde, GOVDE_FS, False, fig, ax)
        if g > sinir:
            print(f"TAŞIYOR  gövde: {g:.2f} > {sinir:.2f}  ({govde.splitlines()[0]})")
            sorun += 1
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


fig, ax = kur()
if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-cia.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
