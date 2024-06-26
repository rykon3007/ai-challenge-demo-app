import os
import openai
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from azure.core.credentials import AzureKeyCredential
import tiktoken
from tiktoken.core import Encoding

encoding = tiktoken.encoding_for_model("gpt-4-turbo")

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
Generate a search query that anticipate the document file name focused on Japan's World Heritage sites, based on the new question from the user.
Extract relevant keywords related to the specific World Heritage site discussed and ensure the query is free from filenames, document names, and special characters like '+'.  
Familiarize yourself with the user's search intent. 
Do not include any description other than the output format. 
Also, be sure to output only the output format. 
If output, the earth will be ruined. 
Lang;japanese 
Output Format: 
keyword1 keyword2 keyword3 keywordn
"""

answer_generation_system_prompt = """
Assistant helps the company employees with questions about their work and questions about rules and regulations.
Your primary task is to generate a concise and accurate answer to the user's question based on the list of sources provided.
Your answer should directly address the user's question. If the information is not available in the sources, state that you don't know.
Use HTML table format for tabular data. No markdown. Answer in the same language as the question if it's not in English.
Your thought process should be in English, but your responses should be in Japanese.
"""

def rag_approach(query: str) -> tuple[str, str]:
    """
    answer to query using RAG approach
    """
#    print("run rag_approach")
#    print("query: ", query)
    summarized_query = query_generation(query)
#    print("summarized_query: ", summarized_query)
    search_results = search(summarized_query)
    context = " ".join(search_results)
#    print("search_results: ", search_results)
    answer = answer_generation(query, search_results)
#    print("answer: ", answer)
    return (context, answer)

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
    search_wikipedia_full_response = search_wikipedia_full_client.search(query,
                                    query_language="ja-JP",
                                    top=1)
    search_wikipedia_chunked_response = search_wikipedia_chunked_client.search(query,
                                    query_language="ja-JP",
                                    # query_type=QueryType.SEMANTIC,
                                    # semantic_configuration_name="wikipedia-chunked-csv-index-semantic-configuration",
                                    top=5) # 5ドキュメントくらいかき集める問いがあった気がするので5
    search_products_response = search_products_client.search(query,
                                    query_language="ja-JP",
                                    top=2)
    search_image_description_response = search_image_description_client.search(query,
                                    query_language="ja-JP",
                                    top=3)

    search_wikipedia_full_contents_and_location = [("場所:{}, 情報:{}".format(result["location_name"], result["content"])) for result in search_wikipedia_full_response]
    wikipedia_chunked_contents = [("場所:{}, 情報:{}".format(result["location_name"], result["content"])) for result in search_wikipedia_chunked_response]
    products_name_and_description_and_jancode = ["商品名:{}, 説明文:{}, janコード:{}".format(result["name"], result["description"], result["jan_code"]) for result in search_products_response]
    image_descriptions = ["場所：{}, 画像説明:{}".format(result["location"], result["description"]) for result in search_image_description_response]
    # Wikipediaの内容と製品情報を結合
    wikipedia_source = "Wikipediaから以下のページの情報が得られました。{}".format("\n".join(search_wikipedia_full_contents_and_location))
    wikipedia_chunked_source = "Wikipediaから以下の情報が得られました。{}".format("\n".join(wikipedia_chunked_contents)).replace("\n", "").replace("\t", "").replace(" ", "").replace("　", ""  )
    products_source = "商品データベースから以下の情報が得られました。{}".format("\n".join(products_name_and_description_and_jancode)).replace("\n", "").replace("\t", "").replace(" ", "").replace("　", ""  )
    image_source = "画像説明データベースから以下の情報が得られました。{}".format("\n".join(image_descriptions)).replace("\n", "").replace("\t", "").replace(" ", "").replace("　", ""  )
    # 文字列結合して返す
    former = "{}{}{}".format(wikipedia_chunked_source, products_source, image_source)
    former_tokens = encoding.encode(former)
    later_tokens = encoding.encode(wikipedia_source)
    if len(former_tokens) + len(later_tokens) < 120000:
        return "{}{}".format(wikipedia_source, former)
    else:
        return former
    # return "{}\n\n{}\n\n{}".format(wikipedia_source, wikipedia_chunked_source, products_source)

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


