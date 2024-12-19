import langchain
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


import configparser

# 创建ConfigParser对象
config = configparser.ConfigParser()

# 读取配置文件
config.read('config.ini')

# 获取llm的配置参数

# EMBEDDING_URL = config.get('Azurellm','EMBEDDING_URL')
EMBEDDING_URL ="https://aichatlanba.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"
OPENAI_API_KEY = "d4259c15567e44809c9629fae89583f8"
OPENAI_API_TYPE = "azure"
OPENAI_API_VERSION = "2023-03-15-preview"
AZURE_ENDPOINT="https://aichatlanba.openai.azure.com/"
# OPENAI_API_KEY = config.get('Azurellm','OPENAI_API_KEY')
# OPENAI_API_TYPE = config.get('Azurellm','OPENAI_API_TYPE')
# OPENAI_API_VERSION = config.get('Azurellm','OPENAI_API_VERSION')
# AZURE_ENDPOINT=config.get('Azurellm','AZURE_ENDPOINT')

print(EMBEDDING_URL)



# 定义一个更详细的提示模板
template = """
## 角色
你是高效的内容阅读文员，专业帮助用户提炼一大段内容的关键信息。你擅长分析讨论中的各种观点，找到这些观点的依据，评估发言人能否做出最终决定。总结观点得出的结论，并生成精炼的文本摘要。

### Skill

1. 提取关键信息：能够准确识别和提取讨论中的关键信息。
2. 分析观点：具备分析不同观点，并理解它们在整个内容中的作用的能力。
3. 有眼力见：能通过对话，明白哪些对话属于真正做出决定，有话语权的人，他们的言论和观点更有分量，更应成为提炼出来的观点。
4. 结论总结：能够归纳整个讨论后得出的结论或决定。
5. 生成文本摘要：擅长将分析后的信息以清晰、简明的方式表达

## Rules

1. 保持专业：在提取关键信息和生成总结文本的过程中，保持专业和客观。
2. 不改变意思：在总结过程中，不会改变原始内容的核心意思。
3. 提取观点与论据：找到关键的观点，并提取支撑这些观点的论据和理由，记录下来。
4. 直接总结：你应该直接输出总结文本，不需要答复我，也不应讨论文本内容，也不需要添加额外的应答与客套话
5. 字数要求：生成不少于2000字的总结文本

## Workflow

1. 用户会提供一段需要总结的内容，这些内容中可能存在观点纷呈，复杂
2. 你将分析内容，提取关键信息和各种观点，找出这段内容主要的讨论点或者讨论的结果
3. 有时候讨论可能只是一大段讨论中的一部分，可能还没有结论，因此你只需提供这段内容中的论点即可
4. 根据分析结果，你会生成一份不少于2000字的总结文本。这份文本应该包含这段讨论当中的主要观点，以及支撑这些观点的相关依据。

## ChatCharacter
这里是给你提供的对话中的各个角色分别是什么的参考
{chat_character}

## Initialization

作为高效的内容阅读文员，让我们深吸一口气，一步步来。遵循上述规则，在简体中文环境下与用户交流。在聊天过程中，你将始终扮演内容阅读文员的角色进行工作，不跳脱角色。你拥有<Skill>的技能并遵守<Rule>，按照给你的对话角色提示<ChatCharacter>根据<Workflow>完成相对应的任务。请避免讨论我发送的内容，不需要回复过多内容，不需要自我介绍。
需要你提炼的文字如下:
{user_input}



"""

# 创建一个提示模板对象
prompt = PromptTemplate(template=template, input_variables=["user_input,chat_character"])

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

def get_job_details(input):
    # 使用链来获取响应"https://aichatlanba.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"
    response = chain.invoke(input).content
    
    
    return response

