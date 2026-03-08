-- Don't Starve Together - Turkce Ceviri (Server)
-- modmain.lua

STRINGS = GLOBAL.STRINGS

modimport("scripts/compat_shb_guard.lua")
modimport("scripts/compat_skilltree.lua")
modimport("scripts/languages/tr_stageactor_map.lua")
modimport("scripts/compat_stageactor_cache.lua")

modimport("scripts/languages/tr_ui.lua")
modimport("scripts/languages/tr_yotb.lua")
modimport("scripts/languages/tr_pearl.lua")
modimport("scripts/languages/tr_dialogue_fixes.lua")
modimport("scripts/compat_levels.lua")
modimport("scripts/languages/tr_skin.lua")

GLOBAL.package.loaded["map/customize"] = nil

local function ApplyAllTranslations()
    STRINGS = GLOBAL.STRINGS
    modimport("scripts/languages/tr_speech.lua")
    modimport("scripts/languages/tr_speech_fixes.lua")
    modimport("scripts/languages/tr_speech_polish.lua")
    modimport("scripts/languages/tr_stageactor.lua")
    modimport("scripts/languages/tr_stageactor_map.lua")
    modimport("scripts/compat_stageactor_cache.lua")
    modimport("scripts/languages/tr_skin.lua")
    modimport("scripts/languages/tr_ui.lua")
    modimport("scripts/languages/tr_yotb.lua")
    modimport("scripts/languages/tr_pearl.lua")
    modimport("scripts/languages/tr_dialogue_fixes.lua")
    modimport("scripts/compat_skilltree.lua")
    modimport("scripts/compat_levels.lua")
    GLOBAL.package.loaded["map/customize"] = nil
    print("[Turkce Ceviri - Server] Tum ceviriler uygulandi!")
end

AddSimPostInit(function()
    ApplyAllTranslations()
end)

AddPlayerPostInit(function(inst)
    if inst == GLOBAL.ThePlayer then
        inst:DoTaskInTime(0, function()
            ApplyAllTranslations()
        end)
    end
end)

AddPrefabPostInit("world", function(inst)
    inst:DoTaskInTime(0, function()
        ApplyAllTranslations()
    end)
end)

print("[Turkce Ceviri - Server] 82.000+ metin Turkceye cevrildi!")
