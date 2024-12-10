from step import Step
from typing import Any

from ..models import model_api

class ModelProcessExcutor(Step):
    

    def execute(self, templates,input_variables=None):
        
        response=model_api.base_excute(templates,input_variables)

        return response
    
    if __name__ == "__main__":
    # 用户输入示例
        process_name = "1.1.4.1 定义战略愿景"
        process_classfication="1 制定愿景和战略 1.1 定义业务理念和长期愿景 1.1.4 建立战略愿景"
        prompts='''
                    ## 流程名称：
                    定义战略愿景

                    ## 目标：
                    明确企业的未来方向和长期目标
                    为企业的发展提供明确的指导方针
                    激励和统一全体员工的努力和行动

                    ## 步骤：

                    ### 1. 进行环境分析
                    - **市场环境**：分析当前市场趋势、客户需求和竞争态势。
                    - **内部环境**：评估企业的资源、能力和核心竞争力。
                    - **宏观环境**：考虑经济、技术、社会和政治因素对企业的影响。

                    ### 2. 确定愿景的核心要素
                    - **长期目标**：明确企业希望在未来5-10年内实现的主要目标。
                    - **价值观**：定义企业的核心价值观和文化，这些将指导企业的决策和行为。
                    - **独特定位**：识别企业在市场中的独特定位和竞争优势。

                    ### 3. 组织高层讨论
                    - **召开战略会议**：邀请企业高层管理团队、董事会成员和其他关键利益相关者参与讨论。
                    - **头脑风暴**：通过头脑风暴会议，集思广益，提出各种可能的发展方向和愿景。
                    - **评估和筛选**：对提出的愿景进行评估，筛选出最具潜力和可行性的选项。

                    ### 4. 定义愿景陈述
                    - **简洁明了**：确保愿景陈述简洁、明了，并能够激发员工的共鸣。
                    - **具体且可衡量**：愿景陈述应包含具体的目标，并且能够被衡量和评估。
                    - **激励性**：愿景应具有激励性，能够激发全体员工的热情和动力。

                    ### 5. 审核和修订
                    - **内部审核**：邀请企业内部不同层级的员工对愿景陈述进行反馈，确保其可行性和合理性。
                    - **外部咨询**：在必要时，邀请外部专家或顾问对愿景进行评估和建议。
                    - **修订**：根据反馈和建议，对愿景陈述进行必要的修订和完善。

                    ### 6. 宣传和沟通
                    - **内部沟通**：通过内部会议、邮件、公告等方式，将愿景传达给全体员工。
                    - **培训和教育**：组织培训和教育活动，帮助员工理解和认同企业愿景。
                    - **外部沟通**：通过媒体、公司官网、宣传资料等方式，将愿景传达给客户、合作伙伴和其他利益相关者。

                    ### 7. 实施和监控
                    - **制定行动计划**：将愿景分解成具体的行动计划和项目，明确责任人和时间表。
                    - **定期评估**：定期评估愿景的实施情况，监控进展，并根据需要进行调整。
                    - **反馈机制**：建立反馈机制，收集员工和其他利益相关者的意见和建议，不断改进和优化愿景。

                    ### 注意事项：
                    - **现实可行性**：确保愿景在现实中具有可行性，不要过于理想化。
                    - **员工参与**：鼓励员工参与愿景的制定和实施过程，增强他们的认同感和责任感。
                    - **灵活应变**：愿景应具备一定的灵活性，以适应外部环境的变化。
                    - **持续沟通**：保持持续的沟通和宣传，确保全体员工始终了解和认同企业愿景。
                    '''
        requirements = execute(prompts)
        print(requirements)
