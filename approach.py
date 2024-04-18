import os
import openai
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

openai.api_type = "azure"
openai.api_version = "2024-02-15-preview"
openai.api_base = os.environ["OPENAI_ENDPOINT"]
openai.api_key = os.environ["OPENAI_API_KEY"]


model_gpt_4_turbo = "gpt-4-turb"

search_wikipedia_full_client = SearchClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    index_name="wikipedia-full-csv-index",
      credential=AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"]))
search_wikipedia_chunked_client = SearchClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    index_name="wikipedia-chunked-csv-index",
      credential=AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"]))
search_products_client = SearchClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    index_name="products-csv-index",
      credential=AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"]))

query_generation_system_prompt = """
Generate a query to search for the answer to the question below. The query should be optimized to search in Azure Search.
Question: What is the capital of Japan?
Query: capital Japan
Question: 日本の首都はどこ？
Query: 首都 日本
"""

answer_generation_system_prompt = """
Generate an answer to the question below using the search results. The answer should be a summary of the search results.
answer should only be a one sentence summary with source document name.
Question: What is the capital of Japan?
Search results: Tokyo.
Answer: Tokyo is the capital of Japan.
Question: 日本の首都はどこ？
Search results: 東京
Answer: 東京が日本の首都です。
"""

def rag_approach(query: str) -> str:
    """
    answer to query using RAG approach
    """
    print("run rag_approach")
    print("query: ", query)
    summarized_query = query_generation(query)
    print("summarized_query: ", summarized_query)
    search_results = search(summarized_query)
    print("search_results: ", search_results)
    answer = answer_generation(query, search_results)
    print("answer: ", answer)
    return answer

def rag_with_image(query: str, image: str) -> str:
    """
    answer to query with image using RAG approach
    """
    summarized_query = query_generation(query)

    search_results = search(summarized_query)
    answer = answer_generation(query, search_results)
    return answer

def query_generation(query: str) -> str:
    """
    generate query using GPT-3.5 to extract keyword
    optimized to search in Azure Search
    """
    response = openai.ChatCompletion.create(
        engine=model_gpt_4_turbo,
        messages=[
            {"role": "system", "content": query_generation_system_prompt},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content

def search(query: str) -> list[str]:
    # search_wikipedia_full_response = search_wikipedia_full_client.search(query,
    #                                 query_language="ja-JP",
    #                                 top=5)
    search_wikipedia_chunked_response = search_wikipedia_chunked_client.search(query,
                                    query_language="ja-JP",
                                    top=5) # 5ドキュメントくらいかき集める問いがあった気がするので5
    search_products_response = search_products_client.search(query,
                                    query_language="ja-JP",
                                    top=2)

    wikipedia_chunked_contents = [result["chunk"] for result in search_wikipedia_chunked_response]
    products_contents = [result["name"] for result in search_products_response]
    # 一旦そのまま文字列結合
    return wikipedia_chunked_contents + products_contents

# def search_with_image_caption(query: str, image_caption: str) -> list[str]:
#     response = search_image_client(
#         index="wikipedia-full-csv-index",
#         query=query
#     )
#     return response.data

def answer_generation(query: str, sources: list[str]) -> str:
    response = openai.ChatCompletion.create(
        engine=model_gpt_4_turbo,
        messages=[
            {"role": "system", "content": answer_generation_system_prompt},
            {"role": "user", "content": query + "\n".join(sources)}
        ]
    )
    return response.choices[0].message.content


