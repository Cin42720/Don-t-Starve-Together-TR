local GLOBAL = GLOBAL
local STRINGS = GLOBAL.STRINGS
local require = GLOBAL.require
local package_loaded = GLOBAL.package.loaded
local pcall = GLOBAL.pcall or pcall
local type = GLOBAL.type or type
local pairs = GLOBAL.pairs or pairs
local ipairs = GLOBAL.ipairs or ipairs
local next = GLOBAL.next or next
local rawget = GLOBAL.rawget or rawget
local rawset = GLOBAL.rawset or rawset
local tostring = GLOBAL.tostring or tostring
local STATE_KEY = "__tt_stageactor_cache_state"

local PLAY_MODULE_BY_PREFAB = {
    playbill_the_doll = "play_the_doll",
    playbill_the_veil = "play_the_veil",
    playbill_the_vault = "play_the_vault",
    playbill_the_princess_yoth = "play_the_princess_yoth",
}
local GENERAL_SCRIPT_MODULE = "play_generalscripts"
local PLAYBILL_CAST_LABEL = "Kadro:"
local PLAYBILL_TITLE_FALLBACKS = {
    ["Act 1 - Scene 1"] = "Perde 1 - Sahne 1",
    ["Act 1 - Scene 2"] = "Perde 1 - Sahne 2",
    ["Act 1 - Scene 3"] = "Perde 1 - Sahne 3",
    ["Act 2 - Scene 1"] = "Perde 2 - Sahne 1",
    ["Act 2 - Scene 2"] = "Perde 2 - Sahne 2",
    ["Act 2 - Scene 3"] = "Perde 2 - Sahne 3",
    ["Act 3 - Scene 1"] = "Perde 3 - Sahne 1",
    ["Act 3 - Scene 2"] = "Perde 3 - Sahne 2",
    ["Act 3 - Scene 3"] = "Perde 3 - Sahne 3",
    ["- The Reunion -"] = "- Kavuşma -",
    ["The Pall"] = "Kefen",
    ["A Task Complete"] = "Görev Tamamlandı",
    ["My Knights Four and I"] = "Dört Şövalyem ve Ben",
}

local state = rawget(GLOBAL, STATE_KEY)
if state == nil then
    state = {
        hooks_installed = false,
    }
    rawset(GLOBAL, STATE_KEY, state)
end

local function SafeCall(label, fn, ...)
    if type(fn) ~= "function" then
        return nil
    end

    local ok, result_a, result_b, result_c, result_d = pcall(fn, ...)
    if not ok then
        print("[Turkce Ceviri] Stageactor cache warning in " .. tostring(label) .. ": " .. tostring(result_a))
        return nil
    end

    return result_a, result_b, result_c, result_d
end

PLAYBILL_TITLE_FALLBACKS["- The Reunion -"] = "- Kavusma -"
PLAYBILL_TITLE_FALLBACKS["A Task Complete"] = "Gorev Tamamlandi"
PLAYBILL_TITLE_FALLBACKS["My Knights Four and I"] = "Dort Sovalyem ve Ben"

local function GetStageactorLineMap()
    local map = rawget(GLOBAL, "TURKCE_STAGEACTOR_LINE_MAP")
    return type(map) == "table" and map or nil
end

local function LocalizeStageLine(line_text)
    local map = GetStageactorLineMap()
    if map ~= nil and type(line_text) == "string" and map[line_text] ~= nil then
        return map[line_text]
    end
    return line_text
end

