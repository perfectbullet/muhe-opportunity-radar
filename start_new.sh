#!/bin/bash

echo "================================"
echo "Muhe Opportunity Radar - 启动脚本"
echo "================================"
echo

# 检查环境变量文件
if [ ! -f .env ]; then
    echo "[警告] .env 文件不存在"
    read -p "是否复制 .env.example 为 .env? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env
        echo "请编辑 .env 文件配置 API 密钥后重新运行"
        exit 1
    else
        exit 1
    fi
fi

echo "请选择启动模式："
echo "[1] FastAPI 后端（端口 8000）"
echo "[2] Vue3 前端（端口 5173）"
echo "[3] 同时启动后端和前端"
echo "[4] Gradio 应用（端口 7860，备用）"
echo "[5] Docker Compose 部署（推荐）"
echo

read -p "请选择 [1-5]: " choice

case $choice in
    1)
        echo
        echo "[启动] FastAPI 后端..."
        python -m uvicorn api.main:app --reload --port 8000
        ;;
    2)
        echo
        echo "[启动] Vue3 前端..."
        cd frontend
        npm run dev
        ;;
    3)
        echo
        echo "[启动] 后端和前端..."
        python -m uvicorn api.main:app --reload --port 8000 &
        sleep 3
        cd frontend
        npm run dev
        ;;
    4)
        echo
        echo "[启动] Gradio 应用（备用）..."
        python app.py
        ;;
    5)
        echo
        echo "[启动] Docker Compose 部署..."
        docker-compose up -d
        echo
        echo "服务已启动："
        echo "- 前端: http://localhost"
        echo "- API: http://localhost:8000/api/docs"
        echo "- Gradio: http://localhost:7860"
        echo "- MongoDB: localhost:27017"
        echo
        echo "查看日志: docker-compose logs -f"
        echo "停止服务: docker-compose down"
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac
