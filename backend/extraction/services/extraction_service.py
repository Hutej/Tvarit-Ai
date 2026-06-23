from documents.repositories.document_repository import DocumentRepository
from documents.parser.factory import ParserFactory
from documents.constants import DocumentType, DocumentStatus, ProcessingStage
from extraction.factory import ExtractorFactory
from extraction.types import ExtractionRequest, ExtractionResult
from documents.exceptions import DocumentNotFoundException

class ExtractionService:
    def __init__(self):
        self.doc_repo = DocumentRepository()

    def extract_document(self, document_id: str) -> ExtractionResult:
        # 1. Load Document
        document = self.doc_repo.get_active_by_id(document_id)
        if not document:
            raise DocumentNotFoundException(f"Document {document_id} not found.")

        # Update stage to EXTRACTION
        self.doc_repo.update_metadata(document_id, {
            "processing_stage": ProcessingStage.EXTRACTION.value,
            "status": DocumentStatus.PROCESSING.value
        })

        try:
            # 2. Use ParserFactory to get parser
            parser = ParserFactory.get_parser_for_document(document)
            
            # 3. Parse Document
            parser_result = parser.parse(document)
            
            # 4. Determine Document Type
            # Try to get it from parser result metadata, fallback to document model, fallback to UNKNOWN
            doc_type_str = parser_result.metadata.document_type_hint or document.document_type
            try:
                doc_type = DocumentType(doc_type_str)
            except ValueError:
                doc_type = DocumentType.UNKNOWN
                
            # 5. Use ExtractorFactory to get extractor
            extractor = ExtractorFactory.get_extractor_for_type(doc_type)
            
            # 6. Run Extractor
            request = ExtractionRequest(
                parser_result=parser_result,
                document_type_hint=doc_type.value
            )
            extraction_result = extractor.extract(request)
            
            # Update stage and status on success
            self.doc_repo.update_metadata(document_id, {
                "processing_stage": ProcessingStage.COMPLETED.value,
                "status": DocumentStatus.PROCESSED.value
            })
            
            return extraction_result
            
        except Exception as e:
            # Update stage and status on failure
            self.doc_repo.update_metadata(document_id, {
                "processing_stage": ProcessingStage.FAILED.value,
                "status": DocumentStatus.FAILED.value
            })
            raise e
