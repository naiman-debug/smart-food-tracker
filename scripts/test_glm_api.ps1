# GLM API Test Script
# UTF-8 Encoding

$GLM_API_KEY = "7ce400cc79454af49b6fd62ebc69e7ab.LiscGibdoY1Dzp4z"
$GLM_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "GLM API Integration Test" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Validate API Key
Write-Host "Test 1: API Key Validation" -ForegroundColor Yellow
Write-Host "------------------------------------------------------------" -ForegroundColor Yellow

$headers = @{
    "Authorization" = "Bearer $GLM_API_KEY"
    "Content-Type" = "application/json"
}

$body = @{
    model = "glm-4.6v-flash"
    messages = @(
        @{
            role = "user"
            content = "Hello, please reply 'Connection OK'"
        }
    )
    max_tokens = 50
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri $GLM_API_URL -Method Post -Headers $headers -Body $body -TimeoutSec 30
    $content = $response.choices[0].message.content
    Write-Host "Status: 200 OK" -ForegroundColor Green
    Write-Host "Response: $content" -ForegroundColor Green
    Write-Host "Result: PASS" -ForegroundColor Green
    $test1_pass = $true
} catch {
    Write-Host "Result: FAIL" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    $test1_pass = $false
}

Write-Host ""

# Test 2: Image Recognition
Write-Host "Test 2: Image Recognition" -ForegroundColor Yellow
Write-Host "------------------------------------------------------------" -ForegroundColor Yellow

$testImageBase64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

$jsonPayload = @{
    model = "glm-4.6v-flash"
    messages = @(
        @{
            role = "user"
            content = @(
                @{
                    type = "image_url"
                    image_url = @{
                        url = $testImageBase64
                    }
                },
                @{
                    type = "text"
                    text = "Identify the food in this image. Only return the food name."
                }
            )
        }
    )
    temperature = 0.3
    max_tokens = 50
}

$jsonString = $jsonPayload | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri $GLM_API_URL -Method Post -Headers $headers -Body $jsonString -TimeoutSec 30
    $content = $response.choices[0].message.content
    Write-Host "Status: 200 OK" -ForegroundColor Green
    Write-Host "Recognition Result: $content" -ForegroundColor Green
    Write-Host "Result: PASS" -ForegroundColor Green
    $test2_pass = $true
} catch {
    Write-Host "Result: FAIL" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    $test2_pass = $false
}

Write-Host ""

# Summary
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Test Summary" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

if ($test1_pass) {
    Write-Host "[PASS] API Key Validation" -ForegroundColor Green
} else {
    Write-Host "[FAIL] API Key Validation" -ForegroundColor Red
}

if ($test2_pass) {
    Write-Host "[PASS] Image Recognition" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Image Recognition" -ForegroundColor Red
}

Write-Host ""

if ($test1_pass -and $test2_pass) {
    Write-Host "All tests passed! GLM integration is working." -ForegroundColor Green
    exit 0
} else {
    Write-Host "Some tests failed. Check configuration or network." -ForegroundColor Yellow
    exit 1
}
