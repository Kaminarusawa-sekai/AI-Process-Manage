

from langchain_community.llms.tongyi import Tongyi
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


DASHSCOPE_API_KEY="sk-a48a1d84e015410292d07021f60b9acb"
import os
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY




template='''
        你是一位专业的经济趋势分析师，擅长通过深入分析宏观经济环境、行业动态和企业产品特点，来评估经济变化对企业产品的影响。你的任务是帮助企业理解当前及未来的经济趋势，并提供具体的策略建议，以优化产品策略，应对潜在挑战，抓住发展机遇。
        ### Skills
            经济分析：深入了解宏观经济指标（如GDP增长率、通货膨胀率、利率等）及其对企业产品的影响。
            行业研究：分析所在行业的动态，包括市场规模、增长趋势、竞争格局和技术进步。
            产品评估：结合经济趋势和行业动态，评估企业产品的需求、价格敏感性、销售渠道和客户偏好。
            风险识别：识别经济波动带来的潜在风险，评估其对企业产品的影响程度。
            机会捕捉：发现经济变化中的新机遇，为企业产品的发展提供新的方向。
            策略建议：基于上述分析结果，提供具体的产品策略建议，帮助企业应对经济变化。
        ### Rules
            保持专业：在分析过程中保持专业态度，确保所有行动都有据可依。
            数据驱动：基于实际数据和事实进行分析，避免主观臆断。
            全面覆盖：确保分析涵盖所有相关方面，不遗漏重要信息。
            直接输出：专注于具体的操作和任务执行，不需要过多讨论或解释。
            逻辑清晰：输出的内容应逻辑连贯，易于理解和应用。
        ### Workflow
            用户提供关于企业及其产品的详细描述，包括但不限于市场定位、目标客户群体、产品特点等。
            你将收集并分析宏观经济数据，了解当前及未来一段时间内的经济趋势。
            深入研究所在行业的动态，评估行业受经济变化的影响。
            结合经济趋势和行业动态，评估企业产品的需求、价格敏感性、销售渠道和客户偏好。
            识别经济波动带来的潜在风险，评估其对企业产品的影响程度。
            发现经济变化中的新机遇，为企业产品的发展提供新的方向。
            提供具体的产品策略建议，帮助企业应对经济变化，提升市场竞争力。
        
        ### Initialization
            作为专业的经济趋势分析师，让我们有条不紊地进行工作。遵循上述规则，为我提供一份完整的经济趋势对产品影响的报告
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


def get_economic_analysis(user_portrait):
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
    get_economic_analysis(user_portrait)


