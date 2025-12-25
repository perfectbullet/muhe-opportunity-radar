@echo off
chcp 65001 >nul
echo ====================================
echo 炑禾机会雷达 - 启动脚本
echo ====================================
echo.

REM 检查环境变量文件
if not exist .env (
    echo [警告] .env 文件不存在，请从 .env.example 复制并配置
    pause
    exit /b 1
)

echo [检查] 检测端口 8000 占用情况...
netstat -ano | findstr :8000 | findstr LISTENING > nul
if not errorlevel 1 (
    echo [警告] 端口 8000 已被占用，正在尝试关闭...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a > nul 2>&1
    timeout /t 2 /nobreak > nul
)

echo.
echo [1/3] 启动 FastAPI 后端...
start "FastAPI Backend" cmd /k .venv\Scripts\python.exe -m uvicorn api.main:app --reload --port 8000

echo [2/3] 等待后端启动并进行健康检查...
set attempt=0
:wait_backend
timeout /t 1 /nobreak > nul
set /a attempt+=1
curl -s -o nul -w "%%{http_code}" http://localhost:8000/health | findstr "200" > nul 2>&1
if errorlevel 1 (
    if %attempt% lss 15 (
        echo    检查中... ^(尝试 %attempt%/15^)
        goto :wait_backend
    )
    echo.
    echo [错误] 后端启动失败或超时（15秒），请检查日志
    echo.
    pause
    exit /b 1
)

echo [成功] 后端已就绪 - http://localhost:8000
echo [3/3] 启动 Vue3 前端...
cd frontend
start "Vue3 Frontend" cmd /k npm run dev

echo.
echo ====================================
echo 服务启动成功！
echo ====================================
echo 后端 API: http://localhost:8000/api/docs
echo 前端界面: http://localhost:5173
echo ====================================
echo.
pause
