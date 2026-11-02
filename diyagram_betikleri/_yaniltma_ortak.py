"""Yanıltma örneklerinin ortak çizim kodu (8. hafta, eksen kaynaklı yanıltma).

Üç küçük grafik yan yana: kesilmiş eksen, ters eksen, ölçek aralığı.
Betikler `varyant` ile hangi sürümün çizileceğini söyler.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

CM = 1 / 2.54
GENISLIK_CM, YUKSEKLIK_CM = 12.6, 4.6

LACIVERT = "#1F3864"
MAVI = "#2E74B5"
GRI = "#8C8C8C"
KIRMIZI = "#A91818"
YANILTICI = "#EB4034"

VERI_KESIK = [96, 98, 97, 99]
VERI_TERS = [10, 12, 15, 18]
VERI_OLCEK = [2, 8, 12, 18, 45]
EKSEN_ETIKET = [0, 10, 20, 50]


def _konum(deger):
    """Değeri, eşit aralıklı görünen etiket konumuna çevirir."""
    for i in range(len(EKSEN_ETIKET) - 1):
        alt, ust = EKSEN_ETIKET[i], EKSEN_ETIKET[i + 1]
        if deger <= ust:
            return i + (deger - alt) / (ust - alt)
    return len(EKSEN_ETIKET) - 1

IPUCLARI = ["eksen 95'ten başlıyor", "eksen ters çevrilmiş", "aralıklar eşit sanılıyor"]


def _susle(ax, yticks, ylim):
    ax.set_xticks([])
    ax.set_yticks(yticks)
    ax.set_ylim(*ylim)
    ax.tick_params(labelsize=6, colors=LACIVERT, length=2)
    for kenar in ("top", "right", "left"):
        ax.spines[kenar].set_visible(False)
    ax.spines["bottom"].set_color(GRI)


def _ipucu(ax, metin, renk=KIRMIZI):
    ax.text(0.02, -0.16, metin, transform=ax.transAxes, fontsize=5.4,
            color=renk, style="italic", va="top")


def _panel_eksenleri(fig):
    return [fig.add_axes([0.06 + i * 0.33, 0.24, 0.26, 0.74]) for i in range(3)]


def _tek_satir(ax1, ax2, ax3, ipuclu):
    ax1.bar(range(4), VERI_KESIK, color=MAVI, width=0.6)
    _susle(ax1, [95, 97, 99], (94.4, 99.6))

    ax2.plot(range(4), VERI_TERS, color=MAVI, lw=1.6, marker="o", ms=2.5)
    _susle(ax2, [0, 10, 20], (21, -1))

    ax3.plot(range(len(VERI_OLCEK)), [_konum(v) for v in VERI_OLCEK],
             color=MAVI, lw=1.6, marker="o", ms=2.5)
    ax3.set_xticks([])
    ax3.set_yticks(range(len(EKSEN_ETIKET)))
    ax3.set_yticklabels([str(e) for e in EKSEN_ETIKET])
    ax3.set_ylim(-0.25, 3.25)
    ax3.tick_params(labelsize=6, colors=LACIVERT, length=2)
    for kenar in ("top", "right", "left"):
        ax3.spines[kenar].set_visible(False)
    ax3.spines["bottom"].set_color(GRI)

    if ipuclu:
        for ax, metin in zip((ax1, ax2, ax3), IPUCLARI):
            _ipucu(ax, metin)


def _cift_satir(fig, vurgu=False, sik=False):
    duzenler = [
        ("bar", VERI_KESIK, (0, 105), (94.4, 99.6), [0, 100], [95, 99]),
        ("line", VERI_TERS, (0, 20), (21, -1), [0, 10, 20], [0, 10, 20]),
    ]
    for i, (tip, veri, dy, yy, dt, yt) in enumerate(duzenler):
        gen = 0.23 if vurgu else 0.26
        sol = (1 / 6 + i / 3) - gen / 2
        ust = fig.add_axes([sol, 0.618, gen, 0.30])
        alt = fig.add_axes([sol, 0.18, gen, 0.30])
        renk_alt = YANILTICI if vurgu else MAVI
        for ax, ylim, ticks, renk in ((ust, dy, dt, MAVI), (alt, yy, yt, renk_alt)):
            if tip == "bar":
                ax.bar(range(4), veri, color=renk, width=0.6)
            else:
                ax.plot(range(4), veri, color=renk, lw=1.4, marker="o", ms=2)
            _susle(ax, ticks, ylim)
        _etiketler(ust, alt, i, vurgu, sik)

    # 3) eşit olmayan aralıklı eksen
    gen = 0.23 if vurgu else 0.26
    sol = (1 / 6 + 2 / 3) - gen / 2
    ust = fig.add_axes([sol, 0.618, gen, 0.30])
    alt = fig.add_axes([sol, 0.18, gen, 0.30])
    renk_alt = YANILTICI if vurgu else MAVI

    ust.plot(range(len(VERI_OLCEK)), VERI_OLCEK, color=MAVI, lw=1.4, marker="o", ms=2)
    _susle(ust, [0, 10, 20, 30, 40], (0, 50))

    alt.plot(range(len(VERI_OLCEK)), [_konum(v) for v in VERI_OLCEK],
             color=renk_alt, lw=1.4, marker="o", ms=2)
    alt.set_xticks([])
    alt.set_yticks(range(len(EKSEN_ETIKET)))
    alt.set_yticklabels([str(e) for e in EKSEN_ETIKET])
    alt.set_ylim(-0.25, 3.25)
    alt.tick_params(labelsize=6, colors=LACIVERT, length=2)
    for kenar in ("top", "right", "left"):
        alt.spines[kenar].set_visible(False)
    alt.spines["bottom"].set_color(GRI)

    _etiketler(ust, alt, 2, vurgu, sik)

    if sik:
        fig.add_artist(plt.Line2D([0.035, 0.965], [0.549, 0.549], transform=fig.transFigure,
                                  color="black", linewidth=1.0))


def _etiketler(ust, alt, i, vurgu, sik):
    ofs = 1.04 if sik else 1.12
    boy = 6.2 if sik else 5.4
    ust.text(0.0, ofs, "doğru", transform=ust.transAxes, fontsize=boy, color=MAVI)
    alt.text(0.0, ofs, "yanıltıcı", transform=alt.transAxes, fontsize=boy,
             color=YANILTICI if vurgu else KIRMIZI)
    if vurgu:
        alt.text(0.02, -0.17, IPUCLARI[i], transform=alt.transAxes, fontsize=5.4,
                 color=YANILTICI, style="italic", va="top")


def ciz(varyant, hedef, olcu=(GENISLIK_CM, YUKSEKLIK_CM)):
    """varyant: 1 = ipuçlu, 2 = doğru/yanıltıcı karşılaştırması, 3 = ipuçsuz,
    4 = karşılaştırma + yanıltıcı vurgulu ve ipuçlu."""
    fig = plt.figure(figsize=(olcu[0] * CM, olcu[1] * CM), dpi=300)
    if varyant in (2, 4, 5):
        _cift_satir(fig, vurgu=(varyant in (4, 5)), sik=(varyant == 5))
    else:
        _tek_satir(*_panel_eksenleri(fig), ipuclu=(varyant == 1))
    fig.savefig(hedef, facecolor="white")
    print(f"yazıldı: {hedef}")
