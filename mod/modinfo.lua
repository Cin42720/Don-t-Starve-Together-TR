-- Don't Starve Together - Türkçe Çeviri Modu
-- modinfo.lua

name = "Türkçe Çeviri / Turkish Translation"
author = "Cin"
version = "1.0.0 BETA"

local desc = {
    en = [[Complete Turkish translation for Don't Starve Together.]],
    tr = [[Don't Starve Together için kapsamlı Türkçe çeviri.]],
}

description = desc[language] or desc.en

api_version = 10

dst_compatible = true
dont_starve_compatible = false
reign_of_giants_compatible = false
shipwrecked_compatible = false

client_only_mod = false
all_clients_require_mod = false

-- icon_atlas = "modicon.xml"
-- icon = "modicon.tex"
server_filter_tags = {"language", "translation", "turkish", "türkçe"}

priority = -100

configuration_options = {}
