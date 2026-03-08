local TheNet = GLOBAL.TheNet
local pairs = GLOBAL.pairs or pairs
local pcall = GLOBAL.pcall or pcall
local print = GLOBAL.print or print
local rawget = GLOBAL.rawget or rawget
local rawset = GLOBAL.rawset or rawset
local type = GLOBAL.type or type
local tostring = GLOBAL.tostring or tostring
local string = GLOBAL.string or string
local ipairs = GLOBAL.ipairs or ipairs

local SNAPSHOT_KEY = "__tt_skilltree_en_snapshot"
local BUILDER_PATCH_KEY = "__tt_skilltree_builder_patch"
local STATE_KEY = "__tt_skilltree_compat_state"

if TheNet ~= nil and TheNet.IsDedicated ~= nil and TheNet:IsDedicated() then
    return
end

local state = rawget(GLOBAL, STATE_KEY)
if state == nil then
    state = {
        hooks_installed = false,
        patch_logged = false,
    }
    rawset(GLOBAL, STATE_KEY, state)
end

local function GetSkillTreeStrings()
    local strings = GLOBAL.STRINGS
    return strings ~= nil and strings.SKILLTREE or nil
end

local function DeepCopySkillStrings(src, seen)
    if type(src) ~= "table" then
        return src
    end

    seen = seen or {}
    if seen[src] ~= nil then
        return seen[src]
    end

    local dst = {}
    seen[src] = dst

    for k, v in pairs(src) do
        if type(v) == "table" then
            dst[k] = DeepCopySkillStrings(v, seen)
        elseif type(v) == "string" then
            dst[k] = v
        end
    end

    return dst
end

local function SnapshotEnglishSkillTree()
    if rawget(GLOBAL, SNAPSHOT_KEY) ~= nil then
        return
    end

    local root = GetSkillTreeStrings()
    if type(root) == "table" then
        rawset(GLOBAL, SNAPSHOT_KEY, DeepCopySkillStrings(root))
    end
end

local function GetEnglishSkillTreeStrings()
    return rawget(GLOBAL, SNAPSHOT_KEY)
end

