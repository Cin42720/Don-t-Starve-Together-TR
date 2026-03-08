local STRINGS = GLOBAL.STRINGS

STRINGS.NAMES.HERMITCRAB = "Pearl"
STRINGS.NAMES.HERMITHOUSE = "Pearl'ün Evi"

STRINGS.HERMITCRAB_TALK_ONSKINREQUEST = {
    LOW = {"Şimdi ne var?"},
    MED = {"Bunlar umarım öncekilerden iyidir."},
    HIGH = {"Aa! Deneyecek daha çok şey mi var?"},
}

STRINGS.HERMITCRAB_TALK_ONPURCHASE = {
    LOW = {"Güzel. Şimdi beni yalnız bırak."},
    MED = {"Seninle iş yapmak güzeldi."},
    HIGH = {"Başka bir şeye ihtiyacın olursa seslen canım!"},
}

STRINGS.HERMITCRAB_COMPLAIN = {
    PLANT_FLOWERS = {
        LOW = {"Tembel arılar... bir damla bal bile yok..."},
        MED = {"Benim çiçek bahçem varken arılar hep bal yapardı."},
        HIGH = {"Canım, bana biraz çiçek dikmeme...", "yardım eder misin?"},
    },
    REMOVE_JUNK = {
        LOW = {"(Söylenir)... su hep çöple dolu..."},
        MED = {"Su öyle çöple dolu ki balıkları bile göremiyorum!"},
        HIGH = {"Çevik görünüyorsun! Sudaki o çöpleri temizler misin?"},
    },
    PLANT_BERRIES = {
        LOW = {"Bütün meyve çalılarım öldü."},
        MED = {"Bahçemi özlüyorum... Eskiden meyve yetiştirirdim..."},
        HIGH = {"Biraz bahçıvanlıkta bana yardım eder misin?", "Yeni meyve çalılarına ihtiyacım var."},
    },
    FILL_MEATRACKS = {
        LOW = {"Hıh... burada kurutacak et hiç olmuyor..."},
        MED = {"Kurutma raflarım yine mi boş?", "Şu yaşlı pençeler için ne çok iş..."},
        HIGH = {"Benim için biraz et kurutur musun, canım?"},
    },
    GIVE_HEAVY_FISH = {
        LOW = {"(Söylenir)... hep ufak tefek balıklar...", "Şöyle güzel iri bir balık yok..."},
        MED = {"Keşke BİRİ bana kocaman, sulu balıklar getirse..."},
        HIGH = {"Bana iri balıklar getirebilirsen...", "öyle mutlu olurum ki!"},
    },
    REMOVE_LUREPLANT = {
        LOW = {"Şu korkunç bitki...", "Ne kadar da çirkin..."},
        MED = {"O yem bitkisi bütün avlumu ele geçirecek!"},
        HIGH = {"Bir iyilik yapar mısın?", "Şu korkunç bitkiyi benim için hallet."},
    },
    GIVE_UMBRELLA = {
        LOW = {"Berbat yağmur...", "Ölümümü bulacağım..."},
        MED = {"Kabuğumun içine kadar su geçti!", "Keşke bir şemsiyem olsa..."},
        HIGH = {"Ne korkunç hava.", "Sende şemsiye var mı canım?"},
    },
    GIVE_PUFFY_VEST = {
        LOW = {"(Söylenir) Hava buz gibi!"},
        MED = {"Brrr, bu soğuk hava romatizmama çok kötü geliyor."},
        HIGH = {"Ahhh, keşke giyebileceğim sıcak bir şey olsaydı."},
    },
    GIVE_FLOWER_SALAD = {
        LOW = {"Hıh. Etrafta çiçek salatası malzemesi bile yok..."},
        MED = {"Sevgilim eskiden en sevdiğimi yapardı... çiçek salatasını..."},
        HIGH = {"Çiçek salatası ne anılar getiriyor...", "Bana biraz yapar mısın?"},
    },
    GIVE_FISH_WINTER = {
        LOW = {"Hıh. Tam da Ice Bream mevsimi olmalı."},
        MED = {"Eskiden bütün kış Ice Bream yakalardım..."},
        HIGH = {"Canım, bana bir Ice Bream yakalar mısın?"},
    },
    GIVE_FISH_SUMMER = {
        LOW = {"Scorching Sunfish şimdi göç ediyor olmalı."},
        MED = {"Yaz deyince aklıma Scorching Sunfish gelir..."},
        HIGH = {"Eğer varsa, bir Scorching Sunfish'i çok isterim."},
    },
    GIVE_FISH_SPRING = {
        LOW = {"Dün birkaç Bloomfin Tuna gördüm sanmıştım..."},
        MED = {"Bu hava Bloomfin Tuna için kusursuz..."},
        HIGH = {"Bir Bloomfin Tuna yakalarsan bana haber ver, canım!"},
    },
    GIVE_FISH_AUTUM = {
        LOW = {"Sanırım Fallounder mevsimi geldi."},
        MED = {"Sonbahar deyince akla nefis bir Fallounder gelir..."},
        HIGH = {"Bana bir Fallounder getirir misin, canım?"},
    },
    MAKE_CHAIR = {
        LOW = {"(Söylenir) kabuğum beni öldürüyor...", "Buralarda oturacak yer de yok..."},
        MED = {"Eski kabuğumu dinlendirecek bir yer de yok..."},
        HIGH = {"Buranın gerçekten ihtiyacı olan şey oturup sohbet edilebilecek güzel bir yer."},
    },
}

