import asyncio
import os
from datetime import datetime, timezone
from typing import Dict
import json
import pandas as pd

import google.generativeai as genai
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.output_parsers import CommaSeparatedListOutputParser, PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from utils.prompt_templates import *

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_llm_instance():
    model = genai.GenerativeModel('gemini-1.5-flash')
    #model = genai.GenerativeModel("gemini-1.0-pro")
    return model


def get_completion(model, prompt):
    response = model.generate_content(prompt)
    return response.text


async def async_get_completion(model, prompt):
    response = await model.generate_content_async(prompt)
    return response.text


def retrieve_sahha_insights(date_time, user_id):
    """
    Integration of Sahha API is not possible now so as aligned, we have retrieved a static json file
    for a given day from the Sahha team. We assume user_id to be 4 and the output is from a given day.
    """
    user_id = 4 #hard-coded

    with open('data/sample_sahha_scores.json') as f:
        d = json.load(f)
    with open('data/sahha_metadata_flatten.json') as f:
        md = json.load(f)

    sophie_dic = d[user_id]
    factors_df = pd.DataFrame(sophie_dic['factors'])

    lacking_df = factors_df[factors_df['state'] == 'low']
    lacking_df['metadata'] = lacking_df['name'].map(md)

    lacking_df['prompt'] = lacking_df.apply(lambda x: f"For {x['name']}, {x['metadata']}, you're at {x['value']} {x['unit']}, "
                                                      f"which is {x['state']}, compared to the average of {x['score']} {x['unit']}.", axis=1)

    sahha_prompt = ' '.join(lacking_df['prompt'].tolist())

    return sahha_prompt
