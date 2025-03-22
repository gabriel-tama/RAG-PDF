# config.py
import os
from typing import Optional, List
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.core import Settings
from transformers import AutoTokenizer

class Config:
    """Configuration for the document indexing and query system."""
    
    def __init__(self, model_name: str = "HuggingFaceH4/zephyr-7b-alpha", embedding_model: str = "BAAI/bge-small-en-v1.5"):
        self.hf_token: Optional[str] = os.getenv("HF_TOKEN")
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name,token=self.hf_token)
        
    def setup_global_settings(self):
        """Configure global settings for LlamaIndex."""
        Settings.llm = HuggingFaceInferenceAPI(
            model_name=self.model_name, 
            token=self.hf_token
        )
        Settings.embed_model = HuggingFaceEmbedding(
            model_name=self.embedding_model
        )

