"""
单词学习领域服务
"""
from typing import List
from ..entities.word import Word
from ..value_objects.definition import Definition
from ..value_objects.sentence import Sentence


class WordLearningService:
    """单词学习领域服务 - 包含核心业务逻辑"""
    
    def validate_word_list(self, words: List[str]) -> List[str]:
        """验证和清理单词列表"""
        valid_words = []
        
        for word in words:
            cleaned = self._clean_word(word)
            if self._is_valid_word(cleaned):
                valid_words.append(cleaned)
        
        # 去重并保持顺序
        return list(dict.fromkeys(valid_words))
    
    def create_word_entities(self, word_texts: List[str]) -> List[Word]:
        """创建单词实体列表"""
        return [Word(text=text) for text in word_texts]
    
    def process_word_definition(self, word: Word, definition_text: str) -> None:
        """处理单词定义"""
        definition = Definition(text=definition_text)
        word.set_definition(definition)
    
    def process_word_sentences(self, word: Word, sentence_texts: List[str]) -> None:
        """处理单词例句"""
        for sentence_text in sentence_texts:
            if sentence_text and sentence_text.strip():
                sentence = Sentence(text=sentence_text)
                word.add_sentence(sentence)
    
    def process_sentence_explanation(self, sentence: Sentence, explanation: str) -> None:
        """处理例句解释"""
        sentence.set_explanation(explanation)
    
    def _clean_word(self, word: str) -> str:
        """清理单词"""
        if not word:
            return ""
        
        # 去除空格和特殊字符，只保留字母和常见字符
        cleaned = ''.join(c for c in word if c.isalpha() or c in '中文').strip()
        return cleaned.lower() if cleaned.isascii() else cleaned
    
    def _is_valid_word(self, word: str) -> bool:
        """验证单词是否有效"""
        return (word and 
                len(word) > 1 and 
                len(word) < 50 and
                not word.isdigit())
    
    def calculate_learning_progress(self, words: List[Word]) -> dict:
        """计算学习进度"""
        total_words = len(words)
        processed_words = len([w for w in words if w.is_processed()])
        total_sentences = sum(w.get_sentence_count() for w in words)
        explained_sentences = sum(
            len([s for s in w.sentences if s.has_explanation()]) 
            for w in words
        )
        
        return {
            "total_words": total_words,
            "processed_words": processed_words,
            "total_sentences": total_sentences,
            "explained_sentences": explained_sentences,
            "completion_rate": processed_words / total_words if total_words > 0 else 0
        }