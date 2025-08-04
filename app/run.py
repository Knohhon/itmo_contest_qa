from llm.rag_chain import create_rag_chain
from llm.qa_rag import get_qa_answer
from processing.splitter import split_html_with_headers
from ingestion.dowload_html import save_to_html

if __name__=='__main__'():
    save_to_html()
    documents = split_html_with_headers(folder_path='./app/data/')
    rag_chain = create_rag_chain(documents)
    