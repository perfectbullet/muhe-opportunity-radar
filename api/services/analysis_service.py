"""分析服务 - 封装核心业务逻辑"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from typing import AsyncGenerator, Dict, Any, List
from analysis.perspective_analyzer import PerspectiveAnalyzer
from storage.db_manager import AnalysisRecordManager


class AnalysisService:
    """分析服务类 - 封装 PerspectiveAnalyzer 为异步接口"""
    
    def __init__(self, llm_provider: str = "siliconflow"):
        self.analyzer = PerspectiveAnalyzer(llm_provider=llm_provider)
        self.record_manager = AnalysisRecordManager()
    
    async def analyze_single_stream(
        self,
        material: str,
        investor_id: str,
        additional_context: str = None
    ) -> AsyncGenerator[str, None]:
        """
        单一视角流式分析
        
        yields: 流式文本片段
        """
        try:
            # 生成分析（这里需要修改 PerspectiveAnalyzer 支持流式输出）
            # 临时方案：一次性返回结果，模拟流式
            result = self.analyzer.analyze_from_perspective(
                material=material,
                investor_id=investor_id,
                additional_context=additional_context
            )
            
            # 模拟流式输出 - 每次返回一个字符
            analysis_text = result['analysis']
            chunk_size = 50  # 每次返回50个字符
            
            for i in range(0, len(analysis_text), chunk_size):
                chunk = analysis_text[i:i + chunk_size]
                yield chunk
                
        except Exception as e:
            yield f"\n\n❌ 分析出错: {str(e)}"
    
    async def analyze_single(
        self,
        material: str,
        investor_id: str,
        additional_context: str = None
    ) -> Dict[str, Any]:
        """
        单一视角完整分析
        
        Returns:
            包含 record_id, analysis 等字段的字典
        """
        result = self.analyzer.analyze_from_perspective(
            material=material,
            investor_id=investor_id,
            additional_context=additional_context
        )
        
        # 结果已包含 record_id（在 analyze_from_perspective 中已保存）
        return result
    
    async def compare_perspectives_stream(
        self,
        material: str,
        investor_ids: List[str],
        additional_context: str = None
    ) -> AsyncGenerator[str, None]:
        """
        多视角对比流式分析
        
        yields: 流式文本片段
        """
        try:
            result = self.analyzer.compare_perspectives(
                material=material,
                investor_ids=investor_ids,
                additional_context=additional_context
            )
            
            # 格式化输出
            output = "# 多视角对比分析\n\n"
            
            # 各投资者分析
            for analysis in result['analyses']:
                output += f"## {analysis['investor_name']} ({analysis['investor_title']})\n\n"
                output += f"{analysis['analysis']}\n\n"
                output += "---\n\n"
            
            # 综合对比
            output += "## 🔍 综合对比总结\n\n"
            output += result['comparison_summary']
            
            # 模拟流式输出
            chunk_size = 80
            for i in range(0, len(output), chunk_size):
                chunk = output[i:i + chunk_size]
                yield chunk
                
        except Exception as e:
            yield f"\n\n❌ 对比分析出错: {str(e)}"
    
    async def compare_perspectives(
        self,
        material: str,
        investor_ids: List[str],
        additional_context: str = None
    ) -> Dict[str, Any]:
        """
        多视角对比完整分析
        
        Returns:
            包含 record_id, analyses, comparison_summary 等字段的字典
        """
        result = self.analyzer.compare_perspectives(
            material=material,
            investor_ids=investor_ids,
            additional_context=additional_context
        )
        
        return result


# 全局服务实例
_analysis_service = None


def get_analysis_service() -> AnalysisService:
    """获取分析服务实例（单例模式）"""
    global _analysis_service
    if _analysis_service is None:
        _analysis_service = AnalysisService()
    return _analysis_service