local function GetLocalizedPlaybillTitle(playbill_title)
    if type(playbill_title) ~= "string" then
        return playbill_title
    end

    local plays = STRINGS ~= nil and STRINGS.PLAYS or nil
    if type(plays) == "table" then
        local enchanted_doll = type(plays.THE_ENCHANTED_DOLL) == "table" and plays.THE_ENCHANTED_DOLL or nil
        local index_by_title = {
            ["Act 1 - Scene 1"] = 1,
            ["Act 1 - Scene 2"] = 2,
            ["Act 1 - Scene 3"] = 3,
            ["Act 2 - Scene 1"] = 4,
            ["Act 2 - Scene 2"] = 5,
            ["Act 2 - Scene 3"] = 6,
            ["Act 3 - Scene 1"] = 7,
            ["Act 3 - Scene 2"] = 8,
            ["Act 3 - Scene 3"] = 9,
            ["- The Reunion -"] = 10,
        }
        local idx = index_by_title[playbill_title]
        if idx ~= nil and enchanted_doll ~= nil and type(enchanted_doll[idx]) == "string" and enchanted_doll[idx] ~= "" then
            return enchanted_doll[idx]
        end
        if playbill_title == "The Pall" and type(plays.THEVEIL) == "string" and plays.THEVEIL ~= "" then
            return plays.THEVEIL
        end
        if playbill_title == "A Task Complete" and type(plays.THEVAULT) == "string" and plays.THEVAULT ~= "" then
            return plays.THEVAULT
        end
        if playbill_title == "My Knights Four and I" and type(plays.THEPRINCESS) == "string" and plays.THEPRINCESS ~= "" then
            return plays.THEPRINCESS
        end
    end

    return PLAYBILL_TITLE_FALLBACKS[playbill_title] or playbill_title
end

local function GetLocalizedCastName(role_name, costume_data)
    local cast = STRINGS ~= nil and STRINGS.CAST or nil
    if type(cast) == "table" and type(role_name) == "string" and type(cast[role_name]) == "string" and cast[role_name] ~= "" then
        return cast[role_name]
    end
    if type(costume_data) == "table" and type(costume_data.name) == "string" and costume_data.name ~= "" then
        return costume_data.name
    end
    return tostring(role_name)
end

local function LocalizePlayCostumes(costumes)
    if type(costumes) ~= "table" then
        return
    end

    for role_name, costume_data in pairs(costumes) do
        if type(costume_data) == "table" then
            costume_data.name = GetLocalizedCastName(role_name, costume_data)
        end
    end
end

local function LocalizeScriptCollection(script_collection)
    if type(script_collection) ~= "table" then
        return
    end

    for _, script_data in pairs(script_collection) do
        if type(script_data) == "table" then
            if type(script_data.playbill) == "string" then
                script_data.playbill = GetLocalizedPlaybillTitle(script_data.playbill)
            end
            if type(script_data.lines) == "table" then
                for _, line in ipairs(script_data.lines) do
                    if type(line) == "table" and line.line ~= nil then
                        line.line = LocalizeStageLine(line.line)
                    end
                end
            end
        end
    end
end

local function DeepCopy(value, seen)
    if type(value) ~= "table" then
        return value
    end

    seen = seen or {}
    if seen[value] ~= nil then
        return seen[value]
    end

    local out = {}
    seen[value] = out
    for k, v in pairs(value) do
        out[DeepCopy(k, seen)] = DeepCopy(v, seen)
    end
    return out
end

local function LoadFreshModule(module_name)
    if type(package_loaded) ~= "table" or type(require) ~= "function" then
        return nil
    end

    package_loaded[module_name] = nil
    local result = SafeCall("require(" .. tostring(module_name) .. ")", require, module_name)
    if type(result) == "table" then
        return result
    end
end

local function ReplaceTableContents(dst, src)
    if type(dst) ~= "table" or type(src) ~= "table" then
        return src
    end

    for k in pairs(dst) do
        dst[k] = nil
    end
    for k, v in pairs(src) do
        dst[k] = v
    end

    return dst
end

local function LoadLocalizedModuleKeepingReference(module_name)
    local original = package_loaded[module_name]
    local localized = LoadFreshModule(module_name)
    if type(localized) ~= "table" then
        if type(original) == "table" then
            package_loaded[module_name] = original
            return original
        end
        return localized
    end

    LocalizeScriptCollection(localized.scripts)
    LocalizePlayCostumes(localized.costumes)

    if type(original) == "table" then
        package_loaded[module_name] = ReplaceTableContents(original, localized)
        LocalizeScriptCollection(original.scripts)
        LocalizePlayCostumes(original.costumes)
        return original
    end

    package_loaded[module_name] = localized
    return localized
end

