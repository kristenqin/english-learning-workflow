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

## 项目架构

采用**分层架构设计**，清晰分离各层职责：

```
english-learning-workflow/
├── 📄 main.py                   # 🆕 新架构主入口
├── 📄 requirements.txt          # 依赖包
├── 📁 src/                      # 🆕 分层架构源代码
│   ├── 🧠 domain/              # 领域层 - 核心业务逻辑
│   │   ├── entities/           # 实体 (Word, ...)
│   │   ├── value_objects/      # 值对象 (Definition, Sentence)
│   │   ├── services/           # 领域服务
│   │   └── repositories/       # 仓储接口
│   ├── 📱 app/                 # 应用层 - 业务流程编排
│   │   ├── workflows/          # 工作流编排
│   │   ├── services/           # 应用服务
│   │   └── handlers/           # 处理器
│   ├── 🔧 infrastructure/       # 基础设施层 - 外部依赖
│   │   ├── external_apis/      # 外部API (DeepSeek, 飞书)
│   │   ├── storage/            # 存储相关
│   │   ├── config/             # 配置管理
│   │   └── container.py        # 依赖注入容器
│   ├── 🖥️  interface/           # 接口层 - 用户交互
│   │   ├── cli/                # 命令行接口
│   │   └── api/                # 未来扩展API接口
│   └── 📚 shared/              # 共享层 - 通用工具
│       ├── utils/              # 工具函数
│       ├── exceptions/         # 异常定义
│       └── types/              # 类型定义
├── 📁 config/                  # 配置文件
├── 📁 scripts/                 # 安装和设置脚本
├── 📁 examples/                # 示例文件
├── 📁 docs/                    # 文档
├── 📁 archive/                 # 归档文件
└── 📁 backup/                  # 🆕 旧版本备份
    └── old_flat_structure/     # 扁平架构备份
```

### 🏗️ 架构优势

- **🎯 单一职责**: 每层专注特定职责
- **🔒 依赖倒置**: 高层不依赖低层实现
- **🧩 松耦合**: 各层间通过接口交互
- **🔧 易扩展**: 新功能容易添加
- **🧪 易测试**: 各层可独立测试

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

# 🆕 新架构 (推荐)
python main.py test 学习

# 处理示例文件
python main.py examples/english_words.txt
python main.py examples/chinese_words.txt

# 处理自定义单词文件
python main.py your_words.txt
```

## 配置说明

详细配置请参考 `config/config.example.yaml` 和 `docs/USAGE.md`。