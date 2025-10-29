"""
单词领域实体
"""
from dataclasses import dataclass
from typing import List, Optional
from ..value_objects.definition import Definition
from ..value_objects.sentence import Sentence


@dataclass
class Word:
    """单词实体"""
    
    text: str
    definition: Optional[Definition] = None
    sentences: List[Sentence] = None
    
    def __post_init__(self):
        if self.sentences is None:
            self.sentences = []
    
    def set_definition(self, definition: Definition) -> None:
        """设置定义"""
        self.definition = definition
    
    def add_sentence(self, sentence: Sentence) -> None:
        """添加例句"""
        self.sentences.append(sentence)
    
    def get_sentence_count(self) -> int:
        """获取例句数量"""
        return len(self.sentences)
    
    def is_processed(self) -> bool:
        """判断是否已处理完成"""
        return (self.definition is not None and 
                len(self.sentences) > 0 and
                all(s.explanation is not None for s in self.sentences))
    
    def __str__(self) -> str:
        return f"Word('{self.text}', {len(self.sentences)} sentences)"