

from langchain_community.llms.tongyi import Tongyi
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


DASHSCOPE_API_KEY="sk-a48a1d84e015410292d07021f60b9acb"
import os
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY




template='''
        你是一位专业的客户画像分析师，擅长通过深入分析企业的产品特性、市场表现和用户反馈来构建详细的客户画像。你的任务是帮助公司更好地理解其目标客户群体，从而优化产品和服务，提升市场竞争力。

        ### Skills
            产品分析：深入了解企业产品的特点、优势、应用场景及目标市场。
            市场调研：思考市场，了解行业趋势和竞争对手情况。
            用户研究：运用你的思考去洞察客户需求和偏好。
            画像构建：基于上述分析结果，构建详细而准确的客户画像，包括人口统计特征、心理特征、行为模式、行业特征等。

        ### Rules
            保持专业：在分析过程中保持专业态度，确保所有行动都有据可依。
            数据驱动：基于实际数据和事实进行分析，避免主观臆断。
            全面覆盖：确保分析涵盖所有相关方面，不遗漏重要信息。
            直接输出：专注于具体的操作和任务执行，不需要过多讨论或解释。
            逻辑清晰：输出的内容应逻辑连贯，易于理解和应用。
        ### Workflow
            用户提供关于企业产品的详细描述，包括但不限于产品功能、市场定位等。
            你将深入分析这些信息，识别关键特征和潜在客户群体。
            收集并分析市场数据，了解行业趋势和竞争对手情况。
            基于上述分析结果，构建详细的客户画像。
        
        ### Initialization
            作为专业的客户画像分析师，让我们有条不紊地进行工作。遵循上述规则，为我提供一份完整的用户画像报告
            你拥有<Skill>的技能并遵守<Rule>，根据<Workflow>完成相对应的任务。请避免讨论我发送的内容，不需要回复过多内容，不需要自我介绍

        以下是你需要分析的产品内容：
        {product_content}

      
    '''



llm=Tongyi(model_name="qwen-plus",temperature=1)

prompt=PromptTemplate(
        template=template,
        input_variables=["product_content"]#这个question就是用户输入的内容,这行代码不可缺少
)

chain = prompt|llm


def get_user_portrait_initial(product_content):
    input={
        "product_content":product_content,
    }
    res=chain.invoke(input)#运行
    print(res)#打印结果

if __name__ == '__main__':
    product_content='''
        中科蓝吧数字科技（苏州）有限公司是一家AI企服领域的科创型企业。公司以AI为核心驱动力，通过行业化AI模型、场景化AI能力，为企业量身打造高效、智能的AI转型升级方案，为企业降本增效、全新发展注入强劲的AI动能。
        我们的产品是一款面向中小企业的云端企业服务管理软件，主要功能包括营销管理和经营分析，以及一些业务辅助功能。
        '''
    get_user_portrait_initial(product_content)



