"""
飞书API客户端模块
"""
import requests
import json
from typing import Dict, Any
import time


class FeishuClient:
    """飞书多维表格客户端"""
    
    def __init__(self, app_id: str, app_secret: str, app_token: str, table_id: str):
        """
        初始化飞书客户端
        
        Args:
            app_id: 飞书应用ID
            app_secret: 飞书应用密钥
            app_token: 多维表格App Token
            table_id: 表格ID
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.app_token = app_token
        self.table_id = table_id
        self.base_url = "https://open.feishu.cn/open-apis"
        self.access_token = None
        self.token_expires_at = 0
    
    def get_access_token(self) -> str:
        """
        获取访问令牌
        
        Returns:
            str: 访问令牌
        """
        # 检查token是否还有效（提前5分钟刷新）
        if self.access_token and time.time() < (self.token_expires_at - 300):
            return self.access_token
        
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    self.access_token = result["tenant_access_token"]
                    # 飞书token有效期2小时，记录过期时间
                    self.token_expires_at = time.time() + 7200
                    return self.access_token
                else:
                    raise Exception(f"获取token失败: {result.get('msg', '未知错误')}")
            else:
                raise Exception(f"HTTP请求失败，状态码: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def write_record(self, word: str, definition: str, sentence: str, explanation: str) -> bool:
        """
        写入一条记录到飞书表格
        
        Args:
            word: 单词
            definition: 定义
            sentence: 例句
            explanation: 解释
            
        Returns:
            bool: 是否写入成功
        """
        try:
            token = self.get_access_token()
            
            url = f"{self.base_url}/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            payload = {
                "fields": {
                    "单词": word,
                    "定义": definition,
                    "例句": sentence,
                    "解释": explanation
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    return True
                else:
                    print(f"写入记录失败: {result.get('msg', '未知错误')}")
                    return False
            else:
                print(f"HTTP请求失败，状态码: {response.status_code}, 响应: {response.text}")
                return False
                
        except Exception as e:
            print(f"写入记录异常: {str(e)}")
            return False
    
    def batch_write_records(self, records: list) -> Dict[str, Any]:
        """
        批量写入记录
        
        Args:
            records: 记录列表，每个记录包含word, definition, sentence, explanation
            
        Returns:
            Dict: 写入结果统计
        """
        success_count = 0
        failed_count = 0
        failed_records = []
        
        for i, record in enumerate(records):
            try:
                success = self.write_record(
                    record["word"],
                    record["definition"], 
                    record["sentence"],
                    record["explanation"]
                )
                
                if success:
                    success_count += 1
                    print(f"✅ 记录 {i+1}/{len(records)} 写入成功: {record['word']} - {record['sentence'][:30]}...")
                else:
                    failed_count += 1
                    failed_records.append(record)
                    print(f"❌ 记录 {i+1}/{len(records)} 写入失败: {record['word']}")
                
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
        """
        测试飞书连接
        
        Returns:
            bool: 连接是否正常
        """
        try:
            token = self.get_access_token()
            
            # 测试获取表格列表（更可靠的测试方法）
            url = f"{self.base_url}/bitable/v1/apps/{self.app_token}/tables"
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("code") == 0
            else:
                return False
                
        except Exception:
            return False
    
    def get_table_fields(self) -> list:
        """
        获取表格字段信息
        
        Returns:
            list: 字段列表
        """
        try:
            token = self.get_access_token()
            
            url = f"{self.base_url}/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/fields"
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    return result.get("data", {}).get("items", [])
            
            return []
            
        except Exception as e:
            print(f"获取字段信息失败: {str(e)}")
            return []
    
    def clear_table(self) -> bool:
        """
        清空表格数据（谨慎使用）
        
        Returns:
            bool: 是否成功
        """
        print("⚠️ 此功能会删除表格中的所有数据，请确认后再使用")
        return False