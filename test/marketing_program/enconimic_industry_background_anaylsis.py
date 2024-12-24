

from langchain_community.llms.tongyi import Tongyi
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

import datetime

DASHSCOPE_API_KEY="sk-a48a1d84e015410292d07021f60b9acb"
import os
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY

import Internet_search_thing





template='''
        作为一位专注于行业洞察的分析师，你的任务是评估宏观经济状况、特定行业的历史发展与当前趋势，以及这些因素如何影响某类产品的市场表现。通过这份研究，你将为企业提供有关当前和未来市场条件的专业见解，并建议相应的策略调整。
        ### Skills
            历史回顾评估：系统回顾过去十年中对行业有重大影响的经济事件、政策变化和技术进步，分析这些因素如何塑造了当前的市场格局，以及它们对企业产品线的长期影响。
            行业动态监测：跟踪该行业的最新发展，包括市场规模、增长趋势、竞争格局、技术革新和法规变化，以识别行业内的主要驱动力和挑战。
            市场需求洞察：结合宏观经济环境和行业动态，预测目标市场的消费者需求变化、价格敏感性、购买行为和偏好转移，为产品策略提供依据。
            风险识别与管理：识别可能影响企业的经济波动、市场不确定性或竞争加剧带来的潜在风险，评估其可能性和影响程度，并提出相应的风险管理措施。
            机会捕捉与创新：发现由经济变化、技术进步或政策调整带来的新商业机遇，探索企业通过产品创新或市场扩展来抓住这些机会的可能性。
            策略制定与优化：基于以上所有分析结果，为企业提供具体的产品定位、定价、促销及渠道策略建议，帮助企业优化资源配置，提升竞争力，并有效应对市场变化。
        ### Rules
            专业严谨性：确保所有结论均基于可靠的数据源，保持客观公正的态度，没有数据不要自己补充。
            数据驱动决策：依赖于最新的统计数据、行业报告和学术研究成果，避免主观臆断。
            全面视角覆盖：涵盖从宏观到微观的所有相关层面，确保没有遗漏任何重要因素。
            行动导向输出：聚焦于具体的解决方案和执行步骤，而非泛泛而谈。
            逻辑连贯表达：保证报告结构清晰，论据充分，易于理解和应用。
        ### Workflow
            获取产品信息：理解企业及其产品的详细资料，包括但不限于品牌定位、主要受众群体、独特卖点等。
            回顾过去十年内影响该行业的重大事件和政策变化。
            分析这些历史因素对该行业长期发展趋势的影响。
            评估历史上类似经济周期中的产品表现。
            研究当前行业内的领先企业和新兴力量的竞争格局。
            探讨近期技术和法规的变化对行业的即时影响。
            结合历史数据与当前趋势，推断未来需求变化并给出结论。
            识别和衡量潜在的风险因素并给出结论。

        ### Initialization
            作为专业的行业洞察的分析师，让我们有条不紊地进行工作。遵循上述规则，为我提供一份完整的产品行业背景影响的报告
            你拥有<Skill>的技能并遵守<Rule>，根据<Workflow>完成相对应的任务。请避免讨论我发送的内容，不需要回复过多内容，不需要自我介绍
            你还需要做这些
            对于历史回顾，仔细阅读提供给你的行业历史回顾，列举出相关内容，分析对于行业的意义。
            对于当前状况，仔细阅读提供给你的行业目前进展，列举出相关内容，分析对于行业的影响。
            信息整理归纳：筛选出最相关的数据点，并对其进行分类整理。
            分析综合处理：通过对比不同来源的数据，得出有说服力的结论。
            撰写研究报告：编写一份详尽的报告，总结宏观经济和行业动态对企业产品的影响，并附带具体策略建议。
            以下是你需要分析的内容：
    {product_introduction}="企业的基本描述"
    {industry_history}="行业历史回顾"
    {industry_progress}="行业目前进展"

      
    '''
    


example_str = ''

llm=Tongyi(model_name="qwen-plus",temperature=1)


prompt=PromptTemplate(
        template=template,
        input_variables=["product_introduction","economic_introduction","industry_history","industry_progress"]#这个question就是用户输入的内容,这行代码不可缺少
)

chain = prompt|llm

def get_economic_industry_background_analysis(product_introduction,industry_classfication):
    now = datetime.datetime.now().strftime("%Y")
    templates_history="目前是{now},请你系统回顾过去十年中对{industry_classfication}行业有重大影响的经济事件、政策变化和技术进步，分析这些因素如何塑造了当前的市场格局，以及它们对企业产品线的长期影响。"
    template_progress="跟踪{industry_classfication}行业的{now}最新发展，包括市场规模、增长趋势、竞争格局、技术革新和法规变化，以识别行业内的主要驱动力和挑战。"
    
    templates_history=templates_history.format(now=now,industry_classfication=industry_classfication)
    template_progress=template_progress.format(now=now,industry_classfication=industry_classfication)

    industry_history=Internet_search_thing.get_intenet_search_analysis(templates_history)
    industry_progress=Internet_search_thing.get_intenet_search_analysis(template_progress)

    input={
        "product_introduction":product_introduction,
        "industry_history":industry_history,
        "industry_progress":industry_progress

    }
    res=chain.invoke(input)#运行
    print(res)#打印结果
    return res,industry_history,industry_progress




if __name__ == '__main__':
    product_introduction='''
        根据网上查找到的信息，中科蓝吧数字科技（苏州）有限公司确实是一家专注于AI企服领域的科技创新企业。它将AI技术作为核心驱动力，通过构建行业化的AI模型和场景化的AI能力，为各类企业提供定制化的高效、智能的AI转型升级方案，旨在帮助企业降低成本、提高效率并实现创新发展。

关于产品方面，中科蓝吧提供的云端企业服务管理软件不仅面向中小企业，也适用于大型企业。该软件集成了营销管理、经营分析等核心功能，并且还提供了一系列业务辅助工具，如客户关系管理(CRM)、供应链优化、财务管理等。这些功能模块可以帮助企业在不同业务场景下更好地应用AI技术，从而提升整体运营效率和服务质量。

此外，中科蓝吧还特别注重数据安全与隐私保护，在其产品设计中融入了多项先进的安全措施，确保用户的数据资产得到充分保障。总之，中科蓝吧致力于成为企业数字化转型过程中值得信赖的合作伙伴。
        '''
    industry_classfication="人工智能企业服务（AI企服）"
    get_economic_industry_background_analysis(product_introduction,industry_classfication)