STRINGS.HERMITCRAB_INVESTIGATE = {
    PLANT_FLOWERS = {
        LOW = {"Hı? Ne yapıyorsun?"},
        MED = {"Hm... bunlar hoş duruyor."},
        HIGH = {"Ne kadar güzel!"},
    },
    PLANT_BERRIES = {
        LOW = {"Eh. En azından işe yarar bir şey yapıyorsun."},
        MED = {"Belki şuraya bir tane daha?"},
        HIGH = {"Bahçıvanlıkta bir harikasın, canım!"},
    },
    FILL_MEATRACKS = {
        LOW = {"Artık istemiyor musun? Bozuldu mu yoksa?"},
        MED = {"Bedava ete asla hayır demem!"},
        HIGH = {"Hoo-hoo! İşte bu, nefis bir kuru et olacak!"},
    },
    REMOVE_LUREPLANT = {
        LOW = {"Harika. Eski baş belamı yeni baş belam temizledi."},
        MED = {"Eh, buna sevindim."},
        HIGH = {"Şu korkunç bitkiye gününü gösterdin!"},
    },
    MAKE_UNCOMFORTABLE_CHAIR = {
        LOW = {"Benim o sallanan şeyin üstüne oturmamı mı bekliyorsun?"},
        MED = {"Bu sandalye mi, yoksa ters gitmiş bir sanat projesi mi?"},
        HIGH = {"Ah. Şey... Üzerinde çok uğraştığın belli, canım!"},
    },
    GIVE_CARPENTRY_BLUEPRINT = {
        LOW = {"Al. Doğru dürüst bir sandalye yapmayı öğren."},
        MED = {"Denemene puan veririm ama bir dahakine düzgün yap."},
        HIGH = {"Al, sana birkaç püf noktası vereyim."},
    },
    CARPENTRY_BLUEPRINT_ONGROUND = {
        LOW = {"Hıh. Planımı yerde öylece bırakmışsın...", "Nankör veletler!"},
        MED = {"Yere atılacağını bilseydim,", "o planı sana hiç vermezdim!"},
        HIGH = {"Şuradaki benim planım değil mi?"},
    },
    CARPENTRY_BLUEPRINT_ININVENTORY = {
        LOW = {"Beni rahat bırak, planımı zaten verdim!"},
        MED = {"O planı hâlâ okuyamadın mı, hı?"},
        HIGH = {"O planı okumaya fırsat bulabildin mi, canım?"},
    },
    ALREADY_KNOWS_CARPENTRY = {
        LOW = {"Sana planımı zaten verdim, dırdır etmeyi bırak!"},
        MED = {"Planımı sana zaten vermemiş miydim?", "Tatlı yaşlı bir kadından faydalanmaya mı çalışıyorsun?"},
        HIGH = {"Sana öğretebileceğim her şeyi zaten biliyorsun, canım."},
    },
    MAKE_CHAIR = {
        LOW = {"Hıh. En azından dağılacak gibi durmuyor."},
        MED = {"Seni bir marangoz sanmazdım, hele yarım yamalak da olsa becerikli bir marangoz hiç!"},
        HIGH = {"Çok hoş olmuş canım! Ağrıyan kabuğumu dinlendirmek için kusursuz."},
    },
}

STRINGS.HERMITCRAB_GREETING = {
    [0] = {"Git başımdan!", "Hadi, şut!", "Beni yalnız bırak!", "Girmek yasak!", "Sahilimden çekil!"},
    [1] = {"Hıh.", "Git de başka birini rahatsız et!"},
    [2] = {"Burada ne yapıyorsun?", "Ne istiyorsun?"},
    [3] = {"Yine mi geldin?", "Yapacak daha iyi bir işin yok mu?", "Baş belası velet..."},
    [4] = {{"Oldukça ısrarcısın.", "Bunu kabul ederim."}, "Hıh. Yeter ki başıma bela olma."},
    [5] = {"Demek pırıltılı kişiliğime doyamıyorsun, ha?", {"Şu gelen de kimmiş... hm...", "Adın neydi senin?"}},
    [6] = {"Neden bana yardım ediyorsun?"},
    [7] = {"Bu eski yeri tek başıma çekip çevirmek zor oldu.", "Ziyaretçilerin ne kadar iyi geldiğini unutmuşum.", "Sana epey sert davrandım, değil mi?"},
    [8] = {"Yine merhaba!", "Bak sen... gelen de %s!"},
    [9] = {"Seni görmek ne güzel, canım!", {"Bu dünya türlü tehlikeyle dolu...", "Dışarıda dikkatli ol, tamam mı?"}},
    [10] = {"Nasıl gidiyor canım?", "Bak sen, en sevdiğim ziyaretçi gelmiş!", "Yeterince yemek yiyor musun?"},
}

