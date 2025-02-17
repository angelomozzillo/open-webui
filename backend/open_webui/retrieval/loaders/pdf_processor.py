import os
import re
import pymupdf as fitz  # PyMuPDF
from typing import Dict
from open_webui.retrieval.loaders.multi_column import column_boxes
from pydantic import BaseModel, Field

class PageContent(BaseModel):
    """Model to store extracted text for a single page."""

    page_number: int
    text: str = Field(..., min_length=1)


class PDFDocument(BaseModel):
    """Model for a processed PDF document."""

    file_name: str
    pages: Dict[int, PageContent]  # {page_number: PageContent}

class PDFProcessor:
    def __init__(self, pdf_path: str):
        """
        Initialize PDF Processor for a single file.
        Args:
            pdf_path (str): Path to the PDF file.
        """
        self.pdf_path = pdf_path
        self.pdf_text: Dict[int, str] = {}  # Store extracted text per page

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans the extracted text.
        """
        text = text.replace("\xa0", " ").replace("\t", " ")
        text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)  # Remove hyphenation
        text = re.sub(r'(?<![.!?])\s*\n\s*(?=[a-zA-Z0-9])', " ", text)  # Join broken lines
        text = re.sub(r"\s{2,}", " ", text).strip()  # Remove extra spaces
        return text
    
    def process_pdf(self):
        if self.pdf_path.endswith(".pdf"):
            try:
                pdf_doc = self.extract_pdf_text()

                # Save full text as a .txt file with page headers
                full_text = "\n\n".join(
                    [f"--- Page {page_num + 1} ---\n{page.text}" for page_num, page in enumerate(pdf_doc.pages.values())]
                )
                return full_text

            except Exception as e:
                print(f"Error processing {self.pdf_path}: {str(e)}")
        else:
            raise Exception(f'Error processing {self.pdf_path}')

    def extract_pdf_text(self) -> Dict[int, str]:
        """
        Extract text from the given PDF and store it in a dictionary.
        Returns:
            Dict[int, str]: Dictionary mapping page numbers to extracted text.
        """
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")

        pages_content = {}
        doc = fitz.open(self.pdf_path)

        for nump, page in enumerate(doc, start=1):
            full_text = []
            foot_margin, head_margin = self.detect_margins(page, nump)
            bboxes = column_boxes(
                page,
                footer_margin=foot_margin,
                header_margin=head_margin,
                no_image_text=True,
            )
            # Sort bounding boxes by their y-coordinates (top to bottom) and then by x-coordinates (left to right)
            bboxes = sorted(bboxes, key=lambda rect: (rect.y0 + rect.x0 * 1.5))
            for rect in bboxes:
                try:
                    rect_text = page.get_text(clip=rect, sort=True)
                    full_text.append(rect_text)
                except Exception as e:
                    continue

            full_text = "\n".join(full_text)
            cleaned_text = self.clean_text(full_text)

            if cleaned_text:
                pages_content[nump] = PageContent(page_number=nump, text=cleaned_text)

        return PDFDocument(file_name=os.path.basename(self.pdf_path), pages=pages_content)
    
    def detect_margins(self, page, nump):
        """
        Detects headers and footers in a PDF page.

        Args:
            page (pymupdf.Page): The PDF page to analyze.
            nump (int): The page number.

        Returns:
            tuple: A tuple containing the footer margin and header margin.
        """
        blocks = page.get_text("dict")["blocks"]
        page_height = page.rect.height

        # Definisci limiti iniziali per l'area di header e footer
        header_limit = (
            0.1 * page_height
        )  # Considera l'area superiore al 10% dell'altezza
        footer_limit = (
            0.1 * page_height
        )  # Considera l'area inferiore al 10% dell'altezza

        header_margin = page_height
        footer_margin = 0
        has_header = False
        has_footer = False

        for block in blocks:
            bbox = block["bbox"]
            y0, y1 = bbox[1], bbox[3]
            # Rileva header: blocchi nel margine superiore
            if y0 < header_limit:
                # Analizza dimensioni e testo del blocco
                block_height = y1 - y0
                block_text = "".join(
                    [
                        span["text"]
                        for line in block.get("lines", [])
                        for span in line.get("spans", [])
                    ]
                ).strip()

                # Debug print statements
                # print(
                #     f"page :{nump} Header candidate: {block_text} (height: {block_height}, y0: {y0}, y1: {y1})"
                # )

                # Condizioni per identificare un header: piccolo e breve
                if block_height < 0.05 * page_height and len(block_text) < 100:
                    header_margin = y1
                    has_header = True
                    break
                else:
                    # È contenuto normale, non un header
                    continue

        for block in blocks:
            bbox = block["bbox"]
            y0, y1 = bbox[1], bbox[3]
            # Rileva footer: blocchi nel margine inferiore
            if y1 > (page_height - footer_limit):
                block_height = y1 - y0
                block_text = "".join(
                    [
                        span["text"]
                        for line in block.get("lines", [])
                        for span in line.get("spans", [])
                    ]
                ).strip()

                # Debug print statements
                # print(
                #     f"page :{nump} Footer candidate: {block_text} (height: {block_height}, y0: {y0}, y1: {y1}), lenght {len(block_text)}, page height {page_height}"
                # )

                # Condizioni per identificare un footer: piccolo e breve
                if block_height < 0.05 * page_height and len(block_text) < 100:
                    footer_margin = page_height - y0
                    has_footer = True
                    break

        # Se non ci sono header/footer, i margini restano 0
        if not has_header:
            header_margin = 0
        if not has_footer:
            footer_margin = 0

        return int(footer_margin), int(header_margin)


if __name__ == "__main__":
    pdf_file_path = "backend/data/uploads/1d0963b0-f965-4a74-b445-f9c5fb8c749c_MOZZILLO_Missione_652_autoriz_dottorandi_signed_signed.pdf"  # Replace with actual PDF file path
    processor = PDFProcessor(pdf_file_path)
    extracted_text = processor.process_pdf()
    print(extracted_text)
