# AGENTS.md

Bu dosya, bu klasörde çalışan yapay zekâ ajanları ve içerik üreten kişiler için hazırlanmıştır.
Projenin nasıl kurulduğunu, hangi kurallara uyulduğunu ve hangi tuzaklara düşülmemesi gerektiğini anlatır.

Son güncelleme: 02.10.2026

---

## 1. Proje nedir

**ENF101 Temel Bilgi Teknolojileri** dersi için 14 haftalık ders materyali.

|                |                                                                                             |
|:-------------- |:------------------------------------------------------------------------------------------- |
| Kurum          | Bilecik Şeyh Edebali Üniversitesi                                                           |
| Hedef kitle    | Tüm fakültelerin 1. sınıf öğrencileri (heterojen, teknik olmayan bölümler dahil)            |
| Öğretim biçimi | Uzaktan / karma. Öğrenciler ekranda izler, PDF'i indirip kendi bilgisayarında açabilir      |
| Ders yükü      | Haftada 40 dakika, 14 hafta                                                                 |
| Ölçme          | Başarı notu = ara sınav (vize) + kısa sınav + final **ortalaması**; alıştırmalar **notsuz** |
| İçerik dili    | Türkçe                                                                                      |

Ders, klasik "temel bilgi teknolojileri" kapsamındadır. **Programlama öğretilmez:** hiçbir haftada kod yazılmaz. **Algoritma** kavramı ise 12. haftada yalnızca tanıtım düzeyinde ele alınır (sıra, karar, tekrar; gündelik bir örnek ve akış diyagramıyla) — çünkü makine öğrenmesinin geleneksel programlamadan farkını açıklamak için gereklidir.

---

## 2. Klasör yapısı

```
2026-ai/
├─ AGENTS.md                     bu dosya
├─ _quarto.yml                   proje ayarları (ortak tema buradan bağlanır)
├─ tema/
│  ├─ notlar.tex                 ders notu · alıştırma · izlence görünümü (TikZ desteği dahil)
│  ├─ notlar-hafta.tex           haftalık ders notu · alıştırma üst/alt bilgi + giriş logosu
│  ├─ sunum.tex                  beamer sunu görünümü
│  ├─ logo.png                   BSEU amblemi (ders notu girişi, sunum kapağı)
│  └─ logobeyaz.png              beyaz amblem (sunum kenar çubuğu)
├─ ornekler/                     Quarto özellik örnekleri (başvuru belgesi, ders içeriği değil)
│  ├─ quarto-ozellikleri.qmd + .pdf + .html        özellik başvuru belgesi
│  ├─ quarto-ozellikleri-sunum.qmd + .pdf          aynı içeriğin sunum sürümü
│  └─ gorseller/
├─ izlence.qmd + .pdf            ders izlencesi
├─ BASLIKLAR.qmd + .pdf          ders içeriği başlıkları (betikle üretilir)
├─ araclar/
│  └─ basliklari-uret.py         BASLIKLAR.qmd'yi ders notlarından üretir
├─ .github/
│  ├─ workflows/
│  │  └─ pdf-paketi.yml          PDF'leri ZIP'leyip sürüme yükler (elle tetiklenir)
│  └─ surum-notlari-baslangic.md sürüm notlarının başlangıç metni (bir kez okunur)
├─ KILAVUZ_Quarto_...qmd + .pdf  hocalar için Quarto kurulum/kullanım kılavuzu
└─ hafta-NN-konu/                NN = 01 … 14, konu = kısa konu adı
   ├─ NN-ders-notu.qmd + .pdf    8–12 sayfa
   ├─ NN-sunum.qmd + .pdf        25–38 slayt (hedef ~30)
   ├─ NN-alistirma.qmd + .pdf     3 sayfa · 10 soru (5 şıklı) + cevap anahtarı
   └─ gorseller/*.png            o haftanın diyagramları
```

