from step import Step
from typing import Any

class ModelProcessExcutor(Step):
    

    def execute(self, prompt,context: Dict[str, Any]) -> Dict[str, Any]:
        print("Executing GetDataStep")
        data = {"data": "some_data"}
        context.update(data)
        return context