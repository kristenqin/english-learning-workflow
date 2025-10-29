"""
内容解析工具 - 共享层
"""
import re
from typing import Dict, List


class ContentParser:
    """内容解析器"""
    
    def parse_definition_and_sentences(self, llm_output: str, current_word: str) -> Dict:
        """解析LLM输出，提取定义和例句列表"""
        try:
            lines = llm_output.strip().split('\n')
            
            # 提取定义
            definition = self._extract_definition(lines, current_word)
            
            # 提取例句
            sentences = self._extract_sentences(lines)
            
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
    
    def _extract_definition(self, lines: List[str], word: str) -> str:
        """从文本行中提取定义"""
        definition = ""
        
        # 方法1: 查找包含 "—" 或 "–" 或 "-" 的行
        for line in lines:
            if '—' in line or '–' in line or '-' in line:
                parts = re.split('[—–-]', line, 1)
                if len(parts) == 2:
                    definition = parts[1].strip()
                    definition = re.sub(r'[{}]', '', definition)
                    break
        
        # 方法2: 如果没找到，尝试查找"定义"关键词后的内容
        if not definition:
            for i, line in enumerate(lines):
                if '定义' in line and '：' in line:
                    definition_part = line.split('：', 1)
                    if len(definition_part) == 2:
                        potential_def = definition_part[1].strip()
                        if potential_def:
                            definition = potential_def
                            break
                    elif i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not next_line.startswith('-'):
                            definition = next_line
                            break
        
        return definition
    
    def _extract_sentences(self, lines: List[str]) -> List[str]:
        """从文本行中提取例句"""
        sentences = []
        
        for line in lines:
            line = line.strip()
            if (line.startswith('-') or 
                line.startswith('•') or 
                line.startswith('*') or
                re.match(r'^\d+\.', line)):
                
                sentence = re.sub(r'^[-•*\d\.\s]+', '', line).strip()
                
                if sentence and len(sentence) > 3:
                    sentence = re.sub(r'\{[^}]*\}', '', sentence).strip()
                    if sentence:
                        sentences.append(sentence)
        
        return sentences
    
    def clean_text(self, text: str) -> str:
        """清理文本"""
        if not text:
            return ""
        
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[{}（）()]', '', text)
        text = re.sub(r'[📚🎯💡⚠️✅]', '', text)
        
        return text