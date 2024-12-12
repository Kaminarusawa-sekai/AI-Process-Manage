


import langchain
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser


from configs import total_config

from pydantic import BaseModel, Field,create_model
from typing import List
import asyncio

from models import replay_results




config=total_config.load_config("../configs/config.yaml")


def get_base_chain(templates:str,input_variables_names:List,output_names:List[str]=None,output_types:List[type]=None,output_descriptions:List[str]=None):
    EMBEDDING_URL=config['models']['EMBEDDING_URL']
    OPENAI_API_KEY=config['models']['OPENAI_API_KEY']
    OPENAI_API_VERSION=config['models']['OPENAI_API_VERSION']
    OPENAI_API_TYPE=config['models']['OPENAI_API_TYPE']
    AZURE_ENDPOINT=config['models']['AZURE_ENDPOINT']

    # 初始化语言模型
    llm = AzureChatOpenAI(azure_endpoint=AZURE_ENDPOINT,
                            openai_api_version=OPENAI_API_VERSION,
                            openai_api_key=OPENAI_API_KEY,
                            azure_deployment="gpt-4o",
                            openai_api_type=OPENAI_API_TYPE,
                            streaming=True,
                            temperature=0.7)
    
    if output_names!=None or output_types!=None or output_descriptions!=None:
        if output_names==None:
            raise Exception("Lack of output_name") 
        if output_types==None:
            raise Exception("Lack of output_type")
        if output_descriptions==None:
            raise Exception("Lack of output_description")
        if len(output_names)==len(output_types)==len(output_descriptions):
            fields=[]
            for i in range(0,len(output_names)):
                fields.append((output_names[i],output_types[i],Field(description=output_descriptions[i])))
            templates=templates+"{format_instructions}"          
            output_instruction=create_model("output_instruction", **{field[0]: (field[1], field[2]) for field in fields})
            outputparser=JsonOutputParser(pydantic_object=output_instruction)
            prompt = PromptTemplate(template=templates,input_variables=input_variables_names,partial_variables={"format_instructions":outputparser.get_format_instructions()})
            chain = prompt|llm|outputparser
        else:
            raise Exception("The quantity is inconsistent")
        
    else:
        prompt = PromptTemplate(template=templates,input_variables=input_variables_names)
        # 创建一个链
        chain = prompt|llm
    return chain

def excute(templates,input_variables:dict=None,output_name:str=None,output_type:type=None,output_description:str=None):
    templates="你是一个流程的执行者，你需要按照给出的步骤完成你的思考，从而完美完成给你的目标流程的执行，并且给出一份符合目标的结果，注意结果中不需要出现你的思考过程，如果有，你要重新读一遍目标并将内容总结一遍再输出"+templates
    if input_variables==None:
        
        chain=get_base_chain(templates,None,output_name,output_type,output_description)
        response = chain.invoke({}).content  
    else:
        
        chain=get_base_chain(templates,input_variables.keys,output_name,output_type,output_description)    
        response = chain.invoke(input_variables).content
    print(response)
    
    
    return response

async def excute_and_replay(templates,input_variables:dict={},process_name:str=None,process_classfication:str=None):
    # output_instruction=create_model(
    #     'output_instruction',
    #     process_name=(str, Field(..., description="在这里填写流程的名字，即process_name")),
    #     process_classfication=(str, Field(..., description="在这里填写流程的分类，即process_classfication")),
    #     process_prompts=(str, Field(..., description="在这里填写上个流程的prompt，即process_prompts")),
    #     process_result=(str, Field(..., description="在这里填写上个流程执行的结果，即process_result")),
    # )
    templates="## 流程名称："+process_name+ "/n ## 流程分类 "+process_classfication+templates
    output_names=["process_name","process_classfication","process_prompts","process_result"]
    output_types=[str,str,str,str]
    output_descriptions=["在这里填写流程的名字，即process_name","在这里填写流程的分类，即process_classfication","在这里填写上个流程的prompt，即process_prompts","在这里填写上个流程执行的结果，即process_result"]

    if input_variables==None:
        # base_chain=get_base_chain(templates,input_variables_names=None, output_names=output_names,output_types=output_types,output_descriptions=output_descriptions)
        base_chain=get_base_chain(templates,input_variables_names=None)
    else:
        base_chain=get_base_chain(templates,input_variables.keys,output_names,output_types,output_descriptions)
    
    # base_prompt = PromptTemplate(template=templates, input_variables=input_variables.keys).format(**input_variables)
    replay_chain=replay_results.get_repaly_results_chain(["process_name","process_classfication","process_prompts","process_result"])
    chain=base_chain|replay_chain
    # response_1=base_chain.invoke(input_variables)
    # print(response_1)
    # response=replay_chain.invoke(response_1)
    # asyncio.run(chain.astream_log(input_variables))
    
    # async for event in chain.astream_events(input_variables,version="v2"):
    #     print(event)
    response=chain.invoke(input_variables)
    print(response)
    return response




# def excute_and_replay(templates,process_name,process_classfication,input_variables):


