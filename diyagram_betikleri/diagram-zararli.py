# 10. hafta: zararlı yazılım türleri — dört kart (2x2).
# Virüs ve solucan · Truva atı · Fidye yazılımı · Casus yazılım.
#
# Kullanım:
#   python3 diyagram_betikleri/diagram-zararli.py            # PNG üretir
#   python3 diyagram_betikleri/diagram-zararli.py --kontrol  # yazı taşması denetimi
#
# Çıktı: hafta-10-bilgi-guvenligi/gorseller/diagram-zararli.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8). Metinler ders notundaki
# dört satırlı tabloyu izler.

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

G, Y = 18.0, 9.0
M, ARA_X, ARA_Y = 0.4, 0.6, 0.6
KUTU_W = (G - 2 * M - ARA_X) / 2
KUTU_H = 3.6

BASLIK_FS, ALT_FS, GOVDE_FS = 12.5, 10.5, 9.5
IC_PAY = 0.35

# (başlık, alt başlık, gövde satırları) — sıra: sol üst, sağ üst, sol alt, sağ alt
KARTLAR = [
    (["VİRÜS VE SOLUCAN"], "(Virus, Worm)",
     ["Dosyalara bulaşarak ya da ağ üzerinden", "kendiliğinden yayılarak başka", "sistemlere ulaşır."]),
    (["TRUVA ATI"], "(Trojan)",
     ["Yararlı veya zararsız bir program gibi", "görünerek kullanıcıyı kandırır;", "zararlı faaliyet yürütür."]),
    (["FİDYE YAZILIMI"], "(Ransomware)",
     ["Dosyaları şifreleyerek veya erişimi", "engelleyerek fidye talep eder."]),
    (["CASUS YAZILIM"], "(Spyware)",
     ["Kullanıcıyı gizlice izleyerek", "parola ve kişisel bilgileri toplar."]),
]


def metin_olc(fig, ax, metin, fs, bold):
    t = ax.text(0, 0, metin, fontsize=fs, fontweight="bold" if bold else "normal")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x1, _), (x2, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    t.remove()
    return x2 - x1


def kart(ax, x, y0, basliklar, alt, govde):
    ax.add_patch(FancyBboxPatch((x, y0), KUTU_W, KUTU_H,
                 boxstyle="round,pad=0.02,rounding_size=0.16",
                 linewidth=1.6, edgecolor=LAC, facecolor=ZEMIN, zorder=2))
    satirlar = [(s, BASLIK_FS, True, LAC, 0.6) for s in basliklar]
    satirlar.append((alt or "", ALT_FS, False, MAVI, 0.5 if alt else 0.28))
    satirlar += [(s, GOVDE_FS, False, GRI, 0.48) for s in govde]
    toplam = sum(s[4] for s in satirlar)
    y = y0 + KUTU_H / 2 + toplam / 2
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
    y_alt = (Y - (2 * KUTU_H + ARA_Y)) / 2
    y_ust = y_alt + KUTU_H + ARA_Y
    x_sol = M
    x_sag = M + KUTU_W + ARA_X
    yerler = [(x_sol, y_ust), (x_sag, y_ust), (x_sol, y_alt), (x_sag, y_alt)]
    for (x, y0), (basliklar, alt, govde) in zip(yerler, KARTLAR):
        kart(ax, x, y0, basliklar, alt, govde)
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
        for satir in govde:
            g = metin_olc(fig, ax, satir, GOVDE_FS, False)
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
