"""
DeepSeek API服务 - 基础设施层
"""
import requests
from typing import Dict, Any


class DeepSeekService:
    """DeepSeek API服务"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def generate_definition_and_examples(self, word: str) -> str:
        """生成单词的第一性原理定义和例句"""
        prompt = f"""请以第一性原理的风格对单词 "{word}" 给出定义，只用一句话总结其本质，不要多余分析或推导。
然后列出至少 10 个不同场景下的具体使用例句，让我可以感受这个单词在不同语境下的使用感受。

输出格式如下：
1️⃣ 定义（第一性原理一句话）：
{word} — {{一句话总结定义}}

2️⃣ 场景示例：
- {{示例句子1}}
- {{示例句子2}}
…
- {{示例句子10}}"""

        return self._call_api(prompt, max_tokens=2000, temperature=0.7)
    
    def explain_sentence_usage(self, word: str, definition: str, sentence: str) -> str:
        """解释例句中单词的用法"""
        prompt = f"""对于下面的单词，我给出了第一性原理定义：
{word} — {definition}

请根据这个定义解释句子中该单词的使用。只输出一句话，完整表达句子中该单词所体现的：

动作（动词体现的行为或过程）

状态（名词或形容词体现的存在或属性）

影响/掌控关系（副词、抽象名词、功能词体现的作用、影响或关系）

不要做额外解释或分析。

例子：
定义：take — 通过接触或意志将某物从外界引入自身掌控之中
输入：He took a deep breath.
输出：他通过意志将外界的空气引入身体，使之成为自身掌控的呼吸。

现在句子：{sentence}"""

        return self._call_api(prompt, max_tokens=500, temperature=0.7)
    
    def _call_api(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """调用DeepSeek API"""
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"API调用失败，状态码: {response.status_code}")
                
        except Exception as e:
            raise Exception(f"LLM调用失败: {str(e)}")
    
    def test_connection(self) -> bool:
        """测试API连接"""
        try:
            response = self._call_api("请回复：连接正常", max_tokens=10)
            return len(response) > 0
        except Exception:
            return False