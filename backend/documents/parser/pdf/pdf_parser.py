import os
from datetime import datetime
import fitz  # PyMuPDF
from typing import Optional

from documents.models import Document
from documents.parser.base import DocumentParser
from documents.parser.types import ParserResult, DocumentMetadata
from documents.parser.exceptions import ParsingFailedException, UnsupportedDocumentException

class PDFParser(DocumentParser):
    """
    Parser for Digital PDF documents using PyMuPDF.
    """

    def supports(self, document: Document) -> bool:
        return document.mime_type == 'application/pdf'

    def validate(self, document: Document) -> bool:
        if not os.path.exists(document.storage_path):
            raise ParsingFailedException(f"File not found: {document.storage_path}")

        try:
            with fitz.open(document.storage_path) as pdf_doc:
                if pdf_doc.page_count <= 0:
                    raise ParsingFailedException("PDF document has no pages.")
        except Exception as e:
            raise ParsingFailedException(f"Failed to open or read PDF: {str(e)}")

        return True

    def get_metadata(self, document: Document) -> DocumentMetadata:
        try:
            with fitz.open(document.storage_path) as pdf_doc:
                meta = pdf_doc.metadata or {}
                
                # Parse creation date if possible (format: D:YYYYMMDDHHmmSSZ)
                creation_date_str = meta.get('creationDate', '')
                parsed_date = None
                # Basic cleanup of PDF date format for datetime parsing if needed
                # (Skipping complex date parsing for now, keeping it robust)

                return DocumentMetadata(
                    page_count=pdf_doc.page_count,
                    title=meta.get('title'),
                    author=meta.get('author'),
                    producer=meta.get('producer'),
                    creation_date=None,  # Requires complex parsing of PDF date string
                    is_scanned=False,
                    language=None,
                    document_type_hint=None
                )
        except Exception as e:
            raise ParsingFailedException(f"Failed to extract metadata: {str(e)}")

    def parse(self, document: Document) -> ParserResult:
        if not self.supports(document):
            raise UnsupportedDocumentException(f"Unsupported MIME type for PDF parser: {document.mime_type}")

        self.validate(document)

        raw_text_parts = []
        warnings = []
        errors = []

        try:
            with fitz.open(document.storage_path) as pdf_doc:
                metadata = self.get_metadata(document)
                
                for page_num in range(pdf_doc.page_count):
                    page = pdf_doc[page_num]
                    text = page.get_text("text")
                    if text:
                        raw_text_parts.append(text.strip())
                    else:
                        warnings.append(f"No text found on page {page_num + 1}")
                    
                    if page_num < pdf_doc.page_count - 1:
                        raw_text_parts.append("\n\n===== PAGE BREAK =====\n\n")

                full_text = "".join(raw_text_parts)

                return ParserResult(
                    raw_text=full_text,
                    tables=[],
                    metadata=metadata,
                    images=[],
                    page_count=pdf_doc.page_count,
                    language=None,
                    warnings=warnings,
                    errors=errors
                )
        except Exception as e:
            raise ParsingFailedException(f"Error during PDF parsing: {str(e)}")
