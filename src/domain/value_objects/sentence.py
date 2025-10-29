"""
例句值对象
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Sentence:
    """例句值对象"""
    
    text: str
    explanation: Optional[str] = None
    
    def __post_init__(self):
        if not self.text or not self.text.strip():
            raise ValueError("例句不能为空")
    
    @property
    def clean_text(self) -> str:
        """获取清理后的例句文本"""
        return self.text.strip()
    
    @property
    def clean_explanation(self) -> str:
        """获取清理后的解释文本"""
        return self.explanation.strip() if self.explanation else ""
    
    def set_explanation(self, explanation: str) -> None:
        """设置解释"""
        if not explanation or not explanation.strip():
            raise ValueError("解释不能为空")
        self.explanation = explanation.strip()
    
    def has_explanation(self) -> bool:
        """是否有解释"""
        return self.explanation is not None and len(self.explanation.strip()) > 0
    
    def __str__(self) -> str:
        return f"Sentence('{self.clean_text[:30]}...', explained={self.has_explanation()})"