# index_builder.py
from llama_index.core import VectorStoreIndex, SimpleKeywordTableIndex
from llama_index.core.indices.composability import ComposableGraph
from typing import Dict, List

class IndexBuilder:
    """Build indices from loaded documents."""
    
    def __init__(self, llm, embed_model):
        """
        Initialize the index builder.
        
        Args:
            llm: Language model to use for indexing
            embed_model: Embedding model to use for indexing
        """
        self.llm = llm
        self.embed_model = embed_model
        
    def build_indices(self, document_dict: Dict[str, List]) -> Dict[str, VectorStoreIndex]:
        """
        Build vector store indices from loaded documents.
        
        Args:
            document_dict: Dictionary mapping titles to documents
            
        Returns:
            Dictionary mapping titles to indices
        """
        indices = {}
        for title, docs in document_dict.items():
            indices[title] = VectorStoreIndex.from_documents(
                docs, 
                llm=self.llm,
                embed_model=self.embed_model
            )
        return indices
    
    @staticmethod
    def generate_index_summaries(titles: List[str]) -> Dict[str, str]:
        """
        Generate summaries for indices.
        
        Args:
            titles: List of document titles
            
        Returns:
            Dictionary mapping titles to summaries
        """
        return {title: f"Car brochures about {title}" for title in titles}
    
    def build_composable_graph(self, indices: Dict[str, VectorStoreIndex], summaries: Dict[str, str]) -> ComposableGraph:
        """
        Build a composable graph from indices.
        
        Args:
            indices: Dictionary mapping titles to indices
            summaries: Dictionary mapping titles to summaries
            
        Returns:
            Composable graph
        """
        return ComposableGraph.from_indices(
            SimpleKeywordTableIndex,
            [index for _, index in indices.items()], 
            [summary for _, summary in summaries.items()],
            max_keywords_per_chunk=50
        )