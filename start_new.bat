@echo off
chcp 936 > nul
echo ================================
echo Muhe Opportunity Radar - 启动脚本
echo ================================
echo.

REM 检查环境变量文件
if not exist .env (
    echo [警告] .env 文件不存在，请从 .env.example 复制并配置
    echo.
    choice /C YN /M "是否复制 .env.example 为 .env"
    if errorlevel 2 goto :end
    copy .env.example .env
    echo 请编辑 .env 文件配置 API 密钥后重新运行
    goto :end
)

echo 请选择启动模式：
echo [1] FastAPI 后端（端口 8000）
echo [2] Vue3 前端（端口 5173）
echo [3] 同时启动后端和前端
echo [4] Gradio 应用（端口 7860，备用）
echo [5] Docker Compose 部署（推荐）
echo.

choice /C 12345 /M "请选择"

if errorlevel 5 goto :docker
if errorlevel 4 goto :gradio
if errorlevel 3 goto :both
if errorlevel 2 goto :frontend
if errorlevel 1 goto :backend

:backend
echo.
echo [启动] FastAPI 后端...
D:\ai_works\muhe-opportunity-radar\.venv\Scripts\python.exe -m uvicorn api.main:app --reload --port 8000
goto :end

:frontend
echo.
echo [启动] Vue3 前端...
cd frontend
call npm run dev
goto :end

:both
echo.
echo [启动] 后端和前端...
echo [检查] 检测端口 8000 占用情况...
netstat -ano | findstr :8000 | findstr LISTENING > nul
if not errorlevel 1 (
    echo [警告] 端口 8000 已被占用，正在尝试关闭...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a > nul 2>&1
    timeout /t 2 /nobreak > nul
)
echo [1/3] 启动 FastAPI 后端...
start "FastAPI Backend" cmd /k D:\ai_works\muhe-opportunity-radar\.venv\Scripts\python.exe -m uvicorn api.main:app --reload --port 8000

echo [2/3] 等待后端启动并进行健康检查...
set attempt=0
:wait_backend
timeout /t 1 /nobreak > nul
powershell -Command "try { $response = Invoke-WebRequest -Uri http://localhost:8000/health -TimeoutSec 2 -UseBasicParsing; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" > nul 2>&1
if errorlevel 1 (
    set /a attempt+=1
    if %attempt% lss 15 (
        echo    检查中... ^(尝试 %attempt%/15^)
        goto :wait_backend
    )
    echo.
    echo [错误] 后端启动失败或超时（15秒），请检查：
    echo   - Python 环境是否正确
    echo   - 端口 8000 是否被占用
    echo   - .env 配置是否正确
    echo.
    goto :end
)

echo [成功] 后端已就绪 - http://localhost:8000
echo [3/3] 启动 Vue3 前端...
cd frontend
start "Vue3 Frontend" cmd /k npm run dev
echo.
echo ================================
echo 服务启动成功！
echo ================================
echo 后端 API: http://localhost:8000/api/docs
echo 前端界面: http://localhost:5173
echo ================================
goto :end

:gradio
echo.
echo [启动] Gradio 应用（备用）...
D:\ai_works\muhe-opportunity-radar\.venv\Scripts\python.exe app.py
goto :end

:docker
echo.
echo [启动] Docker Compose 部署...
docker-compose up -d
echo.
echo 服务已启动：
echo - 前端: http://localhost
echo - API: http://localhost:8000/api/docs
echo - Gradio: http://localhost:7860
echo - MongoDB: localhost:27017
echo.
echo 查看日志: docker-compose logs -f
echo 停止服务: docker-compose down
goto :end

:end
echo.
pause