Klasör adları `hafta-NN-konu` kalıbındadır: hafta numarası **başta** durur (klasör sıralaması ve
`araclar/basliklari-uret.py`'nin `split("-")[1]` çözümlemesi buna bağlıdır), `konu` ise ASCII
(Türkçe karaktersiz) kısa addır — örn. `hafta-10-bilgi-guvenligi`.

Hafta klasörünün içindeki üç belgenin adı da hafta numarasıyla başlar: **`NN-ders-notu`**,
**`NN-sunum`**, **`NN-alistirma`** (`.qmd` ve `.pdf`; örn. `03-alistirma.pdf`). Böylece bir dosya
başka bir klasöre kopyalandığında ya da tek başına paylaşıldığında hangi haftaya ait olduğu adından
anlaşılır. `NN` iki haneli hafta numarasıdır (01 … 14) ve klasör adındaki numarayla aynıdır.

Toplam: 14 hafta · 42 belge (+ izlence ve kılavuz) · 40 diyagram.

---

## 3. Üretim

Her şey **Quarto** ile üretilir. Proje kökünde:

```bash
quarto render hafta-03-yazilim-isletim-sistemleri   # tek haftanın üç belgesini üretir
quarto render izlence.qmd       # tek dosya
```

**Dikkat:** `quarto render` yalnızca **tek yol** alır. `quarto render hafta-01-giris-temel-kavramlar
hafta-03-yazilim-isletim-sistemleri` çalışmaz.
Tam projeyi tek komutta derlemek 3 dakikayı aştığı için uzun işlerde hafta hafta derlemek gerekir.

**Önerilen yol: `araclar/derle.sh`.** Yukarıdaki komutlar yerine bu sarmalayıcı kullanılabilir; çalışma
ağacına geçici `.tex/.aux/.log/.out` bırakmaz ve ders notlarında altbilgiyi garanti eder:

```bash
bash araclar/derle.sh hafta-03-yazilim-isletim-sistemleri   # klasördeki bütün .qmd
bash araclar/derle.sh BASLIKLAR.qmd izlence.qmd             # tek tek dosyalar
bash araclar/derle.sh .                                     # bütün depo
```

**Altbilgi tuzağı (bu betiğin varlık sebebi).** `tema/notlar.tex` altbilgiye `Sayfa n / N` yazar; buradaki
**N**, LaTeX'in belge sonunda yazdığı bir çapraz referanstan (`\pageref{LastPage}`) gelir. Belge **tam sayfa
sınırında** bittiğinde Quarto'nun çalıştırdığı geçiş sayısı yetmez ve son sayfa `Sayfa 11 / 10` gibi **yanlış
toplam** basar. Bu, bayat önbellekten değil belgenin sınırda olmasından kaynaklanır: `.quarto/` ve PDF
silinip **temiz** derlense de olur. `latex-max-runs` da ikinci bir `quarto render` da düzeltmez.

Betik, `.tex`'i koruyarak (`-M keep-tex:true`) derler; son sayfada `Sayfa n / N` görüp tutmuyorsa altbilgi
oturana kadar (en fazla 6 kez) ek `xelatex` geçişi yapar, ardından yan ürünleri siler. Altbilgisi zaten
doğru olan belgelere dokunmaz.

Denenip **işe yaramayan** çözümler — tekrar denenmesin: `\AtEndDocument{\clearpage\label{LastPage}}`
(referans "??" kalır), `totpages` paketi (TinyTeX'te kurulu değil, derleme düşer), etiketi altbilgiye taşımak
(yine "??"), altbilgiden toplamı tümden kaldırmak (çalışır ama `n / N` bilgisi kaybolur — kullanıcı bunu
istemedi). 2026-09-29'da 02, 04, 05, 06, 09, 14. haftalar bu tuzağa yakalanmıştı.

**`BASLIKLAR.qmd` elle düzenlenmez.** `araclar/basliklari-uret.py` betiği bu dosyayı `hafta-*/NN-ders-notu.qmd`
başlıklarından üretir. İçerikte ekleme, çıkarma ya da yer değişikliği yaptıktan sonra — izlenceyi
güncellediğiniz gibi — betiği çalıştırıp belgeyi yeniden derleyin:

```bash
python3 araclar/basliklari-uret.py
quarto render BASLIKLAR.qmd
```

Betik yalnızca standart kütüphane kullanır, ek kurulum gerektirmez. Notlardaki kutu (callout) başlıkları
bölüm sayılmadığı için anahatta yer almaz; böylece belge, notların kendi içindekiler tablosuyla birebir örtüşür.

**PDF paketi elle çıkarılır.** `.github/workflows/pdf-paketi.yml` **kendiliğinden çalışmaz**; sürüm
çıkarmak bilinçli bir adımdır. Tetiklendiğinde ders içeriği olan PDF'leri tek bir ZIP'te toplayıp
**`pdf` etiketli sürüme** yükler (varsa üzerine yazar). `ornekler/` (Quarto başvuru belgeleri) ve
`KILAVUZ_*.pdf` (hocalar için kurulum kılavuzu) ders içeriği sayılmadığı için dışarıda tutulur; ZIP'te
14 haftanın üç belgesi ile izlence ve başlık listesi bulunur. Bağlantı sabittir ve README'de duyurulur:
`https://github.com/ozalpmurat/enf101/releases/download/pdf/enf101-pdf.zip`.
Böylece git kullanmayan hocalar tek bağlantıdan bütün belgeleri indirir.

Çalıştırmak için: **Actions → PDF paketi → Run workflow**. Depoya gönderilmiş commit'ten derlendiği için,
yereldeki gönderilmemiş veya yarım değişiklikler sürüme girmez. Yerelde aynı iş `find` + `zip -@` ile yapılır.

**Sürüm kimliği.** Her sürüm, çıkarıldığı gün ve o günkü kaçıncı sürüm olduğuyla adlandırılır:
`enf101-YYYYMMDDNN` (ör. `enf101-2026092901`). ZIP açıldığında bütün belgeler bu adda **tek bir klasörün**
içindedir; ad aynı zamanda sürüm numarası olarak kullanılır ve sürüm sayfasının başlığında görünür
(`Ders PDF'leri · enf101-2026092901`). ZIP **dosyasının** adı ve indirme bağlantısı bilinçli olarak sabittir.

**Değişiklik günlüğü.** İş akışı her çalıştırmada, bir önceki sürümden bu yana gelen commit başlıklarını
sürüm kimliğiyle başlayan tarihli bir bölüm (`## enf101-2026092901 — 29.09.2026`) olarak sürüm notlarına
ekler; aynı metin ZIP'in içine **`DEGISIKLIKLER.md`** olarak da konur. Sıra numarası ve "hangi commit'ten
bu yana" bilgisi notların içindeki işaretlerden okunur (en üstteki `## enf101-...` başlığı ve
`<!-- son-surum-commit: ... -->` satırı); notlar hiç yoksa `.github/surum-notlari-baslangic.md` temel alınır.
Bu yüzden `checkout` adımı `fetch-depth: 0` ile bütün geçmişi indirir.

**Sürüm sayfası katlanır.** Sürüm sayfasında yalnızca **en yeni üç sürüm** açık durur; daha eskiler
`<details><summary>Önceki sürümler</summary>` kutusunda katlanır. Böylece indirme sayfası sürüm sayısıyla
birlikte uzamaz, günlüğün tamamı tek tıkla açılır. İş akışı her çalıştırmada gövdeyi düz metne indirip
baştan kurduğu için katlama iç içe geçmez; sıra numarası ve commit işareti en üstteki (açık) bölümde
kaldığından durum okuma bozulmaz. **ZIP içindeki `DEGISIKLIKLER.md` katlanmaz** — dosya olarak okunacağı
için orada düz, tam metin durur (katlama etiketi yalnızca web sayfasına aittir).

Bu düzenin iki sonucu var. Birincisi, **commit başlıkları doğrudan günlüğe girer**: notu okuyan kişi bir hoca
veya öğrencidir, bu yüzden commit mesajlarının özet satırı teknik değil, okuyanın anlayacağı dille
yazılmalıdır. İkincisi, sürüm kimliği günlük başlığı olduğu için **her sürüm günlükte yer alır**; içerik
değişmese bile bölüm eklenir ("İçerik değişmedi."), aksi hâlde numaralandırma kopar.

**İçerik dışı değişiklikler.** Yalnızca altyapıyı ilgilendiren commit'lerin başlığı `alt:` ile başlatılır
(ör. `alt: PDF iş akışındaki checkout sürümünü güncelle`). Bunlar günlükten atılmaz ama içerik maddelerinin
altında **"İçerik dışı değişiklikler"** alt başlığı altında, ön ek gösterilmeden listelenir. Böylece günlüğü
okuyan hoca indirdiği dosyaları ilgilendiren değişiklikleri üstte görür; iş akışı ve araç düzeltmeleri altta
kalır, yine de kayda geçer. Kural: bir commit'in başlığı ders içeriğiyle ilgiliyse normal yazılır,
yalnızca üretim/araç/iş akışıyla ilgiliyse `alt:` ön eki kullanılır.

PDF'ler `.qmd` dosyalarının yanına üretilir. Üretim sırasında oluşan geçici dosyalar
(`.quarto/`, `*.log`, `*.tex`, `*_files/`) teslim edilmez; klasör temiz tutulur.

---

## 4. Kritik dosyalar — silinirse proje derlenmez

`_quarto.yml` şu iki dosyaya **referans verir**:

- `tema/notlar.tex`
- `tema/sunum.tex`

`tema/sunum.tex` ise kapak amblemini **`tema/logo.png`**'den alır (bkz. §5 kural 7); bu dosya da
silinirse/taşınırsa sunular amblemsiz derlenir.

**`tema/notlar-hafta.tex`** ise 28 haftalık belgenin (14 ders notu + 14 alıştırma) YAML'ında
`include-in-header: ../tema/notlar-hafta.tex` ile çağrılır; silinir/taşınırsa bu 28 belge derlenmez.
Ayrıntı ve kenar boşluğu/logo kuralları: §6.

Bu dosyalar silinirse veya taşınırsa **hiçbir belge derlenmez** ve şu hata alınır:

```
Error resolving header-includes - unable to open file tema/sunum.tex
```

21.09.2026'da bu durum bir kez yaşandı ve dosyalar yedekten geri yüklendi.
**Bu iki dosyayı silmeyin, taşımayın, adını değiştirmeyin.** Değişiklik gerekiyorsa düzenleyin.

Klasörü taşırken `_quarto.yml`, `tema/` ve `hafta-*/gorseller/` klasörlerinin birlikte taşındığından emin olun.

---

## 5. Sunu yazım kuralları (beamer)

Bu kuralların hepsi **gerçek hatalardan** çıkarılmıştır.

**1. `::: {.block}` kullanma.** Beamer çıktısında kutu üretmez; içeriği düz metne indirger ve
bazı durumlarda kapanış `:::` yerine `::}` kalıntısı bırakarak LaTeX hatası verir.
Vurgu için **kalın metin** kullan. Kutu gerekiyorsa `::: {.callout-warning}` kullan —
beamer'da kenarlıklı kutu ve "Uyarı" etiketiyle düzgün render edilir.

**2. Her `#` bölüm başlığının altında mutlaka bir `##` slayt başlığı olmalı.**
Beamer'da `#` bölüm ayracı, `##` slayt oluşturur. Bir bölüm başlığının altına doğrudan içerik
(tablo, liste) gelirse slayt yapısı bozulur ve **o noktadan sonraki bütün slaytlar tek sayfaya yığılır**.
Hata mesajı vermez, yalnızca sayfa sayısı düşer. 10. haftada bu hata yaşandı: sunu
32 yerine 10 sayfa çıkmıştı. Üretimden sonra slayt sayısını kontrol edin.

**3. `mainfont` ayarlamayın.** `_quarto.yml` içinde font belirtilmemesinin sebebi var:
daha önce "Carlito" ve "TeX Gyre Heros" denendi, ikisi de geliştiricinin makinesinde kurulu olmadığı
için derleme kırıldı. Şu an TeX'in her kurulumda bulunan varsayılan fontu kullanılıyor.
Font değiştirilecekse, seçilen fontun **her işletim sisteminde** var olduğundan emin olunmalıdır.

**4. Slayt sayısı hedefi ~30.** 25–38 aralığı kabul edilebilir; 40'ı geçen sunu sadeleştirilmelidir.

**5. Graphviz şemaları beamer'da slaytı taşar.** Beamer şablonu, Quarto'nun ürettiği Graphviz
görselini slayt sınırına sığdırmaz; görseli sabit 25,4 × 17,8 cm olarak basar ve şema ekrandan taşar.
Hücre seçenekleri (`#| fig-width`) bu diyagram tipinde etkisizdir.
**Çözüm:** şemayı `dot` komutuyla PNG olarak üretip `![](gorseller/x.png){width=50%}` biçiminde ekleyin
(`dot -Tpng -Gdpi=200 -o x.png x.dot`). Mermaid ve TikZ bu sorundan etkilenmez.
Makale (PDF) biçiminde Graphviz **doğrudan çalışır**, çünkü makale şablonu görselleri metin genişliğine sığdırır.

**6. Mermaid şemaları beamer'da ölçeklenemiyor.** Mermaid PDF çıktısında hücre seçenekleri
(`#| fig-width`, `#| fig-height`, `#| out-width`) ya etkisiz ya ters etkili; görsel 63 cm genişliğe çıkıyor.
Belge düzeyi `execute: fig-width` de etkisiz. Beamer şablonu görselleri sınırlamıyor, `\includegraphics`
sarmalaması (Quarto'nun kendi `\pandocbounded` makrosu dâhil) işe yaramıyor.
**Çözüm:** şemayı PNG'ye çevirip `![](gorseller/x.png){width=85%}` biçiminde ekleyin; kaynak `.mmd`
dosyasını yanında tutun.
**Ölçüler (16:9 beamer):** Hannover teması + sol kenar çubuğu + alt şeritle slayt metin alanı
**13,4 × 8,0 cm** (xelatex ile ölçüldü: 381,79 × 227,62 pt). (Kenar çubuğu ve alt şerit yokken,
eski Singapore temasında 398,34 × 252,07 pt = 14,0 × 8,9 cm idi; kenar çubuğu ~1,6 cm, alt şerit
~0,9 cm yer kaplıyor.)
Güvenli üst sınırlar: genişlik %85, yükseklik ~5,8 cm. Bu sınırı aşan görseller slayttan taşar.
**(Uyarı:** bu güvenli sınırlar eski, daha geniş alan için ölçülmüştü; yeni temada yükseklik üst
sınırı oransal olarak **~5,2 cm**'ye iner. İlk uygulamada birkaç diyagramla yeniden doğrulanmalıdır.)
Kare oranlı şemalar %85 genişlikte yükseklik sınırına dayanır; en-boy oranı 2:1'den küçükse
genişliği ~%55'te tutun (oran 1,3 ise %85 zaten taşar).
Makale (PDF) biçiminde Mermaid **doğrudan ve sorunsuz** çalışır; ölçek sorunu yalnızca sunulardadır.

**7. Sunum teması: Hannover + BSEU kimliği (tek kaynak).** Sunuların görünümü üç dosyada tanımlıdır
ve **birlikte** değişir:

- `_quarto.yml` → `theme: Hannover`
- `tema/sunum.tex` → renkler (amblem tonları), kapak (sol dikey bant + logo), kenar çubuğu, alt şerit
- `tema/logo.png` → **kapakta** basılan amblem
- `tema/logobeyaz.png` → **kenar çubuğunda** basılan beyaz amblem (şeffaflığı korunur)

Kenar çubuğunda (içerik slaytları) **sunu adı ve ders adı YAZILMAZ**; onların yerine beyaz amblem
durur. Sunu adı zaten her slaytın alt şeridinde yazdığı için orada tekrar edilmez. Amblemin altında
bölüm navigasyonu aynen kalır.

Renkler amblemden örneklendi: ana koyu kırmızı `#A91818`, gölge `#7C0F0F`, vurgu `#C66A65`,
açık zemin `#F6E8E7`, gri `#5D5E5E`. Onaylanmış tasarım `ornekler/temalar/hafta03/bseu3.pdf`;
tema denemeleri `ornekler/temalar/` altındadır.

Korunacaklar: görselleri sığdıran `\setkeys{Gin}` bloğu (kural 5–6), `mainfont` ayarlanmaması
(kural 3), her `#` altında `##` bulunması (kural 2).

Tuzaklar (ölçülerek bulundu):

- **Kapak bandı, kenar çubuğunun ARKA PLAN katmanından basılır** (`sidebar canvas left` şablonu):
  kapakta 3 cm, içerik slaytlarında kenar çubuğu genişliği kadar. **DİKKAT — bir kez yanlış yapıldı:**
  bant önce kapak şablonunda bir `tikz overlay` olarak çiziliyordu. Arka plan katmanı sayfa çıkışında
  dizildiği için sonuç **derleme geçişine göre değişiyordu: bir geçişte bant var, sonrakinde yok**
  (Quarto 2 geçiş → bant var, +1 geçiş → yok, +2 → var). Bu yöntem terk edildi; tekrar denenmemeli.
- **Kenar çubuğunun arka planını `sidebar canvas left` çizer** (`sidebar left` değil). Kapakta
  boşaltılmazsa çizilen `\vrule` **logonun sol kenarından birkaç piksel keser**; bu yüzden kapağa
  özel olarak 3 cm'lik bant çizecek biçimde yazılmıştır.
- **Kapak ölçütü SLAYIT NUMARASIDIR:** `\ifnum\insertframenumber=1` (kapak) / `>1` (diğerleri).
  Bölüm sayacı kullanılmaz: 1. haftada ilk `#` bölümünden **önce** bir `##` slaytı var ("Dersi Nasıl
  İşleyeceğiz?"); bölüm sayacı orada da 0 kaldığı için o slayt yanlışlıkla kapak sayılıyor, 3 cm'lik
  bant gövdenin üstüne taşıp **madde imlerini örtüyordu** (yaşandı). Kapak, belgenin 1. slaytıdır.
- **Kapakta sözcük bölünmez.** Kapak metni `\raggedright` + `\hyphenpenalty=10000` ile dizilir:
  başlık satır sonunda tire ile kesilmez (`Okuryazar-` / `lık`) ve iki yana yaslamanın açtığı
  kocaman sözcük aralıkları oluşmaz.

**8. Kapak logosunu kaydırmak.** Logo, kapak metninden sonra **içerik olarak** basılır (kırpılmaz).
Metin alanının sol kenarı sayfadan `kenar çubuğu + metin marjı` kadar içeride olduğu için kaydırma
`\dimexpr` ile hesaplanır:

```latex
\hspace*{\dimexpr 1.5cm-\beamer@leftsidebar-\beamer@leftmargin\relax}%
\includegraphics[height=3cm]{../tema/logo.png}
```

`1.5cm`, logo genişliğinin yarısıdır (height 3 cm ⇒ ~3 cm genişlik); böylece logonun **merkezi
bandın sağ kenarına (3,0 cm)** oturur. Sağa/sola kaydırmak için bu değeri değiştirin (ör. `1.7cm`
sağa, `1.3cm` sola). Yükseklik/ölçü için `height` değerini değiştirin; ölçü ipucu: `1 mm ≈ 4 piksel`
(96 dpi). Logo yolu `../tema/logo.png`'dir — xelatex hafta klasöründe çalıştığı için kök değil bir
üst dizin (`../tema/`) kullanılır.

---

## 6. Ders notu kuralları

- Çağrı kutuları (`::: {.callout-note}`, `-tip`, `-warning`) notlarda serbestçe kullanılabilir; PDF'te düzgün render edilir.
- Her hafta şu bölümlerle biter: **Uygulama · Özet · Kendini Sınama Soruları · Kaynaklar**.
- İçindekiler tablosu ve numaralandırma otomatiktir (`toc: true`, `number-sections: true`).
  Başlıklara **elle numara yazılmaz**; sıra değişince numaralar kendiliğinden düzelir.
- Bölüm başlığı **tam metin** olarak figure altına yazılır; Quarto "Şekil 1:" etiketi kendisi ekler.
- **Paragraf `N. ` ile başlamaz.** Satır başındaki "sayı + nokta" pandoc tarafından **sıralı liste** olarak
  çözülür; cümle maddelenir ve devamı maddenin gövdesine girer. En çok haftalara atıf yapan cümlelerde olur
  ("10. haftadaki güvenlik ilkeleri…" → "10." maddesi). Çözüm: noktayı kaçırın — `10\. haftadaki` — ya da
  cümleyi numara satır başına gelmeyecek biçimde kurun. **Kural sunumlar için de geçerlidir.**
  2026-09-29'da 13 cümle bu şekilde düzeltildi (02, 03, 06, 08, 10, 12, 14. haftalar).

**Haftalık belgelerin üst/alt bilgisi, giriş logosu ve kenar boşlukları (2026-10-02).**
14 ders notu ve 14 alıştırma PDF'i `tema/notlar-hafta.tex` katmanını kullanır. Standart:

- **Üst bilgi** (içerik sayfalarında): solda `BŞEÜ`, sağda `ENF101`.
- **Alt bilgi** (içerik sayfalarında): solda `Güncelleme: gg.aa.yyyy`, sağda `Sayfa X / XX`.
  Tarih **elle yazılmaz**; LaTeX'in `\day/\month/\year`'ından gelir, yani derleme (render) günüdür.
  Sıfır dolgusu `\iki` makrosuyla verilir (`\iki{\day}` → `02`).
- **Giriş logosu:** 1. sayfada, başlığın hemen üstünde, ortada, **3 cm** (`\titlehead` ile).
- **Kenar boşlukları:** KOMA varsayılanına göre **alt 2 cm, sağ 1 cm daraltılmıştır** (sol/üst korunur).
  Metin alanı büyüdüğü için belgeler 0–2 sayfa kısalmıştır (hedefler §2).

**Tuzaklar (ölçülerek bulundu, tekrar denenmesin):**
1. **Başlık sayfası "plain" stildedir.** `\maketitle` LaTeX'te `\thispagestyle{plain}` çağırır;
   bu yüzden 1. sayfada üst/alt bilgi görünmez, yalnızca sayfa numarası olur. Bilgi 2. sayfadan başlar.
2. **`\maketitle`'a `\pretocmd` ile logo eklenmez.** KOMA-script (`scrartcl`) başlık sayfasını
   sayfa dolduğunda taşırır; logo başlığı 2. sayfaya iter (denendi, oldu). Doğrusu KOMA'nın
   `\titlehead` alanıdır — başlığın tam üstüne, sayfa kırmadan yerleşir.
3. **Kenar boşluğu `\textwidth`'ı artırarak değiştirilemez.** KOMA `typearea` `\textwidth`'ı
   `\begin{document}` sırasında yeniden hesaplar (bkz. log: `Package typearea Info: ... \textwidth`);
   `\AtBeginDocument` içindeki `\addtolength` bir sonraki `\DIV` hesabında ezilir. Ayrıca yalnızca
   `\textwidth`'ı büyütmek de yetmez: gövde `\columnwidth/\hsize/\linewidth`, fancyhdr ise `\headwidth`
   kullanır. **Çalışan çözüm:** `\AtBeginDocument` içinde beşini birlikte ayarlamak —
   `\addtolength{\textheight}{2cm}`, `\textwidth`, `\columnwidth`, `\hsize`, `\linewidth` (+1 cm) ve
   `\setlength{\headwidth}{\textwidth}`; ardından `\pagestyle{fancy}` yeniden çağrılır.
4. **fancyhdr genişliği `\pagestyle` anında dondurur.** Yalnızca `\fancyhead` tanımlamak yetmez;
   geometri değiştikten sonra `\pagestyle{fancy}` tekrar çağrılmalı, yoksa başlık/alt bilgi eski
   genişlikte kalır (sağa yaslı "ENF101" ortada kalır).

---

## 7. Alıştırma yazım kuralları

Her hafta 10 soru: **8 çoktan seçmeli + 2 doğru–yanlış**. Çoktan seçmeli soruların her biri **beş şıklıdır**
(A–E) ve doğru cevap şıklar arasında dağılır — tek bir harfte birikmez. Cevap anahtarı `{{< pagebreak >}}` ile ayrı
sayfaya alınır ve her soru için kısa gerekçe içerir.

**Soru ile şıklar arasında paragraf boşluğu olmaz.** Soru metni, A) B) C) D) şıkları ve doğru–yanlış
sorularındaki `(   ) Doğru        (   ) Yanlış` satırı tek bir blok hâlinde **bitişik** yazılır;
paragraf boşluğu yalnızca **bir sonraki soruya geçerken** verilir. Amaç, soruyu ve şıklarını gözle
tek bir birim olarak takip edebilmektir; her şık ayrı paragraf olunca blok dağılır.

