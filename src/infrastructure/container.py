"""
依赖注入容器 - 组装各层组件
"""
from ..domain.services.word_learning_service import WordLearningService
from ..app.services.word_learning_app_service import WordLearningAppService
from ..app.workflows.english_learning_workflow import EnglishLearningWorkflow
from .external_apis.deepseek_service import DeepSeekService
from .storage.feishu_repository import FeishuRepository
from .config.config_manager import ConfigManager
from ..shared.utils.content_parser import ContentParser


class Container:
    """依赖注入容器"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_manager = ConfigManager(config_path)
        self._instances = {}
    
    def get_workflow(self) -> EnglishLearningWorkflow:
        """获取工作流实例"""
        if 'workflow' not in self._instances:
            app_service = self.get_app_service()
            self._instances['workflow'] = EnglishLearningWorkflow(app_service)
        return self._instances['workflow']
    
    def get_app_service(self) -> WordLearningAppService:
        """获取应用服务实例"""
        if 'app_service' not in self._instances:
            word_service = self.get_word_service()
            record_repository = self.get_record_repository()
            llm_service = self.get_llm_service()
            content_parser = self.get_content_parser()
            
            self._instances['app_service'] = WordLearningAppService(
                word_service, record_repository, llm_service, content_parser
            )
        return self._instances['app_service']
    
    def get_word_service(self) -> WordLearningService:
        """获取单词服务实例"""
        if 'word_service' not in self._instances:
            self._instances['word_service'] = WordLearningService()
        return self._instances['word_service']
    
    def get_record_repository(self) -> FeishuRepository:
        """获取记录仓储实例"""
        if 'record_repository' not in self._instances:
            feishu_config = self.config_manager.get_feishu_config()
            self._instances['record_repository'] = FeishuRepository(
                app_id=feishu_config['app_id'],
                app_secret=feishu_config['app_secret'],
                app_token=feishu_config['app_token'],
                table_id=feishu_config['table_id']
            )
        return self._instances['record_repository']
    
    def get_llm_service(self) -> DeepSeekService:
        """获取LLM服务实例"""
        if 'llm_service' not in self._instances:
            deepseek_config = self.config_manager.get_deepseek_config()
            self._instances['llm_service'] = DeepSeekService(
                api_key=deepseek_config['api_key'],
                base_url=deepseek_config.get('base_url', 'https://api.deepseek.com')
            )
        return self._instances['llm_service']
    
    def get_content_parser(self) -> ContentParser:
        """获取内容解析器实例"""
        if 'content_parser' not in self._instances:
            self._instances['content_parser'] = ContentParser()
        return self._instances['content_parser']
    
    def validate_configuration(self) -> bool:
        """验证配置"""
        return self.config_manager.validate_config()