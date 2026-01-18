# 작업 이름
$TaskName = "FinanceBlogBot"

# 실행할 프로그램 (배치 파일)
$Action = New-ScheduledTaskAction -Execute "c:\quant\run_bot.bat"

# 실행 시간 (매일 오전 7시)
$Trigger = New-ScheduledTaskTrigger -Daily -At "07:00AM"

# 작업 설정 (절전 모드에서도 깨어나서 실행)
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -WakeToRun

# 기존 작업이 있다면 삭제
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

# 새 작업 등록
Register-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings -TaskName $TaskName -Description "매일 아침 7시에 금융 블로그 포스팅"

Write-Host "✅ 작업 스케줄러 등록 완료! 매일 오전 7시에 실행됩니다."
Write-Host "테스트하려면 작업 스케줄러에서 '$TaskName'을 찾아 우클릭 -> 실행을 누르세요."