Kural şöyle uygulanır: blok içindeki her satırın sonuna `\` (pandoc sert satır sonu) konur, satırlar
arasına **boş satır konmaz**; blokların arasına bir boş satır bırakılır.

```markdown
**1.** Soru metni?\
A) Birinci şık\
B) İkinci şık\
C) Üçüncü şık\
D) Dördüncü şık

**2.** Sonraki soru?\
A) ...
```

Blok içindeki satırlar böylece aynı LaTeX paragrafına girer ve aralarında paragraf aralığı oluşmaz.
Boş satır bırakılırsa her şık ayrı paragraf olur ve blok dağılır. **Son satıra `\` konmaz**; blok
normal paragraf sonuyla kapanır.

Bu kural **yalnızca alıştırmalar** içindir; ders notunda paragraflar normal biçimde ayrılır.
28.09.2026'da 14 haftanın tamamına uygulandı; her alıştırma 4 sayfadan 3 sayfaya indi.

**Boş satır yalnızca aralık sorunu değildir.** Her şık kendi paragrafı olduğunda pandoc, `A)`, `B)`,
`C)`, `D)` ile başlayan satırları **sıralı liste** olarak çözer. Şık metni tek başına anlamlı bir
işaret olduğunda içerik bozulur: 8. haftanın "formül hangi işaretle başlar?" sorusunda `A) #`
şıkkı **boş** basılmış, `D) +` şıkkı ise madde imine (`•`) dönüşmüştü; liste ayrıca sayfa
sınırından bölünmüştü. Satırlar bitişik yazılınca bu satırlar düz metin olarak kalır ve sorun
kendiliğinden ortadan kalkar. Çoktan seçmeli şıkların harf etiketleri bu yüzden her zaman
`A)` biçiminde ve soruya bitişik yazılır.

