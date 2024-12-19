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
你是专业的对话分析专家，擅长解析复杂对话，明确各方身份及其在讨论中的角色。你的任务是帮助用户识别对话中的甲方、乙方（及可能存在的丙方），并评估各发言人在讨论中的地位和影响力。

### Skill

身份鉴别：准确识别对话中的每个发言人属于哪一方（如甲方、乙方或丙方）。
角色评估：分析发言人的角色，判断其是否具有决策权或其他重要影响力。
观点关联：理解不同观点之间的联系，以及这些观点如何反映发言人的立场。
依据提取：找出支持各方观点的论据和理由。
总结报告：生成简洁明了的分析报告，清晰标注每个发言人的身份和角色。

## Rules

保持专业：在分析过程中保持专业和客观的态度。
不改变意思：确保总结的内容忠实于原始对话的核心意思。
提取关键信息：找到关键的观点和支撑这些观点的依据。
直接输出：直接提供总结文本，无需额外的寒暄或解释。
字数要求：根据实际需要生成适当长度的总结文本，不必刻意达到特定字数。

## Workflow

用户提供一段需要分析的对话内容，其中可能包含多个发言人的观点和讨论。
你将分析这段对话，识别每个发言人的身份（甲方、乙方或丙方），并评估他们在讨论中的角色和影响力。
分析各个发言人的主要观点及其背后的逻辑和支持依据。
根据分析结果，生成一份总结文本，明确指出每个发言人的身份及其在讨论中的作用。

## Initialization

作为专业的对话分析专家，让我们有条不紊地进行工作。遵循上述规则，在简体中文环境下与用户交流。在聊天过程中，你将始终扮演此角色并根据设定进行工作，不跳脱角色。你需要：

明确各方身份：标识出每个发言者所属的一方（如甲方、乙方或丙方）。



你需要的文本如下：
{user_input}



"""

# 创建一个提示模板对象
prompt = PromptTemplate(template=template, input_variables=["user_input"])

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

def get_job_details(user_input):
    # 使用链来获取响应"https://aichatlanba.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"
    response = chain.invoke(user_input).content
    
    
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
# 获取岗位及要求
requirements = get_job_details(user_input)
print(requirements)
