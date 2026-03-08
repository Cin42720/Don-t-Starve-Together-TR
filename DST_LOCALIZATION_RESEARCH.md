# DST Localization Research

Araştırma tarihi: 2026-03-06

Bu not, DST Türkçe yerelleştirmesini satır satır değil, oyunun kendi kavram dili ve karakter sesi üzerinden toparlamak için hazırlandı.

## 1. Kullandığım ana kaynaklar

Yerel, oyunun kendi kaynakları:

- `data/scripts/strings.lua`
- `data/scripts/speech_waxwell.lua`
- `data/scripts/speech_walter.lua`
- `data/scripts/speech_wanda.lua`
- `data/scripts/speech_wortox.lua`
- `data/scripts/speech_wurt.lua`
- `data/speech_en.json`
- `data/speech_tr.json`
- `mod/scripts/languages/tr_ui.lua`
- `mod/scripts/languages/tr_speech_fixes.lua`

Harici referanslar:

- https://dontstarve.fandom.com/wiki/Nightmare_Fuel
- https://dontstarve.fandom.com/wiki/Pure_Horror
- https://dontstarve.fandom.com/wiki/The_Constant
- https://dontstarve.fandom.com/wiki/Wagstaff
- https://dontstarve.fandom.com/wiki/Crabby_Hermit
- https://dontstarve.fandom.com/wiki/Shadow_Thurible
- https://dontstarve.fandom.com/wiki/Reanimated_Skeleton

## 2. Yüksek güvenli dünyaterimi notları

### The Constant

- Oyun içi lore ve wiki tarafında `The Constant` ayrı bir boyut/alan adı olarak kullanılıyor.
- Bu yüzden genel öneri: `Sabit` gibi düz anlamsal çeviri yerine `Constant` olarak bırakmak.
- `Constant'ın ...` yapısı Türkçede daha doğal duruyor.

### Nightmare Fuel

- Bu öğe düz anlamda benzin/odun benzeri sıradan bir `yakıt` değil.
- Kaynaklarda gölge/magic üretimiyle bağlantılı bir madde, tortu, artık ve güç taşıyıcısı gibi çalışıyor.
- Fandom özeti de bunu büyü eşyaları üretmekte ve bazı gölge nesneleri beslemekte kullanılan özel bir madde olarak anlatıyor.
- Bu yüzden `Kabus Yakıtı` birçok satırda fazla mekanik, düz ve komik kaçıyor.

Güçlü adaylar:

- `Kâbus Özü`
- `Kâbus Esansı`

Çalışma kuralı:

- Nesnenin adı olarak `yakıt`tan kaçın.
- Ama gerçekten bir şeyi besleme/çalıştırma işlevi anlatılıyorsa fiil düzeyinde `yakıt`, `beslemek`, `güç vermek`, `çalıştırmak` kullanılabilir.

### Pure Horror

- `Pure Horror`, `Nightmare Fuel` ile akraba ama daha ileri/arıtılmış bir gölge maddesi gibi kullanılıyor.
- Kaynaklarda hem Shadowcrafting üretimi için malzeme hem de Nightmare Fuel kullanan şeyler için daha verimli besleyici madde olarak geçiyor.
- Bu yüzden `Saf Korku` teknik olarak anlaşılır olsa da, ton olarak fazla soyut ve zayıf kalabiliyor.

Güçlü adaylar:

- `Saf Dehşet`
- `Arı Dehşet`

Not:

- Bu terim seçimi, `Nightmare Fuel` ile birlikte düşünülmeli. Biri değişip öbürü sabit kalırsa terminoloji dağılıyor.

### Fuel / fueled / fuel source

Bu kökün çevirisi bağlama göre ayrılmalı:

- Kamp ateşi, fener, ocak, thurible gibi gerçekten beslenen nesneler: `yakıt`, `yakıtla beslemek`, `yakıtı bitmek`
- Gölge/lunar madde bir makineyi güç kaynağı olarak çalıştırıyorsa: `enerji kaynağı`, `besleyici madde`, `güç kaynağı`
- Tamamen mistik bir özden söz ediliyorsa: `öz`, `esans`, `karanlık madde` türü çözümler daha uygun

Yani `fuel` her yerde aynı Türkçe karşılıkla gitmemeli.

### Proper noun'lar

Aşağıdakiler çevrilmemeli, sabit kalmalı:

- `Wagstaff`
- `Pearl`
- `Charlie`
- `Maxwell`
- `The Constant` için de büyük olasılıkla aynı yaklaşım daha doğru

NPC/unvan veya sınıf adı olanlar ise bağlama göre çevrilebilir:

- `Crabby Hermit`
- `Ancient Fuelweaver`
- `Nightmare Werepig`
- `Scrappy Werepig`

