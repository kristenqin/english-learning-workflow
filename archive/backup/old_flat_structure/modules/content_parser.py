"""
内容解析模块 - 解析LLM输出的定义和例句
"""
import re
from typing import Dict, List


class ContentParser:
    """内容解析器"""
    
    def parse_definition_and_sentences(self, llm_output: str, current_word: str) -> Dict:
        """
        解析LLM输出，提取定义和例句列表
        
        Args:
            llm_output: LLM的输出内容
            current_word: 当前处理的单词
            
        Returns:
            Dict: 包含定义和例句的字典
        """
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
        """
        从文本行中提取定义
        
        Args:
            lines: 文本行列表
            word: 目标单词
            
        Returns:
            str: 提取的定义
        """
        definition = ""
        
        # 方法1: 查找包含 "—" 或 "–" 或 "-" 的行
        for line in lines:
            if '—' in line or '–' in line or '-' in line:
                # 提取 "单词 — 定义" 格式
                parts = re.split('[—–-]', line, 1)
                if len(parts) == 2:
                    definition = parts[1].strip()
                    # 去除可能的花括号
                    definition = re.sub(r'[{}]', '', definition)
                    break
        
        # 方法2: 如果没找到，尝试查找"定义"关键词后的内容
        if not definition:
            for i, line in enumerate(lines):
                if '定义' in line and '：' in line:
                    # 查找定义行后面的内容
                    definition_part = line.split('：', 1)
                    if len(definition_part) == 2:
                        potential_def = definition_part[1].strip()
                        if potential_def:
                            definition = potential_def
                            break
                    # 或者查找下一行
                    elif i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not next_line.startswith('-'):
                            definition = next_line
                            break
        
        # 方法3: 查找包含单词本身的定义行
        if not definition:
            for line in lines:
                line_lower = line.lower()
                word_lower = word.lower()
                if word_lower in line_lower and ('是' in line or '表示' in line or '指' in line):
                    definition = line.strip()
                    break
        
        return definition
    
    def _extract_sentences(self, lines: List[str]) -> List[str]:
        """
        从文本行中提取例句
        
        Args:
            lines: 文本行列表
            
        Returns:
            List[str]: 例句列表
        """
        sentences = []
        
        # 查找以特定符号开头的行作为例句
        for line in lines:
            line = line.strip()
            # 匹配以 -, •, *, 数字. 开头的行
            if (line.startswith('-') or 
                line.startswith('•') or 
                line.startswith('*') or
                re.match(r'^\d+\.', line)):
                
                # 清理开头的符号
                sentence = re.sub(r'^[-•*\d\.\s]+', '', line).strip()
                
                # 过滤掉空句子和太短的句子
                if sentence and len(sentence) > 3:
                    # 去除可能的花括号内容
                    sentence = re.sub(r'\{[^}]*\}', '', sentence).strip()
                    if sentence:
                        sentences.append(sentence)
        
        # 如果没有找到，尝试查找场景示例部分
        if not sentences:
            in_examples_section = False
            for line in lines:
                line = line.strip()
                if '场景示例' in line or '示例' in line:
                    in_examples_section = True
                    continue
                
                if in_examples_section and line:
                    # 如果遇到新的section，停止
                    if line.startswith('3️⃣') or line.startswith('##'):
                        break
                    
                    # 清理行并添加到例句
                    cleaned = re.sub(r'^[-•*\d\.\s]+', '', line).strip()
                    cleaned = re.sub(r'\{[^}]*\}', '', cleaned).strip()
                    if cleaned and len(cleaned) > 3:
                        sentences.append(cleaned)
        
        return sentences
    
    def validate_content(self, content: Dict) -> bool:
        """
        验证解析的内容是否有效
        
        Args:
            content: 解析后的内容字典
            
        Returns:
            bool: 内容是否有效
        """
        if not content:
            return False
        
        # 检查定义是否有效
        definition = content.get("definition", "")
        if not definition or "解析错误" in definition or "提取失败" in definition:
            return False
        
        # 检查例句数量
        sentences = content.get("sentences", [])
        if len(sentences) < 3:  # 至少需要3个例句
            return False
        
        return True
    
    def clean_text(self, text: str) -> str:
        """
        清理文本，去除不必要的字符
        
        Args:
            text: 原始文本
            
        Returns:
            str: 清理后的文本
        """
        if not text:
            return ""
        
        # 去除多余的空白字符
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 去除特殊符号
        text = re.sub(r'[{}（）()]', '', text)
        
        # 去除emoji符号（可选）
        text = re.sub(r'[📚🎯💡⚠️✅]', '', text)
        
        return text