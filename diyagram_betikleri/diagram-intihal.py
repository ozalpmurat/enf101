# 7. hafta: akademik dürüstlük — doğru ve yanlış davranışlar, kaynak künyesi.
# Kullanım: python3 diyagram_betikleri/diagram-intihal.py [--kontrol]
#           --kontrol : yazıların kutulara sığıp sığmadığını ölçer, PNG üretmez
# Çıktı:    hafta-07-kelime-islemci/gorseller/diagram-intihal.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8); başlık slaytta/ders notunda
# altyazıdır. İçerik, ders notundaki "İntihal yalnızca kopyala-yapıştır değildir"
# ve "Kaynak nasıl gösterilir?" bölümleriyle hizalanmıştır.

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-07-kelime-islemci" / "gorseller"

LAC = "#1F3864"     # lacivert
MAVI = "#2E74B5"    # doğru işareti
ACIK = "#DCE7F5"    # açık mavi kutu
ZEMIN = "#EDF2F9"   # zemin bandı
GRI = "#595959"     # madde metni
KIRMIZI = "#9E2B2B"     # yanlış işareti
ACIK_KIRMIZI = "#E3C9C9"  # yanlış sütunu zemini

plt.rcParams["font.family"] = "DejaVu Sans"

# veri birimi = cm; figür 17,4 × 6,96 cm (200 dpi)
G, Y = 17.4, 6.96

SUTUN_H = 4.3                 # iki sütunun ortak yüksekliği
SUTUN_Y0 = 2.05
BASLIK_B = 0.8                # sütun başlık bandı
SOL_X, SAG_X, SUTUN_W = 0.6, 8.9, 7.9
SUT_PAY = 0.45                # sütun içi yatay pay
BASLIK_FS, MADDE_FS = 11, 8.5

DOGRU = [
    "✓ Alıntıyı tırnak içinde ver, kaynağı göster",
    "✓ Kendi cümlelerinle özetle, kaynağı göster",
    "✓ Kullandığın her kaynağı listeye ekle",
]
YANLIS = [
    "✗ Kaynak göstermeden kopyalamak",
    "✗ Birkaç kelimeyi değiştirip kullanmak",
    "✗ Yapay zekâ metnini kendi işin gibi sunmak",
    "✗ Başkasının ödevini kendi adına vermek",
]

ALT_X, ALT_W, ALT_Y, ALT_H = 0.6, 16.2, 0.5, 1.15
ALT_METIN = ("Kaynak gösterirken: yazar, eser adı, yayın yılı, sayfa "
             "— ve nereden erişildiği")
ALT_FS = 9.5


def metin_olc(fig, ax, metin, fs, bold):
    """metnin eksen birimindeki (cm) genişliği."""
    t = ax.text(0, 0, metin, fontsize=fs, fontweight="bold" if bold else "normal")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x1, _), (x2, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    t.remove()
    return x2 - x1


def kontrol(fig, ax):
    """yazılar kutuya sığıyor mu; sığmıyorsa ölçü yazılır."""
    sorun = 0
    sinir = SUTUN_W - 2 * SUT_PAY
    for m in DOGRU + YANLIS:
        g = metin_olc(fig, ax, m, MADDE_FS, False)
        if g > sinir:
            print(f"TAŞIYOR  sütun maddesi: {g:.2f} > {sinir:.2f}  ({m})")
            sorun += 1
    for baslik in ("DOĞRU", "YANLIŞ (İNTİHAL)"):
        g = metin_olc(fig, ax, baslik, BASLIK_FS, True)
        if g > SUTUN_W - 0.4:
            print(f"TAŞIYOR  {baslik} başlığı: {g:.2f} > {SUTUN_W - 0.4:.2f}")
            sorun += 1
    g = metin_olc(fig, ax, ALT_METIN, ALT_FS, False)
    if g > ALT_W - 0.8:
        print(f"TAŞIYOR  alt satır: {g:.2f} > {ALT_W - 0.8:.2f}")
        sorun += 1
    print(f"şema: sütunlar x {SOL_X:.1f}–{SOL_X + SUTUN_W:.1f} ve "
          f"{SAG_X:.1f}–{SAG_X + SUTUN_W:.1f}, eksen {G} cm")
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


def kutu(ax, x, y, w, h, fc, renk=LAC, kalinlik=1.6, yuvarlak=0.10):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.02,rounding_size={yuvarlak}",
                 linewidth=kalinlik, edgecolor=renk, facecolor=fc, zorder=2))


fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, G)
ax.set_ylim(0, Y)
ax.axis("off")

# zemin bandı
ax.add_patch(FancyBboxPatch((0.15, 0.15), G - 0.3, Y - 0.3,
             boxstyle="round,pad=0.02,rounding_size=0.14",
             linewidth=0, facecolor=ZEMIN, zorder=0))

BASLIK_Y0 = SUTUN_Y0 + SUTUN_H - BASLIK_B
GOVDE_UST = BASLIK_Y0 - 0.35      # ilk maddenin hizası
GOVDE_ALT = SUTUN_Y0 + 0.35       # son maddenin alt sınırı


def sutun(x, baslik, renk, baslik_zemin, maddeler):
    kutu(ax, x, SUTUN_Y0, SUTUN_W, SUTUN_H, "#FFFFFF")
    kutu(ax, x, BASLIK_Y0, SUTUN_W, BASLIK_B, baslik_zemin, yuvarlak=0.08)
    ax.text(x + SUTUN_W / 2, BASLIK_Y0 + BASLIK_B / 2, baslik,
            ha="center", va="center", fontsize=BASLIK_FS, color=renk,
            fontweight="bold", zorder=3)
    aralik = (GOVDE_UST - GOVDE_ALT) / max(len(maddeler) - 1, 1)
    for i, m in enumerate(maddeler):
        ax.text(x + SUT_PAY, GOVDE_UST - i * aralik, m, ha="left", va="center",
                fontsize=MADDE_FS, color=GRI, zorder=3)


sutun(SOL_X, "DOĞRU", LAC, ACIK, DOGRU)
sutun(SAG_X, "YANLIŞ (İNTİHAL)", KIRMIZI, ACIK_KIRMIZI, YANLIS)

# alt künye satırı
kutu(ax, ALT_X, ALT_Y, ALT_W, ALT_H, ACIK, renk=ACIK, kalinlik=0, yuvarlak=0.12)
ax.text(ALT_X + ALT_W / 2, ALT_Y + ALT_H / 2, ALT_METIN, ha="center",
        va="center", fontsize=ALT_FS, color=LAC, zorder=3)

if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-intihal.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
