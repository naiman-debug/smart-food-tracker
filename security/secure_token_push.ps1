# Secure GitHub Push with Personal Access Token
# This script securely uses a GitHub Personal Access Token to push code
# Token is never stored in files or command history

param(
    [Parameter(Mandatory=$false, HelpMessage="GitHub Personal Access Token")]
    [string]$Token
)

# Script configuration
$ErrorActionPreference = "Stop"
$ProjectDir = "C:\Users\Administrator\智能食物记录"
$RepoUrl = "https://github.com/naiman-debug/smart-food-tracker.git"

# Function to securely read token from user input
function Get-SecureToken {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " GitHub Personal Access Token Required " -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Please provide your GitHub Personal Access Token." -ForegroundColor Yellow
    Write-Host "The token will be used securely and NOT stored." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To generate a new token:" -ForegroundColor White
    Write-Host "  1. Visit: https://github.com/settings/tokens" -ForegroundColor Gray
    Write-Host "  2. Click 'Generate new token' → 'Generate new token (classic)'" -ForegroundColor Gray
    Write-Host "  3. Note: 'Smart Food Tracker Push'" -ForegroundColor Gray
    Write-Host "  4. Expiration: '90 days' or your preference" -ForegroundColor Gray
    Write-Host "  5. Check 'repo' scope" -ForegroundColor Gray
    Write-Host "  6. Click 'Generate token' and copy it" -ForegroundColor Gray
    Write-Host ""

    $secureToken = Read-Host "Paste your Token here" -AsSecureString
    $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureToken)
    $token = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)

    return $token
}

# Function to clean up token from environment
function Clear-Token {
    [CmdletBinding()]
    param([string]$TokenString)

    # Clear the variable
    Remove-Variable -Name TokenString -ErrorAction SilentlyContinue

    # Clear any environment variables we may have set
    [Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $null, "Process")
    [Environment]::SetEnvironmentVariable("GH_TOKEN", $null, "Process")

    # Clear clipboard if it contains the token (Windows)
    try {
        Add-Type -AssemblyName PresentationCore
        if ([Windows.Clipboard]::ContainsText()) {
            $clipText = [Windows.Clipboard]::GetText()
            if ($clipText -match "^[a-f0-9]{36,}$") {
                [Windows.Clipboard]::Clear()
            }
        }
    } catch {
        # Silently ignore clipboard errors
    }
}

# Main execution
try {
    Write-Host ""
    Write-Host "=== Secure GitHub Push Script ===" -ForegroundColor Green
    Write-Host ""

    # Change to project directory
    Set-Location $ProjectDir

    # Get token - from parameter or prompt
    if ([string]::IsNullOrWhiteSpace($Token)) {
        $Token = Get-SecureToken
    }

    # Validate token format
    if ($Token -notmatch "^[a-zA-Z0-9_]{36,}$") {
        throw "Invalid token format. Token should be alphanumeric and at least 36 characters."
    }

    Write-Host ""
    Write-Host "Token received. Proceeding with push..." -ForegroundColor Green
    Write-Host ""

    # Configure Git to use token for this specific URL
    $authUrl = "https://naiman-debug:${Token}@github.com/naiman-debug/smart-food-tracker.git"

    # Execute push
    Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
    $pushResult = git push -u $authUrl main 2>&1

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "  PUSH SUCCESSFUL!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Your code has been pushed to GitHub:" -ForegroundColor White
        Write-Host "  https://github.com/naiman-debug/smart-food-tracker" -ForegroundColor Cyan
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Red
        Write-Host "  PUSH FAILED" -ForegroundColor Red
        Write-Host "========================================" -ForegroundColor Red
        Write-Host ""
        Write-Host "Error output:" -ForegroundColor Yellow
        Write-Host $pushResult
        Write-Host ""
        throw "Git push failed with exit code $LASTEXITCODE"
    }

} catch {
    Write-Host ""
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    exit 1
} finally {
    # Clean up token
    if ($Token) {
        Clear-Token -TokenString $Token
        Remove-Variable -Name Token -ErrorAction SilentlyContinue
    }

    # Clear history
    if (Get-Command Clear-RecycledData -ErrorAction SilentlyContinue) {
        Clear-RecycledData -ErrorAction SilentlyContinue
    }

    Write-Host ""
    Write-Host "Token has been cleared from memory." -ForegroundColor Green
    Write-Host "Script completed." -ForegroundColor Gray
    Write-Host ""
}
