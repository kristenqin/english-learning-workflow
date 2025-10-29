"""
定义值对象
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Definition:
    """定义值对象 - 不可变"""
    
    text: str
    principle_type: str = "first_principle"  # 第一性原理
    
    def __post_init__(self):
        if not self.text or not self.text.strip():
            raise ValueError("定义不能为空")
        if len(self.text) > 500:
            raise ValueError("定义过长")
    
    @property
    def clean_text(self) -> str:
        """获取清理后的文本"""
        return self.text.strip()
    
    def __str__(self) -> str:
        return self.clean_text