Ama burada önce terim politikası netleşmeli; yoksa bir yerde ad, bir yerde unvan gibi davranılıyor.

## 3. Karakter sesi araştırması

Çeviri problemi yalnız kelimede değil, karakter sesi kayınca da başlıyor.

### Wilson

- Bilim takıntılı, meraklı, hafif kendini beğenmiş.
- `science` vurgusu karakter kimliğinin parçası.
- Her `science` satırını `bilim` diye dümdüz çevirmek yetmez; bazen ünlem, bazen kibir, bazen merak tonu taşıyor.

Çeviri ilkesi:

- Hafif geveze, zeki, kendinden memnun.
- Aşırı argo veya aşırı düz Türkçe Wilson'ı bozar.

### Willow

- Kısa, sivri, yangın odaklı, hafif yıkıcı zevk taşıyan bir ses.
- Cümleleri fazla açıklamacı olunca karakter dağılıyor.

Çeviri ilkesi:

- Kısa ve tok.
- Ateşle ilgili satırlarda gereksiz resmiyet yok.

### Wendy

- Melankolik, şiirsel ama teatral değil.
- Ağır dramaya kaçınca komikleşiyor.

Çeviri ilkesi:

- Karanlık ama sade.
- Lirizm var, fakat süslü söz şişkinliği yok.

### Wolfgang

- Basit konuşuyor ama aptal değil.
- Güç, korku ve özgüven ekseni var.

Çeviri ilkesi:

- Çocuklaştırma yapma.
- Az kelimeli ama tok konuşsun.

### Wickerbottom

- Akademik, ölçülü, tam cümle kuran biri.
- Teknik terimleri taşıyabilecek nadir karakterlerden.

Çeviri ilkesi:

- Düzgün, dikkatli, öğretici.
- Sokak dili veya kaba espri olmaz.

### Woodie

- Rustik ve sıcak.
- `eh` tiki önemli ama her satıra yapıştırılmamalı.

Çeviri ilkesi:

- Hafif taşra tonu.
- Karikatür Kanadalı yapma.

### Maxwell

- Aristokratik, kibirli, alaycı, sahne insanı.
- Şakaları birebir kelime oyunu taşımak yerine aynı etkiyi taşımalı.
- Çeviri düzleştiğinde Maxwell hemen sıradanlaşıyor.

Çeviri ilkesi:

- Keskin, cilalı, hafif küçümseyici.
- Türkçede çalışmayan kelime oyunlarını işlevsel espriye çevir.
- `ışığa şükürler olsun` gibi literal ve ruhsuz kalıplardan kaçın.

### Webber

- Çocuk sesi var.
- Birçok satırda `we/us` kullanıyor; tekil çevrilince karakter bozuluyor.

Çeviri ilkesi:

- `biz` hissi korunmalı.
- Masum ve tatlı; yapay bebek dili değil.

### Winona

- Çalışan sınıf, pratik, mekanik kafalı.
- Doğrudan konuşuyor.

Çeviri ilkesi:

- İş bilen, lafı dolandırmayan.
- Fazla kitap Türkçesi kaldırmaz.

### Wortox

- Kafiye, iç ses, kelime oyunu, sıçrayan ritim.
- Tam kafiyeye zorlanınca Türkçede çok kolay sirke dönüyor.

Çeviri ilkesi:

- Mutlaka işlevsel ritim olsun.
- Ama başarısız tam kafiye yerine yarım uyak, ses oyunu, ritim öncelikli.
- `hyuyu` tiki korunmalı.

### Wurt

- Bilinçli şekilde bozuk/sade sözdizimi.
- `florp`, `glorp` gibi sesler kimliğin parçası.

Çeviri ilkesi:

- Cümleler kısa.
- Kırık ama anlaşılır.
- Çocukça değil, Mermce etkili olmalı.

### Walter

- İzcilik, heves, hafif baba şakası, masumiyet.
- Şakaları kötü olabilir; zaten karakterin parçası.

Çeviri ilkesi:

- Samimi ve hevesli.
- Espri çalışmıyorsa “kötü ama sevimli” bir tona düşmeli.

### Wanda

- Zaman temalı, sabırsız, kuru mizahı var.

Çeviri ilkesi:

- Keskin ve aceleci.
- Fazla genç/argo ton verme.

### Warly

- Aşçı gözüyle konuşur.
- Fransız dokunuşu tamamen silinmemeli.

Çeviri ilkesi:

- Yemek metaforları korunmalı.
- `non?` gibi küçük işaretler dozunda kalmalı.

### WX-78

- Büyük harf, makine dili, küçümseme.

Çeviri ilkesi:

- Robotik ritim korunmalı.
- Gereksiz uzun cümleler karakteri bozar.

### Wathgrithr / Wigfrid

