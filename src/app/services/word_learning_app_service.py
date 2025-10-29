"""
单词学习应用服务 - 编排业务流程
"""
from typing import List, Dict, Any
from ...domain.entities.word import Word
from ...domain.services.word_learning_service import WordLearningService
from ...domain.repositories.learning_record_repository import LearningRecordRepository


class WordLearningAppService:
    """单词学习应用服务"""
    
    def __init__(
        self,
        word_service: WordLearningService,
        record_repository: LearningRecordRepository,
        llm_service: Any,  # 外部LLM服务
        content_parser: Any  # 内容解析器
    ):
        self.word_service = word_service
        self.record_repository = record_repository
        self.llm_service = llm_service
        self.content_parser = content_parser
    
    def process_word_list(self, word_list_text: str) -> Dict[str, Any]:
        """处理单词列表的完整流程"""
        try:
            # 1. 解析和验证单词
            raw_words = word_list_text.strip().split('\n')
            raw_words = [w.strip() for w in raw_words if w.strip()]
            
            valid_words = self.word_service.validate_word_list(raw_words)
            word_entities = self.word_service.create_word_entities(valid_words)
            
            # 2. 处理每个单词
            records = []
            for word in word_entities:
                word_records = self._process_single_word(word)
                records.extend(word_records)
            
            # 3. 批量保存记录
            save_result = self.record_repository.save_batch_records(records)
            
            # 4. 计算统计信息
            progress = self.word_service.calculate_learning_progress(word_entities)
            
            return {
                "status": "success",
                "words_processed": word_entities,
                "records_created": len(records),
                "save_result": save_result,
                "progress": progress
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "words_processed": [],
                "records_created": 0
            }
    
    def process_single_word_test(self, word_text: str) -> Dict[str, Any]:
        """处理单个单词（测试模式）"""
        try:
            # 验证单词
            valid_words = self.word_service.validate_word_list([word_text])
            if not valid_words:
                return {"status": "failed", "error": "无效的单词"}
            
            word = Word(text=valid_words[0])
            
            # 生成定义和例句
            self._generate_word_content(word)
            
            # 生成第一个例句的解释（测试模式只处理一个）
            if word.sentences:
                first_sentence = word.sentences[0]
                explanation = self.llm_service.explain_sentence_usage(
                    word.text, word.definition.text, first_sentence.text
                )
                self.word_service.process_sentence_explanation(first_sentence, explanation)
            
            return {
                "status": "success",
                "word": word.text,
                "definition": word.definition.text if word.definition else None,
                "sentence": first_sentence.text if word.sentences else None,
                "explanation": first_sentence.explanation if word.sentences and word.sentences[0].has_explanation() else None,
                "total_sentences": len(word.sentences)
            }
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def _process_single_word(self, word: Word) -> List[Dict[str, Any]]:
        """处理单个单词的完整流程"""
        records = []
        
        # 1. 生成定义和例句
        self._generate_word_content(word)
        
        # 2. 为每个例句生成解释并创建记录
        for sentence in word.sentences:
            try:
                # 生成解释
                explanation = self.llm_service.explain_sentence_usage(
                    word.text, word.definition.text, sentence.text
                )
                self.word_service.process_sentence_explanation(sentence, explanation)
                
                # 创建记录
                record = {
                    "word": word.text,
                    "definition": word.definition.text,
                    "sentence": sentence.text,
                    "explanation": sentence.explanation
                }
                records.append(record)
                
            except Exception as e:
                # 记录错误但继续处理其他例句
                print(f"处理例句失败: {str(e)}")
                continue
        
        return records
    
    def _generate_word_content(self, word: Word) -> None:
        """生成单词的定义和例句"""
        # 调用LLM生成定义和例句
        llm_output = self.llm_service.generate_definition_and_examples(word.text)
        
        # 解析LLM输出
        parsed_content = self.content_parser.parse_definition_and_sentences(
            llm_output, word.text
        )
        
        # 设置定义
        if parsed_content["definition"]:
            self.word_service.process_word_definition(word, parsed_content["definition"])
        
        # 添加例句
        if parsed_content["sentences"]:
            self.word_service.process_word_sentences(word, parsed_content["sentences"])