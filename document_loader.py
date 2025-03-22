# document_loader.py
from llama_index.core import SimpleDirectoryReader
from typing import Dict, List

class DocumentLoader:
    """Load documents from PDF files."""
    
    @staticmethod
    def load_documents(titles: List[str], base_path: str = "./", urls: List[str]= [""]) -> Dict[str, List]:
        """
        Load documents specified by titles from the base_path.
        
        Args:
            titles: List of document titles to load
            base_path: Base directory path
            
        Returns:
            Dictionary mapping titles to loaded documents
        """
        loaded_docs = {}
        for i in range(len(titles)):
            file_path = f"{titles[i]}.pdf"
            loaded_docs[titles[i]] = SimpleDirectoryReader(input_files=[file_path]).load_data()
            for j in range(len(loaded_docs[titles[i]])):
                loaded_docs[titles[i]][j].metadata["url"]=urls[i]

        return loaded_docs