- Yüksek tondan, sahneli, destansı konuşur.
- Ama komik tarafı da var.

Çeviri ilkesi:

- Epik ve oynanmış dursun.
- Her şeyi `lokma`, `yem`, `ganimet` diye çözmek tonu daraltıyor.

### Pearl

- Sevecen yaşlı hanımefendi tonu.
- `dearie` tekrar ediyor ama bu tekrar sıcaklık yaratıyor.

Çeviri ilkesi:

- `canım`, `canım benim`, `şekerim` çizgisine yakın düşün.
- Fazla resmi ya da fazla mahalle ağzı olmamalı.

### Wagstaff

- Mucit, takıntılı, yarı çılgın, teknik düşünen biri.
- Kuru akademik değil; keşif coşkusu var.

Çeviri ilkesi:

- Teknik ama canlı.
- Yaşlı mucit merakı korunmalı.

## 4. Şu anki TR dosyalarında görünen ana risk kümeleri

### A. `yakıt`ın semantik taşması

Sorun:

- `Kabus Yakıtı`
- `gölge yakıtı`
- `karanlık yakıt`
- `canlı yakıt`
- `yakıt seni değiştirmiş`

Bu kullanım, nesnenin mistik/lore ağırlığını düşürüyor ve Türkçede fazla mekanik kalıyor.

### B. `lokma`nın aşırı kullanımı

Sorun örnekleri:

- `Bu zar zor bir lokma!`
- `Bu zar zor bir lokma.`
- `Lezzetli küçük bir lokma!`
- `Seni tek lokmada yiyeceğim`

Sorun:

- Yemek bağlamında doğal.
- Ama her küçük yaratık, küçük et parçası veya küçümseme cümlesi `lokma` olunca ton tekdüze ve bazen komik oluyor.

Çeviri ilkesi:

- `dişe dokunmaz`
- `ancak atıştırmalık olur`
- `tek lokmalık`
- `bu mu şimdi`
- `avuç içi kadar`
- `çerezlik`

gibi karşılıklar karaktere göre değişmeli.

### C. Proper noun + Türkçe ek birleşimleri

Örnekler:

- `Pearl'ün`
- `Constant'ın`

Bu alan tamamen yanlış değil, ama telaffuz politikası netleşmeli.

Not:

- `Pearl'ün` yazımı teknik olarak yürür, ama kulağa sert gelebilir.
- `Pearl'in` daha akıcı gelebilir.
- Bu tamamen proje içi standart kararı gerektiriyor.

### D. `science` / `shadow` / `lunar` kümeleri

Bu üçlü DST'nin ana kavram omurgası.

Sorun:

- Bir yerde çok literal.
- Bir yerde çok serbest.
- Bir yerde teknik terim, bir yerde şiirsel imge olarak kullanılıyor.

Öneri:

- Önce bu üçlü için küçük bir sözlük kilitlenmeli.

## 5. Yüksek öncelikli revizyon sırası

1. Büyük sözlük kararı

- The Constant
- Nightmare Fuel
- Pure Horror
- lunar / shadow / fueled / fuel source

2. Proper noun ve adlandırma katmanı

- Pearl
- Wagstaff
- Charlie
- boss/unvan isimleri

3. Karakter sesi katmanı

- Maxwell
- Wathgrithr
- Walter
- Wortox
- Pearl
- Wagstaff

4. Geriye kalan konuşma polish turu

- Özellikle `lokma`, `yakıt`, literal kelime oyunu, düz İngilizce söz dizimi kalıntıları

## 6. Sonraki uygulama için önerdiğim yöntem

Bir sonraki revizyonda şöyle ilerlemek daha sağlıklı:

1. Önce mini sözlük kilitlenir.
2. Sonra bu sözlüğe bağlı isim/malzeme/UI satırları düzeltilir.
3. Ardından karakter karakter ton cilası yapılır.
4. Son aşamada ekran görüntüsüyle gelen istisnalar temizlenir.

Bu sırayı atlayıp tek tek satır düzeltmeye devam edersek:

- aynı terim farklı dosyalarda farklı kalır
- bir karakterde düzelttiğimiz tonu başka yerde yine bozarız
- çeviri her turda biraz daha “eğreti” görünür

## 7. Benim mevcut net kanaatim

Yüksek güvenle söyleyebileceğim üç nokta var:

- `The Constant` büyük ihtimalle çevrilmemeli.
- `Nightmare Fuel` için `yakıt` merkezli yaklaşım fazla düz.
- Satırların önemli bir kısmı kelime hatasından çok karakter sesi ve kavram seviyesi uyumsuzluğundan sırıtmış durumda.

Yani bundan sonraki iş, yalnız “yanlış cümle düzeltme” işi değil; küçük bir terminoloji ve ton standardizasyonu işi.
