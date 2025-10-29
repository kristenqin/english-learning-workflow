"""
飞书仓储实现 - 基础设施层
"""
import requests
import time
from typing import List, Dict, Any
from ...domain.repositories.learning_record_repository import LearningRecordRepository
from ...domain.entities.word import Word
from ...domain.value_objects.sentence import Sentence


class FeishuRepository(LearningRecordRepository):
    """飞书多维表格仓储实现"""
    
    def __init__(self, app_id: str, app_secret: str, app_token: str, table_id: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.app_token = app_token
        self.table_id = table_id
        self.base_url = "https://open.feishu.cn/open-apis"
        self.access_token = None
        self.token_expires_at = 0
    
    def save_word_record(self, word: Word, sentence: Sentence) -> bool:
        """保存单词学习记录"""
        try:
            token = self._get_access_token()
            
            url = f"{self.base_url}/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            payload = {
                "fields": {
                    "单词": word.text,
                    "定义": word.definition.text if word.definition else "",
                    "例句": sentence.text,
                    "解释": sentence.explanation or ""
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("code") == 0
            else:
                print(f"写入失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"写入记录异常: {str(e)}")
            return False
    
    def save_batch_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量保存学习记录"""
        success_count = 0
        failed_count = 0
        failed_records = []
        
        for i, record in enumerate(records):
            try:
                # 创建临时的Word和Sentence对象用于保存
                word = Word(text=record["word"])
                if record.get("definition"):
                    from ...domain.value_objects.definition import Definition
                    word.set_definition(Definition(text=record["definition"]))
                
                sentence = Sentence(text=record["sentence"])
                if record.get("explanation"):
                    sentence.set_explanation(record["explanation"])
                
                success = self.save_word_record(word, sentence)
                
                if success:
                    success_count += 1
                    print(f"✅ 记录 {i+1}/{len(records)} 写入成功")
                else:
                    failed_count += 1
                    failed_records.append(record)
                    print(f"❌ 记录 {i+1}/{len(records)} 写入失败")
                
                # 添加延迟避免API限制
                time.sleep(0.1)
                
            except Exception as e:
                failed_count += 1
                failed_records.append(record)
                print(f"❌ 记录 {i+1}/{len(records)} 写入异常: {str(e)}")
        
        return {
            "total": len(records),
            "success": success_count,
            "failed": failed_count,
            "failed_records": failed_records
        }
    
    def test_connection(self) -> bool:
        """测试连接"""
        try:
            token = self._get_access_token()
            
            url = f"{self.base_url}/bitable/v1/apps/{self.app_token}/tables"
            headers = {"Authorization": f"Bearer {token}"}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("code") == 0
            else:
                return False
                
        except Exception:
            return False
    
    def _get_access_token(self) -> str:
        """获取访问令牌"""
        # 检查token是否还有效
        if self.access_token and time.time() < (self.token_expires_at - 300):
            return self.access_token
        
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                self.access_token = result["tenant_access_token"]
                self.token_expires_at = time.time() + 7200
                return self.access_token
            else:
                raise Exception(f"获取token失败: {result.get('msg', '未知错误')}")
        else:
            raise Exception(f"HTTP请求失败，状态码: {response.status_code}")