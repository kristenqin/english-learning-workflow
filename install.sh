#!/bin/bash

# 英语学习工作流安装脚本

echo "🚀 开始安装英语学习工作流"

# 检查Python版本
python_version=$(python3 --version 2>&1)
echo "Python版本: $python_version"

# 创建虚拟环境
echo "📦 创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo "✅ 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📦 安装依赖包..."
pip install -r requirements.txt

# 运行设置脚本
echo "⚙️ 运行项目设置..."
python setup.py

echo ""
echo "🎉 安装完成！"
echo ""
echo "使用方法:"
echo "1. 激活虚拟环境: source venv/bin/activate"
echo "2. 编辑配置文件: config/config.yaml"
echo "3. 运行工作流: python workflow.py words_sample.txt"
echo "4. 测试单词: python workflow.py test take"