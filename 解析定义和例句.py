import re

def main(llm_output: str, current_word: str) -> dict:
    """
    解析LLM输出，提取定义和例句列表
    """
    try:
        lines = llm_output.strip().split('\n')

        # 提取定义
        definition = ""
        for line in lines:
            if '—' in line or '–' in line or '-' in line:
                # 提取 "单词 — 定义" 格式
                parts = re.split('[—–-]', line, 1)
                if len(parts) == 2:
                    definition = parts[1].strip()
                    break

        # 如果没找到，尝试其他方式
        if not definition:
            for i, line in enumerate(lines):
                if '定义' in line and i + 1 < len(lines):
                    definition = lines[i + 1].strip()
                    break

        # 提取例句（以 - 或 • 开头的行）
        sentences = []
        for line in lines:
            line = line.strip()
            if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                sentence = line.lstrip('-•* ').strip()
                if sentence:
                    sentences.append(sentence)

        return {
            "definition": definition if definition else "定义提取失败",
            "sentences": sentences,
            "sentence_count": len(sentences)
        }
    except Exception as e:
        return {
            "definition": f"解析错误: {str(e)}",
            "sentences": [],
            "sentence_count": 0
        }