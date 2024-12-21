

from langchain_community.llms.tongyi import Tongyi
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


DASHSCOPE_API_KEY="sk-a48a1d84e015410292d07021f60b9acb"
import os
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY




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
        {user_portrait}

      
    '''




llm=Tongyi(model_name="qwen-plus",temperature=1,enable_search=True)


prompt=PromptTemplate(
        template=template,
        input_variables=["user_portrait"]#这个question就是用户输入的内容,这行代码不可缺少
)

chain = prompt|llm


def get_identify_compeitors(user_portrait):
    input={
        "user_portrait":user_portrait,
    }
    res=chain.invoke(input)#运行
    print(res)#打印结果
    return res



if __name__ == '__main__':
    user_portrait='''
        ### 用户画像构建报告

        #### 产品分析
        我们的产品是一款面向中小企业的云端企业服务管理软件，主要功能包括营销管理和经营分析，以及一些业务辅助功能。该产品通过云服务提供，确保了数据的可访问性和实时性。产品定位为中小企业提供高效、便捷的管理工具，以提高运营效率和决策质量。

        #### 市场调研
        当前市场上，中小企业管理软件市场竞争激烈，主要竞争对手包括Salesforce、Zoho、钉钉等。这些竞争对手提供类似或相同的功能，但价格和定制能力各有差异。市场上存在对更加个性化和定制化服务的需求，同时也需要更具成本效益的解决方案。

        #### 用户研究
        目标客户群体主要是中小企业的管理人员和运营人员，他们关注提高工作效率和降低成本。他们可能倾向于使用简单易用、价格适中且提供定制服务的软件产品。

        #### 画像构建
        **人口统计特征**
        - 年龄：25-55岁，主要是企业的中层管理人员和决策者。
        - 性别：无明显偏好，男性和女性比例均衡。
        - 教育背景：大专及以上学历，具有相关行业背景者优先。
        - 职业：中小企业管理层，如销售经理、运营总监、财务总监等。
        - 收入水平：中等收入，对成本效益敏感。

        **心理特征**
        - 重视效率和成本控制。
        - 倾向于使用简单易用的产品。
        - 寻求定制化和专业化的服务。
        - 重视数据安全和隐私保护。

        **行为模式**
        - 习惯于通过互联网获取信息和服务。
        - 倾向于使用移动端应用。
        - 习惯于定期更新和升级服务。
        - 对于新技术和新功能持开放态度。

        **行业特征**
        - 主要服务于IT、教育、医疗、零售等行业。
        - 对于特定行业的需求和法规有较高的敏感性。

        **总结**
        基于上述分析，我们构建的客户画像是一群年龄在25-55岁之间的中小企业管理人员，他们追求效率和成本效益，倾向于使用简单易用且提供定制化服务的软件产品。他们关注数据安全和隐私保 护，并且对新技术持开放态度。他们主要来自IT、教育、医疗、零售等行业，并对特定行业的法规有较高的敏感性。

        以上是根据提供的信息构建的用户画像报告，根据实际数据和事实进行分析，确保逻辑清晰且易于理解和应用。如有需要，可以根据实际情况调整和完善画像内容。
        '''
    get_identify_compeitors(user_portrait)


