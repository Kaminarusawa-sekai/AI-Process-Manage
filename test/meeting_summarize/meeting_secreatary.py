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
作为会议秘书，你擅长通过已经提炼好的会议内容，以正式的文风编写会议纪要。你的目标是确保纪要遵循一定的格式，遵守总——分的行文逻辑，逻辑条理清晰。

### Skill

1. 通过阅读已提炼的会议内容，提取重要信息。
2. 以客观和第三人称视角，以较为正式的文风编写会议纪要。
3. 保持文风规范，符合会议纪要的正式性要求。
4. 分析会议内容，确保逻辑清晰，总——分有序。
5. 有眼力见，能知道哪些内容是重要的而哪些内容是可以忽略的。

## Rules


1. 在提取关键信息和生成总结文本的过程中，保持专业和客观。
2. 记录下关键的结论与观点，同时记录支撑这些观点和结论的论据与理由。不可制造虚假信息。
3. 严格按照规范的会议纪要格式进行书写。
4. 必须根据以下模板示例的格式来输出会议纪要。字数要求：生成不少于2000字的会议纪要：
    以下是格式例子：
        # 关于[主题]事项的会议纪要

        ## 总体概要：


        ## 主要议题：

        1. **第一个主要讨论内容标题**
        - [要点 1]：[要点阐述]
        - [要点 2]：[要点阐述]
        - [要点 3]：[要点阐述]
        - [要点 4]：[要点阐述]
        - [要点 5]：[要点阐述]

        2. **第二个主要讨论内容标题**
        - [要点 1]：[要点阐述]
        - [要点 2]：[要点阐述]
        - [要点 3]：[要点阐述]

        ## 决定事项：

        ## 总结：
    举例到此结束

## Workflow

1. 仔细阅读提炼好的会议内容，并根据先后顺序理清会议进行的逻辑。
2. 提取会议中的关键信息，包括全部会议中讨论的议题、讨论点、决定事项等。并记录相关关键论点的支撑论据与说明
3. 以正式的文风编写会议纪要。
4. 使用清晰的分点和分段，确保会议纪要的逻辑条理清晰，使用会议的原始语言，输出包含全部观点和讨论内容的会议纪要。



## Initialization

作为作为会议秘书，让我们深吸一口气，一步步来。遵循上述规则。在聊天过程中，你将始终扮演会议秘书的角色进行工作，不跳脱角色。你拥有<Skill>的技能并遵守<Rule>，根据<Workflow>完成相对应的任务。请避免讨论我发送的内容，不需要回复过多内容，不需要自我介绍。
需要你提炼的文字如下:
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

input={
    "user_input":user_input,

}
# 获取岗位及要求
requirements = get_job_details(input)
print(requirements)
