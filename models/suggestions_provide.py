


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
作为一位资深的企业服务专家，您的一位同事刚刚完成了一项业务。这项业务是关于{process_classfication}的{process_name}，对流程执行可能存在的问题的分析是{result_evaluations}
请您根据流程的执行结果和对标目标的情况，评估流程的结果的状况。

请确保您的总结和建议按照以下思路：
1. 回顾与总结
成果确认：简要概述本次复盘的主要发现。哪些目标达到了预期？哪些未达到？
原因分析：基于之前的分析，总结成功和失败的关键原因。这些原因如何影响了最终的结果？
2. 改进建议
策略调整：对于未达成的目标，提出具体的改进策略。如果同样的情况再次发生，应该如何调整策略以确保更好的结果？
资源分配：评估现有资源（时间、资金、人力）的使用效率。未来应如何更有效地分配资源以支持目标的实现？
3. 流程优化
过程改进：针对执行过程中遇到的问题，提出具体的流程优化建议。哪些步骤可以简化或删除？哪些环节可以增加或强化？
工具与技术：考虑是否有新的工具或技术可以帮助提高效率或效果。它们如何融入现有的工作流程中？
4. 学习与发展
知识应用：根据所学到的经验，如何将其应用于未来的工作中？有哪些具体的行动计划？
技能提升：团队和个人需要在哪些方面进一步提升技能？计划采取哪些措施来促进这种发展？
5. 风险管理
风险识别：识别在未来项目中可能遇到的风险。这些风险是如何被预见的？是否有类似的过去经验？
预防措施：针对已识别的风险，提出具体的预防措施。如何建立早期预警机制以及时应对潜在问题？
6. 沟通与协作
内部沟通：评估团队内部的沟通效率。如何改善信息流动，确保所有成员都能及时了解最新进展？
外部协作：如果涉及到外部合作伙伴，如何优化协作流程？是否存在改进的空间？
7. 文化与环境
组织文化：反思组织文化对项目的影响。是否有必要调整某些文化元素以更好地支持目标实现？
工作环境：评估工作环境对团队绩效的影响。是否需要做出任何改变来提升工作效率和员工满意度？
8. 具体流程优化方案或Prompts优化方案
评估必要性：基于以上分析，评估当前流程或prompts是否需要优化。如果不需要，请返回“不需要”。

9. 结论与行动
最终建议：综合所有分析和建议，提出一套完整的行动指南。这套指南应清晰、具体且具有可操作性。
如果认为需要优化，请详细列出具体优化方案。包括但不限于修改现有流程、引入新流程、更新工具和技术等。
如果认为不需要优化，请返回“不需要”。

"""

# 创建一个提示模板对象
prompt = PromptTemplate(template=template, input_variables=["process_name","process_classfication","process_prompts","process_result","result_evaluations"])

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

def get_process_suggestions_provide(process_name,process_classfication,process_prompts,process_result,result_evaluations):
    input={
        "process_name":process_name,
        "process_classfication":process_classfication,
        "process_prompts":process_prompts,
        "process_result":process_result,
        "result_evaluations":result_evaluations
    }
    # 使用链来获取响应"https://aichatlanba.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"
    response = chain.invoke(input).content
    
    
    return response





if __name__ == "__main__":
    # 用户输入示例
    process_name = "1.1.4.1 定义战略愿景"
    process_classfication="1 制定愿景和战略 1.1 定义业务理念和长期愿景 1.1.4 建立战略愿景"
    requirements = get_process_suggestions_provide(process_name,process_classfication)
    print(requirements)




