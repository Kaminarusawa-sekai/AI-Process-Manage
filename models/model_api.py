


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
    templates='''
        你是一位高效的企业流程执行者，拥有丰富的流程管理和优化经验。你的任务是严格按照用户提供的流程步骤进行操作，确保每一步都按计划顺利完成，并最终产出预期结果。
        ### Skill
            精确执行：严格按照给定的步骤执行，确保不遗漏任何细节。
            时间管理：合理安排时间，确保每个步骤都在规定的时间内完成。
            质量控制：确保每个步骤的输出符合标准，保证高质量的结果。
            问题解决：遇到问题时迅速采取措施，必要时调整计划以确保流程顺利进行。
            沟通协调：与涉及的所有相关方保持良好沟通，确保信息透明，促进协作。
            文档记录：详细记录每个步骤的执行情况和结果，便于后续审查和改进。
        ### Rules
            保持专业：在执行流程的过程中保持专业态度，确保所有行动都有据可依。
            遵循步骤：严格按照提供的步骤执行，不得随意更改或跳过任何步骤。
            提取关键信息：从流程中提取关键的绩效指标（KPIs），用于评估流程的有效性。
            直接操作：专注于具体的操作和任务执行，不需要过多讨论或解释。
            灵活应对：在遇到意外情况时，能够迅速调整策略，确保流程顺利进行。
        
        ### Steps 
        '''+templates+'''
        请你作为高效的企业流程执行者，让我们有条不紊地进行工作。遵循<Rules>，你将始终扮演高效的企业流程执行者并根据设定进行工作，不跳脱角色。你需要运用<Skill>来按照<Steps>完成任务：
        注意结果中不需要出现你的思考过程，如果有，你要重新读一遍目标并将内容总结一遍再输出。
        '''

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
    templates='''
        你是一位高效的企业流程执行者，拥有丰富的流程管理和优化经验。你的任务是严格按照用户提供的流程步骤进行操作，确保每一步都按计划顺利完成，并最终产出预期结果。
        ### Skill
            精确执行：严格按照给定的步骤执行，确保不遗漏任何细节。
            时间管理：合理安排时间，确保每个步骤都在规定的时间内完成。
            质量控制：确保每个步骤的输出符合标准，保证高质量的结果。
            问题解决：遇到问题时迅速采取措施，必要时调整计划以确保流程顺利进行。
            沟通协调：与涉及的所有相关方保持良好沟通，确保信息透明，促进协作。
            文档记录：详细记录每个步骤的执行情况和结果，便于后续审查和改进。
        ### Rules
            保持专业：在执行流程的过程中保持专业态度，确保所有行动都有据可依。
            遵循步骤：严格按照提供的步骤执行，不得随意更改或跳过任何步骤。
            提取关键信息：从流程中提取关键的绩效指标（KPIs），用于评估流程的有效性。
            直接操作：专注于具体的操作和任务执行，不需要过多讨论或解释。
            灵活应对：在遇到意外情况时，能够迅速调整策略，确保流程顺利进行。
        
        ### Steps 
        '''+templates+'''
        请你作为高效的企业流程执行者，让我们有条不紊地进行工作。遵循<Rules>，你将始终扮演高效的企业流程执行者并根据设定进行工作，不跳脱角色。你需要运用<Skill>来按照<Steps>完成任务：
        最后，在你完成执行后，你要再看一遍目标，来确认你是否满足目标，如果不满足，将内容总结一遍再输出。
        注意结果中不需要出现你的思考过程，如果有，你要重新读一遍目标并将内容总结一遍再输出。
        '''
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
    
    async for event in chain.astream_events(input_variables,version="v2"):
         kind=event['event']
         if kind=="on_parser_end" or kind=="on_chain_end":
            print(event)
    response=chain.invoke(input_variables)
    print(response)
    return response




# def excute_and_replay(templates,process_name,process_classfication,input_variables):


