


import os
import dashscope
import datetime


template='''
        你是一位专业的信息搜集者，我会给你一个需求，你需要提炼其中的关键词并在互联网上寻找相关的信息，不得自行编造，得到结果后整理成完善的报告阐述给我       

      
    '''

template.format(now=datetime.datetime.now().strftime("%Y-%m"))

input=''''
    以下是你需要分析的内容：
    {search_content}="问题的基本描述"
'''


def get_intenet_search_analysis(search_content):
    content=input.format(search_content=search_content)
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
    search_content='''
        根据网上查找到的信息，中科蓝吧数字科技（苏州）有限公司确实是一家专注于AI企服领域的科技创新企业。它将AI技术作为核心驱动力，通过构建行业化的AI模型和场景化的AI能力，为各类企业提供定制化的高效、智能的AI转型升级方案，旨在帮助企业降低成本、提高效率并实现创新发展。

关于产品方面，中科蓝吧提供的云端企业服务管理软件不仅面向中小企业，也适用于大型企业。该软件集成了营销管理、经营分析等核心功能，并且还提供了一系列业务辅助工具，如客户关系管理(CRM)、供应链优化、财务管理等。这些功能模块可以帮助企业在不同业务场景下更好地应用AI技术，从而提升整体运营效率和服务质量。

此外，中科蓝吧还特别注重数据安全与隐私保护，在其产品设计中融入了多项先进的安全措施，确保用户的数据资产得到充分保障。总之，中科蓝吧致力于成为企业数字化转型过程中值得信赖的合作伙伴。
        '''
    get_intenet_search_analysis(search_content)

