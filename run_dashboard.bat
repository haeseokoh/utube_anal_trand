@echo off
chcp 65001 > nul
echo ====================================================================
echo   YouTube Macro & Analyst Trend Intelligence System
echo   유튜브 경제 분석가 트렌드 인텔리전스 대시보드 구동기
echo ====================================================================
echo.

REM 가상환경 또는 기본 파이썬 인터프리터 점검
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python이 시스템에 설치되어 있지 않거나 PATH에 등록되지 않았습니다.
    pause
    exit /b
)

echo [INFO] 서버 시작 중... (http://localhost:8001)
python main.py --port 8001

pause
