

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
作为一位资深的企业服务专家，您的一位同事刚刚完成了一项业务。这项业务是关于{process_classfication}的{process_name}，流程的原定目标是{process_prompts}。流程执行的结果是{process_result},流程执行下来的评估情况是{result_evalution}
请您根据流程的执行结果和流程评估情况，评估出现问题的原因。

请确保您的总结和建议按照以下思路：
1. 初始条件与背景
设定环境：回顾目标设定时的内外部环境。当时有哪些关键的因素影响了决策？这些因素是如何被考虑进来的？
资源与限制：在开始时，可用的资源（如时间、资金、人力）是什么情况？是否存在任何已知的约束条件？
2. 目标与期望
明确意图：最初设定的目标是什么？这些目标背后的动机是什么？它们是否充分反映了组织或个人的需求和愿景？
预期成果：对于每个目标，最初的期望成果是什么？这些期望是基于什么样的假设或预测？
3. 行动路径与执行
策略选择：在追求目标的过程中采用了哪些具体策略或方法？这些选择是如何做出的？是否有其他备选方案？
实施过程：描述实际采取的行动步骤。这些步骤是否严格按照计划进行？如果不是，发生了什么变化，为什么？
4. 成功因素分析
促成要素：识别并详细说明那些对成功起到关键作用的因素。它们为何如此重要？如何能够重复利用这些成功的要素？
模式识别：在整个过程中，是否发现了有助于成功的特定行为模式或工作流程？这些模式是否可以在未来复制？
5. 遇到的障碍与问题
挑战剖析：列出遇到的主要障碍和问题。这些问题的根本原因是什么？它们是如何影响最终结果的？
错误根源：深入探讨任何失误或失败的根本原因。这可能涉及到人的因素、流程缺陷或是外部不可控因素。
6. 内外部影响
内部动态：团队内部的动力、沟通和协作对结果产生了怎样的影响？是否存在需要改进的地方？
外部因素：外界环境（如市场变化、政策调整等）对项目有何影响？这些因素是如何被预见和应对的？
7. 原因关联性
因果关系：建立成功因素与障碍之间的联系。哪些成功的原因直接抵消了某些障碍的影响？反之亦然。
非显而易见的联系：是否存在一些不易察觉但对结果产生重大影响的因素？如果存在，它们是如何发挥作用的？
8. 学习与发展
知识积累：通过这次经历，学到了哪些关于成功原因的新见解或理论？这些知识如何指导未来的行动？
能力提升：团队和个人在这次实践中获得了哪些技能上的提升？这些能力在未来的工作中将如何应用？
9. 改进措施
预防措施：基于对原因的分析，提出具体的预防措施以避免未来出现类似的问题或障碍。
增强策略：确定哪些成功的做法应该加强或推广，以便在未来取得更好的结果。
10. 未来展望
持续发展：根据此次分析，规划未来应如何调整策略或改变方向以更好地实现目标。
信心水平：评估对未来目标的信心程度。基于当前的理解，还需要做哪些准备来确保更高的成功率？

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

def get_process_reason_analysis(process_name,process_classfication,process_prompts,process_result,result_evalution):
    input={
        "process_name":process_name,
        "process_classfication":process_classfication,
        "process_prompts":process_prompts,
        "process_result":process_result,
        "result_evalution":result_evalution
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




