import os
import log
from tika import parser
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def initialize(directory):

    # holds the data from the pdfs
    log.log("Parse PDFs into list ")
    all_content = []

    # all the files in pdfs directory
    for filename in os.listdir(directory):
        # check if the file is a pdf
        if filename.endswith(".pdf"):
            # get the content of the pdf
            file_path = os.path.join(directory, filename)
            raw = parser.from_file(file_path)
            all_content.append(raw['content'])
    log.log("Parse PDFs into list ")
    
   
    # split the content into chunks
    log.log("Split PDFs into chunks")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.create_documents(all_content)
    log.log("Split PDFs into chunks")

    
    # create the embeddings model
    log.log("Create embeddings model")
    embeddings_model = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-l6-v2',
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )
    log.log("Create embeddings model")

    '''
    chunks_text = [chunk.page_content for chunk in chunks]
    embeddings = embeddings_model.embed_documents(chunks_text)
    '''

    # create the chroma database (also makes the emeddigns for the chunks of text)
    log.log("Create Chroma vector database")
    chromadb = Chroma.from_documents(chunks, embeddings_model)
    log.log("Create Chroma vector database")
    
    return chromadb

def query(chroma, query_text):
    
    # search for similar documents
    log.log("Query Chroma vector database")
    docs = chroma.similarity_search(query_text)
    log.log("Query Chroma vector database")

    return [doc.page_content for doc in docs]
    