---

## 8. Görsel üretimi

Mevcut 40 diyagramın tamamı **matplotlib** ile üretildi (kaynak betikler ayrı bir çalışma alanında tutuldu).
Tema renkleri: lacivert `#1F3864`, mavi `#2E74B5`, açık zemin `#EDF2F9`, gri `#595959`.

**Ölçü kuralları (iki tur hatadan sonra çıkarıldı):**

1. **Figürün genişliği yazı boyutunu belirler.** Geniş bir figürü slayta sığdırınca
   içindeki yazı da küçülür. Hedef genişlik ~18–23 cm; daha geniş figürler sayfada okunmaz hâle gelir.
2. **Sayfa genişliğine en fazla 5 kart sığar.** Üstüne çıkınca kart başına düşen genişlik azalır ve
   isimler bile kesilir. 10 olaylık bir zaman çizelgesi bu yüzden iki satıra bölündü.
3. Figür boyutu ile eksen oranı uyuşmazsa `bbox_inches="tight"` kırpması punto/birim oranını bozar;
   bunun yerine ekseni figüre tam oturtmak (`fig.add_axes([0,0,1,1])`) daha öngörülebilirdir.

**Ölçü birimi cm'dir.** Görsel ölçüleri **cm, mm veya yüzde** ile verilir; inç kullanılmaz.
Yerleştirmede `{width=8cm}`, `{width=85mm}` ve `{width=85%}` üçü de doğrudan çalışır — pandoc bunları
`\includegraphics` seçeneğine aynen geçirir. Genişlik açıkça verildiğinde görselin dpi damgası sonucu
etkilemez (72 dpi ile 300 dpi aynı sonucu verir). Genişlik verilmezse fiziksel boyut **piksel ÷ dpi**
ile hesaplanır; bu yüzden 72 dpi damgalı PNG'ler (ör. mermaid çıktıları) olduğundan kat kat büyük basılır.
Tek istisna **matplotlib**'tir: `figsize` API'si tanımı gereği inç alır, cm değeri 2,54'e bölünerek verilir
(`figsize=(18/2.54, 12/2.54)`). Graphviz'in `size` ve `margin` nitelikleri de inçtir; orada piksel
kontrolü `-Gdpi` ile yapılır, vektör (SVG/PDF) çıktıda ölçü sorunu hiç yoktur.

