local TheNet = GLOBAL.TheNet
local pcall = GLOBAL.pcall
local print = GLOBAL.print
local select = GLOBAL.select
local tostring = GLOBAL.tostring
local type = GLOBAL.type

if TheNet ~= nil and TheNet.IsDedicated ~= nil and TheNet:IsDedicated() then
    return
end

local Text = GLOBAL.require("widgets/text")

if Text._tt_safe_truncate_guard_applied then
    return
end

Text._tt_safe_truncate_guard_applied = true

local function SafeSetString(widget, value)
    if widget == nil or widget.inst == nil or widget.inst.TextWidget == nil then
        return false
    end

    local ok = pcall(function()
        widget.inst.TextWidget:SetString(value or "")
    end)

    return ok
end

local function SafeGetRegionWidth(widget)
    if widget == nil or widget.inst == nil or widget.inst.TextWidget == nil then
        return nil
    end

    local ok, width = pcall(function()
        return select(1, widget.inst.TextWidget:GetRegionSize())
    end)

    if ok and type(width) == "number" then
        return width
    end

    return nil
end

function Text:SetTruncatedString(str, maxwidth, maxchars, ellipses)
    local str_fits = true
    str = str ~= nil and tostring(str):match("^[^\n\v\f\r]*") or ""

    if #str > 0 then
        if type(ellipses) ~= "string" then
            ellipses = ellipses and "..." or ""
        end

        if maxchars ~= nil and str:utf8len() > maxchars then
            str = str:utf8sub(1, maxchars)
            SafeSetString(self, str .. ellipses)
            str_fits = false
        else
            SafeSetString(self, str)
        end

        if maxwidth ~= nil then
            while true do
                local region_w = SafeGetRegionWidth(self)
                if type(region_w) ~= "number" or region_w <= maxwidth then
                    break
                end

                local truncated = str:utf8sub(1, -2)
                if truncated == nil or truncated == str then
                    break
                end

                str = truncated
                SafeSetString(self, str .. ellipses)
                str_fits = false

                if str == "" then
                    break
                end
            end
        end
    else
        SafeSetString(self, "")
    end

    return str_fits
end

print("[Turkce Ceviri] Applied safe text truncate guard.")
