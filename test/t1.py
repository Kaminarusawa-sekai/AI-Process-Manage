from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field


EMBEDDING_URL = "https://aichatlanba.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"
OPENAI_API_KEY = "d4259c15567e44809c9629fae89583f8"
OPENAI_API_TYPE = "azure"
OPENAI_API_VERSION ="2023-03-15-preview"
AZURE_ENDPOINT = "https://aichatlanba.openai.azure.com/"



# 初始化语言模型
llm = AzureChatOpenAI(azure_endpoint=AZURE_ENDPOINT,
                        openai_api_version=OPENAI_API_VERSION,
                        openai_api_key=OPENAI_API_KEY,
                        azure_deployment="gpt-4o",
                        openai_api_type=OPENAI_API_TYPE,
                        streaming=True,
                        temperature=0.7)


one_template = """
你是一个植物学家。给定花的名称和类型，你需要为这种花写一个200字左右的介绍。
花名: {name}颜色: {color}
植物学家: 这是关于上述花的介绍:
"""
one_prompt_template = PromptTemplate(
    template=one_template,
    input_variables=["name", "color"],
)
class one_out(BaseModel):
    introduction: str = Field(description="花卉介绍")

output_parser = PydanticOutputParser(pydantic_object=one_out)
introduction_chain=one_prompt_template|llm|output_parser
# introduction_chain = LLMChain(
#     llm=llm,
#     prompt=one_prompt_template,
#     output_key="introduction",
# )

two_template = """
你是一位鲜花评论家。给定一种花的介绍，你需要为这种花写一篇200字左右的评论。
鲜花介绍:{introduction}
花评人对上述花的评论:
"""
two_prompt_template = PromptTemplate(
    template=two_template,
    input_variables=["introduction"],
)
class two_out(BaseModel):
    review: str = Field(description="花卉评论")

review_chain=two_prompt_template|llm|PydanticOutputParser(pydantic_object=two_out)


overall_chain = introduction_chain|review_chain|output_parser
print(introduction_chain.invoke({"name": "玫瑰", "color": "红色"}))
result = overall_chain({"name": "玫瑰", "color": "红色"})
print(result)