STRINGS.HERMITCRAB_DEFAULT_REWARD = {
    LOW = {"Demek bana yardım ettiğin için bir şey istiyorsun ha?", "Peki."},
    MED = {"Galiba etrafta olman o kadar da kötü değil."},
    HIGH = {"Ne büyük yardım! Teşekkür ederim."},
}

STRINGS.HERMITCRAB_GROUP_REWARD = {
    LOW = {"Ne çevirdiğini bilmiyorum", "ama bana borç çıkardığını sanma!"},
    MED = {"Meşgulmüşsün! Sanırım karşılığını vermeliyim."},
    HIGH = {"Harika iş çıkardın!", "Al, yapabileceğimin en azı bu."},
}

STRINGS.HERMITCRAB_INTRODUCE = {"Benim için çok şey yaptın.", "Bana Pearl de, olur mu?"}

STRINGS.HERMITCRAB_REWARD = {
    FIX_HOUSE_1 = {
        LOW = {"İyi, en azından evimi tamamen mahvetmedin."},
        MED = {"Bir süredir burayı toparlamayı düşünüyordum..."},
        HIGH = {"Aman tanrım, yepyeni gibi olmuş!"},
    },
    FIX_HOUSE_2 = {
        LOW = {"...Sanırım bu bir gelişme."},
        MED = {"Bunu... benim için mi yaptın...?"},
        HIGH = {"Ah canım, bu yere yaptıklarına bayıldım!"},
    },
    FIX_HOUSE_3 = {
        LOW = {"Aa. Evet, biraz daha iyi görünüyor."},
        MED = {"Burayı zor tanıdım!", "Aman öyle endişeli bakma, bu iyi bir şey."},
        HIGH = {"Ah, harika olmuş!", "Kendimi sarayındaki bir kraliçe gibi hissediyorum", "Hoo-hoo!"},
    },
    PLANT_FLOWERS = {
        LOW = {"Eh, en azından arılarım şimdi mutlu."},
        MED = {"Arılarım heyecandan vızıldıyor!"},
        HIGH = {"Arılarım yıllardır bu kadar mutlu görünmemişti!"},
    },
    REMOVE_JUNK = {
        LOW = {"Hıh. Epey uzun sürdü."},
        MED = {"Bunca çöp gidince balık tutmak daha kolay olacak!"},
        HIGH = {"Ahhh...", "O çöplerin gitmesi içimi öyle rahatlattı ki."},
    },
    PLANT_BERRIES = {
        LOW = {"Biraz daha düzgün sıralara dikebilirdin...", "Ama idare eder sanırım."},
        MED = {"Taze meyve yemeyeli ne kadar oldu hatırlamıyorum!"},
        HIGH = {"Ayy, ne düşünceli bir genç veletsin!", "Gel yanaklarını sıkayım!"},
    },
    FILL_MEATRACKS = {
        LOW = {"Tahmin edeyim, karşılığında bir şey istiyorsun? Peki..."},
        MED = {"Sağ ol... ama bunun arkadaş olduğumuz anlamına geldiğini sanma!"},
        HIGH = {"Umarım sana fazla zahmet olmamıştır..."},
    },
    GIVE_HEAVY_FISH = {
        LOW = {"Bunu bana niye veriyorsun?", "Dur, almayacağımı da söylemedim ya!"},
        MED = {"Aaa, ne iri bir balık yığını bu!"},
        HIGH = {"Hoo-hoo!", "Bunlar gerçekten etkileyici balıklar, canım!"},
    },
    REMOVE_LUREPLANT = {
        LOW = {"Bunun için ödül falan hak ettiğini mi sanıyorsun?", "Hıh."},
        MED = {"En azından yarım yamalak da olsa yabani ot temizliyorsun."},
        HIGH = {"Oh, ne rahatlık!", "Şu bitki bir süredir bana yan gözle bakıyordu."},
    },
    GIVE_UMBRELLA = {
        LOW = {"Sanırım bu iş görür."},
        MED = {"Neden bana karşı bu kadar iyisin?"},
        HIGH = {"Sensiz ne yapardım, canım?"},
    },
    GIVE_PUFFY_VEST = {
        LOW = {"Hıh. En azından donarak ölmeyeceğim."},
        MED = {"Bu... gerçekten çok nazikçe."},
        HIGH = {"Ah canım, ne kadar düşüncelisin!"},
    },
    GIVE_FLOWER_SALAD = {
        LOW = {"..."},
        MED = {"...Teşekkür ederim. Çok uzun zaman olmuş."},
        HIGH = {"Teşekkür ederim canım...", "Yolculuklarında başka yengeçlere rastladın mı?"},
    },
    GIVE_FLOWER_SALAD_POST_RELOCATION = {"Teşekkür ederim canım, eskiden bu çiçek salatasını çok severdim."},
    GIVE_FISH_WINTER = {
        LOW = {"Hıh. Bunu şu oltayla daha hızlı yakalayabilirdin."},
        MED = {"Ah... sağ ol. Al, zahmetin için bunu götür."},
        HIGH = {"Teşekkür ederim canım! Al, şunlardan bir tane al sen de."},
    },
    GIVE_FISH_SUMMER = {
        LOW = {"Hıh. Bunu şu oltayla daha hızlı yakalayabilirdin."},
        MED = {"Ah... sağ ol. Al, zahmetin için bunu götür."},
        HIGH = {"Teşekkür ederim canım! Al, şunlardan bir tane al sen de."},
    },
    GIVE_FISH_SPRING = {
        LOW = {"Hıh. Bunu şu oltayla daha hızlı yakalayabilirdin."},
        MED = {"Ah... sağ ol. Al, zahmetin için bunu götür."},
        HIGH = {"Teşekkür ederim canım! Al, şunlardan bir tane al sen de."},
    },
    GIVE_FISH_AUTUM = {
        LOW = {"Hıh. Bunu şu oltayla daha hızlı yakalayabilirdin."},
        MED = {"Ah... sağ ol. Al, zahmetin için bunu götür."},
        HIGH = {"Teşekkür ederim canım! Al, şunlardan bir tane al sen de."},
    },
    MAKE_CHAIR = {
        LOW = {"Hıh. En azından dağılacak gibi durmuyor."},
        MED = {"Seni bir marangoz sanmazdım, hele yarım yamalak da olsa becerikli bir marangoz hiç!"},
        HIGH = {"Çok hoş olmuş canım! Ağrıyan kabuğumu dinlendirmek için kusursuz."},
    },
}

