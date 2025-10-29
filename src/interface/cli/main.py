"""
命令行接口 - 接口层
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from src.infrastructure.container import Container


class CLI:
    """命令行接口"""
    
    def __init__(self):
        self.container = Container()
    
    def run(self, args):
        """运行CLI"""
        if len(args) < 2:
            self._show_usage()
            return
        
        try:
            # 验证配置
            if not self.container.validate_configuration():
                print("❌ 配置文件验证失败，请检查API密钥配置")
                return
            
            workflow = self.container.get_workflow()
            
            if args[1] == "test" and len(args) > 2:
                # 测试模式
                result = workflow.execute_test_workflow(args[2])
                print(f"\\n测试结果: {result}")
            else:
                # 批量模式
                word_file = args[1]
                result = workflow.execute_batch_workflow(word_file_path=word_file)
                print(f"\\n最终结果: {result}")
                
        except Exception as e:
            print(f"❌ 程序执行失败: {str(e)}")
    
    def _show_usage(self):
        """显示使用说明"""
        print("使用方法:")
        print("  python -m src.interface.cli.main <单词文件路径>")
        print("  python -m src.interface.cli.main test <单词>")


def main():
    """主函数"""
    cli = CLI()
    cli.run(sys.argv)


if __name__ == "__main__":
    main()