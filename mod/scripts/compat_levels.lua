local ipairs = GLOBAL.ipairs
local pcall = GLOBAL.pcall
local print = GLOBAL.print
local rawget = GLOBAL.rawget
local type = GLOBAL.type

local PRESET_KEYS = {
    COMPLETE_DARKNESS = { name = "COMPLETE_DARKNESS", desc = "COMPLETE_DARKNESS" },
    DST_CAVE = { name = "DST_CAVE", desc = "DST_CAVE" },
    DST_CAVE_PLUS = { name = "DST_CAVE_PLUS", desc = "DST_CAVE_PLUS" },
    ENDLESS = { name = "ENDLESS", desc = "ENDLESS" },
    LAVAARENA = { name = "LAVAARENA", desc = "LAVAARENA" },
    LIGHTS_OUT = { name = "LIGHTS_OUT", desc = "LIGHTS_OUT" },
    MOD_MISSING = { name = "MOD_MISSING", desc = "MOD_MISSING" },
    QUAGMIRE = { name = "QUAGMIRE", desc = "QUAGMIRE" },
    RELAXED = { name = "RELAXED", desc = "RELAXED" },
    SURVIVAL_DEFAULT_PLUS = { name = "SURVIVAL_DEFAULT_PLUS", desc = "SURVIVAL_DEFAULT_PLUS" },
    SURVIVAL_TOGETHER = { name = "SURVIVAL_TOGETHER", desc = "SURVIVAL_TOGETHER" },
    SURVIVAL_TOGETHER_CLASSIC = { name = "SURVIVAL_TOGETHER_CLASSIC", desc = "SURVIVAL_TOGETHER_CLASSIC" },
    TERRARIA = { name = "TERRARIA", desc = "TERRARIA" },
    TERRARIA_CAVE = { name = "TERRARIA_CAVE", desc = "TERRARIA_CAVE" },
    WILDERNESS = { name = "WILDERNESS", desc = "WILDERNESS" },
}

local PLAYSTYLE_KEYS = {
    endless = PRESET_KEYS.ENDLESS,
    lightsout = PRESET_KEYS.COMPLETE_DARKNESS,
    relaxed = PRESET_KEYS.RELAXED,
    survival = PRESET_KEYS.SURVIVAL_TOGETHER,
    wilderness = PRESET_KEYS.WILDERNESS,
}

local function GetCustomizationStrings()
    local ui = GLOBAL.STRINGS ~= nil and GLOBAL.STRINGS.UI or nil
    return ui ~= nil and ui.CUSTOMIZATIONSCREEN or nil
end

local function GetLocalizedName(keys)
    local customization = GetCustomizationStrings()
    if customization == nil or type(customization.PRESETLEVELS) ~= "table" or keys == nil then
        return nil
    end

    return customization.PRESETLEVELS[keys.name]
end

local function GetLocalizedDesc(keys)
    local customization = GetCustomizationStrings()
    if customization == nil or type(customization.PRESETLEVELDESC) ~= "table" or keys == nil then
        return nil
    end

    return customization.PRESETLEVELDESC[keys.desc]
end

local function ApplyPresetStrings(data, keys)
    if type(data) ~= "table" or keys == nil then
        return data
    end

    local localized_name = GetLocalizedName(keys)
    if type(localized_name) == "string" and localized_name ~= "" then
        data.name = localized_name
    end

    local localized_desc = GetLocalizedDesc(keys)
    if type(localized_desc) == "string" and localized_desc ~= "" then
        data.desc = localized_desc
    end

    return data
end

local function PatchDataGetter(levels, method_name)
    local old_method = levels[method_name]
    if type(old_method) ~= "function" then
        return
    end

    levels[method_name] = function(id, ...)
        local data = old_method(id, ...)
        return ApplyPresetStrings(data, PRESET_KEYS[id])
    end
end

local function PatchTextGetter(levels, method_name, getter)
    local old_method = levels[method_name]
    if type(old_method) ~= "function" then
        return
    end

    levels[method_name] = function(id, ...)
        local text = old_method(id, ...)
        local localized = getter(PRESET_KEYS[id])
        if type(localized) == "string" and localized ~= "" then
            return localized
        end
        return text
    end
end

local function PatchListGetter(levels, method_name)
    local old_method = levels[method_name]
    if type(old_method) ~= "function" then
        return
    end

    levels[method_name] = function(...)
        local list = old_method(...)
        if type(list) == "table" then
            for _, entry in ipairs(list) do
                if type(entry) == "table" then
                    local localized = GetLocalizedName(PRESET_KEYS[entry.data])
                    if type(localized) == "string" and localized ~= "" then
                        entry.text = localized
                    end
                end
            end
        end
        return list
    end
end

local function PatchPlaystyleGetter(levels)
    local old_method = levels.GetPlaystyleDef
    if type(old_method) ~= "function" then
        return
    end

    levels.GetPlaystyleDef = function(id, ...)
        local data = old_method(id, ...)
        return ApplyPresetStrings(data, PLAYSTYLE_KEYS[id])
    end
end

local function PatchLevelsModule(levels)
    if type(levels) ~= "table" or levels._tt_levels_localized then
        return false
    end

    levels._tt_levels_localized = true

    PatchPlaystyleGetter(levels)

    for _, method_name in ipairs({
        "GetDataForLevelID",
        "GetDataForSettingsID",
        "GetDataForWorldGenID",
        "GetDataForID",
    }) do
        PatchDataGetter(levels, method_name)
    end

    for _, method_name in ipairs({
        "GetNameForLevelID",
        "GetNameForSettingsID",
        "GetNameForWorldGenID",
        "GetNameForID",
    }) do
        PatchTextGetter(levels, method_name, GetLocalizedName)
    end

    for _, method_name in ipairs({
        "GetDescForLevelID",
        "GetDescForSettingsID",
        "GetDescForWorldGenID",
        "GetDescForID",
    }) do
        PatchTextGetter(levels, method_name, GetLocalizedDesc)
    end

    for _, method_name in ipairs({
        "GetLevelList",
        "GetSettingsList",
        "GetWorldGenList",
        "GetList",
    }) do
        PatchListGetter(levels, method_name)
    end

    print("[Turkce Ceviri] Applied level/preset localization compatibility.")
    return true
end

local package_loaded = GLOBAL.package ~= nil and GLOBAL.package.loaded or nil
local function TryPatchLevels()
    if type(package_loaded) ~= "table" then
        return false
    end

    local levels = rawget(package_loaded, "map/levels")
    if type(levels) ~= "table" and type(GLOBAL.require) == "function" then
        local ok, loaded = pcall(GLOBAL.require, "map/levels")
        if ok then
            levels = loaded
        end
    end

    return PatchLevelsModule(levels)
end

if not TryPatchLevels() then
    AddSimPostInit(function()
        TryPatchLevels()
    end)

    AddGamePostInit(function()
        TryPatchLevels()
    end)
end
