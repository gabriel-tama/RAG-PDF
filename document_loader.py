# document_loader.py
from llama_index.core import SimpleDirectoryReader
from typing import Dict, List
from llama_index.readers.file import UnstructuredReader


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
        # loader = UnstructuredLoader(
        #     file_path=f"{titles[i]}.pdf",
        #     strategy="hi_res",
        # )
        loaded_docs = {}
        for i in range(len(titles)):
            # loader = UnstructuredLoader(
            #     file_path=f"{titles[i]}.pdf",
            #     strategy="hi_res",
            # )
            # loader.load()
            # for doc in loader.lazy_load():
            #     docs.append(doc)
            file_path = f"{titles[i]}.pdf"
            loader = UnstructuredReader()

            # loaded_docs[titles[i]] = SimpleDirectoryReader(input_files=[file_path], file_extractor={".pdf": UnstructuredReader()}).load_data()
            loaded_docs[titles[i]] = loader.load_data(
                                    unstructured_kwargs={"filename": file_path,"strategy":"hi_res"}
                                )
            # loaded_docs[titles[i]] = loader.load()
            for j in range(len(loaded_docs[titles[i]])):
                loaded_docs[titles[i]][j].metadata["url"]=urls[i]

        return loaded_docs