local function RefreshLoadedStageModules()
    LoadLocalizedModuleKeepingReference(GENERAL_SCRIPT_MODULE)

    local seen = {}
    for _, module_name in pairs(PLAY_MODULE_BY_PREFAB) do
        if not seen[module_name] then
            seen[module_name] = true
            LoadLocalizedModuleKeepingReference(module_name)
        end
    end
end

local function ApplyPlaybillLocalization(playbill)
    if playbill == nil or playbill.inst == nil then
        return false
    end

    RefreshLoadedStageModules()

    local module_name = PLAY_MODULE_BY_PREFAB[playbill.inst.prefab]
    if module_name == nil then
        return false
    end

    local play = LoadLocalizedModuleKeepingReference(module_name)
    if play == nil then
        return false
    end

    local current_act = playbill.current_act
    playbill.costumes = DeepCopy(play.costumes or {})
    playbill.scripts = DeepCopy(play.scripts or {})
    playbill.starting_act = play.starting_act

    if current_act ~= nil and playbill.scripts[current_act] ~= nil then
        playbill.current_act = current_act
    else
        playbill.current_act = play.starting_act
    end

    return true
end

local function RefreshLecternText(lectern)
    if lectern ~= nil and lectern.components ~= nil and lectern.components.playbill_lecturn ~= nil then
        SafeCall("playbill_lecturn:UpdateText", lectern.components.playbill_lecturn.UpdateText, lectern.components.playbill_lecturn)
    end
end

local function RefreshStageProp(stageactingprop)
    if stageactingprop == nil or stageactingprop.inst == nil then
        return
    end

    RefreshLoadedStageModules()

    local general_scripts = LoadLocalizedModuleKeepingReference(GENERAL_SCRIPT_MODULE)
    if general_scripts ~= nil then
        stageactingprop.generalscripts = DeepCopy(general_scripts)
        if stageactingprop.scripts ~= nil then
            for script_name, script_data in pairs(general_scripts) do
                stageactingprop.scripts[script_name] = DeepCopy(script_data)
            end
        end
    end

    local tracker = stageactingprop.inst.components ~= nil and stageactingprop.inst.components.entitytracker or nil
    local lectern = tracker ~= nil and SafeCall("entitytracker:GetEntity", tracker.GetEntity, tracker, "lecturn") or nil
    local playbill_item = lectern ~= nil
        and lectern.components ~= nil
        and lectern.components.playbill_lecturn ~= nil
        and lectern.components.playbill_lecturn.playbill_item
        or nil
    local playbill = playbill_item ~= nil and playbill_item.components ~= nil and playbill_item.components.playbill or nil

    if playbill == nil then
        return
    end

    SafeCall("ApplyPlaybillLocalization(stageprop)", ApplyPlaybillLocalization, playbill)

    local old_add_play = stageactingprop._turkce_old_addplay or stageactingprop.AddPlay
    if old_add_play == nil then
        return
    end

    local current_act = stageactingprop.current_act
    if current_act == nil or playbill.scripts[current_act] == nil then
        current_act = playbill.current_act or playbill.starting_act
    end

    stageactingprop._turkce_stageactor_refreshing = true
    SafeCall("stageactingprop:AddPlay", old_add_play, stageactingprop, {
        costumes = DeepCopy(playbill.costumes or {}),
        scripts = DeepCopy(playbill.scripts or {}),
        current_act = current_act,
        starting_act = playbill.starting_act,
    })
    stageactingprop._turkce_stageactor_refreshing = nil

    RefreshLecternText(lectern)
end

local function PatchExistingEntities()
    RefreshLoadedStageModules()

    local ents = GLOBAL.Ents
    if ents == nil then
        return
    end

    for _, ent in pairs(ents) do
        if ent ~= nil and ent.components ~= nil then
            if ent.components.playbill ~= nil then
                SafeCall("ApplyPlaybillLocalization(existing)", ApplyPlaybillLocalization, ent.components.playbill)
            end
            if ent.components.stageactingprop ~= nil then
                SafeCall("RefreshStageProp(existing)", RefreshStageProp, ent.components.stageactingprop)
            end
            if ent.components.playbill_lecturn ~= nil then
                SafeCall("RefreshLecternText(existing)", RefreshLecternText, ent)
            end
        end
    end
end

