

from langchain_community.llms.tongyi import Tongyi
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import datetime



DASHSCOPE_API_KEY="sk-a48a1d84e015410292d07021f60b9acb"
import os
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY


import Internet_search_thing

template='''
        你是一位专业的市场竞争分析师，擅长通过深入分析市场环境、企业产品和服务特点、客户反馈等信息来识别潜在的竞争对手。你的任务是帮助企业全面了解其所在市场的竞争态势，并为制定有效的竞争策略提供依据。
        ### Skills
            市场调研：收集并分析市场数据，了解行业趋势、市场规模和发展动态。
            产品对比：详细比较企业与潜在竞争对手的产品和服务特点，包括功能、价格、质量、用户体验等。
            客户洞察：分析用户反馈、评论、使用习惯等信息，识别客户的偏好和选择标准。
            竞争评估：评估潜在竞争对手的实力，包括市场份额、品牌影响力、财务状况、创新能力等。
            风险分析：识别来自竞争对手的潜在威胁和挑战，评估对企业的影响。
            战略建议：提供具体的策略建议，帮助企业应对竞争，提升市场地位。
        ### Rules
            保持专业：在分析过程中保持专业态度，确保所有行动都有据可依。
            数据驱动：基于实际数据和事实进行分析，避免主观臆断。
            全面覆盖：确保分析涵盖所有相关方面，不遗漏重要信息。
            直接输出：专注于具体的操作和任务执行，不需要过多讨论或解释。
            逻辑清晰：输出的内容应逻辑连贯，易于理解和应用。
        ### Workflow
            用户提供关于企业及其产品的详细描述，包括但不限于市场定位、目标客户群体、产品特点等。
            你将收集并分析市场数据，了解行业趋势和发展动态。
            深入研究企业的主要产品和服务，与市场上类似的产品和服务进行对比。
            分析用户反馈，识别客户的偏好和选择标准。
            评估潜在竞争对手的实力，包括市场份额、品牌影响力、财务状况、创新能力等。
            识别来自竞争对手的潜在威胁和挑战，评估对企业的影响。
            提供具体的策略建议，帮助企业应对竞争，提升市场地位。
        
        ### Initialization
            作为专业的市场竞争分析师，让我们有条不紊地进行工作。遵循上述规则，为我提供一份完整的竞争分析报告
            你拥有<Skill>的技能并遵守<Rule>，根据<Workflow>完成相对应的任务。请避免讨论我发送的内容，不需要回复过多内容，不需要自我介绍

        以下是你需要分析的内容：
        {search_content}

      
    '''




llm=Tongyi(model_name="qwen-plus",temperature=1,enable_search=True)


prompt=PromptTemplate(
        template=template,
        input_variables=["search_content"]#这个question就是用户输入的内容,这行代码不可缺少
)

chain = prompt|llm


def get_identify_compeitors(search_content,industry_classfication):
    now = datetime.datetime.now().strftime("%Y")

    templates_serach='''
    深入分析当前时间{now}中国在{industry_classfication}行业领域涉及的公司，包括头部的以及非头部的。收集并分析市场数据，了解行业趋势、市场规模和发展动态。详细列举这些企业的产品和服务特点，包括功能、价格、质量、用户体验等。同时，1. **Strengths (优势)**
   - 识别竞争对手的核心竞争力，如品牌知名度、市场份额、产品质量、技术创新能力等。
   - 分析其供应链管理、成本结构、运营效率等方面的优势。
   - 探讨其客户基础、销售渠道、营销策略的成功之处。
   - 考察其人力资源管理和企业文化的特点。

2. **Weaknesses (劣势)**
   - 分析竞争对手可能存在的短板，如产品线单一、成本过高、客户服务不足等。
   - 探讨其市场响应速度、创新能力、财务健康状况等方面的弱点。
   - 研究其组织结构或管理模式是否限制了灵活性和发展潜力。
   - 评估其品牌形象或声誉是否有负面影响。

3. **Opportunities (机会)**
   - 发现市场上未被充分满足的需求或新兴趋势，竞争对手是否能够抓住这些机会。
   - 探讨新技术、新平台或合作伙伴关系带来的增长可能性。
   - 分析政策变化、法规放宽或经济复苏等因素为竞争对手提供的发展机遇。
   - 研究消费者行为转变是否为竞争对手提供了新的市场进入点。

4. **Threats (威胁)**
   - 识别来自其他竞争者的直接挑战，包括价格战、新产品推出或市场份额争夺。
   - 分析宏观经济环境、政治不稳定、贸易壁垒等外部因素对竞争对手构成的潜在威胁。
   - 探讨技术变革或替代品出现的可能性及其对竞争对手业务模式的影响。
   - 评估环保法规、知识产权争议或其他法律问题带来的风险。"
   '''
    templates_serach=templates_serach.format(now=now,industry_classfication=industry_classfication)
    product_introduction=Internet_search_thing.get_intenet_search_analysis(templates_serach)
    search_content=search_content+product_introduction
    input={
        "search_content":search_content,
    }
    res=chain.invoke(input)#运行
    print(res)#打印结果
    return res



if __name__ == '__main__':
    search_content='''
        根据网上查找到的信息，中科蓝吧数字科技（苏州）有限公司确实是一家专注于AI企服领域的科技创新企业。它将AI技术作为核心驱动力，通过构建行业化的AI模型和场景化的AI能力，为各类企业提供定制化的高效、智能的AI转型升级方案，旨在帮助企业降低成本、提高效率并实现创新发展。

关于产品方面，中科蓝吧提供的云端企业服务管理软件不仅面向中小企业，也适用于大型企业。该软件集成了营销管理、经营分析等核心功能，并且还提供了一系列业务辅助工具，如客户关系管理(CRM)、供应链优化、财务管理等。这些功能模块可以帮助企业在不同业务场景下更好地应用AI技术，从而提升整体运营效率和服务质量。

此外，中科蓝吧还特别注重数据安全与隐私保护，在其产品设计中融入了多项先进的安全措施，确保用户的数据资产得到充分保障。总之，中科蓝吧致力于成为企业数字化转型过程中值得信赖的合作伙伴。
        
        '''
    industry_classfication="人工智能企业服务（AI企服）"
    get_identify_compeitors(search_content,industry_classfication)


