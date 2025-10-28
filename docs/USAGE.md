# 使用指南

## 快速开始

### 1. 安装和配置

```bash
# 运行安装脚本
./scripts/install.sh

# 编辑配置文件
cp config/config.example.yaml config/config.yaml
# 然后编辑 config/config.yaml 填入你的API密钥
```

### 2. 基本用法

```bash
# 激活虚拟环境
source venv/bin/activate

# 测试单个单词
python workflow.py test 单词

# 处理单词文件
python workflow.py examples/english_words.txt
python workflow.py examples/chinese_words.txt
```

## 示例文件

- `examples/english_words.txt` - 英文单词示例
- `examples/chinese_words.txt` - 中文单词示例
- `examples/words_sample.txt` - 基础示例文件

## 配置说明

详见 `config/config.example.yaml` 中的注释说明。

## 故障排除

常见问题及解决方案请参考主 README.md 文件。