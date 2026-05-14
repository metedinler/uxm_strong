Param(
    [string]$RepoRoot = "C:\Users\mete\Downloads\UXMC\ucma\_forensic\strongest2_src"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Set-Location $RepoRoot

$reportDir = Join-Path $RepoRoot "uxm_s\reports"
if (!(Test-Path $reportDir)) {
    New-Item -ItemType Directory -Path $reportDir | Out-Null
}

$compileCmd = "fbc -c uxm_s/src/uxm_s_pipeline.bas"
$compileOk = $true
$compileOut = ""

try {
    $compileOut = & fbc -c uxm_s/src/uxm_s_pipeline.bas 2>&1 | Out-String
} catch {
    $compileOk = $false
    $compileOut = $_.Exception.Message
}

if ($LASTEXITCODE -ne 0) {
    $compileOk = $false
}

$objectPath = Join-Path $RepoRoot "uxm_s\src\uxm_s_pipeline.o"
$hasObject = Test-Path $objectPath

$gateResult = [ordered]@{
    stage = "Asama-3"
    compileCommand = $compileCmd
    compileOk = $compileOk
    objectExists = $hasObject
    objectPath = $objectPath
    timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
}

$gateJson = $gateResult | ConvertTo-Json -Depth 4
$gateJsonPath = Join-Path $reportDir "ASAMA3_GATE_RESULT.json"
$gateTxtPath = Join-Path $reportDir "ASAMA3_GATE_RESULT_TR.md"

$gateJson | Out-File -FilePath $gateJsonPath -Encoding utf8

$md = @()
$md += "# Asama-3 Gate Sonucu"
$md += ""
$md += "- Zaman: $($gateResult.timestamp)"
$md += "- Derleme komutu: $($gateResult.compileCommand)"
$md += "- Derleme basarili: $($gateResult.compileOk)"
$md += "- Obje dosyasi var: $($gateResult.objectExists)"
$md += "- Obje dosyasi: $($gateResult.objectPath)"
$md += ""
$md += "## Derleme Ciktisi"
$md += ""
$md += '```'
$md += $compileOut
$md += '```'

$md -join "`n" | Out-File -FilePath $gateTxtPath -Encoding utf8

Write-Host "[ASAMA3_GATE] json=$gateJsonPath"
Write-Host "[ASAMA3_GATE] md=$gateTxtPath"
if ($compileOk -and $hasObject) {
    exit 0
}
exit 1
