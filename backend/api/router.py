from ninja_extra import NinjaExtraAPI
from documents.api.endpoints import DocumentController

api = NinjaExtraAPI(
    title="Tvarit AI API",
    description="API for Tvarit AI - Prior Authorization Pre-validation System",
    version="1.0.0",
)

api.register_controllers(DocumentController)

