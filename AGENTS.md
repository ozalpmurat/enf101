# AGENTS.md

Bu dosya, bu klasörde çalışan yapay zekâ ajanları ve içerik üreten kişiler için hazırlanmıştır.
Projenin nasıl kurulduğunu, hangi kurallara uyulduğunu ve hangi tuzaklara düşülmemesi gerektiğini anlatır.

Son güncelleme: 28.09.2026

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

Ders, klasik "temel bilgi teknolojileri" kapsamındadır; **programlama ve algoritma bilinçli olarak kapsam dışıdır**.

---

## 2. Klasör yapısı

```
2026-ai/
├─ AGENTS.md                     bu dosya
├─ _quarto.yml                   proje ayarları (ortak tema buradan bağlanır)
├─ tema/
│  ├─ notlar.tex                 ders notu · alıştırma · izlence görünümü (TikZ desteği dahil)
│  └─ sunum.tex                  beamer sunu görünümü
├─ ornekler/                     Quarto özellik örnekleri (başvuru belgesi, ders içeriği değil)
│  ├─ quarto-ozellikleri.qmd + .pdf + .html        özellik başvuru belgesi
│  ├─ quarto-ozellikleri-sunum.qmd + .pdf          aynı içeriğin sunum sürümü
│  └─ gorseller/
├─ izlence.qmd + .pdf            ders izlencesi
├─ KILAVUZ_Quarto_...qmd + .pdf  hocalar için Quarto kurulum/kullanım kılavuzu
└─ hafta-NN/                     NN = 01 … 14
   ├─ ders-notu.qmd + .pdf       8–12 sayfa
   ├─ sunum.qmd + .pdf           25–38 slayt (hedef ~30)
   ├─ alistirma.qmd + .pdf        4 sayfa · 10 soru + cevap anahtarı
   └─ gorseller/*.png            o haftanın diyagramları
```

Toplam: 14 hafta · 42 belge (+ izlence ve kılavuz) · 38 diyagram.

---

## 3. Üretim

Her şey **Quarto** ile üretilir. Proje kökünde:

```bash
quarto render hafta-03          # tek haftanın üç belgesini üretir
quarto render izlence.qmd       # tek dosya
```

**Dikkat:** `quarto render` yalnızca **tek yol** alır. `quarto render hafta-01 hafta-03` çalışmaz.
Tam projeyi tek komutta derlemek 3 dakikayı aştığı için uzun işlerde hafta hafta derlemek gerekir.

PDF'ler `.qmd` dosyalarının yanına üretilir. Üretim sırasında oluşan geçici dosyalar
(`.quarto/`, `*.log`, `*.tex`, `*_files/`) teslim edilmez; klasör temiz tutulur.

---

## 4. Kritik dosyalar — silinirse proje derlenmez

`_quarto.yml` şu iki dosyaya **referans verir**:

- `tema/notlar.tex`
- `tema/sunum.tex`

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
**Ölçüler (16:9 beamer):** slayt metin alanı **14,0 × 8,9 cm** (xelatex ile ölçüldü: 398,34 × 252,07 pt).
Güvenli üst sınırlar: genişlik %85, yükseklik ~5,8 cm. Bu sınırı aşan görseller slayttan taşar.
Kare oranlı şemalar %85 genişlikte yükseklik sınırına dayanır; en-boy oranı 2:1'den küçükse
genişliği ~%55'te tutun (oran 1,3 ise %85 zaten taşar).
Makale (PDF) biçiminde Mermaid **doğrudan ve sorunsuz** çalışır; ölçek sorunu yalnızca sunulardadır.

---

## 6. Ders notu kuralları

- Çağrı kutuları (`::: {.callout-note}`, `-tip`, `-warning`) notlarda serbestçe kullanılabilir; PDF'te düzgün render edilir.
- Her hafta şu bölümlerle biter: **Uygulama · Özet · Kendini Sınama Soruları · Kaynaklar**.
- İçindekiler tablosu ve numaralandırma otomatiktir (`toc: true`, `number-sections: true`).
  Başlıklara **elle numara yazılmaz**; sıra değişince numaralar kendiliğinden düzelir.
- Bölüm başlığı **tam metin** olarak figure altına yazılır; Quarto "Şekil 1:" etiketini kendisi ekler.

---

## 7. Görsel üretimi

Mevcut 38 diyagramın tamamı **matplotlib** ile üretildi (kaynak betikler ayrı bir çalışma alanında tutuldu).
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

---

## 8. İçerik ilkeleri

