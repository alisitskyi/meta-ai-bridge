# Windows Installer for meta-ads-ai-bridge
param(
    [string]$AccessToken = "",
    [string]$AccountId = ""
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Installing meta-ads-ai-bridge (Windows) " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "[ERROR] Python is not installed or not in PATH." -ForegroundColor Red
    exit 1
}
Write-Host "[+] Found Python: $($pythonCmd.Source)" -ForegroundColor Green

# 2. Install dependencies
Write-Host "[*] Installing dependencies..." -ForegroundColor Yellow
python -m pip install -r "$PSScriptRoot\requirements.txt" --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies." -ForegroundColor Red
    exit 1
}
Write-Host "[+] Dependencies installed successfully." -ForegroundColor Green

# 3. Create ~/.meta_ads directory
$metaHome = "$HOME\.meta_ads"
$metaBin = "$metaHome\bin"
New-Item -ItemType Directory -Path $metaHome -Force | Out-Null
New-Item -ItemType Directory -Path $metaBin -Force | Out-Null

Copy-Item "$PSScriptRoot\src\meta_ai\cli.py" -Destination "$metaHome\meta_tool.py" -Force

"@echo off`r`npython `"$metaHome\meta_tool.py`" %*" | Set-Content "$metaBin\fbads.cmd" -Force
"& python `"$metaHome\meta_tool.py`" `$args" | Set-Content "$metaBin\fbads.ps1" -Force
"@echo off`r`npython `"$metaHome\meta_tool.py`" %*" | Set-Content "$metaBin\meta-ads.cmd" -Force
"& python `"$metaHome\meta_tool.py`" `$args" | Set-Content "$metaBin\meta-ads.ps1" -Force

# 4. Handle configuration
if ($AccessToken) {
    & python "$metaHome\meta_tool.py" config --access-token $AccessToken
}
if ($AccountId) {
    & python "$metaHome\meta_tool.py" config --account-id $AccountId
}

# 5. Add to User PATH
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($userPath -notlike "*$metaBin*") {
    $newUserPath = $userPath.TrimEnd(';') + ";$metaBin"
    [Environment]::SetEnvironmentVariable("PATH", $newUserPath, "User")
    Write-Host "[+] Added $metaBin to permanent User PATH." -ForegroundColor Green
} else {
    Write-Host "[+] $metaBin is already in User PATH." -ForegroundColor Green
}

$env:PATH = "$env:PATH;$metaBin"

Write-Host "`n[+] Installation complete!" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor White
Write-Host "1. Set access token: fbads config --access-token <YOUR_TOKEN>"
Write-Host "2. List accessible ad accounts: fbads accounts"
Write-Host "3. View campaigns: fbads campaigns"
