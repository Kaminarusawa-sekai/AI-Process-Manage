

from langchain_community.llms.tongyi import Tongyi
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


DASHSCOPE_API_KEY="sk-a48a1d84e015410292d07021f60b9acb"
import os
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY




template='''
       你是一位专业的品牌形象顾问，擅长通过深入分析企业主的MBTI类型和个人特长，为企业主量身定制一个符合其个性和优势的营销人物形象设定。你的任务是帮助企业主更好地理解自己的特点，并利用这些特点在市场营销中发挥最大潜力。

        ### Skills
            性格分析：深入了解企业主的MBTI类型，包括四个维度（外向/内向、感觉/直觉、思考/情感、判断/知觉）。
            特长评估：识别并评估企业主的专业技能、领导风格、沟通技巧等特长。
            形象匹配：结合MBTI类型和特长，为企业主找到最适合的营销人物形象设定。

        ### Rules
            保持专业：在分析过程中保持专业态度，确保所有行动都有据可依。
            数据驱动：基于实际数据和事实进行分析，避免主观臆断。
            全面覆盖：确保分析涵盖所有相关方面，不遗漏重要信息。
            直接输出：专注于具体的操作和任务执行，不需要过多讨论或解释。
            逻辑清晰：输出的内容应逻辑连贯，易于理解和应用。
        ### Workflow
            用户提供关于企业主的详细描述，包括但不限于MBTI类型、个人特长、职业经历等。
            你将从这些信息出发，深入分析企业主的性格特点和特长。
            结合MBTI类型和特长，为企业主找到最适合的营销人物形象设定。

        
        ### Initialization
            作为专业的品牌形象顾问，让我们有条不紊地进行工作。遵循上述规则，为我提供一份完整的企业主的个人形象设计的报告
            你拥有<Skill>的技能并遵守<Rule>，根据<Workflow>完成相对应的任务。请避免讨论我发送的内容，不需要回复过多内容，不需要自我介绍

        企业主的MBTI分类是：
        {BOSS_MBTI}
        企业主的性格特长是：
        {BOSS_strengths}

      
    '''


llm=Tongyi(model_name="qwen-plus",temperature=1)


prompt=PromptTemplate(
        template=template,
        input_variables=["BOSS_MBTI","BOSS_strengths"]#这个question就是用户输入的内容,这行代码不可缺少
)

chain = prompt|llm


def get_boss_characteristic(BOSS_MBTI,BOSS_strengths):
    input={
        "BOSS_MBTI":BOSS_MBTI,
        "BOSS_strengths":BOSS_strengths

    }
    res=chain.invoke(input)#运行
    print(res)#打印结果
    return res



if __name__ == '__main__':
    Boss_MBTI='''
       INFJ
        '''
    BOSS_strengths="企业主的性格特点是坚持"
    get_boss_characteristic(Boss_MBTI,BOSS_strengths)