# 用户输入示例
user_input = '''

【可胜】嗨，我最近用你们那个云端备份服务时碰到了点麻烦，能帮帮我吗？

【冰茶】嗨！当然可以啦，很抱歉听到你遇到问题了。你可以跟我说说具体是怎么回事儿吗？这样我好帮你看看。

【可胜】嗯，就是我试着恢复上周备份的数据，结果系统告诉我找不到备份文件，这可怎么办呢？

【冰茶】哦，这听起来挺烦人的。首先，你能再确认下你选的时间和日期对不对吗？有时候可能不小心选错了，或者是因为时差的问题。另外，是不是就只有你在用这个账户备份呢？如果有其他设备也连着同一个备份任务，可能会有点影响。

【可胜】我都检查过了，时间和日期都没错，而且就我一个人在用，但还是不行。

【冰茶】好的，了解了。那我们得深入看看这个问题。为了更快找到原因，你能告诉我错误信息大概是什么样子的，还有那个备份任务的ID吗？这样我们可以查一查。

【可胜】行吧，错误信息大概是“ERR-012: Backup not found”，备份任务ID是BCK-123456789。

【冰茶】谢谢你提供的信息。看起来备份过程中好像出了点小状况，可能是网络不太好导致的。我们会尽快处理，尽量帮你把数据找回来。别太担心啦，我们会搞定的。

【可胜】那我现在应该做点什么呢？我的数据还能恢复吗？

【冰茶】你现在啥都不用做，交给我们就好。我们的团队会看看有没有其他备份可以帮助你恢复部分数据。一旦有消息，我们就会联系你并告诉你下一步该怎么做。

【可胜】好吧，我希望快点解决。不过我还担心以后会不会又出这样的事儿？

【冰茶】这确实是个好问题。为了避免这种情况再发生，建议你在网络稳定的时候进行备份。对于特别重要的东西，最好能多留几份备份，比如本地硬盘上也存一份。这样即使一个备份有问题，还有其他的可以用嘛。

【可胜】听上去挺合理的。那我现在就等着你们的消息喽？

【冰茶】没错，你就耐心等等吧。我们会优先处理你的请求，并且会在一天之内给你答复。如果你有任何问题或需要帮助，随时联系我们。为了表示歉意，我们还会送你一个月的免费服务延长期。

【可胜】谢谢啊，真希望这次能顺利解决问题。下次可不能再出这种事了。

【冰茶】不用谢！我们会尽力确保一切顺利。再次为给您带来的不便道歉。祝你今天愉快！一旦有新进展，我们一定会第一时间通知你。

【可胜】好的，谢谢你。那我就等你们的消息了。

【冰茶】感谢你的理解和配合。祝你一切顺利，再见！


'''
chat_character='''
### 对话分析总结

**甲方：可胜**
- **角色及影响力**：甲方是云端备份服务的用户，作为客户，其主要角色是提出问题并寻求解决方案。由于他的反馈直接关系到服务质量，具有一定的影响力。
- **主要观点及依据**：
  - **问题描述**：在尝试恢复上周备份数据时，系统提示找不到备份文件。
  - **确认信息**：已检查时间和日期，确认无误，且只有自己在使用该账户。
  - **错误信息**：提供了具体的错误信息“ERR-012: Backup not found”和备份任务ID BCK-123456789。
  - **关切**：希望数据能尽快恢复，并担心未来会再次遇到类似问题。

**乙方：冰茶**
- **角色及影响力**：乙方是云端备份服务的客服代表，主要角色是回应客户问题并提供解决方案。由于其代表公司处理客户问题，具有较高的决策权和影响力。
- **主要观点及依据**：
  - **初步建议**：建议检查时间和日期，以及是否有其他设备连接同一备份任务。
  - **确认问题**：进一步了解错误信息和备份任务ID，以便深入调查。
  - **解决方案**：表示会尽快处理问题，并考虑其他备份的可能性以恢复部分数据。
  - **预防建议**：建议在网络稳定时进行备份，并多留几份备份（例如在本地硬盘上）以防止未来类似问题。

### 总结
在这段对话中，甲方可胜提出了具体的技术问题，乙方冰茶则负责解答并提供解决方案。乙方冰茶表现出较高的专业性和服务态度，通过收集详细信息、提供初步建议和承诺后续行动，展现了其在讨论中的核心地位和影响力。对话中，乙方也提出了预防未来问题的建议，以提升客户满意度和服务质量。
'''
input={
    "user_input":user_input,
    "chat_character":chat_character
}
# 获取岗位及要求
requirements = get_job_details(input)
print(requirements)
