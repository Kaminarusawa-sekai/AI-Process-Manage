


import langchain
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


from configs import total_config

from langchain_core.pydantic_v1 import BaseModel, Field,create_model
from typing import List





config=total_config.load_config("../configs/config.yaml")
def get_base_chain(templates,input_variables):
    EMBEDDING_URL=config['models']['EMBEDDING_URL']
    OPENAI_API_KEY=config['models']['OPENAI_API_KEY']
    OPENAI_API_VERSION=config['models']['OPENAI_API_VERSION']
    OPENAI_API_TYPE=config['models']['OPENAI_API_TYPE']
    AZURE_ENDPOINT=config['models']['AZURE_ENDPOINT']

    prompt = PromptTemplate(template=templates, input_variables=input_variables.keys)

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
    return chain

def get_base_chain_with_output(templates,input_variables:dict,output_name:str,output_type:type,output_description:str):
    EMBEDDING_URL=config['models']['EMBEDDING_URL']
    OPENAI_API_KEY=config['models']['OPENAI_API_KEY']
    OPENAI_API_VERSION=config['models']['OPENAI_API_VERSION']
    OPENAI_API_TYPE=config['models']['OPENAI_API_TYPE']
    AZURE_ENDPOINT=config['models']['AZURE_ENDPOINT']

    output_instruction=create_model(
    'output_instruction',
    output_name=(output_type, Field(..., description=output_description)))

    


    prompt = PromptTemplate(template=templates, input_variables=input_variables.keys,partial_variables=output_instruction.get_format_instructions())

    # 初始化语言模型
    llm = AzureChatOpenAI(azure_endpoint=AZURE_ENDPOINT,
                            openai_api_version=OPENAI_API_VERSION,
                            openai_api_key=OPENAI_API_KEY,
                            azure_deployment="gpt-4o",
                            openai_api_type=OPENAI_API_TYPE,
                            streaming=True,
                            temperature=0.7)

    # 创建一个链
    chain = prompt|llm|output_instruction
    return chain

def base_excute(templates,input_variables):
    chain=get_base_chain(templates,input_variables)
    
    response = chain.invoke(input_variables).content
    
    
    return response




# def excute_and_replay(templates,process_name,process_classfication,input_variables):


