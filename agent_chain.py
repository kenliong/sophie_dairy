import os
from typing import Dict

import google.generativeai as genai
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from old_diary_entries import old_diary_entries

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def initialize_vector_store(old_diary_entries: list):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vector_store = FAISS.from_texts(old_diary_entries, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store


# initialize_vector_store(old_diary_entries)


def format_diary_entry(diary_entry_path: str, **kwargs):
    """
    Format diary entry for vector store
    """
    diary_entry_path = "test_diary.txt"
    diary_entry = TextLoader(diary_entry_path).load()
    diary_with_metadata = {
        "metadata": [{"date": diary_entry["datetime"]}, {"title": diary_entry["title"]}],
        "diary_content": diary_entry["content"],
    }
    return diary_with_metadata


def add_diary_to_vector_store(diary_entry: Dict):
    """
    'dairy_entry': should be a path to a .txt file
    Add new diary entries to the vector store
    If vector store already exists, add new entries to it
    Otherwise, create a new vector store
    """

    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    if os.path.exists("faiss_index"):
        vector_store = FAISS.load_local(
            "faiss_index", embeddings=embeddings, allow_dangerous_deserialization=True
        )
    else:
        vector_store = FAISS()

    formatted_diary_entry = format_diary_entry(diary_entry)
    vector_store.add_documents(
        documents=formatted_diary_entry["diary_content"],
        metadatas=formatted_diary_entry["metadata"],
    )

    results = vector_store.asimilarity_search(formatted_diary_entry["diary_content"], top_k=1)
    for result in results:
        print(f"Diary content: {result['text']}")
        print(f"Metadata: {result['metadata']}")

    vector_store.save_local("faiss_index")
    return vector_store


def generate_initial_prompts():
    """
    Generates starter prompts based on past diary entries
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vector_store = FAISS.load_local(
        "faiss_index", embeddings=embeddings, allow_dangerous_deserialization=True
    )
    past_entries = vector_store.search(" ", search_type="similarity", k=5)
    context = "\n".join(entry.page_content for entry in past_entries)

    prompt_template = f"""
    You are a pen pal for a friend who has been struggling with their mental health.
    Based on the following past diary entries, generate 5 relevant questions to prompt your friend to start journalling.
    Past Entries: {context}

    Questions:
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["context"])
    chain = LLMChain(llm=model, prompt=prompt)

    result = chain.run({"context": context})
    return result


def chat_chain():
    """
    Uses langchain to create a question-answering chain for chatbot
    """

    # TODO: Implement this function

    return
