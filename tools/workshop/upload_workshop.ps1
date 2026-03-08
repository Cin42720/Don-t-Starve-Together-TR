param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("client", "server")]
    [string]$Target,

    [Parameter(Mandatory = $true)]
    [string]$SteamCmdPath,

    [string]$SteamUser = "",
    [string]$PublishedFileId = "",
    [ValidateSet("public", "friends", "hidden")]
    [string]$Visibility = "hidden",
    [string]$ChangeNote = "Workshop update."
)

$ErrorActionPreference = "Stop"

$renderScript = Join-Path $PSScriptRoot "render_workshop_files.py"
$python = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "py" }

& $python $renderScript

$template = if ($Target -eq "client") {
    Join-Path $PSScriptRoot "workshop_client.vdf"
} else {
    Join-Path $PSScriptRoot "workshop_server.vdf"
}

$visibilityMap = @{
    public  = "0"
    friends = "1"
    hidden  = "2"
}

$tempVdf = Join-Path $env:TEMP ("dst_workshop_" + $Target + ".vdf")
$content = Get-Content -Path $template -Raw -Encoding UTF8
$content = $content -replace '"publishedfileid"\s+"[^"]*"', ('"publishedfileid"' + "`t" + "`t" + '"' + $PublishedFileId + '"')
$content = $content -replace '"visibility"\s+"[^"]*"', ('"visibility"' + "`t" + "`t" + '"' + $visibilityMap[$Visibility] + '"')
$content = $content -replace '"changenote"\s+"[^"]*"', ('"changenote"' + "`t" + '"' + ($ChangeNote -replace '"', "'") + '"')
Set-Content -Path $tempVdf -Value $content -Encoding UTF8

if (-not (Test-Path $SteamCmdPath)) {
    throw "steamcmd.exe bulunamadi: $SteamCmdPath"
}

if ([string]::IsNullOrWhiteSpace($SteamUser)) {
    throw "SteamUser parametresi gerekli. Steam kullanici adinizi verin."
}

& $SteamCmdPath +login $SteamUser +workshop_build_item $tempVdf +quit
