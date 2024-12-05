

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
作为一位资深的企业服务专家，您的一位同事刚刚完成了一项业务。这项业务是关于{process_classfication}的{process_name}，流程的原定目标是{process_prompts}。流程执行的结果是{process_result}
请您根据流程的执行结果，回顾是否和目标一致。

请确保您的总结和建议按照以下思路：
1. 初始设置回顾
问题分解：请列出最初设定的目标。这些目标是具体、可衡量、可实现、相关且时限明确（SMART）的吗？
需求确认：当初设定这些目标时，期望解决哪些问题或满足什么需求？是否有隐含的需求未被注意到？
2. 成果评估
核心成就：对于每个目标，请简要描述取得的成果。是否达到了预期的结果？
非显而易见的影响：有哪些未曾预料到的正面或负面影响发生？这些影响如何改变了你对目标的看法？
3. 过程反思
路径选择：回顾实现目标的过程，是否遵循了最初的计划？如果不是，是什么原因导致了改变？
模式识别：在追求目标的过程中，发现了哪些有助于或阻碍成功的模式和趋势？
4. 挑战与障碍
遇到的问题：在尝试达成目标的路上遇到了哪些挑战？这些问题是如何处理的？
错误与教训：承认并分析过程中犯下的错误。从这些经历中学到了什么可以应用在未来的情况中？
5. 学习与发展
知识获取：在整个过程中，学到了哪些新技能或获得了哪些新的见解？
个人成长：这些经历对你个人或团队的发展产生了怎样的影响？
6. 改进措施
优化建议：根据上述反思，提出具体的改进建议来优化未来的目标设定和实现过程。
创新应用：考虑是否有任何新颖的方法或工具可以帮助更好地达成目标。
7. 未来展望
持续发展：基于这次的经验，如何规划未来的行动？设定了哪些新的长期或短期目标？
信心水平：对实现新目标有多大信心？还需要做哪些准备以提高成功率？

"""

# 创建一个提示模板对象
prompt = PromptTemplate(template=template, input_variables=["process_name","process_classfication","process_prompts","process_result"])

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

def get_process_goals_review(process_name,process_classfication,process_prompts,process_result):
    input={
        "process_name":process_name,
        "process_classfication":process_classfication,
        "process_prompts":process_prompts,
        "process_result":process_result
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




