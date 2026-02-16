import os
from utils.logger_handler import logger
from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
import random
from utils.config_handler import agent_conf
from utils.path_tool import get_abs_path
import requests
rag = RagSummarizeService()

user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010",]
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
             "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12", ]

external_data = {}


@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)


@tool(description="获取指定城市的天气，以消息字符串的形式返回")
def get_weather(city: str) -> str:
    """
    使用API恒州天气API获取真实天气信息
    需要在config/agent.yml中配置API ID和KEY
    """
    try:
        # 从配置文件读取API凭证
        api_id = agent_conf.get("weather_api_id", "10013023")
        api_key = agent_conf.get("weather_api_key", "4519d1d82ad334242a2d1a9632b1420b")
        
        if api_id == "10000000" or api_key == "your_key_here":
            logger.warning("[get_weather]请在config/agent.yml中配置正确的API ID和KEY")
            return _mock_weather_data(city)
        
        # 城市映射表（将常用城市名转换为API所需格式）
        city_mapping = {
            "北京": ("北京", "北京"),
            "上海": ("上海", "上海"),
            "广州": ("广东", "广州"),
            "深圳": ("广东", "深圳"),
            "杭州": ("浙江", "杭州"),
            "南京": ("江苏", "南京"),
            "成都": ("四川", "成都"),
            "重庆": ("重庆", "重庆"),
            "武汉": ("湖北", "武汉"),
            "西安": ("陕西", "西安"),
            "天津": ("天津", "天津"),
            "苏州": ("江苏", "苏州"),
            "长沙": ("湖南", "长沙"),
            "郑州": ("河南", "郑州"),
            "青岛": ("山东", "青岛"),
            "大连": ("辽宁", "大连"),
            "厦门": ("福建", "厦门"),
            "宁波": ("浙江", "宁波"),
            "无锡": ("江苏", "无锡"),
            "合肥": ("安徽", "合肥"),
            "绵阳": ("四川", "绵阳"),
        }
        
        # 获取省份和城市信息
        if city in city_mapping:
            sheng, place = city_mapping[city]
        else:
            # 如果城市不在映射表中，尝试直接使用城市名
            sheng = ""
            place = city
            logger.info(f"[get_weather]城市{city}未在映射表中，将直接查询")
        
        # 构造请求URL
        if sheng:
            url = f'https://cn.apihz.cn/api/tianqi/tqyb.php?id={api_id}&key={api_key}&sheng={sheng}&place={place}'
        else:
            url = f'https://cn.apihz.cn/api/tianqi/tqyb.php?id={api_id}&key={api_key}&place={place}'
        
        # 发送GET请求
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # 解析JSON响应
        data = response.json()
        print("成功",str(data))
        # 检查API返回状态
        if data.get('code') == 200:
            # 成功获取天气数据
            weather_info = f"城市{data.get('place', city)}天气为"
            
            # 处理天气状况
            weather1 = data.get('weather1', '')
            weather2 = data.get('weather2', '')
            
            if weather1 and weather2 and weather1 != weather2:
                weather_info += f"{weather1}转{weather2}"
            elif weather1:
                weather_info += weather1
            else:
                weather_info += "晴天"
            
            # 添加温度信息
            temperature = data.get('temperature', '')
            if temperature:
                weather_info += f"，气温{temperature}"
            
            # 添加湿度信息
            humidity = data.get('humidity', '')
            if humidity:
                weather_info += f"，湿度{humidity}%"
            
            # 添加风力信息
            wind_direction = data.get('windDirection', '')
            wind_scale = data.get('windScale', '')
            if wind_direction and wind_scale:
                weather_info += f"，{wind_direction}{wind_scale}"
            
            return weather_info
        else:
            # API返回错误
            error_msg = data.get('msg', '未知错误')
            logger.warning(f"[get_weather]API请求失败: {error_msg}")
            return _mock_weather_data(city)
            
    except requests.exceptions.Timeout:
        logger.error(f"[get_weather]{city}天气请求超时")
        return _mock_weather_data(city)
    except requests.exceptions.ConnectionError:
        logger.error(f"[get_weather]{city}天气连接失败")
        return _mock_weather_data(city)
    except requests.exceptions.RequestException as e:
        logger.error(f"[get_weather]{city}天气请求异常: {str(e)}")
        return _mock_weather_data(city)
    except Exception as e:
        logger.error(f"[get_weather]{city}获取天气时发生未知错误: {str(e)}")
        return _mock_weather_data(city)

def _mock_weather_data(city: str) -> str:
    """
    备用的模拟天气数据（当API调用失败时使用）
    """
    import random
    weather_types = ["晴天", "多云", "阴天", "小雨", "中雨", "晴转多云"]
    temperatures = ["22℃", "25℃", "28℃", "18℃", "20℃", "26℃"]
    humidity_levels = ["45%", "50%", "55%", "60%", "65%"]
    wind_conditions = ["南风1级", "北风2级", "东风1-2级", "西南风3级"]
    
    weather = random.choice(weather_types)
    temp = random.choice(temperatures)
    humidity = random.choice(humidity_levels)
    wind = random.choice(wind_conditions)
    
    return f"城市{city}天气为{weather}，气温{temp}，空气湿度{humidity}，{wind}"


@tool(description="获取用户所在城市的名称，以纯字符串形式返回")
def get_user_location() -> str:
    return random.choice(["深圳", "合肥", "杭州"])


@tool(description="获取用户的ID，以纯字符串形式返回")
def get_user_id() -> str:
    return random.choice(user_ids)


@tool(description="获取当前月份，以纯字符串形式返回")
def get_current_month() -> str:
    return random.choice(month_arr)


def generate_external_data():
    """
    {
        "user_id": {
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            ...
        },
        "user_id": {
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            ...
        },
        "user_id": {
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            ...
        },
        ...
    }
    :return:
    """
    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")

                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }


@tool(description="从外部系统中获取指定用户在指定月份的使用记录，以纯字符串形式返回， 如果未检索到返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()

    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"[fetch_external_data]未能检索到用户：{user_id}在{month}的使用记录数据")
        return ""


@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已调用"
