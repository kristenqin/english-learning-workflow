"""
单词列表解析模块
"""
from typing import List


class WordParser:
    """单词列表解析器"""
    
    def parse_word_list(self, word_list_text: str) -> dict:
        """
        将输入的文本按行分割成单词列表
        
        Args:
            word_list_text: 包含单词的文本，每行一个单词
            
        Returns:
            dict: 包含单词列表和总数的字典
        """
        lines = word_list_text.strip().split('\n')
        words = [line.strip() for line in lines if line.strip()]
        
        return {
            "words": words,
            "total_count": len(words)
        }
    
    def parse_from_file(self, file_path: str) -> dict:
        """
        从文件中读取单词列表
        
        Args:
            file_path: 单词文件路径
            
        Returns:
            dict: 包含单词列表和总数的字典
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse_word_list(content)
        except FileNotFoundError:
            raise Exception(f"文件未找到: {file_path}")
        except Exception as e:
            raise Exception(f"读取文件失败: {str(e)}")
    
    def validate_words(self, words: List[str]) -> List[str]:
        """
        验证和清理单词列表
        
        Args:
            words: 单词列表
            
        Returns:
            List[str]: 清理后的单词列表
        """
        valid_words = []
        for word in words:
            # 去除空格和特殊字符，只保留字母
            cleaned_word = ''.join(c for c in word if c.isalpha()).lower()
            if cleaned_word and len(cleaned_word) > 1:
                valid_words.append(cleaned_word)
        
        # 去重
        return list(set(valid_words))