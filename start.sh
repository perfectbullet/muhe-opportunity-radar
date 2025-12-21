#!/bin/bash

echo "===================================="
echo "炑禾机会雷达 - 启动脚本"
echo "===================================="
echo ""

echo "激活虚拟环境..."
source .venv/bin/activate

echo ""
echo "启动 Gradio 应用..."
echo "访问地址: http://localhost:7860"
echo ""

python app.py
