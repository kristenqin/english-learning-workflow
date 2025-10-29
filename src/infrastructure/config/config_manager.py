"""
配置管理器 - 基础设施层
"""
import yaml
import os
from typing import Dict, Any


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self._config = None
    
    @property
    def config(self) -> Dict[str, Any]:
        """获取配置"""
        if self._config is None:
            self._config = self._load_config()
        return self._config
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            raise Exception(f"配置文件加载失败: {str(e)}")
    
    def get_deepseek_config(self) -> Dict[str, str]:
        """获取DeepSeek配置"""
        return self.config.get("deepseek", {})
    
    def get_feishu_config(self) -> Dict[str, str]:
        """获取飞书配置"""
        return self.config.get("feishu", {})
    
    def get_workflow_config(self) -> Dict[str, Any]:
        """获取工作流配置"""
        return self.config.get("workflow", {})
    
    def validate_config(self) -> bool:
        """验证配置完整性"""
        required_keys = [
            'deepseek.api_key',
            'feishu.app_id', 
            'feishu.app_secret',
            'feishu.app_token',
            'feishu.table_id'
        ]
        
        for key_path in required_keys:
            keys = key_path.split('.')
            value = self.config
            for key in keys:
                value = value.get(key, '')
            
            if not value or str(value).startswith('YOUR_'):
                return False
        
        return True