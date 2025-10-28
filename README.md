# 英语单词学习工作流

本项目是一个基于Python的本地英语学习工作流，可以自动为英语单词生成第一性原理定义、例句和解释，并写入飞书多维表格。

## 功能特点

✅ **第一性原理学习** - 为每个单词生成深层次的本质定义  
✅ **丰富例句** - 自动生成10+个不同场景的使用例句  
✅ **智能解释** - 基于定义对每个例句进行详细解释  
✅ **飞书集成** - 自动写入飞书多维表格，便于复习和管理  
✅ **本地运行** - 无需依赖在线工作流平台  
✅ **批量处理** - 支持批量处理多个单词  
✅ **多语言支持** - 支持中英文单词学习

## 项目结构

```
english-learning-workflow/
├── README.md                 # 项目说明
├── requirements.txt          # 依赖包
├── workflow.py              # 主工作流程序
├── config/                  # 配置文件
│   ├── config.example.yaml  # 配置模板
│   └── config.yaml          # 实际配置（需要手动创建）
├── modules/                 # 核心模块
│   ├── word_parser.py       # 单词解析
│   ├── llm_client.py        # LLM调用
│   ├── content_parser.py    # 内容解析
│   └── feishu_client.py     # 飞书API
├── scripts/                 # 安装和设置脚本
│   ├── install.sh           # 自动安装脚本
│   └── setup.py            # 项目设置
├── examples/                # 示例文件
│   ├── english_words.txt    # 英文单词示例
│   ├── chinese_words.txt    # 中文单词示例
│   └── words_sample.txt     # 基础示例
├── docs/                    # 文档
│   ├── USAGE.md            # 详细使用指南
│   └── Dify工作流搭建指南.md  # Dify平台对比
└── archive/                 # 归档文件
```

## 快速开始

### 1. 安装和配置

```bash
# 一键安装
./scripts/install.sh

# 或手动安装
pip install -r requirements.txt

# 配置API密钥
cp config/config.example.yaml config/config.yaml
# 编辑 config/config.yaml 填入你的API密钥
```

### 2. 基本用法

```bash
# 激活虚拟环境
source venv/bin/activate

# 测试单个单词
python workflow.py test 学习

# 处理示例文件
python workflow.py examples/english_words.txt
python workflow.py examples/chinese_words.txt

# 处理自定义单词文件
python workflow.py your_words.txt
```

## 配置说明

详细配置请参考 `config/config.example.yaml` 和 `docs/USAGE.md`。