**İleride başka araçlar da kullanılabilir** (21.09.2026'da test edildi, üçü de çalışıyor):

| Araç               | Ne zaman                                                                                 | Gereksinim                           |
|:------------------ |:---------------------------------------------------------------------------------------- |:------------------------------------ |
| **Mermaid**        | Akış şemaları, süreç adımları, karar ağaçları. Metin olarak `.qmd` içinde durur          | PDF için Chrome                      |
| **TikZ**           | Kurumsal görünümün kritik olduğu yerler. Belgenin tipografisini ve renklerini aynen alır | `\usepackage{tikz}` (ek kurulum yok) |
| **Graphviz (DOT)** | Düğüm-kenar ilişkisinin yoğun olduğu yapılar (ağ şemaları)                               | PDF için Chrome                      |
| **matplotlib**     | Mevcut diyagramlar; paletle birebir uyum garantisi                                       | Python + matplotlib                  |

TikZ ortak temada etkinleştirilmiştir (`\usepackage{tikz}` ve şekil kütüphaneleri `tema/notlar.tex` içinde).
TikZ şemalarında kullanılabilecek renk adları: `navy`/`enfnavy`, `accentcol`/`enfaccent`, `greytext`/`enfgrey`, `lightbg`. İki ad kümesi de her iki temada tanımlıdır (takma ad olarak eklendi), böylece ders notu ve sunu dosyalarında aynı adlar kullanılabilir.

Chrome gereken araçlar için: `quarto install chrome-headless-shell` (tek seferlik, ~150 MB).
Mermaid ve Graphviz kendi varsayılan font ve renkleriyle çizer — belgeye "yabancı" durabilir;
kurumsal palete çekmek için ayrıca tema ayarı gerekir.

**Fotoğraflar.** Diyagramın yanında, konunun somut nesnesini göstermek için fotoğraf kullanılır: donanım
parçaları, bağlantı noktaları, depolama aygıtları, ağ donanımı, giyilebilir ve IoT cihazları, tarihsel
hesaplama makineleri. Soyut konularda (veri–enformasyon–bilgi, KVKK, etik, güvenlik kavramları) fotoğraf
aramak yerine şema çizilir. **Fotoğraf diyagramın yerini almaz**, yanına gelir: şema "nerede, ne işe yarar"
sorusunu, fotoğraf "gerçekte nasıl görünür" sorusunu yanıtlar.

- **Kaynak:** Wikimedia Commons. Lisans Commons API'sinden **doğrulanır**, dosya adından tahmin edilmez.
  Kabul: CC0, kamu malı, CC BY, CC BY-SA. Red: FAL, GFDL, NC, ND ve lisansı belirsiz olanlar.
- **Kaynak gösterimi:** Atıf gerektiren her fotoğraf için haftanın Kaynaklar bölümüne "Görsel kaynakları"
  listesi eklenir: *Dosya adı — Yazar, Lisans.* CC0/kamu malı olanlar için zorunlu değildir ama künyesi
  yine yazılır.
- **Dosya adı:** `gorseller/foto-<konu>.jpg` (ASCII, küçük harf, tire) — örn. `foto-anakart.jpg`,
  `foto-cpu-soketi.jpg`. Şemalar `diagram-*.png`, ekran görüntüleri `ekran-*.png` kalıbındadır;
  üçü karışmaz.
- **Ekran görüntüsü:** belirli bir sistemin penceresi, kavramı somutlaştırmak için **örnek olarak**
  kullanılabilir (§9). Baskıda okunabilirlik için kare en az ~600 px genişlikte olmalı ve genişliği
  açıkça verilmelidir (`{width=…}`); gösterildiğinde **hangi sistem olduğu yazılır**.
- **Ölçü:** İnen dosyanın en uzun kenarı **~1000 piksel** olmalı (baskıda ~10 cm genişlik ≈ 254 dpi).
  Commons dosyaları 72 dpi damgalı gelir; bu yüzden yerleştirmede **her fotoğrafa açık `{width=…}` yazılır**,
  aksi hâlde §8'in ölçü kuralı gereği kat kat büyük basılır. Gereğinden büyük dosya PDF'i şişirir:
  2. haftada 1600 piksellik 10 fotoğraf ders notunu 299 KB'tan 5,43 MB'a çıkarmıştı.
- **Ders notunda yerleşim:** `::: {#fig-ad layout-ncol=N}` bloğu. **Kimlik ve başlık zorunludur:** bunlar
  olmadan Quarto bloğu şekil saymaz, alt görseller "(a)" etiketi alır, ana "Şekil N" başlığı basılmaz,
  ama numara yine tüketilir ve numaralandırma atlar.
- **Sunumda yerleşim:** Görseller **aynı paragrafta bitişik** yazılır
  (`![](gorseller/a.jpg){width=45%} ![](gorseller/b.jpg){width=45%}`); `layout-ncol` sunumda her görsele
  "Şekil N" başlığı eklediği için kullanılmaz. Büyük bir şema ya da tablo içeren slayta fotoğraf sırası
  **eklenmez** (başlıklardan sonra gövdeye kalan alan ~7 cm'dir, fotoğrafın altı kesilir); fotoğraf sırasına
  kendi slaydı verilir — dört fotoğraf %23 genişlikle ve tek satır açıklamayla rahat oturur.
- **Kapsam:** Fotoğraf eklendiğinde **ders notu ve sunum birlikte** güncellenir ve ikisi de yeniden derlenir;
  sunuma slayt eklendiyse `python3 araclar/basliklari-uret.py` çalıştırılıp `BASLIKLAR.qmd` yenilenir (§3).
- **İçerik sınırları:** Markanın baskın olduğu kare seçilmez (§9 marka kuralıyla gerilim); tanınabilir insan
  içeren kare kullanılmaz (model izni gerekir). Fotoğraf metinde geçmeyen bir olgu getiriyorsa (model adı,
  tarih) başlıkta açıkça belirtilir.
- **Bütçe:** Fotoğraf sayfa/slayt sayısını artırır. Gerekiyorsa görselin metnin yerine geçmesi yeğlenir;
  hedefler §2 ve §5'te.

---

## 9. İçerik ilkeleri

- **Platformdan bağımsız.** Belirli bir işletim sistemi, ofis sürümü veya marka öğretilmez;
  menü yolları, düğme adları ve sürüm karşılaştırmaları yazılmaz; kavramlar anlatılır. Yazılım adları **örnek olarak** geçebilir (adı ve ne işe yaradığı), ancak her konuda ücretsiz bir **çevrimiçi** seçenek ile kurulabilen **açık kaynak** bir seçenek birlikte gösterilir; ortam seçimi öğrenciye bırakılır. Açık ve kapalı kaynak yazılımlar birlikte tanıtılır.
  **Ekran görüntüleri yasak değildir.** Belirli bir sistemin penceresi, bir kavramı somutlaştırmak
  için **örnek olarak** gösterilebilir; gösterildiğinde **hangi sistem olduğu açıkça yazılır**
  (ör. "Windows'un biçimlendirme penceresi"). Kuralın yasakladığı şey, o sistemi **tek doğru yolmuş
  gibi** anlatmak ve öğrenciden menü ezberi beklemektir; örnek olarak göstermek serbesttir.
  (Kullanıcı kararı, 2026-09-30 — 4. haftadaki biçimlendirme ekran görüntüsü vesilesiyle.)
- **Sade dil.** Hedef kitle teknik olmayan bölümlerden geliyor. Jargon ilk kullanımda tanımlanır.
- **Aşırı teknik ayrıntıdan kaçınılır.** İşlemci mimarisi, önbellek katmanları, DDR nesilleri,
  protokol başlık yapıları gibi konular 1. sınıf için gereksizdir; "kısaca değinmek yeter" düzeyinde kalır.
- **Uygulamaya bağlama.** Her konu günlük hayattan bir örnekle veya somut bir alıştırmayla bağlanır.
- **Etkileşim gözetilir.** Ders 40 dakika ve uzaktan işleniyor; düz anlatım yerine soru-cevap,
  canlı quiz ve tartışma için alan bırakılır. Ders notu **tam** tutulur, sınıf oturumu **seçici** olur.
- **Kaynak gösterimi.** Kullanılan kaynaklar kamuya açık ve doğrulanabilir olmalıdır
  (BTK, KVKK, USOM, TÜBİTAK BİLGEM, TÜİK, Pardus gibi). Uydurma künye yazılmaz.
- **Türkiye'ye özgü bağlam** korunur: e-Devlet, e-imza, KVKK, Pardus gibi konular dersin ayırt edici yanıdır.
- **Ölçü birimleri metrik (SI).** Metin içinde uzunluk ölçüleri cm, mm, metre ile verilir; inç kullanılmaz.

---

## 10. Haftalık paket standardı

Her hafta için üç belge:

| Belge         | İçerik                                                                                                     |
|:------------- |:---------------------------------------------------------------------------------------------------------- |
| **ders-notu** | Kurumsal kapak yok; başlık bloğu. Öğrenme çıktıları, ana içerik, uygulama, özet, kendini sınama, kaynaklar |
| **sunum**     | Bölüm ayraçları + slaytlar. Öğrenme çıktılarıyla başlar, "gelecek hafta" ile biter                         |
| **alıştırma** | 8 çoktan seçmeli (beş şıklı) + 2 doğru-yanlış; cevap anahtarı ayrı sayfada, kısa gerekçeli                 |

Üçünde de aynı başlık yapısı ve aynı görsel dil kullanılır; haftalar arası tutarlılık esastır.

**Terim notu:** Haftalık paylaşılan üçüncü belge **alıştırma**dır ve notla değerlendirilmez. "Kısa sınav"
(bazen "quiz" de denir) ise vize ve final ile birlikte başarı notuna giren ayrı bir ölçme aracıdır;
alıştırmayla karıştırılmamalıdır.

---

## 11. Teslim öncesi doğrulama

```bash
# 1. Derleme — klasörü kopyalayıp sıfırdan derleyin (kaynak klasörde artık bırakmasın)
cp -r . /tmp/kontrol && cd /tmp/kontrol && rm -f *.pdf hafta-*/*.pdf && quarto render hafta-01-giris-temel-kavramlar

# 2. Boş/bozuk sayfa taraması
for f in hafta-*/*.pdf; do
  pdftotext "$f" - | awk 'BEGIN{RS="\f"} {gsub(/[ \t\n]/,""); if(length<25) c++} END{if(c>0) print FILENAME, c}'
done

# 3. Beamer yapı kontrolü — her '#' altında '##' var mı?
#    (yoksa slaytlar tek sayfaya yığılır, hata mesajı çıkmaz)
awk '/^# /{if(p!=""&&!f)print "SORUN:",p; p=$0; f=0; next} /^## /{f=1} END{if(p!=""&&!f)print "SORUN:",p}' hafta-*/[0-9][0-9]-sunum.qmd

# 4. Kalıntı sözdizimi
grep -rn "{.block}" hafta-*/[0-9][0-9]-sunum.qmd

# 5. İnç kalıntısı — içerikte ölçüler cm/mm veya yüzde olmalı
#    (desenli arama "bilinçli" gibi kelimelere takılmaz, "inçe" gibi ekleri yakalar;
#     *.md dışarıda: bu dosyanın kendi kural metni inç kelimesini içeriyor)
grep -rnE '[^[:alpha:]]inç|^inç' --include="*.qmd" --include="*.tex" .

# 6. Alıştırmada soru ile şıklar bitişik mi?
#    (soru satırından hemen sonra boş satır varsa blok dağılmış demektir — bkz. §7)
awk 'p ~ /^\*\*[0-9]+\.\*\*/ && $0=="" {print FILENAME": "NR". satır — sorudan sonra boş satır"} {p=$0}' hafta-*/[0-9][0-9]-alistirma.qmd
#    Çıktı boş olmalı. Sonuç varsa ilgili soru bloğundaki boş satırlar kaldırılıp
#    satır sonlarına `\` eklenir.

# 7. İçerik başlıkları kaynaklarla uyumlu mu? (commit beklemeye gerek yok)
python3 araclar/basliklari-uret.py --kontrol

# 8. Altbilgi doğru mu? — her ders notunun son sayfası "Sayfa n / n" yazmalı
#    (yanlışsa: bash araclar/derle.sh <klasör>; bkz. §3)
for f in hafta-*/[0-9][0-9]-ders-notu.pdf; do
  n=$(pdfinfo "$f" | awk '/^Pages/{print $2}')
  s=$(pdftotext -layout -f "$n" -l "$n" "$f" - | grep -oE 'Sayfa [0-9]+ / [0-9]+' | head -1)
  [ "$s" = "Sayfa $n / $n" ] || echo "HATA: $f -> ${s:-altbilgi yok} (gerçek $n)"
done

# 9. Üst/alt bilgi yerinde mi? — her haftalık belgenin 2. sayfasında
#    BŞEÜ + ENF101 (üst) ve "Güncelleme: gg.aa.yyyy" (alt) bulunmalı (bkz. §6)
for f in hafta-*/[0-9][0-9]-ders-notu.pdf hafta-*/[0-9][0-9]-alistirma.pdf; do
  t=$(pdftotext -layout -f 2 -l 2 "$f" -)
  echo "$t" | grep -q "BŞEÜ" && echo "$t" | grep -q "ENF101" || echo "HATA: üst bilgi yok -> $f"
  echo "$t" | grep -qE "Güncelleme: [0-9]{2}\.[0-9]{2}\.[0-9]{4}" || echo "HATA: tarih yok -> $f"
done
```

---

## 12. Bekleyen işler

**Açık — karar bekleyen iş yok (30.09.2026).** Sunum teması yaygınlaştırması tamamlandı; ders
notları **ENF lacivertinde kalıyor** (kullanıcı kararı, 30.09.2026).

Kapatılan başlıklar ve kararları:

- **Sunum teması yaygınlaştırma (30.09.2026):** Şablon Hannover + BSEU kimliğine çevrildi
  (`tema/sunum.tex`, `tema/logo.png`, `_quarto.yml`; §5 kural 7–8). **14 haftanın tamamı +
  `ornekler/quarto-ozellikleri-sunum.qmd`** yeni temayla yeniden derlendi; slayt sayıları birebir
  korundu (01:28, 02:37, 03:35, 04:39, 05:39, 06:36, 07:39, 08:39, 09:31, 10:38, 11:30, 12:29,
  13:30, 14:38; örnek:38). Hafta-02 ve 03 kenar çubuğuna beyaz amblem gelmeden önce derlenmişti,
  onlar da yenilendi. Ders notları ve alıştırmalar **değişmedi**. Bu iş sırasında `tema/sunum.tex`'te
  eksik olan ortak TikZ renk adları (`navy`/`enfnavy`, `accentcol`/`enfaccent`, `greytext`/`enfgrey`,
  `lightbg`; §8) geri eklendi — şablon yenilenirken düşmüşlerdi ve TikZ şeması içeren örnek sunumu
  "Undefined color `enfnavy`" hatasıyla derlenmez hâle getirmişlerdi.


- **Sunu kalabalığı:** 4. hafta 38, 7. hafta 39 slayt. Kullanıcı bu yoğunluğu kabul etti (hedef ~30,
  kabul edilen üst sınır 38; 39 onaylı). Yeni bir konu eklenirse başka bir yerden yer açmak gerekir.
- **Uyarı kutuları:** 4. ve 5. haftada ikişer olan `callout-warning` kutuları 14 sununun tamamına
  yaygınlaştırıldı; artık her sunuda en az bir kutu var.
- **Çıktı eşlemesi (K1–K9):** izlence ile haftalık belgeler arasındaki eşleme gözden geçirildi.
  4. haftaya K4 eklendi (bulut ve işbirliği araçları), 3. haftadaki K2 bağlantısı kaldırıldı
     (donanım çıktısı, yazılım haftasına bağlıydı), K3'e işletim sistemi aileleri eklendi.
- **Haftalık belgelere kurumsal üst/alt bilgi ve giriş logosu (02.10.2026):** 14 ders notu + 14
  alıştırma `tema/notlar-hafta.tex` katmanını kullanır (üst: BŞEÜ/ENF101, alt: güncelleme tarihi +
  sayfa, girişte 3 cm logo). Kenar boşlukları alt 2 cm / sağ 1 cm daraltıldı. Ayrıntı ve dört tuzağı:
  §6. izlence, BASLIKLAR ve KILAVUZ bu katmanı **kullanmaz** (bilinçli).

---

## 13. Sürüm ve kaynak notu

- PDF motoru **XeLaTeX**. **Sürüm sabitlenmez:** güncel Quarto ve güncel TeX Live kullanılır.
  Belirli bir sürüme bağlı kalınmaz; hangi sürüm kuruluysa onun çıktısı esas alınır.
- **Esas olan kaynaktır:** ölçüt, `.qmd` dosyalarının düzgün derlenmesidir. PDF'ler onlardan üretilen
  çıktılardır; sürüm yükseltmesinde hepsini birden yenilemek gerekmez, sürüme bağlı ufak görsel
  farklar (madde imi glifi gibi) kabul edilir.
- Bu belgeler, `eski/` klasöründe bulunan ve önceki yıllarda farklı kişilerce hazırlanmış
  malzemeden **bilinçli olarak ayrılarak** yeniden yazılmıştır. Eski malzemedeki aşırı detaylı
  ve kapsam dışı bölümler (donanım arıza çözümleri, programlama, protokol ayrıntıları, mevzuat maddeleri)
  yeni içeriğe alınmamıştır.
