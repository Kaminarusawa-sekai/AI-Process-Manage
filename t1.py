from typing import List

from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser


JsonOutputKeyToolsParser(key_name="Joke", first_tool_only=True)