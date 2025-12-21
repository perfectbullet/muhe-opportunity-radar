@echo off
chcp 65001 >nul
echo ====================================
echo 炑禾机会雷达 - 启动脚本
echo ====================================
echo.

echo 激活虚拟环境...
call .venv\Scripts\activate.bat

echo.
echo 启动 Gradio 应用...
echo 访问地址: http://localhost:7860
echo.

python app.py

pause