STRINGS.HERMITCRAB_STORE_UNLOCK_1 = {"Demek takas etmek istiyorsun?", "Yoksa vaktimi mi boşa harcıyorsun?"}
STRINGS.HERMITCRAB_STORE_UNLOCK_2 = {"Belki takas edecek birkaç yemim vardır...", "tabii karşılayabiliyorsan."}
STRINGS.HERMITCRAB_STORE_UNLOCK_3 = {"Peki, kolumu büktün.", "Sana İYİ yemlerimi göstereceğim."}
STRINGS.HERMITCRAB_STORE_UNLOCK_4 = {"Takas için yeni şeylerim var,", "ama ucuz değiller!"}
STRINGS.HERMITCRAB_STORE_UNLOCK_5 = {"Bu yaşlı kabuk yumuşuyor olmalı...", "dükkâna özel bir şey koydum."}

STRINGS.HERMITCRAB_PLANTED_LUREPLANT_DIED = {
    LOW = {"Güzel deneme.\nKendi pisliğini temizlediğin için bir şey kazanamazsın."},
    MED = {"Ödülü bu kadar mı istiyorsun?"},
    HIGH = {"Canım, onu senin diktiğini biliyorum.\nBeni etkilemene gerek yok."},
}

STRINGS.HERMITCRAB_GO_HOME = {"Eski kabuğumu biraz dinlendireyim."}
STRINGS.HERMITCRAB_PANIC = {"Hiçbir şey göremiyorum!"}
STRINGS.HERMITCRAB_PANICHAUNT = {"Beni daha şimdi alamazsınız, ruhlar!"}
STRINGS.HERMITCRAB_PANICFIRE = {"Aaah! Izgara olmayacağım!"}
STRINGS.HERMITCRAB_FIGHT = {{"Seni serseri!", "Benim gibi tatlı, masum yaşlı bir hanıma zorbalık mı yapıyorsun!"}}

STRINGS.HERMITCRAB_ATTEMPT_TRADE = {
    LOW = {"Takas edecek bir şeyin yoksa benimle konuşma."},
    MED = {"Bugün takas edecek bir şeyin var mı?"},
    HIGH = {"En sevdiğim müşterim!", "Bugün ne lazım canım?"},
}

STRINGS.HERMITCRAB_GETFISH_BIG = {"İşte buna düzgün boy balık derim!"}

STRINGS.HERMITCRAB_REFUSE_SMALL_FISH = {
    "Buna mı etkileyici diyorsun, {weight}?\nBu ne, minnacık bir balık mı?",
    "Vay canına, {weight}...\nHayatımda bu kadar küçük balık yakalamadım.",
    "Sadece {weight} mi?\nBunu geri salmalıydın.",
}

STRINGS.HERMITCRAB_REFUSE_SALAD = {"Bunu şimdi istemiyorum...", "beni fazla hüzünlendiriyor..."}
STRINGS.HERMITCRAB_REFUSE_ICE_HOT = {"Saçmalama, burası zaten buz gibi!"}
STRINGS.HERMITCRAB_REFUSE_ICE_HAD = {"Daha fazla buza ihtiyacım yok."}
STRINGS.HERMITCRAB_REFUSE_UMBRELLA = {"Yağmur bile yağmıyor..."}
STRINGS.HERMITCRAB_REFUSE_UMBRELLA_HASONE = {"Kendi şemsiyem gayet yeter, teşekkür ederim."}
STRINGS.HERMITCRAB_REFUSE_COAT = {"Sen tut onu, üşümüyorum."}
STRINGS.HERMITCRAB_REFUSE_COAT_HASONE = {"Üstümdeki paltoyu beğeniyorum, çok teşekkür ederim."}
STRINGS.HERMITCRAB_REFUSE_VEST = {"Bunu bu sıcakta giyersem haşlanırım!"}
STRINGS.HERMITCRAB_REFUSE_MAPSCROLL = {"Buna ihtiyacım yok, evim burada!"}

