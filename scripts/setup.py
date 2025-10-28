#!/usr/bin/env python3
"""
英语学习工作流设置脚本
"""
import os
import shutil
import sys


def setup_project():
    """设置项目"""
    print("🚀 开始设置英语学习工作流项目")
    
    # 1. 检查并创建配置文件
    config_file = "config/config.yaml"
    config_example = "config/config.example.yaml"
    
    if not os.path.exists(config_file):
        if os.path.exists(config_example):
            shutil.copy(config_example, config_file)
            print(f"✅ 已创建配置文件: {config_file}")
            print("⚠️  请编辑 config/config.yaml 填入您的API密钥")
        else:
            print(f"❌ 找不到配置模板文件: {config_example}")
            return False
    else:
        print(f"✅ 配置文件已存在: {config_file}")
    
    # 2. 检查依赖
    try:
        import yaml
        import requests
        print("✅ 核心依赖已安装")
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    # 3. 创建日志目录
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"✅ 已创建日志目录: {log_dir}")
    
    # 4. 测试模块导入
    try:
        from modules.word_parser import WordParser
        from modules.llm_client import LLMClient
        from modules.content_parser import ContentParser
        from modules.feishu_client import FeishuClient
        print("✅ 所有模块导入正常")
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False
    
    print("\\n🎉 项目设置完成！")
    print("\\n下一步:")
    print("1. 编辑 config/config.yaml 填入您的API密钥")
    print("2. 准备单词文件 (如 words.txt)")
    print("3. 运行: python workflow.py words.txt")
    
    return True


def check_config():
    """检查配置文件"""
    config_file = "config/config.yaml"
    
    if not os.path.exists(config_file):
        print(f"❌ 配置文件不存在: {config_file}")
        return False
    
    try:
        import yaml
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 检查必要配置
        required_keys = [
            'deepseek.api_key',
            'feishu.app_id', 
            'feishu.app_secret',
            'feishu.app_token',
            'feishu.table_id'
        ]
        
        for key_path in required_keys:
            keys = key_path.split('.')
            value = config
            for key in keys:
                value = value.get(key, '')
            
            if not value or value.startswith('YOUR_'):
                print(f"❌ 配置项未设置: {key_path}")
                return False
        
        print("✅ 配置文件检查通过")
        return True
        
    except Exception as e:
        print(f"❌ 配置文件格式错误: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_config()
    else:
        setup_project()