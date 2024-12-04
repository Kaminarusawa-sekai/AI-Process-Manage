


import langchain
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

import total_config



total_config['models']['EMBEDDING_URL']