STRINGS.HERMITCRAB_ANNOUNCE_ROYALTY = {
    "Vay, pek bir asil ve görkemli görünüyorsun.",
    "Ben de kendimi \"soyluluğun\" huzurunda sanmıyordum doğrusu.",
    "Beni etkilemek için kibirli bir şapkadan fazlası gerekir.",
}

STRINGS.HERMITCRAB_ANNOUNCE_OCEANFISHING_LINESNAP = {"Aah! Aptal şey!"}

STRINGS.HERMITCRAB_ANNOUNCE_OCEANFISHING_IDLE_QUOTE = {
    "Hıh. Balıklar bugün yemlenmiyor...",
    "Bu kadar nazlanmayın da kancama gelin!",
    "\"Sık sık en yüksek tepeden bakarım ki kayıkçımı göreyim...\"",
    "Hım-dı-dım...",
    "Bir türlü bir şey yakalayamıyorum...",
}

STRINGS.HERMITCRAB_ANNOUNCE_OCEANFISHING_LINETOOLOOSE = {"Ahh, şu yorgun yaşlı pençeler!"}
STRINGS.HERMITCRAB_ANNOUNCE_OCEANFISHING_BADCAST = {"Eskisi kadar iyi değilim galiba..."}
STRINGS.HERMITCRAB_ANNOUNCE_OCEANFISHING_GOTAWAY = {"Seni kaygan küçük sersem!", "Kancama geri dön!"}

STRINGS.HERMITCRAB_ANNOUNCE_OCEANFISHING_BOTHERED = {
    LOW = {"Aah! Balığımı kaçırttın!"},
    MED = {"Daha iyi bir zamanı bekleyemez miydin?"},
    HIGH = {"Senin için her zaman vakit ayırırım, canım."},
}

STRINGS.HERMITCRAB_ANNOUNCE_ADDED_RELOCATION_KIT = {
    LOW = {"Hıh! Beni kandırdın! Bu ada berbat!", "Bunu düzeltmek zorundasın...", "...yoksa o hurda toplayıcısından farkın kalmaz!", "Sana işine yarayacak bir şey vereceğim, gerçekten yardım etmeyi düşünüyorsan."},
    MED = {"Aah! Bu harita işe yaramadı.", "Belki o hurda toplayıcısı seni de kandırmıştır.", "Yaşayacak daha iyi bir yere ihtiyacım var.", "Bana yardım etmene yardım edecek bir şeyim var."},
    HIGH = {"Ah canım, o hurda toplayıcısı bizi kötü bir haritayla kandırmış.", "Bana daha iyi bir yuva bulmama yardım eder misin?", "Sana bana yardım etmeni kolaylaştıracak küçük bir şey vereceğim!"},
}

STRINGS.HERMITCRAB_LEVEL10_PLAYERGOOD = {"Seni iyi görmek güzel, canım."}
STRINGS.HERMITCRAB_LEVEL10_LOWHEALTH = {{"Aman tanrım, sana ne oldu?", "Daha dikkatli olmalısın!"}}
STRINGS.HERMITCRAB_LEVEL10_LOWSANITY = {{"Bir şey canını sıkıyor gibi görünüyorsun.", "Her şey yolunda mı canım?"}}
STRINGS.HERMITCRAB_LEVEL10_LOWHUNGER = {{"Hıh... zayıf görünüyorsun.", "Doğru dürüst yemek yiyor musun?"}}

STRINGS.HERMITCRAB_THROWBOTTLE = {
    LOW = {"Şişelerimi toplayıp duruyorsun!", "Şimdi iki kat fazlasını göndermem gerekecek!"},
    MED = {"Sanırım birilerine ulaşmalarına seviniyorum, hepsi bu."},
    HIGH = {"Belki ona ulaşacak olan şişe budur..."},
}

STRINGS.HERMITCRAB_THROWBOTTLE_POST_RELOCATION = {"Umarım bunu yolculuklarında bulur ve ziyaretime geri gelirsin, canım!"}

STRINGS.HERMITCRAB_HARVESTMEAT = {
    LOW = {"Hıh... biraz lifli görünüyor."},
    MED = {"Hm... fena görünmüyor."},
    HIGH = {"Aaa, şöyle lezzetli kuru etlere bayılırım!"},
}

STRINGS.HERMITCRAB_MOON_FISSURE_VENT = {
    LOW = {"Şu lanet yarıkları kapatmam sonsuza dek sürdü...", "Onlarla oynayıp durma!"},
    MED = {"En güzel bahçe süsleri sayılmazlar ama insanın kafasını açık tutuyorlar."},
    HIGH = {"Oraya yerleşene kadar o tuhaf musallatları fark etmemiştim.", "Berbat şeylerdi, kabuğumu ürpertiyorlardı...", "Birimiz gidecekti, o da ben olmayacaktım!"},
}

