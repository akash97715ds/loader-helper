# Assuming UnstructuredFileLoader is defined and correctly imported

from langchain.document_loaders import UnstructuredFileLoader
from collections import defaultdict

class CategoryContentFetcher(UnstructuredFileLoader):
    def __init__(self, file_path, mode="elements", strategy="hi_res"):
        """
        Initializes the CategoryContentFetcher with file path, mode, and strategy.
        
        :param file_path: Path to the file to be processed.
        :param mode: Loading mode, passed to UnstructuredFileLoader.
        :param strategy: Strategy for loading, passed to UnstructuredFileLoader.
        """
        # Initialize the superclass with the file path and any other necessary parameters
        super().__init__(file_path, mode=mode, strategy=strategy)
        # Load the documents immediately or as per your requirement
        self.documents = self.load()  # Assuming load() is a method from UnstructuredFileLoader
        self.category_counts = self._calculate_category_counts()

    def _calculate_category_counts(self):
        """
        Calculates the counts of each category found in the documents.
        
        :return: A dictionary with categories as keys and their counts as values.
        """
        category_counts = {}
        for doc in self.documents:
            # Assuming each 'doc' has a 'metadata' attribute with a 'category' key
            category = doc.metadata.get('category')
            if category:
                category_counts[category] = category_counts.get(category, 0) + 1
        return category_counts

    def fetch_content_by_category(self, category="Table"):
        """
        Fetches page_content of documents that have a specified category in their metadata.
        
        :param category: Category to filter the documents by. Default is "Table".
        :return: List of page_content strings from documents matching the specified category.
        """
        return [(doc.page_content, doc.metadata) for doc in self.documents if doc.metadata.get('category') == category]

    def get_category_counts(self):
        """
        Returns the calculated counts of each category.
        
        :return: A dictionary with categories as keys and their counts as values.
        """
        return self.category_counts
    def enhance_table_content(self, documents):
        """
        Enhances the content of documents categorized as tables by organizing, sorting, and merging them
        based on their parent_id and page_number.
        
        :param documents: List of tuples, each containing page_content and metadata, to be enhanced.
        :return: A dictionary of merged contents by parent_id.
        """
        organized_docs = defaultdict(list)
        for content, metadata in documents:
            parent_id = metadata.get('parent_id', 'no_parent')  # Handle documents without a parent_id
            organized_docs[parent_id].append((content, metadata))
        
        # Ensure each group is sorted by page_number
        for parent_id in organized_docs:
            organized_docs[parent_id].sort(key=lambda x: x[1]['page_number'])
        
        # Step 2: Merge contents
        merged_contents = {}
        for parent_id, docs in organized_docs.items():
            # Simple string concatenation to merge document content
            merged_content = " ".join([doc[0] for doc in docs])
            merged_contents[parent_id] = merged_content
        
        # Return the merged contents organized by parent_id
        return merged_contents
