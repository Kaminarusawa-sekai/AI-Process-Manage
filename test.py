from models import prompts_generate


process_name = "1.1.4.1 定义战略愿景"
process_classfication="1 制定愿景和战略 1.1 定义业务理念和长期愿景 1.1.4 建立战略愿景"
requirements = prompts_generate.get_process_prompt(process_name,process_classfication)
print(requirements)