STRINGS.HERMITCRAB_GOT_PEARL = {"Ah...", "...sanırım artık anlıyorum.", "Bunu bana geri getirdiğin için teşekkür ederim.", "İyi ki bana dönüp durdun.", "Dostum.", "Minnetimin küçük bir göstergesi olarak sana özel yapımımı paylaşmak istiyorum."}
STRINGS.HERMITCRAB_WANT_HOUSE = {"Evimi toparlamak için biraz yardıma gerçekten ihtiyacım var..."}
STRINGS.HERMITCRAB_GIVE_PEARL = {"Yolculuklarında sevgilime rastlarsan...", "Şunu... bu inciyi ona verir misin?", "Tanıyacaktır."}
STRINGS.HERMITCRAB_GOT_MAPSCROLL_BAD = {"Bu harita bana göre değil.", "Beni özel bir yere götürmüyor."}
STRINGS.HERMITCRAB_GOT_MAPSCROLL_GOOD = {"Bu haritadaki ada güzel görünüyor...", "En azından o hurda toplayıcısından uzak.", "Giderdim ama...", "Hayır. Gideceğim.", "Onu beklemekten bıktım."}
STRINGS.HERMITCRAB_ANNOUNCE_SPOOKED = "Bunu gördün mü?!"
STRINGS.HERMITCRAB_ANNOUNCE_TOOL_SLIP = "Vay be, o alet çok kaygan!"

STRINGS.HERMITCRAB_ANNOUNCE_GOING_TEASHOP = {
    "Sabret biraz canım!",
    "Bir dakikaya oradayım.",
    "Sabırlı ol canım. Geliyorum.",
}

STRINGS.HERMITCRAB_TEASHOP_IDLE = {
    "Benim demlediğim çayın üstüne yok.",
    "Susamış görünüyorsun canım!",
    "Pearl'ün Çay Dükkanı'na hoş geldin.",
    "Merhaba canım. Ne istersin?",
    "En sevdiğin çay hangisi?",
    "Benim çayımdan ister misin?",
}

STRINGS.HERMITCRAB_TEASHOP_TRADE = {
    "Harika bir gün geçir!",
    "Buyur bakalım.",
    "Afiyet olsun canım!",
    "Umarım beğenirsin!",
    "Senin için özel demlendi, canım!",
}

STRINGS.HERMITCRAB_ANNOUNCE_LEFT_TEASHOP = {
    "Arkadaşlarına da uğramalarını söyle canım!",
    "Ziyaretin için teşekkür ederim!",
    "Yine gel canım!",
}

STRINGS.HERMITCRAB_TEASHOP_HIT = {
    "Neden öyle yapıyorsun canım?",
    "Dükkânımı taşımama yardım mı ediyorsun?",
    "Dikkat et canım!",
}

STRINGS.HERMITCRAB_TEASHOP_BURN = {
    "Dükkânım yanıyor!",
    "Aman, bu tam bir felaket!",
    "Neden?!",
}

STRINGS.HERMITCRAB_TEASHOP_PLAYER_BURN = {
    "Aman canım! Ne yaptın sen?",
    "Bunu neden yaptın canım?",
    "Aman hayır! Dükkânımı yaktın!",
}

STRINGS.HERMITCRAB_DECOR_PRAISES = {
    "Canım benim! Yerime yaptıklarına bayıldım!",
    "Teşekkür ederim canım! Artık gerçekten ev gibi hissettiriyor!",
    "Amanın, dekorasyondan gerçekten anlıyorsun!",
    "Canım, başardın! Evim harika görünüyor!",
    "Bayıldım canım! Yardımın için teşekkür ederim!",
    "Ah canım, burası gerçekten sıcacık bir yuvaya dönüştü! Teşekkür ederim.",
    "Evimi ne kadar güzel süsledin canım!",
}

STRINGS.HERMITCRAB_DECOR_ALL_TROPHY_FISH = {
    "Bunların hepsini nasıl yakaladın? İnanılmaz, canım!",
    "Artık bütün balıklara sahibim canım! Muhteşem!",
    "Koleksiyonum tamamlandı! Sen en iyisisin canım!",
    "Ne olağanüstü bir başarı! Hepsini yakaladın canım!",
}

