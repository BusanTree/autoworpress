# WordPress 자동 포스팅 작업 스케줄러 등록 스크립트

# 관리자 권한 확인
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "⚠️  이 스크립트는 관리자 권한이 필요합니다." -ForegroundColor Yellow
    Write-Host "   PowerShell을 관리자 권한으로 실행한 후 다시 시도하세요." -ForegroundColor Yellow
    pause
    exit
}

$scriptPath = $PSScriptRoot
$pythonScript = Join-Path $scriptPath "wordpress_bot.py"

# Python 경로 자동 탐지
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonPath) {
    Write-Host "❌ Python을 찾을 수 없습니다!" -ForegroundColor Red
    Write-Host "   Python이 설치되어 있고 PATH에 등록되어 있는지 확인하세요." -ForegroundColor Yellow
    pause
    exit
}

Write-Host "=" * 60
Write-Host "📅 WordPress 자동 포스팅 - 작업 스케줄러 등록" -ForegroundColor Cyan
Write-Host "=" * 60
Write-Host ""
Write-Host "Python 경로: $pythonPath" -ForegroundColor Green
Write-Host "스크립트 경로: $pythonScript" -ForegroundColor Green
Write-Host ""

# 사용자에게 시간 입력 받기
$defaultTime = "09:00AM"
$timeInput = Read-Host "실행 시간을 입력하세요 (기본값: $defaultTime, 예: 10:30AM)"
if ([string]::IsNullOrWhiteSpace($timeInput)) {
    $timeInput = $defaultTime
}

Write-Host ""
Write-Host "⏰ 설정된 시간: $timeInput" -ForegroundColor Yellow
Write-Host ""

# 작업 생성
try {
    # 작업 동작 정의
    $action = New-ScheduledTaskAction `
        -Execute $pythonPath `
        -Argument "`"$pythonScript`"" `
        -WorkingDirectory $scriptPath

    # 트리거 정의 (매일)
    $trigger = New-ScheduledTaskTrigger `
        -Daily `
        -At $timeInput

    # 설정
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -ExecutionTimeLimit (New-TimeSpan -Hours 1)

    # 작업 등록
    $taskName = "WordPress Auto Poster"
    
    # 기존 작업이 있으면 삭제
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "🔄 기존 작업을 삭제하고 새로 등록합니다..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }

    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description "워드프레스 자동 포스팅 (매일 $timeInput)" `
        -Force

    Write-Host ""
    Write-Host "=" * 60
    Write-Host "✅ 작업 스케줄러 등록 완료!" -ForegroundColor Green
    Write-Host "=" * 60
    Write-Host ""
    Write-Host "작업 이름: $taskName" -ForegroundColor Cyan
    Write-Host "실행 시간: 매일 $timeInput" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "💡 확인 방법:" -ForegroundColor Yellow
    Write-Host "   1. 작업 스케줄러 열기: taskschd.msc" -ForegroundColor White
    Write-Host "   2. 왼쪽 '작업 스케줄러 라이브러리' 클릭" -ForegroundColor White
    Write-Host "   3. 'WordPress Auto Poster' 작업 찾기" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 수동 실행:" -ForegroundColor Yellow
    Write-Host "   작업 우클릭 → '실행'" -ForegroundColor White
    Write-Host ""

}
catch {
    Write-Host ""
    Write-Host "❌ 오류 발생:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
}

pause
