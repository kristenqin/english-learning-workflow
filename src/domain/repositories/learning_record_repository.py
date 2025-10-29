"""
学习记录仓储接口
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..entities.word import Word
from ..value_objects.sentence import Sentence


class LearningRecordRepository(ABC):
    """学习记录仓储接口"""
    
    @abstractmethod
    def save_word_record(self, word: Word, sentence: Sentence) -> bool:
        """保存单词学习记录"""
        pass
    
    @abstractmethod
    def save_batch_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量保存学习记录"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """测试连接"""
        pass