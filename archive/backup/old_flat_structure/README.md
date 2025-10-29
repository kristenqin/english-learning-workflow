# 旧版本扁平架构备份

这个目录包含了项目重构前的扁平架构代码，保留用于参考。

## 备份内容

- `modules/` - 原有的扁平模块结构
  - `word_parser.py` - 单词解析
  - `llm_client.py` - LLM调用
  - `content_parser.py` - 内容解析
  - `feishu_client.py` - 飞书API
- `workflow_old.py` - 原有的主工作流文件

## 迁移说明

项目已重构为分层架构，新的入口是：
- `python main.py` - 使用新架构
- 或者使用具体模块：`python -m src.interface.cli.main`

## 兼容性

如果需要使用旧版本，可以：
1. 将 `modules/` 复制回根目录
2. 将 `workflow_old.py` 重命名为 `workflow.py`
3. 使用 `python workflow.py` 运行

但建议使用新的分层架构，具有更好的可维护性和扩展性。