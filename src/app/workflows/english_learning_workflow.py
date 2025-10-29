"""
英语学习工作流编排器
"""
import time
from typing import Dict, Any, Optional
from ..services.word_learning_app_service import WordLearningAppService


class EnglishLearningWorkflow:
    """英语学习工作流编排器"""
    
    def __init__(self, app_service: WordLearningAppService):
        self.app_service = app_service
    
    def execute_batch_workflow(
        self, 
        word_list_text: Optional[str] = None, 
        word_file_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """执行批量学习工作流"""
        print("🚀 开始执行英语单词学习工作流")
        start_time = time.time()
        
        try:
            # 1. 获取输入
            if word_file_path:
                with open(word_file_path, 'r', encoding='utf-8') as f:
                    word_list_text = f.read()
            
            if not word_list_text:
                raise Exception("请提供单词列表文本或文件路径")
            
            print("\\n📝 步骤1: 解析单词列表")
            
            # 2. 测试连接
            print("\\n🔗 步骤2: 测试API连接")
            # 这里可以添加连接测试逻辑
            
            # 3. 处理单词列表
            print("\\n🧠 步骤3: 处理单词和生成内容")
            result = self.app_service.process_word_list(word_list_text)
            
            # 4. 生成结果报告
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            if result["status"] == "success":
                result["duration_seconds"] = duration
                
                print(f"\\n🎉 工作流执行完成！")
                print(f"📊 处理统计:")
                print(f"  - 单词数量: {result['progress']['total_words']}")
                print(f"  - 生成记录: {result['records_created']}")
                print(f"  - 耗时: {duration} 秒")
            
            return result
            
        except Exception as e:
            print(f"\\n❌ 工作流执行失败: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "duration_seconds": round(time.time() - start_time, 2)
            }
    
    def execute_test_workflow(self, word: str) -> Dict[str, Any]:
        """执行单词测试工作流"""
        print(f"🧪 测试模式: 处理单词 '{word}'")
        
        try:
            result = self.app_service.process_single_word_test(word)
            
            if result["status"] == "success":
                print("1. 生成定义和例句...")
                print(f"定义: {result['definition']}")
                print(f"例句: {result['sentence']}")
                print(f"解释: {result['explanation']}")
                print(f"总例句数: {result['total_sentences']}")
            
            return result
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}