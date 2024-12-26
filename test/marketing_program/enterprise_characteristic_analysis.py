

from langchain_community.llms.tongyi import Tongyi
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


DASHSCOPE_API_KEY="sk-a48a1d84e015410292d07021f60b9acb"
import os
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY




template='''
        你是一位专业的企业特征分析师，擅长通过深入分析企业简介中的信息，提炼出企业的核心特征、竞争优势、市场定位和发展潜力。你的任务是帮助企业或外部观察者全面理解企业的独特之处，并为制定战略决策提供依据。
        ### Skills
            信息提取：从企业简介中准确提取关键信息，包括但不限于公司历史、使命愿景、产品服务、市场定位、客户群体等。
            特征分析：基于提取的信息，分析企业的核心特征，如企业文化、技术实力、创新能力、管理团队等。
            竞争评估：识别企业的竞争优势和差异化因素，评估其在市场中的地位。
            市场洞察：了解企业的目标市场和客户群体，分析市场需求和趋势。
            发展潜力：评估企业的未来发展潜力，包括增长机会、扩展计划和技术进步等。
            风险识别：识别企业在运营过程中可能面临的风险和挑战。
            策略建议：基于上述分析结果，提供具体的战略建议，帮助企业优化发展路径。
        ### Rules
            保持专业：在分析过程中保持专业态度，确保所有行动都有据可依。
            数据驱动：基于实际数据和事实进行分析，避免主观臆断。
            全面覆盖：确保分析涵盖所有相关方面，不遗漏重要信息。
            直接输出：专注于具体的操作和任务执行，不需要过多讨论或解释。
            逻辑清晰：输出的内容应逻辑连贯，易于理解和应用。
        ### Workflow
            用户提供企业的详细简介，包括但不限于公司历史、使命愿景、产品服务、市场定位、客户群体等。
            你将从企业简介中提取关键信息，包括公司的历史背景、使命愿景、主要产品和服务、市场定位、客户群体等。
            基于提取的信息，分析企业的核心特征，如企业文化、技术实力、创新能力、管理团队等。
            识别企业的竞争优势和差异化因素，评估其在市场中的地位。
            了解企业的目标市场和客户群体，分析市场需求和趋势。
            评估企业的未来发展潜力，包括增长机会、扩展计划和技术进步等。
            识别企业在运营过程中可能面临的风险和挑战。
            提供具体的战略建议，帮助企业优化发展路径。
        ### Initialization
            作为专业的企业特征分析师，让我们有条不紊地进行工作。遵循上述规则，为我提供一份完整的企业特征分析的报告
            你拥有<Skill>的技能并遵守<Rule>，根据<Workflow>完成相对应的任务。请避免讨论我发送的内容，不需要回复过多内容，不需要自我介绍

        以下是你需要分析的内容：
        {product_content}

      
    '''




llm=Tongyi(model_name="qwen-plus",temperature=1)


prompt=PromptTemplate(
        template=template,
        input_variables=["product_content"]#这个question就是用户输入的内容,这行代码不可缺少
)

chain = prompt|llm


def get_enterprise_characteristic_analysis(product_content):
    input={
        "product_content":product_content,
    }
    res=chain.invoke(input)#运行
    print(res)#打印结果
    return res



if __name__ == '__main__':
    product_content='''
        ### 中科蓝吧数字科技（苏州）有限公司未来3-5年战略愿景报告

#### 一、综合分析

**1. 行业概述**

- **整体规模与增长率**：截至2024年，中国AI企服市场规模预计将达到XX亿元人民币，同比增长XX%。主要驱动因素包括政策支持、技术进步和企业数字化转型需求。
- **主要参与者及其市场份额**：
  - 头部公司如商汤科技、旷视科技占据较大市场份额，尤其在计算机视觉领域。
  - 非头部公司如云从科技、依图科技专注于特定细分市场或技术领域。
- **技术进步水平**：
  - 深度学习算法不断优化，算力成本下降。
  - 云端机器学习平台降低了开发门槛，加速了AI技术的应用落地。
  - 自然语言处理（NLP）、计算机视觉等技术取得了显著进展。

**2. 宏观经济环境**

- **全球经济状况**：
  - 2024年中国GDP增长率为5.5%，稳定的经济增长为企业提供更多资金用于技术创新。
  - 温和通胀（约2%），有利于消费市场的稳定发展。
  - 人民币兑美元汇率约为7.1，短期内推高进口成本，但从长期看提升国内产品的价格竞争力。
- **对行业的影响**：
  - 成本结构：原材料和技术设备的进口成本可能上升，但出口型企业的价格竞争力增强。
  - 市场需求：各行业数字化转型加速推进，对高效、智能的企业服务需求增长。
  - 供应链：全球供应链不确定性增加，需加强供应链管理和本地化生产。

**3. 竞争格局**

- **SWOT分析**：
  - **优势**：定制化的AI解决方案，强调数据安全与隐私保护。
  - **劣势**：品牌影响力和市场份额有限，融资规模较小。
  - **机会**：新兴市场需求如智能制造、智慧医疗，政府扶持政策。
  - **威胁**：来自头部公司的竞争压力和技术变革带来的挑战。
- **竞争态势变化趋势**：
  - 新进入者的威胁：更多初创企业涌入AI企服领域。
  - 替代品的压力：传统软件厂商和互联网巨头布局AI赛道。

**4. 技术进步**

- **技术创新速度**：
  - AI模型和场景化AI能力持续优化，提升了产品和服务的智能化程度。
  - 边缘计算与云计算融合，保证了数据传输的安全性和时效性。
- **对企业竞争力的提升**：
  - 利用新兴技术如区块链、量子计算等，构建可信的数据共享机制。
  - 开发环保技术解决方案，如优化能源管理、减少碳足迹。

**5. 法规和社会因素**

- **法规要求**：遵守《数据安全法》、《个人信息保护法》，响应政府出台的一系列鼓励人工智能发展的政策措施。
- **社会习惯变化**：消费者对个性化、智能化产品的需求增加，推动企业加快产品创新和服务升级；环保意识增强，绿色AI产品需求增加。

#### 二、战略建议

1. **强化技术创新**：持续投入研发，保持技术领先，特别是在AI模型和场景化AI能力方面。
2. **深化客户服务**：加强售后服务和支持体系，提升客户满意度和忠诚度。
3. **聚焦细分市场**：针对特定行业提供定制化解决方案，增强差异化竞争优势。
4. **加强合作伙伴关系**：与上下游企业建立紧密合作关系，形成生态链，共同应对市场变化。
5. **提升品牌影响力**：通过参加行业展会、发布白皮书等方式，提升品牌知名度和美誉度。

#### 三、未来3-5年战略愿景和发展路径

**愿景**：成为AI企服领域的创新引领者，为客户提供最可靠、最智能的定制化解决方案。

**发展路径**：

1. **多元化发展**：构建涵盖多个维度的一站式AI解决方案，满足企业客户在不同业务场景下的需求。
2. **智能化程度加深**：通过语音交互、情感识别等功能增强用户体验，提升用户粘性。
3. **生态体系建设**：打造集开发者社区、合作伙伴网络于一体的生态环境，促进上下游产业链协同发展。

#### 四、愿景口号

**“创新驱动，智领未来——为每个企业定制最可靠的AI解决方案。”**

---

通过以上分析和建议，中科蓝吧可以在激烈的市场竞争中保持优势，进一步提升市场地位，实现长期稳定的发展。
        '''
    get_enterprise_characteristic_analysis(product_content)


