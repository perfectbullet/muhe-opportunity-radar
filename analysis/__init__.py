"""
Analysis 模块 - 多投资理念分析
"""

from .investor_profiles import (
    InvestorProfile,
    InvestorProfileManager,
    load_investor_profile,
    list_all_investors
)

from .perspective_analyzer import (
    PerspectiveAnalyzer,
    quick_analyze
)

__all__ = [
    'InvestorProfile',
    'InvestorProfileManager',
    'load_investor_profile',
    'list_all_investors',
    'PerspectiveAnalyzer',
    'quick_analyze',
]

__version__ = '1.0.0'
