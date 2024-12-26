

from langchain_community.llms.tongyi import Tongyi
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

import datetime

DASHSCOPE_API_KEY="sk-a48a1d84e015410292d07021f60b9acb"
import os
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY
import dashscope
dashscope.api_key="sk-a48a1d84e015410292d07021f60b9acb"

import Internet_search_thing





template='''
        作为一位专业的市场分析师，你的任务是对特定行业的市场环境进行全面的PESTEL分析。通过评估政治、经济、社会文化、技术、环境和法律因素，为企业提供有关当前市场条件的专业见解，并建议相应的策略调整。
        ### Skills
            1. **Political Factors (政治因素)**
            - 分析政府政策、法律法规的变化及其对企业运营的影响。
            - 探讨税收政策、贸易协定、关税、补贴等政策对行业成本结构和市场竞争的影响。
            - 识别国家或地区层面的政治稳定性和国际关系可能带来的风险与机遇。

            2. **Economic Factors (经济因素)**
            - 深入研究宏观经济状况，包括GDP增长率、通货膨胀率、失业率、汇率波动、GDP增长率、通货膨胀率、利率、消费者信心指数等因素。
            - 分析这些经济指标对企业收入、成本和利润的潜在影响。
            - 探讨全球经济趋势及本地经济环境之间的相互作用。

            3. **Social/Cultural Factors (社会文化因素)**
            - 研究消费者偏好、生活方式和社会习惯的变化趋势。
            - 了解人口统计特征（如年龄分布、性别比例、家庭结构）对市场需求的影响。
            - 探讨社交媒体、文化潮流以及社会价值观转变对产品接受度的作用。

            4. **Technological Factors (技术因素)**
            - 分析技术创新的速度和技术进步对企业产品和服务的影响。
            - 探讨新兴技术（如人工智能、物联网、区块链等）的应用前景及其对企业竞争力的提升。
            - 评估企业内部研发能力和外部技术合作的可能性。

            5. **Environmental Factors (环境因素)**
            - 考察环保法规对企业生产过程和供应链管理的要求。
            - 分析消费者对绿色产品和可持续发展的关注度增加对企业战略的影响。
            - 探讨气候变化、资源枯竭等问题可能带来的长期挑战和机会。

            6. **Legal Factors (法律因素)**
            - 审查相关行业的法律法规，特别是和行业相关的法律等方面的规定。
            - 评估新出台或即将实施的法律对企业合规成本和业务模式的影响。
            - 探讨跨国经营中不同司法管辖区之间的法律差异及应对策略。
        ### Rules
            专业严谨性：确保所有结论均基于可靠的数据源，保持客观公正的态度，没有数据不要自己补充。
            数据驱动决策：依赖于最新的统计数据、行业报告和学术研究成果，避免主观臆断。
            全面视角覆盖：涵盖从宏观到微观的所有相关层面，确保没有遗漏任何重要因素。
            行动导向输出：聚焦于具体的解决方案和执行步骤，而非泛泛而谈。
            逻辑连贯表达：保证报告结构清晰，论据充分，易于理解和应用。
        ### Workflow

            1. 对于每个因素，整理并分析所收集的数据，找出关键点和趋势。评估这些因素如何相互作用，共同影响市场环境和对行业的影响。
            2. 基于分析结果，确定哪些因素最有可能影响企业的短期和长期发展。
            3. 根据以上所有发现，提出具体的战略建议，帮助企业更好地适应市场变化。

        ### Initialization
            作为专业的行业洞察的分析师，让我们有条不紊地进行工作。遵循上述规则，为我提供一份完整的产品行业背景影响的报告
            你拥有<Skill>的技能并遵守<Rule>，根据<Workflow>完成相对应的任务。请避免讨论我发送的内容，不需要回复过多内容，不需要自我介绍
            你还需要做这些
            分析经济状况：仔细阅读提供给你的当前经济环境描述，列举出相关内容，分析对于行业的影响。
            对于历史回顾，仔细阅读提供给你的行业历史回顾，列举出相关内容，分析对于行业的意义。
            对于当前状况，仔细阅读提供给你的行业目前进展，列举出相关内容，分析对于行业的影响。
            信息整理归纳：筛选出最相关的数据点，并对其进行分类整理。
            分析综合处理：通过对比不同来源的数据，得出有说服力的宏观环境对于行业如何的结论。
            撰写研究报告：编写一份详尽的报告，总结宏观环境对行业的影响，并附带具体策略建议。
            以下是你需要分析的内容：
    {product_introduction}="企业的基本描述"
    {political_introduction}="当前政治环境描述"
    {economic_introduction}="当前经济环境描述"
    {social_introduction}="当前社会环境描述"
    {technological_introduction}="当前技术环境描述"
    {environmental_introduction}="当前环保环境描述"
    {legal_introduction}="当前法律环境描述"

      
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
    templates_political="深入分析当前时间{now}中国政府政策、法律法规的变化及其对{industry_classfication}行业运营的影响，探讨税收政策、贸易协定、关税、补贴等政策对行业成本结构和市场竞争的影响，识别国家或地区层面的政治稳定性和国际关系可能带来的风险与机遇。"
    templates_econimic="深入分析当前时间{now}下中国关键经济指标，包括但不限于分析中国的GDP增长率、美元利率、中国的通货膨胀率、中国的失业率、中国的汇率波动、消费者信心指数等因素的当前状态，理解它们如何塑造{industry_classfication}行业的整体环境，并影响特定产品的市场表现。"
    templates_social="深入分析当前时间{now}研究中国消费者偏好、生活方式和社会习惯的变化趋势，对{industry_classfication}行业运营的影响。了解人口统计特征（如年龄分布、性别比例、家庭结构）对市场需求的影响。 探讨社交媒体、文化潮流以及社会价值观转变对产品接受度的作用。"
    templates_technological="深入分析当前时间{now}技术创新的速度和技术进步对{industry_classfication}行业产品和服务的影响。探讨新兴技术（如人工智能、网络直播等）的应用前景及其对行业运营的影响。评估企业内部研发能力和外部技术合作的可能性。"
    templates_environmental="深入分析当前时间{now}考察中国环保法规对{industry_classfication}行业的影响。分析消费者对绿色产品和可持续发展的关注度增加对企业战略的影响。"
    templates_legal="深入分析当前时间{now}审查{industry_classfication}行业的中国的法律法规，特别是直接影响行业等方面的规定，评估新出台或即将实施的法律对企业合规成本和业务模式的影响。"
   
    templates_political=templates_political.format(now=now,industry_classfication=industry_classfication)
    templates_econimic=templates_econimic.format(now=now,industry_classfication=industry_classfication)
    templates_social=templates_social.format(now=now,industry_classfication=industry_classfication)
    templates_technological=templates_technological.format(now=now,industry_classfication=industry_classfication)
    templates_environmental=templates_environmental.format(now=now,industry_classfication=industry_classfication)
    templates_legal=templates_legal.format(now=now,industry_classfication=industry_classfication)

    political_introduction=Internet_search_thing.get_intenet_search_analysis(templates_political)
    economic_introduction=Internet_search_thing.get_intenet_search_analysis(templates_econimic)
    social_introduction=Internet_search_thing.get_intenet_search_analysis(templates_social)
    technological_introduction=Internet_search_thing.get_intenet_search_analysis(templates_technological)
    environmental_introduction=Internet_search_thing.get_intenet_search_analysis(templates_environmental)
    
    
   
    llm_legal=Tongyi(model_name="farui-plus",temperature=1)
    llm_legal.model_name="farui-plus"
    prompt_legal=PromptTemplate(
        template=templates_legal)
    chain_legal = prompt_legal|llm_legal
    legal_introduction=chain_legal.invoke(input={})
    print(legal_introduction)


    input={
        "product_introduction":product_introduction,
        "political_introduction":political_introduction,
        "economic_introduction":economic_introduction,
        "social_introduction":social_introduction,
        "technological_introduction":technological_introduction,
        "environmental_introduction":environmental_introduction,
        "legal_introduction":legal_introduction

    }
    res=chain.invoke(input)#运行
    print(res)#打印结果
    
    return res,political_introduction,economic_introduction,social_introduction,technological_introduction,environmental_introduction,legal_introduction




if __name__ == '__main__':
    product_introduction='''
        根据网上查找到的信息，中科蓝吧数字科技（苏州）有限公司确实是一家专注于AI企服领域的科技创新企业。它将AI技术作为核心驱动力，通过构建行业化的AI模型和场景化的AI能力，为各类企业提供定制化的高效、智能的AI转型升级方案，旨在帮助企业降低成本、提高效率并实现创新发展。

关于产品方面，中科蓝吧提供的云端企业服务管理软件不仅面向中小企业，也适用于大型企业。该软件集成了营销管理、经营分析等核心功能，并且还提供了一系列业务辅助工具，如客户关系管理(CRM)、供应链优化、财务管理等。这些功能模块可以帮助企业在不同业务场景下更好地应用AI技术，从而提升整体运营效率和服务质量。

此外，中科蓝吧还特别注重数据安全与隐私保护，在其产品设计中融入了多项先进的安全措施，确保用户的数据资产得到充分保障。总之，中科蓝吧致力于成为企业数字化转型过程中值得信赖的合作伙伴。
        '''
    industry_classfication="人工智能企业服务（AI企服）"
    get_economic_industry_background_analysis(product_introduction,industry_classfication)

