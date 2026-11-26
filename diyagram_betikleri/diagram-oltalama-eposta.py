# 10. hafta: oltalama e-postasının anatomisi.
# Solda markasız bir e-posta penceresi örneği, sağda numaralı işaretlerin açıklaması.
#
# Kullanım:
#   python3 diyagram_betikleri/diagram-oltalama-eposta.py            # PNG üretir
#   python3 diyagram_betikleri/diagram-oltalama-eposta.py --kontrol  # taşma denetimi
#
# Çıktı: hafta-10-bilgi-guvenligi/gorseller/diagram-oltalama-eposta.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8). Gerçek bir e-posta ekran
# görüntüsü değil, kavramı gösteren kurgusal (temsilî) bir örnektir; adresler
# ve içerik uydurmadır.

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-10-bilgi-guvenligi" / "gorseller"

LAC = "#1F3864"
MAVI = "#2E74B5"
GRI = "#595959"
KIRMIZI = "#A93A3A"
RULE = "#C9D3E0"

plt.rcParams["font.family"] = "DejaVu Sans"

G, Y = 21.0, 9.0
X0, W = 0.5, 12.4
YB, YU = 0.6, 8.8
LEG_X = 13.7

ALAN_FS, GOVDE_FS = 9.5, 9.5
LEG_FS = 8.8


def metin_olc(fig, ax, metin, fs, bold):
    t = ax.text(0, 0, metin, fontsize=fs, fontweight="bold" if bold else "normal")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x1, _), (x2, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    t.remove()
    return x2 - x1


def numara(ax, cx, cy, n):
    ax.add_patch(Circle((cx, cy), 0.22, linewidth=1.4, edgecolor=KIRMIZI,
                        facecolor=KIRMIZI, zorder=6))
    ax.text(cx, cy, str(n), ha="center", va="center", fontsize=8,
            color="white", fontweight="bold", zorder=7)


def kur():
    fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, G)
    ax.set_ylim(0, Y)
    ax.axis("off")

    # pencere gövdesi
    ax.add_patch(FancyBboxPatch((X0, YB), W, YU - YB,
                 boxstyle="round,pad=0.02,rounding_size=0.10",
                 linewidth=1.6, edgecolor=LAC, facecolor="white", zorder=1))
    # başlık şeridi
    ax.add_patch(FancyBboxPatch((X0, YU - 0.86), W, 0.86,
                 boxstyle="round,pad=0.02,rounding_size=0.10",
                 linewidth=1.6, edgecolor=LAC, facecolor=LAC, zorder=2))
    ax.text(X0 + 0.35, YU - 0.43, "Gelen Kutusu", ha="left", va="center",
            fontsize=10.5, color="white", fontweight="bold", zorder=3)

    # alanlar
    alanlar = [
        (7.35, "Gönderen", "destek@guvenli-banka-dogrula.com", 1),
        (6.75, "Konu", "Son uyarı: Hesabınız 24 saat içinde kapatılacak!", 2),
    ]
    for y, ad, deger, n in alanlar:
        ax.plot([X0 + 0.25, X0 + W - 0.25], [y - 0.28, y - 0.28],
                color=RULE, linewidth=1, zorder=2)
        ax.text(X0 + 0.35, y, ad, ha="left", va="center", fontsize=ALAN_FS,
                color=LAC, fontweight="bold", zorder=3)
        ax.text(X0 + 2.6, y, deger, ha="left", va="center", fontsize=ALAN_FS,
                color=GRI, zorder=3)
        numara(ax, X0 + W - 0.55, y, n)

    # gövde
    govde = [
        (6.05, "Sayın müşteri,", GRI),
        (5.45, "Hesabınızda şüpheli bir işlem tespit ettik.", GRI),
        (4.85, "Doğrulamak için parola ve kart bilgilerinizi girin:", GRI),
    ]
    for y, metin, renk in govde:
        ax.text(X0 + 0.5, y, metin, ha="left", va="center", fontsize=GOVDE_FS,
                color=renk, zorder=3)
    baglanti = "https://guvenli-banka-dogrula.com/giris"
    ax.text(X0 + 0.5, 4.25, baglanti, ha="left", va="center", fontsize=GOVDE_FS,
            color=MAVI, zorder=3)
    ax.plot([X0 + 0.5, X0 + 0.5 + metin_olc(fig, ax, baglanti, GOVDE_FS, False)],
            [4.05, 4.05], color=MAVI, linewidth=0.9, zorder=3)
    numara(ax, X0 + W - 0.55, 4.25, 3)

    # ek
    ax.plot([X0 + 0.25, X0 + W - 0.25], [1.75, 1.75], color=RULE, linewidth=1, zorder=2)
    ax.text(X0 + 0.35, 1.35, "Ek:", ha="left", va="center", fontsize=ALAN_FS,
            color=LAC, fontweight="bold", zorder=3)
    ax.text(X0 + 1.0, 1.35, "hesap-ozeti.pdf", ha="left", va="center",
            fontsize=ALAN_FS, color=GRI, zorder=3)
    numara(ax, X0 + W - 0.55, 1.35, 4)

    # sağ sütun: açıklamalar
    aciklamalar = [
        (7.35, 1, "Gönderen adresi gerçek\nkuruma benzemiyor"),
        (6.05, 2, "Acele ettiren, tehditkâr\nkonu"),
        (4.75, 3, "Parola ve kart bilgisi\nisteniyor"),
        (3.45, 4, "Beklenmedik ek: zararlı\nyazılım bulaştırabilir"),
    ]
    for y, n, metin in aciklamalar:
        numara(ax, LEG_X + 0.22, y, n)
        ax.text(LEG_X + 0.6, y, metin, ha="left", va="center", fontsize=LEG_FS,
                color=GRI, linespacing=1.5, zorder=3)
    return fig, ax


def kontrol(fig, ax):
    sorun = 0
    alan_sinir = W - 2.6 - 0.85
    for deger in ["destek@guvenli-banka-dogrula.com",
                  "Son uyarı: Hesabınız 24 saat içinde kapatılacak!"]:
        g = metin_olc(fig, ax, deger, ALAN_FS, False)
        if g > alan_sinir:
            print(f"TAŞIYOR  alan: {g:.2f} > {alan_sinir:.2f}  ({deger})")
            sorun += 1
    govde_metinler = ["Sayın müşteri,", "Hesabınızda şüpheli bir işlem tespit ettik.",
                      "Doğrulamak için parola ve kart bilgilerinizi girin:",
                      "https://guvenli-banka-dogrula.com/giris"]
    govde_sinir = W - 1.1
    for metin in govde_metinler:
        g = metin_olc(fig, ax, metin, GOVDE_FS, False)
        if g > govde_sinir:
            print(f"TAŞIYOR  gövde: {g:.2f} > {govde_sinir:.2f}  ({metin})")
            sorun += 1
    leg_sinir = G - (LEG_X + 0.6) - 0.2
    for metin in ["Gönderen adresi gerçek", "kuruma benzemiyor",
                  "Acele ettiren, tehditkâr", "Parola ve kart bilgisi",
                  "isteniyor", "Beklenmedik ek: zararlı", "yazılım bulaştırabilir"]:
        g = metin_olc(fig, ax, metin, LEG_FS, False)
        if g > leg_sinir:
            print(f"TAŞIYOR  açıklama: {g:.2f} > {leg_sinir:.2f}  ({metin})")
            sorun += 1
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


fig, ax = kur()
if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-oltalama-eposta.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