- **Platformdan bağımsız.** Belirli bir işletim sistemi, ofis sürümü veya marka öğretilmez;
  menü yolları yerine kavramlar anlatılır. Açık ve kapalı kaynak yazılımlar birlikte tanıtılır.
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

## 9. Haftalık paket standardı

Her hafta için üç belge:

| Belge         | İçerik                                                                                                     |
|:------------- |:---------------------------------------------------------------------------------------------------------- |
| **ders-notu** | Kurumsal kapak yok; başlık bloğu. Öğrenme çıktıları, ana içerik, uygulama, özet, kendini sınama, kaynaklar |
| **sunum**     | Bölüm ayraçları + slaytlar. Öğrenme çıktılarıyla başlar, "gelecek hafta" ile biter                         |
| **alıştırma** | 8 çoktan seçmeli + 2 doğru-yanlış; cevap anahtarı ayrı sayfada, kısa gerekçeli                             |

Üçünde de aynı başlık yapısı ve aynı görsel dil kullanılır; haftalar arası tutarlılık esastır.

**Terim notu:** Haftalık paylaşılan üçüncü belge **alıştırma**dır ve notla değerlendirilmez. "Kısa sınav"
(bazen "quiz" de denir) ise vize ve final ile birlikte başarı notuna giren ayrı bir ölçme aracıdır;
alıştırmayla karıştırılmamalıdır.

---

## 10. Teslim öncesi doğrulama

```bash
# 1. Derleme — klasörü kopyalayıp sıfırdan derleyin (kaynak klasörde artık bırakmasın)
cp -r . /tmp/kontrol && cd /tmp/kontrol && rm -f *.pdf hafta-*/*.pdf && quarto render hafta-01

# 2. Boş/bozuk sayfa taraması
for f in hafta-*/*.pdf; do
  pdftotext "$f" - | awk 'BEGIN{RS="\f"} {gsub(/[ \t\n]/,""); if(length<25) c++} END{if(c>0) print FILENAME, c}'
done

# 3. Beamer yapı kontrolü — her '#' altında '##' var mı?
#    (yoksa slaytlar tek sayfaya yığılır, hata mesajı çıkmaz)
awk '/^# /{if(p!=""&&!f)print "SORUN:",p; p=$0; f=0; next} /^## /{f=1} END{if(p!=""&&!f)print "SORUN:",p}' hafta-*/sunum.qmd

# 4. Kalıntı sözdizimi
grep -rn "{.block}" hafta-*/sunum.qmd

# 5. İnç kalıntısı — içerikte ölçüler cm/mm veya yüzde olmalı
#    (desenli arama "bilinçli" gibi kelimelere takılmaz, "inçe" gibi ekleri yakalar;
#     *.md dışarıda: bu dosyanın kendi kural metni inç kelimesini içeriyor)
grep -rnE '[^[:alpha:]]inç|^inç' --include="*.qmd" --include="*.tex" .
```

---

## 11. Bekleyen işler

- **4. ve 7. hafta sunuları kalabalık** (38'er slayt). Sadeleştirme önerildi, karar bekliyor.
- **4. ve 5. hafta sunularında 2'şer uyarı kutusu var**, diğer 12 sunuda yok. Tutarlılık için
  ya kaldırılmalı ya diğerlerine yaygınlaştırılmalı.
- **Yapay zekâ yeterliliği (K9)** ve izlencedeki diğer çıktı güncellemeleri yapıldı; ancak ders
  izlencesi ile haftalık belgeler arasında çıktı kodları (K1–K9) eşlemesi gözden geçirilebilir.

---

## 12. Sürüm ve kaynak notu

- PDF motoru **XeLaTeX**. **Sürüm sabitlenmez:** güncel Quarto ve güncel TeX Live kullanılır.
  Belirli bir sürüme bağlı kalınmaz; hangi sürüm kuruluysa onun çıktısı esas alınır.
- **Esas olan kaynaktır:** ölçüt, `.qmd` dosyalarının düzgün derlenmesidir. PDF'ler onlardan üretilen
  çıktılardır; sürüm yükseltmesinde hepsini birden yenilemek gerekmez, sürüme bağlı ufak görsel
  farklar (madde imi glifi gibi) kabul edilir.
- Bu belgeler, `eski/` klasöründe bulunan ve önceki yıllarda farklı kişilerce hazırlanmış
  malzemeden **bilinçli olarak ayrılarak** yeniden yazılmıştır. Eski malzemedeki aşırı detaylı
  ve kapsam dışı bölümler (donanım arıza çözümleri, programlama, protokol ayrıntıları, mevzuat maddeleri)
  yeni içeriğe alınmamıştır.