local existing_patch = rawget(GLOBAL, "TurkceCeviriApplyStageactorCachePatch")
if existing_patch ~= nil then
    SafeCall("PatchExistingEntities(reimport)", existing_patch)
    return
end

rawset(GLOBAL, "TurkceCeviriApplyStageactorCachePatch", PatchExistingEntities)

AddComponentPostInit("playbill", function(self)
    if self == nil or self.inst == nil or self.inst.DoTaskInTime == nil then
        return
    end
    self.inst:DoTaskInTime(0, function()
        SafeCall("ApplyPlaybillLocalization(task)", ApplyPlaybillLocalization, self)
    end)
end)

AddComponentPostInit("playbill_lecturn", function(self)
    if self == nil then
        return
    end
    if not self._turkce_stageactor_updatetext_wrapped and self.UpdateText ~= nil then
        self._turkce_stageactor_updatetext_wrapped = true
        self._turkce_old_updatetext = self.UpdateText
        self.UpdateText = function(self)
            if self.playbill_item ~= nil and self.playbill_item.components ~= nil and self.playbill_item.components.playbill ~= nil then
                local pb = self.playbill_item.components.playbill
                local script = pb.scripts ~= nil and pb.scripts[pb.current_act] or nil
                local writeable = self.inst ~= nil and self.inst.components ~= nil and self.inst.components.writeable or nil
                if script ~= nil and writeable ~= nil then
                    local text = GetLocalizedPlaybillTitle(script.playbill) .. "\n" .. PLAYBILL_CAST_LABEL
                    for _, cast_member in ipairs(script.cast or {}) do
                        text = text .. "\n" .. GetLocalizedCastName(cast_member, pb.costumes ~= nil and pb.costumes[cast_member] or nil)
                    end
                    writeable:SetText(text)
                    self.inst:PushEvent("text_changed")
                    return
                end
            end
            return SafeCall("playbill_lecturn:old_UpdateText", self._turkce_old_updatetext, self)
        end
    end
    local old_swap_playbill = self.SwapPlayBill
    if old_swap_playbill ~= nil and not self._turkce_stageactor_swap_wrapped then
        self._turkce_stageactor_swap_wrapped = true
        self.SwapPlayBill = function(self, playbill, doer)
            local result = SafeCall("playbill_lecturn:SwapPlayBill", old_swap_playbill, self, playbill, doer)
            if self.playbill_item ~= nil and self.playbill_item.components ~= nil and self.playbill_item.components.playbill ~= nil then
                SafeCall("ApplyPlaybillLocalization(swap)", ApplyPlaybillLocalization, self.playbill_item.components.playbill)
            end
            if self.stage ~= nil and self.stage.components ~= nil and self.stage.components.stageactingprop ~= nil then
                SafeCall("RefreshStageProp(swap)", RefreshStageProp, self.stage.components.stageactingprop)
            end
            SafeCall("playbill_lecturn:UpdateText(swap)", self.UpdateText, self)
            return result
        end
    end
end)

AddComponentPostInit("stageactingprop", function(self)
    if self == nil then
        return
    end
    if not self._turkce_stageactor_addplay_wrapped then
        self._turkce_stageactor_addplay_wrapped = true
        self._turkce_old_addplay = self.AddPlay
        self.AddPlay = function(self, playdata)
            local result = SafeCall("stageactingprop:old_AddPlay", self._turkce_old_addplay, self, playdata)
            if not self._turkce_stageactor_refreshing then
                SafeCall("RefreshStageProp(addplay)", RefreshStageProp, self)
            end
            return result
        end
    end

    if self.inst ~= nil and self.inst.DoTaskInTime ~= nil then
        self.inst:DoTaskInTime(0, function()
            SafeCall("RefreshStageProp(task)", RefreshStageProp, self)
        end)
    end
end)

if not state.hooks_installed then
    state.hooks_installed = true

    AddSimPostInit(function()
        SafeCall("PatchExistingEntities(sim)", PatchExistingEntities)
    end)

    AddGamePostInit(function()
        SafeCall("PatchExistingEntities(game)", PatchExistingEntities)
    end)
end

SafeCall("PatchExistingEntities(init)", PatchExistingEntities)
