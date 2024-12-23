

import os
import dashscope





template='''
        你是一位专业的信息分析者，我会给你一段公司和公司主要产品的简介，但是未必非常准确，你需要在互联网上寻找这家公司和他的产品的介绍，并将正确的内容组织语言阐述给我
      
    '''

input=''''
    以下是你需要分析的内容：
    {product_content}="企业的基本描述"
'''




def get_initial_introduction(product_content):
    content=input.format(product_content=product_content)
    messages = [
    {'role': 'system', 'content': template},
    {'role': 'user', 'content': content}
    ]
    response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key="sk-a48a1d84e015410292d07021f60b9acb",
        model="qwen-plus", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages,
        result_format='message',
        enable_search=True
    )
    res=response.output.choices[0].message.content#运行
    print(res)#打印结果
    return res

if __name__ == '__main__':
    product_content='''
        中科蓝吧数字科技（苏州）有限公司是一家AI企服领域的科创型企业。公司以AI为核心驱动力，通过行业化AI模型、场景化AI能力，为企业量身打造高效、智能的AI转型升级方案，为企业降本增效、全新发展注入强劲的AI动能。
        我们的产品是一款面向中小企业的云端企业服务管理软件，主要功能包括营销管理和经营分析，以及一些业务辅助功能。
        '''
    get_initial_introduction(product_content)



