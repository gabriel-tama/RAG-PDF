# query_engine_builder.py
from llama_index.core.indices.query.query_transform.base import DecomposeQueryTransform
from llama_index.core.query_engine.transform_query_engine import TransformQueryEngine
from llama_index.core.indices.composability import ComposableGraph
from typing import Dict

class QueryEngineBuilder:
    """Build query engines for indices and graphs."""
    
    def __init__(self, llm):
        """
        Initialize the query engine builder.
        
        Args:
            llm: Language model to use for querying
        """
        self.llm = llm
        self.decompose_transform = DecomposeQueryTransform(self.llm, verbose=True)
        
    def build_custom_query_engines(self, indices: Dict[str, object], graph: ComposableGraph) -> Dict[str, object]:
        """
        Build custom query engines for indices and graphs.
        
        Args:
            indices: Dictionary mapping titles to indices
            graph: Composable graph
            
        Returns:
            Dictionary mapping index IDs to query engines
        """
        custom_query_engines = {}
        
        # Build query engines for individual indices
        for index in indices.values():
            query_engine = index.as_query_engine(llm=self.llm)
            transform_extra_info = {'index_summary': index.index_struct.summary}
            transformed_query_engine = TransformQueryEngine(
                query_engine, 
                self.decompose_transform, 
                transform_metadata=transform_extra_info
            )
            custom_query_engines[index.index_id] = transformed_query_engine
        
        # Build query engine for the root index
        custom_query_engines[graph.root_index.index_id] = graph.root_index.as_query_engine(
            retriever_mode='simple', 
            response_mode='tree_summarize', 
            llm=self.llm
        )
        
        return custom_query_engines
    
    def build_graph_query_engine(self, graph: ComposableGraph, custom_query_engines: Dict[str, object]):
        """
        Build a graph query engine.
        
        Args:
            graph: Composable graph
            custom_query_engines: Dictionary mapping index IDs to query engines
            
        Returns:
            Graph query engine
        """
        return graph.as_query_engine(custom_query_engines=custom_query_engines)

