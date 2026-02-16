#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气API测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.tools.agent_tools import get_weather

def test_weather_function():
    """测试天气功能"""
    print("🔍 测试天气API功能...")
    print("=" * 50)
    
    # 测试几个城市
    test_cities = ["北京", "上海", "广州", "深圳", "成都", "绵阳", "合肥", "杭州"]
    
    for city in test_cities:
        print(f"📍 城市: {city}")
        try:
            result = get_weather(city)
            print(f"🌤️  天气: {result}")
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
        print("-" * 30)
    
    print("✅ 测试完成!")

if __name__ == "__main__":
    test_weather_function()