STRINGS.HERMITCRAB_DECOR_CONTENT = {
    TILES = {"Bu benim kendi sahilim! Bayıldım canım!", "Teşekkür ederim canım. Sahili ayağıma getirdin!", "Mükemmel canım! Sahildeki evim gibi oldu!"},
    ORNAMENTS = {"Harika! Rüzgârda salınışlarına bayıldım.", "Muhteşemler canım.", "Kesinlikle çok güzeller canım."},
    DECORATION_TAKER = {"Harika masalar için teşekkür ederim canım.", "Benim için yaptığın bu güzel masalara bayıldım canım."},
    FACED_CHAIR = {"Artık bu sandalyelerden birine oturup bacaklarımı dinlendirebilir ve bir fincan çayın tadını çıkarabilirim!", "Ziyarete geldiğinde oturman için artık sandalyelerim var!"},
    POTTED_PLANTS = {"Bu saksı bitkileri çok güzel canım.", "Bu saksı bitkilerine bayıldım. Teşekkür ederim canım."},
    DOCK_POSTS = {"İskele kazıkları gerçekten harika canım!", "İskele kazıklarıma bayıldım canım!"},
    PICKABLE_PLANTS = {"Her yer ne kadar canlı görünüyor!", "Canım, gerçekten yeşil ellisin!", "İhtiyacım olan her bitki pençemin ucunda! Ne kadar düşüncelisin canım."},
    LIGHT_POSTS = {"Evim artık ne kadar aydınlık ve güzel!", "Bütün bu ışıklar ortamı gerçekten canlandırıyor!", "Işıklar öyle sıcak ve rahat bir parıltı veriyor ki. Mükemmel."},
    MEAT_RACKS = {"Yeni kurutma raflarıma bayıldım!", "Teşekkür ederim canım! Artık kurutacak çok yerim var!", "Artık bir daha kurutma alanım tükenmeyecek!"},
    FLOWERS = {"Ah canım, benim için diktiğin bütün çiçeklere bayıldım!", "Bahçem sayende güzel çiçeklerle doldu canım!", "Bütün bu çiçekler beni çok mutlu ediyor! Teşekkür ederim canım."},
    BEE_BOXES = {"Bütün arı kovanları için teşekkür ederim canım!", "Arılarım yeni evlerine bayıldı! Teşekkür ederim canım!", "Bunca arı kovanı! Artık çayım için bolca balım olacak!"},
    WATER_TREE = {"Benim için ne harika bir ağaç diktin canım!", "Ağacıma bayıldım canım! Beni sıcak güneşten ve soğuk yağmurdan koruyor!", "Benim için bu güzel ağacı diktiğin için teşekkür ederim canım."},
    CRITTER_PET = {"Şirkete pek alışık değilim canım... sen hariç, şimdi bir de bu tatlı minik şey hariç.", "Bana bu kusursuz küçük dostu getirdiğin için teşekkür ederim canım."},
    HOT_SPRING = {"Artık içine girip biraz keyif yapabilir, şu yaşlı kabuğumu dinlendirebilirim.", "Ne güzel bir sıcak kaynak olmuş canım! Ne zaman istersen gel, keyif yap.", "Bu harika sıcak kaynak için teşekkür ederim canım."},
    TEA_SHOP = {"Aman canım! Bütün farklı çaylarımı tatmanı sabırsızlıkla bekliyorum!", "Sonunda Pearl'ün Çay Dükkanı hizmete açılabilir!", "Çay dükkânımı kurmama yardım ettiğin için teşekkür ederim canım."},
}

STRINGS.HERMITCRAB_CRITTER_BANTER = {
    "Merhaba, kıymetli minik şey.",
    "Sen dünyanın en tatlısı değil misin?",
    "Ne kadar da tatlı küçücük bir şeysin sen.",
    "Aşırı tatlısın!",
    "Sana çok iyi bakacağım.",
    "Beni çok mutlu ediyorsun!",
    "Awww...",
}

STRINGS.HERMITCRAB_CRITTER_FEED = {
    "Acıkmış olmalısın!",
    "Hadi ye bakalım, tatlım.",
    "Nefis değil mi?",
}

STRINGS.HERMITCRAB_DECOR_COMPLAIN_AREA = {
    MOON_ISLAND = {"Bu yer bana fena baş ağrısı yapıyor!", "Şu tuhaf küçük musallatlar burada her yerde!", "Bana yaşayacak yeni bir yer bulmama yardım et canım.", "Ah canım. Buradan hiç hoşlanmıyorum. Lütfen taşınmama yardım et!"},
}

