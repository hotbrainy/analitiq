import os
from typing import List, Optional
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunkLoader:
    def __init__(self, project_name: str):
        self.project_name = project_name

    def load_and_chunk_documents(self, path: str, extension: Optional[str] = None, chunk_size: int = 2000, chunk_overlap: int = 200):
        """
        Load files from a directory or a single file, split them into chunks, and return a list of Chunk objects.

        Parameters:
            path: Path to the file or directory containing files to be chunked.
            extension: File extension to filter the files in the directory.
            chunk_size: The size of chunks into which to split the documents.
            chunk_overlap: How much the chunks should overlap.

        Returns:
            document chunks

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file's extension is not among the allowed ones.
        """
        if os.path.isfile(path):
            loader = TextLoader(path)
        elif os.path.isdir(path):
            loader = DirectoryLoader(path, glob=f"**/*.{extension}", loader_cls=TextLoader)
        else:
            raise FileNotFoundError(f"{path} does not exist or is a special file (e.g., socket, device file, etc.).")

        documents = loader.load()
        doc_lengths = {doc.metadata['source']: len(doc.page_content) for doc in documents}

        doc_splitter = RecursiveCharacterTextSplitter(chunk_size=int(chunk_size), chunk_overlap=int(chunk_overlap))
        documents_chunks = doc_splitter.split_documents(documents)

        return documents_chunks, doc_lengths
