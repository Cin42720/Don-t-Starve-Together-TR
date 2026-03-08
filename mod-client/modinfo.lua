-- Don't Starve Together - Turkish Translation (Client)
-- modinfo.lua

name = "Türkçe Çeviri / Turkish Translation"
author = "Cin"
version = "1.0.0 BETA"

local desc = {
    en = [[Versiyon Beta
Don't Starve Together için istemci tarafı Türkçe çeviri paketi.
En iyi sonuç için server moduyla birlikte kullanın.
]],
    tr = [[Versiyon Beta
Don't Starve Together için istemci tarafı Türkçe çeviri paketi.
En iyi sonuç için server moduyla birlikte kullanın.
]],
}

description = desc[language] or desc.en

api_version = 10

dst_compatible = true
dont_starve_compatible = false
reign_of_giants_compatible = false
shipwrecked_compatible = false

client_only_mod = true
all_clients_require_mod = false

icon_atlas = "modicon.xml"
icon = "modicon.tex"
server_filter_tags = {"language", "translation", "turkish", "türkçe"}

priority = -100

configuration_options = {}
