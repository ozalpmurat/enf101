# 10. hafta: zararlı yazılım türleri — üç grup.
# Kartlar: bulaşma ve yayılma amaçlı (virüs, solucan, truva atı),
# fidye yazılımı (ransomware) ve casus yazılım (spyware).
#
# Kullanım:
#   python3 diyagram_betikleri/diagram-zararli.py            # PNG üretir
#   python3 diyagram_betikleri/diagram-zararli.py --kontrol  # yazı taşması denetimi
#
# Çıktı: hafta-10-bilgi-guvenligi/gorseller/diagram-zararli.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8). Metinler ders notundaki
# üç satırlı tabloyu izler.

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

plt.rcParams["font.family"] = "DejaVu Sans"

G, Y = 20.0, 5.2
M, ARA = 0.5, 0.6
KUTU_W = (G - 2 * M - 2 * ARA) / 3
KUTU_H = 4.0
Y0 = (Y - KUTU_H) / 2

BASLIK_FS, ALT_FS, GOVDE_FS = 11.5, 10.5, 9.8
IC_PAY = 0.3

# (başlık satırları, alt başlık, [(gövde satırı, kalın mı)])
KARTLAR = [
    (["BULAŞMA VE YAYILMA", "AMAÇLI"], None,
     [("Virüs · Solucan · Truva atı", True),
      ("Sisteme girer ve yayılır", False)]),
    (["FİDYE YAZILIMI"], "(Ransomware)",
     [("Dosyaları şifreler veya", False),
      ("erişimi engeller;", False),
      ("fidye talep eder", False)]),
    (["CASUS YAZILIM"], "(Spyware)",
     [("Gizlice izler; parola ve", False),
      ("kişisel bilgileri toplar", False)]),
]


def metin_olc(fig, ax, metin, fs, bold):
    t = ax.text(0, 0, metin, fontsize=fs, fontweight="bold" if bold else "normal")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x1, _), (x2, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    t.remove()
    return x2 - x1


def kart(ax, x, basliklar, alt, govde):
    ax.add_patch(FancyBboxPatch((x, Y0), KUTU_W, KUTU_H,
                 boxstyle="round,pad=0.02,rounding_size=0.16",
                 linewidth=1.6, edgecolor=LAC, facecolor=ZEMIN, zorder=2))
    # satırları topla: (metin, puntosu, kalın, renk, satır payı)
    satirlar = [(s, BASLIK_FS, True, LAC, 0.55) for s in basliklar]
    satirlar.append((alt or "", ALT_FS, False, MAVI, 0.58 if alt else 0.3))
    for i, (s, kalin) in enumerate(govde):
        satirlar.append((s, GOVDE_FS, kalin, LAC if kalin else GRI,
                         0.5 if i == 0 else 0.46))
    toplam = sum(s[4] for s in satirlar)
    y = Y0 + KUTU_H / 2 + toplam / 2
    for metin, fs, kalin, renk, pay in satirlar:
        y -= pay / 2
        if metin:
            ax.text(x + KUTU_W / 2, y, metin, ha="center", va="center",
                    fontsize=fs, color=renk,
                    fontweight="bold" if kalin else "normal", zorder=3)
        y -= pay / 2


def kur():
    fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, G)
    ax.set_ylim(0, Y)
    ax.axis("off")
    for i, (basliklar, alt, govde) in enumerate(KARTLAR):
        kart(ax, M + i * (KUTU_W + ARA), basliklar, alt, govde)
    return fig, ax


def kontrol(fig, ax):
    sorun = 0
    sinir = KUTU_W - 2 * IC_PAY
    for basliklar, alt, govde in KARTLAR:
        for satir in basliklar:
            g = metin_olc(fig, ax, satir, BASLIK_FS, True)
            if g > sinir:
                print(f"TAŞIYOR  başlık: {g:.2f} > {sinir:.2f}  ({satir})")
                sorun += 1
        if alt:
            g = metin_olc(fig, ax, alt, ALT_FS, False)
            if g > sinir:
                print(f"TAŞIYOR  alt başlık: {g:.2f} > {sinir:.2f}  ({alt})")
                sorun += 1
        for satir, kalin in govde:
            g = metin_olc(fig, ax, satir, GOVDE_FS, kalin)
            if g > sinir:
                print(f"TAŞIYOR  gövde: {g:.2f} > {sinir:.2f}  ({satir})")
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
