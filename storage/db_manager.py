"""
MongoDB 数据库管理模块（异步版本）
用于保存和查询投资分析历史记录
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

try:
    from motor.motor_asyncio import AsyncIOMotorClient
    from pymongo import ASCENDING, DESCENDING
    from pymongo.errors import ConnectionFailure, OperationFailure
    MOTOR_AVAILABLE = True
except ImportError:
    MOTOR_AVAILABLE = False
    print("⚠️  motor 未安装，请运行: pip install motor")

# 加载环境变量
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass


class AnalysisRecordManager:
    """投资分析记录管理器（异步版本）"""
    
    def __init__(
        self,
        connection_string: Optional[str] = None,
        db_name: Optional[str] = None,
        collection_name: str = "analysis_records"
    ):
        """
        初始化数据库管理器
        
        Args:
            connection_string: MongoDB 连接字符串，默认从环境变量读取
            db_name: 数据库名称，默认从环境变量读取
            collection_name: 集合名称，默认为 analysis_records
        """
        if not MOTOR_AVAILABLE:
            raise ImportError("需要安装 motor 库")
        
        # 获取配置
        self.connection_string = connection_string or os.getenv(
            "MONGODB_URI", 
            "mongodb://localhost:27017/"
        )
        self.db_name = db_name or os.getenv(
            "MONGODB_DB_NAME",
            "muhe_opportunity_radar"
        )
        self.collection_name = collection_name
        
        # 连接数据库
        self.client = None
        self.db = None
        self.collection = None
        self._init_connection()
    
    def _init_connection(self):
        """初始化数据库连接"""
        try:
            self.client = AsyncIOMotorClient(
                self.connection_string,
                serverSelectionTimeoutMS=5000
            )
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            
            print(f"✓ 已初始化 MongoDB 连接: {self.db_name}.{self.collection_name}")
            
        except Exception as e:
            print(f"✗ MongoDB 初始化出错: {e}")
            self.client = None
    
    async def ensure_indexes(self):
        """创建数据库索引以提高查询性能（异步）"""
        if not self.client:
            return
            
        try:
            # 时间戳索引（降序，最新的在前）
            await self.collection.create_index([("created_at", DESCENDING)])
            
            # 投资者ID索引
            await self.collection.create_index("investor_id")
            
            # 复合索引：投资者+时间
            await self.collection.create_index([
                ("investor_id", ASCENDING),
                ("created_at", DESCENDING)
            ])
            
            print("✓ MongoDB 索引创建成功")
            
        except Exception as e:
            print(f"⚠️  创建索引时出错: {e}")
    
 
    async def save_analysis(
        self,
        material: str,
        investor_id: str,
        investor_name: str,
        analysis_result: str,
        additional_context: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Optional[str]:
        """
        保存单次分析记录（异步）
        
        Args:
            material: 分析材料
            investor_id: 投资者ID
            investor_name: 投资者名称
            analysis_result: 分析结果
            additional_context: 额外上下文
            metadata: 其他元数据
            
        Returns:
            记录的ID，失败返回None
        """
        if not self.client:
            print("⚠️  MongoDB 未连接，跳过保存")
            return None
        
        try:
            record = {
                "material": material,
                "investor_id": investor_id,
                "investor_name": investor_name,
                "analysis_result": analysis_result,
                "additional_context": additional_context,
                "metadata": metadata or {},
                "created_at": datetime.utcnow(),
                "material_length": len(material),
                "analysis_length": len(analysis_result)
            }
            
            result = await self.collection.insert_one(record)
            print(f"✓ 已保存分析记录: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"✗ 保存分析记录失败: {e}")
            return None
    
    async def save_comparison(
        self,
        material: str,
        investor_ids: List[str],
        analyses: List[Dict],
        comparison_summary: str,
        additional_context: Optional[str] = None
    ) -> Optional[str]:
        """
        保存多视角对比分析记录（异步）
        
        Args:
            material: 分析材料
            investor_ids: 投资者ID列表
            analyses: 各投资者的分析结果列表
            comparison_summary: 对比总结
            additional_context: 额外上下文
            
        Returns:
            记录的ID，失败返回None
        """
        if not self.client:
            print("⚠️  MongoDB 未连接，跳过保存")
            return None
        
        try:
            record = {
                "type": "comparison",
                "material": material,
                "investor_ids": investor_ids,
                "investor_count": len(investor_ids),
                "analyses": analyses,
                "comparison_summary": comparison_summary,
                "additional_context": additional_context,
                "created_at": datetime.utcnow(),
                "material_length": len(material)
            }
            
            result = await self.collection.insert_one(record)
            print(f"✓ 已保存对比分析记录: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"✗ 保存对比分析记录失败: {e}")
            return None
    
    async def get_recent_analyses(
        self,
        limit: int = 10,
        investor_id: Optional[str] = None
    ) -> List[Dict]:
        """
        获取最近的分析记录（异步）
        
        Args:
            limit: 返回记录数量
            investor_id: 可选的投资者ID筛选
            
        Returns:
            分析记录列表
        """
        if not self.client:
            return []
        
        try:
            query = {}
            if investor_id:
                query["investor_id"] = investor_id
            
            cursor = self.collection.find(query).sort(
                "created_at", DESCENDING
            ).limit(limit)
            
            return await cursor.to_list(length=limit)
            
        except Exception as e:
            print(f"✗ 查询分析记录失败: {e}")
            return []
    
    async def get_analysis_by_id(self, record_id: str) -> Optional[Dict]:
        """
        根据ID获取分析记录（异步）
        
        Args:
            record_id: 记录ID
            
        Returns:
            分析记录，不存在返回None
        """
        if not self.client:
            return None
        
        try:
            from bson.objectid import ObjectId
            return await self.collection.find_one({"_id": ObjectId(record_id)})
        except Exception as e:
            print(f"✗ 查询分析记录失败: {e}")
            return None
    
    async def search_analyses(
        self,
        keyword: str,
        limit: int = 20
    ) -> List[Dict]:
        """
        搜索分析记录（异步）
        
        Args:
            keyword: 搜索关键词
            limit: 返回记录数量
            
        Returns:
            匹配的分析记录列表
        """
        if not self.client:
            return []
        
        try:
            # 使用正则表达式搜索
            query = {
                "$or": [
                    {"material": {"$regex": keyword, "$options": "i"}},
                    {"analysis_result": {"$regex": keyword, "$options": "i"}},
                    {"investor_name": {"$regex": keyword, "$options": "i"}}
                ]
            }
            
            cursor = self.collection.find(query).sort(
                "created_at", DESCENDING
            ).limit(limit)
            
            return await cursor.to_list(length=limit)
            
        except Exception as e:
            print(f"✗ 搜索分析记录失败: {e}")
            return []
    
    async def get_statistics(self) -> Dict:
        """
        获取分析记录统计信息（异步）
        
        Returns:
            统计信息字典
        """
        if not self.client:
            return {}
        
        try:
            total_count = await self.collection.count_documents({})
            
            # 按投资者统计
            investor_stats = await self.collection.aggregate([
                {"$group": {
                    "_id": "$investor_id",
                    "count": {"$sum": 1},
                    "investor_name": {"$first": "$investor_name"}
                }},
                {"$sort": {"count": -1}}
            ]).to_list(length=None)
            
            # 按类型统计
            type_stats = await self.collection.aggregate([
                {"$group": {
                    "_id": "$type",
                    "count": {"$sum": 1}
                }}
            ]).to_list(length=None)
            
            return {
                "total_count": total_count,
                "investor_stats": investor_stats,
                "type_stats": type_stats
            }
            
        except Exception as e:
            print(f"✗ 获取统计信息失败: {e}")
            return {}
    
    def close(self):
        """关闭数据库连接"""
        if self.client:
            self.client.close()
            print("✓ MongoDB 连接已关闭")


if __name__ == '__main__':
    # 测试代码
    print("测试 MongoDB 数据库管理模块...\n")
    
    try:
        # 创建管理器
        manager = AnalysisRecordManager()
        
        # 测试保存单个分析
        print("\n测试保存单个分析记录：")
        record_id = manager.save_analysis(
            material="测试材料：某科技公司Q3财报",
            investor_id="buffett",
            investor_name="沃伦·巴菲特",
            analysis_result="这是一个测试分析结果...",
            additional_context="测试上下文",
            metadata={"test": True}
        )
        
        if record_id:
            print(f"记录ID: {record_id}")
        
        # 测试查询
        print("\n测试查询最近记录：")
        recent = manager.get_recent_analyses(limit=5)
        print(f"找到 {len(recent)} 条记录")
        
        # 测试统计
        print("\n测试统计信息：")
        stats = manager.get_statistics()
        print(f"总记录数: {stats.get('total_count', 0)}")
        
        # 关闭连接
        manager.close()
        
        print("\n✓ 测试完成")
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
