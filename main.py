import streamlit as st

from config import Config
from document_loader import DocumentLoader
from index_builder import IndexBuilder
from query_engine_builder import QueryEngineBuilder

from llama_index.core import Settings

# Page configuration
st.set_page_config(
    page_title="RAG Knowledge Assistant",
    page_icon="🧠",
)

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Main application area
st.title("RAG Knowledge Assistant")


config = Config()
config.setup_global_settings()

# Define document titles
wiki_titles = ["2021_ALL-NEW-ISUZU-D-MAX", "2021_ALL-NEW-ISUZU-mu-X",  "ISUZU_BROSUR_PDF_PORTRAIT_TRAGA_MEI2023", "BROSUR_EURO4-FVZ","2023_ELF_Brosur_NLR-NLR-L_Maret"]
wiki_titles_url = ["https://isuzu-astra.com/wp-content/uploads/2021/11/2021_ALL-NEW-ISUZU-D-MAX.pdf","https://isuzu-astra.com/wp-content/uploads/2021/11/2021_ALL-NEW-ISUZU-mu-X.pdf","https://isuzu-astra.com/wp-content/uploads/2023/04/2023_ELF_Brosur_NLR-NLR-L_Maret.pdf","https://isuzu-astra.com/wp-content/uploads/2023/05/ISUZU_BROSUR_PDF_PORTRAIT_TRAGA_MEI2023.pdf","https://isuzu-astra.com/wp-content/uploads/2022/04/BROSUR_EURO4-FVZ.pdf"]
# Load documents
document_loader = DocumentLoader()
docs = document_loader.load_documents(wiki_titles,urls=wiki_titles_url)

# Build indices
index_builder = IndexBuilder(Settings.llm, Settings.embed_model)
indices = index_builder.build_indices(docs)
summaries = index_builder.generate_index_summaries(wiki_titles)
graph = index_builder.build_composable_graph(indices, summaries)

# Build query engines
query_engine_builder = QueryEngineBuilder(Settings.llm)
custom_query_engines = query_engine_builder.build_custom_query_engines(indices, graph)
query_engine = query_engine_builder.build_graph_query_engine(graph, custom_query_engines)

# Execute query
# query = "How many products in Isuzu DMAX and Isuzu MuX combined? Name them all."





# Query input
user_query = st.chat_input("Ask a question...")

# Process the query
if user_query:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_query)
    
    response = query_engine.query(user_query)

    # Get the response from the model
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # This is where you would connect to your RAG backend
            # Replace with your actual RAG implementation

            
            # Replace these placeholders with your actual RAG output
            # answer = "This is a response from your RAG system. Connect this UI to your backend to get real answers."

            sources = set()

            # Display the answer
            st.write(response.response)
            # print(response.source_nodes)
            for m in response.metadata:
                if response.metadata.get(m,{}).get("url",None):
                    sources.add(response.metadata.get(m).get("url"))

            sources_text = ""
            for i in sources:
                sources_text+=f"{i.split('/')[-1][:-3]} Link : {i} \n\n"


            # Display sources in an expander
            with st.expander("View Sources"):
                st.write(sources_text)
            
            # Add assistant message to chat history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response.response,
                "sources": sources_text
            })