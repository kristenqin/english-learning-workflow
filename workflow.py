"""
英语单词学习工作流主控制器
"""
import os
import sys
import yaml
import time
from typing import List, Dict, Any
from modules.word_parser import WordParser
from modules.llm_client import LLMClient
from modules.content_parser import ContentParser
from modules.feishu_client import FeishuClient


class EnglishLearningWorkflow:
    """英语学习工作流"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        初始化工作流
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self.load_config(config_path)
        self.word_parser = WordParser()
        self.content_parser = ContentParser()
        
        # 初始化LLM客户端
        self.llm_client = LLMClient(
            api_key=self.config["deepseek"]["api_key"],
            base_url=self.config["deepseek"].get("base_url", "https://api.deepseek.com")
        )
        
        # 初始化飞书客户端
        self.feishu_client = FeishuClient(
            app_id=self.config["feishu"]["app_id"],
            app_secret=self.config["feishu"]["app_secret"],
            app_token=self.config["feishu"]["app_token"],
            table_id=self.config["feishu"]["table_id"]
        )
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            Dict: 配置字典
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            raise Exception(f"配置文件加载失败: {str(e)}")
    
    def run_workflow(self, word_list_text: str = None, word_file_path: str = None) -> Dict[str, Any]:
        """
        运行完整工作流
        
        Args:
            word_list_text: 单词列表文本
            word_file_path: 单词文件路径
            
        Returns:
            Dict: 执行结果
        """
        print("🚀 开始执行英语单词学习工作流")
        start_time = time.time()
        
        try:
            # 1. 解析单词列表
            print("\\n📝 步骤1: 解析单词列表")
            if word_file_path:
                word_result = self.word_parser.parse_from_file(word_file_path)
            elif word_list_text:
                word_result = self.word_parser.parse_word_list(word_list_text)
            else:
                raise Exception("请提供单词列表文本或文件路径")
            
            words = word_result["words"]
            words = self.word_parser.validate_words(words)
            print(f"✅ 解析完成，共 {len(words)} 个单词: {', '.join(words[:5])}{'...' if len(words) > 5 else ''}")
            
            # 2. 测试连接
            print("\\n🔗 步骤2: 测试API连接")
            if not self.llm_client.test_connection():
                raise Exception("DeepSeek API 连接失败，请检查API Key")
            print("✅ DeepSeek API 连接正常")
            
            if not self.feishu_client.test_connection():
                raise Exception("飞书API连接失败，请检查配置")
            print("✅ 飞书API连接正常")
            
            # 3. 处理每个单词
            print("\\n🧠 步骤3: 处理单词和生成内容")
            all_records = []
            
            for i, word in enumerate(words):
                print(f"\\n📖 处理单词 {i+1}/{len(words)}: {word}")
                
                try:
                    # 生成定义和例句
                    print("  - 生成定义和例句...")
                    llm_output = self.llm_client.generate_definition_and_examples(word)
                    
                    # 解析定义和例句
                    content = self.content_parser.parse_definition_and_sentences(llm_output, word)
                    
                    if not self.content_parser.validate_content(content):
                        print(f"  ❌ 内容解析失败，跳过单词: {word}")
                        continue
                    
                    definition = content["definition"]
                    sentences = content["sentences"]
                    print(f"  ✅ 生成 {len(sentences)} 个例句")
                    
                    # 处理每个例句
                    for j, sentence in enumerate(sentences):
                        try:
                            print(f"    - 处理例句 {j+1}/{len(sentences)}")
                            
                            # 生成例句解释
                            explanation = self.llm_client.explain_sentence_usage(word, definition, sentence)
                            explanation = self.content_parser.clean_text(explanation)
                            
                            # 准备记录
                            record = {
                                "word": word,
                                "definition": definition,
                                "sentence": sentence,
                                "explanation": explanation
                            }
                            all_records.append(record)
                            
                            # 实时写入或批量写入
                            if self.config.get("workflow", {}).get("batch_write", False):
                                continue  # 批量模式，稍后写入
                            else:
                                # 实时写入模式
                                success = self.feishu_client.write_record(
                                    word, definition, sentence, explanation
                                )
                                if not success:
                                    print(f"    ❌ 写入失败")
                            
                            # 添加延迟避免API限制
                            time.sleep(self.config.get("workflow", {}).get("delay_seconds", 1))
                            
                        except Exception as e:
                            print(f"    ❌ 例句处理失败: {str(e)}")
                            continue
                    
                except Exception as e:
                    print(f"  ❌ 单词处理失败: {str(e)}")
                    continue
            
            # 4. 批量写入（如果启用）
            if self.config.get("workflow", {}).get("batch_write", False) and all_records:
                print(f"\\n💾 步骤4: 批量写入 {len(all_records)} 条记录到飞书")
                write_result = self.feishu_client.batch_write_records(all_records)
                print(f"✅ 批量写入完成: 成功 {write_result['success']}, 失败 {write_result['failed']}")
            
            # 5. 生成结果报告
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            result = {
                "status": "success",
                "total_words": len(words),
                "total_records": len(all_records),
                "duration_seconds": duration,
                "words_processed": words
            }
            
            print(f"\\n🎉 工作流执行完成！")
            print(f"📊 处理统计:")
            print(f"  - 单词数量: {result['total_words']}")
            print(f"  - 生成记录: {result['total_records']}")
            print(f"  - 耗时: {duration} 秒")
            
            return result
            
        except Exception as e:
            print(f"\\n❌ 工作流执行失败: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "duration_seconds": round(time.time() - start_time, 2)
            }
    
    def run_single_word(self, word: str) -> Dict[str, Any]:
        """
        处理单个单词（用于测试）
        
        Args:
            word: 目标单词
            
        Returns:
            Dict: 处理结果
        """
        print(f"🧪 测试模式: 处理单词 '{word}'")
        
        try:
            # 生成定义和例句
            print("1. 生成定义和例句...")
            llm_output = self.llm_client.generate_definition_and_examples(word)
            print(f"LLM输出:\\n{llm_output}\\n")
            
            # 解析内容
            print("2. 解析定义和例句...")
            content = self.content_parser.parse_definition_and_sentences(llm_output, word)
            print(f"解析结果: {content}\\n")
            
            if not content["sentences"]:
                return {"status": "failed", "error": "未找到有效例句"}
            
            # 处理第一个例句作为示例
            sentence = content["sentences"][0]
            print(f"3. 解释例句: {sentence}")
            explanation = self.llm_client.explain_sentence_usage(word, content["definition"], sentence)
            print(f"例句解释: {explanation}\\n")
            
            return {
                "status": "success",
                "word": word,
                "definition": content["definition"],
                "sentence": sentence,
                "explanation": explanation,
                "total_sentences": len(content["sentences"])
            }
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python workflow.py <单词文件路径>")
        print("  python workflow.py test <单词>")
        return
    
    try:
        workflow = EnglishLearningWorkflow()
        
        if sys.argv[1] == "test" and len(sys.argv) > 2:
            # 测试模式
            result = workflow.run_single_word(sys.argv[2])
            print(f"\\n测试结果: {result}")
        else:
            # 正常模式
            word_file = sys.argv[1]
            result = workflow.run_workflow(word_file_path=word_file)
            print(f"\\n最终结果: {result}")
            
    except Exception as e:
        print(f"❌ 程序执行失败: {str(e)}")


if __name__ == "__main__":
    main()