local function AddCandidate(candidates, seen, value)
    if type(value) ~= "string" or value == "" or seen[value] then
        return
    end
    seen[value] = true
    candidates[#candidates + 1] = value
end

local function BuildSkillKeyCandidates(prefab_key, skill_key)
    local candidates, seen = {}, {}

    AddCandidate(candidates, seen, skill_key)

    local prefix = prefab_key .. "_"
    if skill_key:sub(1, #prefix) == prefix then
        local stripped = skill_key:sub(#prefix + 1)
        AddCandidate(candidates, seen, stripped)
        AddCandidate(candidates, seen, stripped:gsub("(%a)(%d+)$", "%1_%2"))
        AddCandidate(candidates, seen, stripped:gsub("%d+$", ""))
        AddCandidate(candidates, seen, stripped:gsub("_(%d+)$", ""))
    end

    AddCandidate(candidates, seen, skill_key:gsub("(%a)(%d+)$", "%1_%2"))
    AddCandidate(candidates, seen, skill_key:gsub("%d+$", ""))
    AddCandidate(candidates, seen, skill_key:gsub("_(%d+)$", ""))

    return candidates
end

local function FindLocalizedByEnglish(root, english_root, prefab_key, english_value, suffix)
    if type(root) ~= "table" or type(english_root) ~= "table" or type(english_value) ~= "string" or english_value == "" then
        return nil
    end

    local prefab_strings = root[prefab_key]
    local english_prefab_strings = english_root[prefab_key]
    if type(prefab_strings) == "table" and type(english_prefab_strings) == "table" then
        for key, english_text in pairs(english_prefab_strings) do
            if type(key) == "string" and key:sub(-#suffix) == suffix and english_text == english_value then
                local localized = prefab_strings[key]
                if type(localized) == "string" and localized ~= "" then
                    return localized
                end
            end
        end
    end

    for key, english_text in pairs(english_root) do
        if type(key) == "string" and key:sub(-#suffix) == suffix and english_text == english_value then
            local localized = root[key]
            if type(localized) == "string" and localized ~= "" then
                return localized
            end
        end
    end

    return nil
end

local function ReadSkillString(root, english_root, prefab_key, skill_key, suffix, english_value)
    if type(root) ~= "table" then
        return nil
    end

    local prefab_strings = root[prefab_key]
    if type(prefab_strings) == "table" then
        for _, candidate in ipairs(BuildSkillKeyCandidates(prefab_key, skill_key)) do
            local localized = prefab_strings[candidate .. suffix]
            if type(localized) == "string" and localized ~= "" then
                return localized
            end
        end
    end

    local generic_lock = skill_key:match("^[A-Z0-9]+_(ALLEGIANCE_LOCK_%d+)$")
    if generic_lock ~= nil then
        local localized = root[generic_lock .. suffix]
        if type(localized) == "string" and localized ~= "" then
            return localized
        end
    end

    for _, candidate in ipairs(BuildSkillKeyCandidates(prefab_key, skill_key)) do
        local localized = root[candidate .. suffix]
        if type(localized) == "string" and localized ~= "" then
            return localized
        end
    end

    return FindLocalizedByEnglish(root, english_root, prefab_key, english_value, suffix)
end

local function ResolveSkillString(prefabname, skillname, suffix, english_value)
    local root = GetSkillTreeStrings()
    local english_root = GetEnglishSkillTreeStrings()
    if type(root) ~= "table" or type(prefabname) ~= "string" or type(skillname) ~= "string" then
        return nil
    end

    return ReadSkillString(root, english_root, string.upper(prefabname), string.upper(skillname), suffix, english_value)
end

local function RefreshSkillDefs(skilltreedata_all)
    if type(skilltreedata_all) ~= "table" or type(skilltreedata_all.SKILLTREE_DEFS) ~= "table" then
        return false
    end

    local root = GetSkillTreeStrings()
    local english_root = GetEnglishSkillTreeStrings()
    if type(root) ~= "table" then
        return false
    end

    for prefabname, skilldefs in pairs(skilltreedata_all.SKILLTREE_DEFS) do
        if type(skilldefs) == "table" then
            local prefab_key = string.upper(prefabname)
            for skillname, data in pairs(skilldefs) do
                if type(data) == "table" then
                    local skill_key = string.upper(skillname)
                    local english_title = type(data.title) == "string" and data.title or nil
                    local english_desc = type(data.desc) == "string" and data.desc or nil

                    local title = ReadSkillString(root, english_root, prefab_key, skill_key, "_TITLE", english_title)
                    if title ~= nil then
                        data.title = title
                    end

                    local desc = ReadSkillString(root, english_root, prefab_key, skill_key, "_DESC", english_desc)
                    if desc ~= nil then
                        data.desc = desc
                    end
                end
            end
        end
    end

    return true
end

local function TryPatchSkillTree()
    if type(GLOBAL.require) ~= "function" then
        return false
    end

    local ok, skilltreedata_all = pcall(GLOBAL.require, "prefabs/skilltree_defs")
    if not ok then
        return false
    end

    if RefreshSkillDefs(skilltreedata_all) then
        if not state.patch_logged then
            print("[Turkce Ceviri] Applied skill tree localization compatibility.")
            state.patch_logged = true
        end
        return true
    end

    return false
end

local function PatchSkillTreeBuilderGlobals()
    if rawget(GLOBAL, BUILDER_PATCH_KEY) then
        return
    end

    if type(GLOBAL.gettitle) == "function" then
        local previous_gettitle = GLOBAL.gettitle
        GLOBAL.gettitle = function(skill, prefabname, skillgraphics)
            local ok, current = pcall(previous_gettitle, skill, prefabname, skillgraphics)
            if not ok then
                return nil
            end
            local localized = ResolveSkillString(prefabname, skill, "_TITLE", current)
            return localized or current
        end
    end

    if type(GLOBAL.getdesc) == "function" then
        local previous_getdesc = GLOBAL.getdesc
        GLOBAL.getdesc = function(skill, prefabname)
            local ok, current = pcall(previous_getdesc, skill, prefabname)
            if not ok then
                return nil
            end
            local localized = ResolveSkillString(prefabname, skill, "_DESC", current)
            return localized or current
        end
    end

    rawset(GLOBAL, BUILDER_PATCH_KEY, true)
end

SnapshotEnglishSkillTree()
TryPatchSkillTree()

if state.hooks_installed then
    return
end

state.hooks_installed = true

AddSimPostInit(function()
    TryPatchSkillTree()
end)

AddGamePostInit(function()
    TryPatchSkillTree()
end)

AddClassPostConstruct("widgets/redux/skilltreebuilder", function(self)
    if self == nil or self._tt_skilltree_refresh_wrapped then
        return
    end

    self._tt_skilltree_refresh_wrapped = true
    PatchSkillTreeBuilderGlobals()
    TryPatchSkillTree()

    if type(self.RefreshTree) == "function" then
        local previous_refresh_tree = self.RefreshTree
        self.RefreshTree = function(builder, ...)
            local ok, result = pcall(previous_refresh_tree, builder, ...)
            if not ok then
                print("[Turkce Ceviri] Skill tree refresh warning: " .. tostring(result))
                return nil
            end

            local update_ok, update_err = pcall(function()
                if builder.selectedskill ~= nil and builder.target ~= nil and builder.infopanel ~= nil then
                    if builder.infopanel.title ~= nil then
                        local title = ResolveSkillString(builder.target, builder.selectedskill, "_TITLE", GLOBAL.gettitle(builder.selectedskill, builder.target, builder.skillgraphics or {}))
                        if type(title) == "string" and title ~= "" then
                            builder.infopanel.title:SetString(title)
                        end
                    end

                    if builder.infopanel.desc ~= nil then
                        local desc = ResolveSkillString(builder.target, builder.selectedskill, "_DESC", GLOBAL.getdesc(builder.selectedskill, builder.target))
                        if type(desc) == "string" and desc ~= "" then
                            builder.infopanel.desc:SetMultilineTruncatedString(desc, 3, 400, nil, nil, true, 6)
                        end
                    end
                end
            end)
            if not update_ok then
                print("[Turkce Ceviri] Skill tree info panel warning: " .. tostring(update_err))
            end

            return result
        end
    end
end)