STRINGS.HERMITCRAB_DECOR_COMPLAIN = {
    FLOWERS = {
        LOW = {"Çiçeklerimi gerçekten özlüyorum canım. Benim için biraz diker misin?", "Birkaç çiçek evimi çok daha güzel yapardı. Bana biraz diker misin canım?"},
        MED = {"Diktiğin çiçeklere bayıldım canım. Birkaç tane daha harika olur.", "Sadece birkaç çiçek daha olsa tam olacak canım."},
    },
    BEE_BOXES = {
        LOW = {"Arılarımın yaşayacak daha fazla eve ihtiyacı var. Onlara birkaç tane yapar mısın canım?", "Canım, arılarım için daha fazla eve ihtiyacım var. Lütfen yardım et!"},
        MED = {"Arılarım evlerini seviyor ama birkaç tane daha çok iyi olur canım!", "Canım, arılarım için birkaç ev daha yapar mısın?"},
    },
    TILES = {
        LOW = {"Canım, sahili çok özledim. Burası ona hiç benzemiyor.", "Buraya aitmişim gibi hissetmiyorum. Keşke biraz daha sahil gibi olsa."},
        MED = {"Burası sahil gibi hissettirmeye başladı ama biraz daha gerek sanki canım.", "Ah canım, benim sahilim gibi hissettirmesi için biraz daha lazım."},
    },
    FISHING_MARKERS = {
        LOW = {"Balık tutmak için daha çok yerim var ama birkaç noktaya hâlâ ulaşamıyorum canım.", "Canım, sevdiğim birkaç balık tutma noktasına daha ulaşamıyorum."},
        MED = {"Daha iyi ama hâlâ daha çok balık tutma noktasına ihtiyacım var!", "Sevdiğim balık noktalarının yarısına ulaşamıyorum canım."},
        HIGH = {"Canım, balık tutacak hiç yerim kalmadı!", "Balık tutacak hiçbir yerim yok! Lütfen yardım et canım!"},
    },
    TROPHY_FISH = {
        LOW = {"Sergilemek için daha çok iri balık isterdim!", "Birkaç iri balık daha harika olur canım!"},
    },
    ORNAMENTS = {
        LOW = {"Bu rüzgâr süslerine bayıldım. Birkaç tane daha olabilir mi?", "Canım, bu rüzgâr süsleri çok güzel! Biraz daha, lütfen!"},
        MED = {"Bir ya da iki rüzgâr süsü daha yeterli olur!", "Neredeyse yeterince rüzgâr süsümüz oldu canım!"},
    },
    DECORATION_TAKER = {
        LOW = {"Canım, bana birkaç masa yapar mısın lütfen?", "Evim için birkaç masaya ihtiyacım var canım!"},
        MED = {"Masalar için teşekkür ederim ama birkaç tane daha olsa çok iyi olur.", "Birkaç masa daha tam yerinde olur canım!"},
    },
    POTTED_PLANTS = {
        LOW = {"Canım, bitkilerim için bana birkaç saksı yapar mısın lütfen?", "Bitkilerim için birkaç saksım olsa çok sevinirim canım!"},
        MED = {"Bu saksılar harika ama birkaç tane daha olsa çok iyi olur.", "Bitkilerim için birkaç saksı daha yeterli olur canım."},
    },
    DOCK_POSTS = {
        LOW = {"Canım, benim için biraz iskele kazığı yapar mısın lütfen?"},
        MED = {"Yaptığın iskele kazıklarına bayıldım canım. Birkaç tane daha ne güzel olurdu!", "Birkaç iskele kazığı daha olsa ne hoş olur canım!"},
    },
    FACED_CHAIR = {
        LOW = {"Oturacak hiçbir yer yok canım! Bana birkaç sandalye yapmama yardım et lütfen.", "Evim için birkaç sandalye olsa çok iyi olur canım."},
        MED = {"Yaptığın sandalyeler çok güzel canım. Birkaç tane daha harika olur.", "Bana birkaç sandalye daha yapar mısın canım?"},
    },
    PICKABLE_PLANTS = {
        LOW = {"Bundan daha fazla bitkiye ihtiyacımız olacak canım.", "Biraz daha bitki ne hoş olurdu canım!"},
        MED = {"Bütün bu bitkilere bayıldım! Belki bir iki tane daha?", "Neredeyse mükemmel canım! Sadece birkaç bitki daha!"},
    },
    LIGHT_POSTS = {
        LOW = {"Burada hâlâ biraz fazla loş canım!", "Biraz daha ışık çok güzel olur canım."},
        MED = {"Işıklar çok hoş! Bir iki tane daha yeterli olur.", "Canım, biraz daha ışık lütfen!"},
    },
    MEAT_RACKS = {
        LOW = {"Canım, bana birkaç büyük kurutma rafı yapar mısın lütfen?", "Birkaç kurutma rafı daha olsa çok sevinirim canım."},
        MED = {"Harika! Belki bir iki büyük kurutma rafı daha, canım?", "Az kaldı canım! Sadece bir iki büyük kurutma rafı daha!"},
    },
    SPAWNER = {
        LOW = {"Şu yaratıkların saklanacak yalnızca birkaç yeri daha kaldı!", "Canım, birkaç kötü komşudan daha kurtulmama yardım eder misin lütfen?"},
        MED = {"Yaratıkların saklanabileceği hâlâ bir sürü yer var!", "Hâlâ pek çok sevimsiz komşum var. Lütfen yardım et canım!"},
        HIGH = {"Ah canım, burada yaratıkların çıktığı ne çok yer var!", "Yaratıklar burada her yönden geliyor! Lütfen buraları onlar yüzünden temizle canım!"},
    },
    JUNK = {
        LOW = {"Evim neredeyse çöpten arındı! Sadece birkaç parça kaldı.", "Neredeyse bitti! Biraz daha çöp temizlememe yardım eder misin canım?"},
        MED = {"Yerim hâlâ biraz çöple dolu. Temizlememe yardım eder misin lütfen?", "Canım benim, etraftaki çöpleri temizlememde bana yardım edersen çok minnettar olurum."},
        HIGH = {"Canım, evimin etrafı çöple sarılmış! Temizlememe yardım eder misin lütfen?", "Her yer çöp dolu! Temizlemek için yardımına ihtiyacım var canım!"},
    },
}
