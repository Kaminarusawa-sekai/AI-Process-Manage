from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseExcuteLLModel(ABC):
    """抽象基类，所有具体步骤都应该继承自这个类"""

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行步骤逻辑，并返回更新后的上下文"""
        pass