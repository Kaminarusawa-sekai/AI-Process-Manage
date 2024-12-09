

import langchain
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser

from models import model_api




# 定义一个更详细的提示模板
template = """
你是一个业务流程专家，我给你一个流程的名字和他所属于的流程大类，请你按照下面的示例为我写出如何执行这个流程
我的流程是{process_name}，所属类别是{process_classfication}

以下是示例部分，你可以参考示例：
## 流程名称：
识别竞争对手
## 目标：
明确了解行业内的主要竞争者
收集关于竞争对手的信息，以便制定有效的市场策略
## 步骤：
定义目标市场
确定您的产品或服务的目标市场。
明确您的客户群体是谁。
确定竞争对手类型
直接竞争对手：提供相同产品或服务的企业。
间接竞争对手：提供替代解决方案或满足相同需求的不同方式的企业。
潜在竞争对手：新进入市场的公司或即将推出相似产品的现有企业。
收集信息
使用网络搜索、行业报告、社交媒体、新闻报道等资源收集信息。
参加行业会议、展览和研讨会，直接与行业参与者交流。
访问竞争对手的网站，查看他们的产品和服务描述、价格策略等。
分析竞争对手的优势和劣势
使用SWOT分析（优势Strengths、劣势Weaknesses、机会Opportunities、威胁Threats）来评估每个竞争对手。
关注他们的市场定位、品牌形象、客户服务、技术创新等方面。
评估竞争对手的市场表现
查看市场份额、增长率、客户满意度等指标。
分析他们的营销策略、销售渠道和客户关系管理。
监控竞争对手动态
设置Google Alerts或其他通知系统，跟踪竞争对手的新动向。
定期更新竞争对手分析报告，确保信息的时效性。
利用收集到的信息
基于对竞争对手的理解，调整自己的市场策略。
发现并利用市场中的空白点或未被充分开发的机会。
持续学习与改进
将识别竞争对手的过程作为持续学习的一部分，定期回顾和更新竞争对手分析。
鼓励团队成员分享关于竞争对手的新发现和见解。
### 注意事项：
在收集和使用竞争对手信息时，要遵守法律法规，尊重知识产权。
确保所有数据来源的可靠性和准确性。
避免仅依赖公开资料，尝试获取第一手信息以获得更深入的洞察。

"""


def get_process_prompt(process_name,process_classfication):
    input={
        "process_name":process_name,
        "process_classfication":process_classfication
    }
    
    response=model_api.excute(template,input)
    # 使用链来获取响应"https://aichatlanba.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"
    
    return response





if __name__ == "__main__":
    # 用户输入示例
    process_name = "1.1.4.1 定义战略愿景"
    process_classfication="1 制定愿景和战略 1.1 定义业务理念和长期愿景 1.1.4 建立战略愿景"
    requirements = get_process_prompt(process_name,process_classfication)
    print(requirements)




