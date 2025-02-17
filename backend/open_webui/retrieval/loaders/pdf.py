from typing import AsyncIterator, Iterator, List, Tuple
import re
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
import io
from open_webui.retrieval.loaders.pdf_processor import PDFProcessor


class TxtDocumentLoader(BaseLoader):
    """An example document loader that reads a file line by line."""

    def __init__(self, file_path: str) -> None:
        """Initialize the loader with a file path.

        Args:
            file_path: The path to the file to load.
        """
        print('Init')
        self.file_path = file_path
        
    def parse_page_number(self, line: str) -> int:
        """Extract the page number from a line with page header.

        Args:
            line (str): A line with a page header like '--- Page {page_num + 1} ---'.
        
        Returns:
            int: The page number extracted from the header.
        """
        match = re.match(r"--- Page (\d+) ---", line.strip())
        if match:
            return int(match.group(1))
        return -1  # Return -1 if no page header is found

    def lazy_load(self) -> Iterator[Document]:
        """A lazy loader that reads a file line by line."""
        text_content = PDFProcessor(self.file_path).process_pdf()
        print(text_content)

        f = io.StringIO(text_content)
        
        line_number = 0
        page_number = 0  # Initialize with page 0

        for line in f:
            # Skip lines that are empty or contain only whitespace
            if line.strip() == "":
                continue

            # Try to find page number based on page header
            current_page_number = self.parse_page_number(line)
            if current_page_number != -1:
                page_number = current_page_number
                continue  # Skip adding page headers as content

            # Yield Document with page number and line content (without the page header)
            yield Document(
                page_content=line.strip(),  # Remove leading/trailing spaces
                metadata={
                    "line_number": line_number,
                    "page_number": page_number,
                    "source": self.file_path,
                },
            )
            line_number += 1

    async def alazy_load(self) -> AsyncIterator[Document]:
        """An async lazy loader that reads a file line by line."""
        text_content = PDFProcessor(self.file_path).process_pdf()
        print(text_content)
        f = io.StringIO(text_content)

        line_number = 0
        page_number = 0  # Initialize with page 0

        async for line in f:
            # Skip lines that are empty or contain only whitespace
            if line.strip() == "":
                continue

            # Try to find page number based on page header
            current_page_number = self.parse_page_number(line)
            if current_page_number != -1:
                page_number = current_page_number
                continue  # Skip adding page headers as content

            # Yield Document with page number and line content (without the page header)
            yield Document(
                page_content=line.strip(),  # Remove leading/trailing spaces
                metadata={
                    "line_number": line_number,
                    "page_number": page_number,
                    "source": self.file_path,
                },
            )
            line_number += 1
