import markdown
from anytree import Node, RenderTree
from bs4 import BeautifulSoup


import langchain
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain



EMBEDDING_URL ="https://aichatlanba.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"
OPENAI_API_KEY = "d4259c15567e44809c9629fae89583f8"
OPENAI_API_TYPE = "azure"
OPENAI_API_VERSION = "2023-03-15-preview"
AZURE_ENDPOINT="https://aichatlanba.openai.azure.com/"


print(EMBEDDING_URL)



# 定义一个更详细的提示模板
template = """
作为一位资深的企业服务专家，您的一位同事刚刚完成了一项业务。这项业务是关于{process_classfication}的{process_name}，流程的原定目标是{process_prompts}。流程执行的结果是{process_result}，对标目标的情况{goals_reviews}
请您根据流程的执行结果和对标目标的情况，评估流程的结果的状况。

请确保您的总结和建议按照以下思路：
1. 结果概述
明确目标：回顾最初设定的具体目标是什么？这些目标是否清晰、具体且具有挑战性？
成果描述：对于每个目标，请详细列出最终取得的结果。结果是超出预期、符合预期还是低于预期？
2. 影响与效果
核心成就：哪些行动或决策直接促成了主要的成功？它们对组织或个人产生了什么积极的影响？
非显而易见的效果：在实现目标的过程中，是否发现了未曾预料到的正面或负面影响？这些效果如何改变了你对结果的看法？
3. 成功因素分析
关键驱动：确定并解释推动成功的几个最关键因素。这些因素是否可以复制或增强？
模式识别：在达成目标的过程中，是否有特定的行为模式或工作流程显著促进了成功？
4. 遇到的障碍与问题
挑战应对：在追求目标的路上遇到了哪些主要障碍？这些问题是如何解决的，或者未能解决的原因是什么？
错误与教训：承认并分析过程中出现的任何失误。从这些经历中学到了什么可以应用在未来的情况中？
5. 绩效评估
效率评估：评估为实现目标所投入的时间、资源和努力是否合理。如果重新来过，会做出怎样的调整？
质量评估：结果的质量如何？它是否满足了所有利益相关方的期望？如果不满意，原因可能是什么？
6. 学习与发展
知识获取：在整个过程中，学到了哪些新技能或获得了哪些新的见解？
团队成长：这些经验对团队的成长和发展有何贡献？团队成员之间的协作是否得到了改善？
7. 改进措施
优化建议：基于上述反思，提出具体的改进建议来优化未来的目标设定和实现过程。
创新应用：考虑是否有任何新颖的方法或工具可以帮助更好地达成目标，提高效率或效果。
8. 未来展望
持续发展：基于这次的经验，如何规划未来的行动？设定了哪些新的长期或短期目标？
信心水平：对实现新目标有多大信心？还需要做哪些准备以提高成功率？

"""

# 创建一个提示模板对象
prompt = PromptTemplate(template=template, input_variables=["process_name","process_classfication","process_prompts","process_result","goals_reviews"])

# 初始化语言模型
llm = AzureChatOpenAI(azure_endpoint=AZURE_ENDPOINT,
                          openai_api_version=OPENAI_API_VERSION,
                          openai_api_key=OPENAI_API_KEY,
                          azure_deployment="gpt-4o",
                          openai_api_type=OPENAI_API_TYPE,
                          streaming=True,
                          temperature=0.7)

# 创建一个链
chain = prompt|llm

def get_process_result_evalution(process_name,process_classfication,process_prompts,process_result,goals_reviews):
    input={
        "process_name":process_name,
        "process_classfication":process_classfication,
        "process_prompts":process_prompts,
        "process_result":process_result,
        "goals_reviews":goals_reviews
    }
    # 使用链来获取响应"https://aichatlanba.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"
    response = chain.invoke(input).content
    
    
    return response





if __name__ == "__main__":
    # 用户输入示例
    process_name = "1.1.4.1 定义战略愿景"
    process_classfication="1 制定愿景和战略 1.1 定义业务理念和长期愿景 1.1.4 建立战略愿景"
    requirements = get_process_goals_review(process_name,process_classfication)
    print(requirements)




