

import langchain
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser

from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

EMBEDDING_URL ="https://aichatlanba.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"
OPENAI_API_KEY = "d4259c15567e44809c9629fae89583f8"
OPENAI_API_TYPE = "azure"
OPENAI_API_VERSION = "2023-03-15-preview"
AZURE_ENDPOINT="https://aichatlanba.openai.azure.com/"

print(EMBEDDING_URL)

class goals_review_instruction(BaseModel):
    goals_review: str = Field(description="与目标对比的结果")

class result_evalution_instruction(BaseModel):
    result_evalution:str=Field(description="流程的结果的状况是")

class reason_analysis_instruction(BaseModel):
    reason_analysis:str=Field(description="出现问题的原因是")

class suggestion_provider_instruction(BaseModel):
    suggestion_provider:str=Field(description="可能存在的建议是")


# 定义一个更详细的提示模板
goals_review_template = """
作为一位资深的企业服务专家，您的一位同事刚刚完成了一项业务。这项业务是关于{process_classfication}的{process_name}，流程的原定目标是{process_prompts}。流程执行的结果是{process_result}
请您根据流程的执行结果，回顾是否和目标一致。
{format_instructions}

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

result_evalution_template = """
作为一位资深的企业服务专家，您的一位同事刚刚完成了一项业务。这项业务是关于{process_classfication}的{process_name}，对标目标的情况是{goals_reviews}
请您根据流程的执行结果和对标目标的情况，评估流程的结果的状况。
{format_instructions}

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


reason_analysis_template = """
作为一位资深的企业服务专家，您的一位同事刚刚完成了一项业务。这项业务是关于{process_classfication}的{process_name},流程执行下来的评估情况是{result_evalution}
请您根据流程的执行结果和流程评估情况，评估出现问题的原因。
{format_instructions}

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

suggestion_provider_template = """
作为一位资深的企业服务专家，您的一位同事刚刚完成了一项业务。这项业务是关于{process_classfication}的{process_name}，对流程执行可能存在的问题的分析是{result_evaluations}
请您根据流程的执行结果和对标目标的情况，给出可能存在的建议，如果你觉得满意可以不提供建议。
{format_instructions}

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

llm = AzureChatOpenAI(azure_endpoint=AZURE_ENDPOINT,
                          openai_api_version=OPENAI_API_VERSION,
                          openai_api_key=OPENAI_API_KEY,
                          azure_deployment="gpt-4o",
                          openai_api_type=OPENAI_API_TYPE,
                          streaming=True,
                          temperature=0.7)

goals_review_output_parser = PydanticOutputParser(pydantic_object=goals_review_instruction)
result_evalution=PydanticOutputParser(pydantic_object=result_evalution_instruction)
reason_analysis=PydanticOutputParser(pydantic_object=reason_analysis_instruction)
suggestion_provider=PydanticOutputParser(pydantic_object=suggestion_provider_instruction)

goals_review_prompts=PromptTemplate(template=goals_review_template, 
                        input_variables=["process_name","process_classfication","process_prompts","process_result"],
                        partial_variables=output_parser.get_format_instructions())

