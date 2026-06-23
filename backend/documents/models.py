from django.db import models
from django.utils import timezone
import uuid

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_filename = models.CharField(max_length=255)
    stored_filename = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)
    extension = models.CharField(max_length=10)
    mime_type = models.CharField(max_length=100)
    size = models.BigIntegerField()
    sha256_checksum = models.CharField(max_length=64, unique=True, db_index=True)
    storage_path = models.CharField(max_length=1024)
    upload_timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, default='UPLOADED')
    processing_stage = models.CharField(max_length=50, default='UPLOAD')
    document_type = models.CharField(max_length=50, default='UNKNOWN')
    page_count = models.IntegerField(null=True, blank=True)
    is_scanned = models.BooleanField(null=True, blank=True)
    patient_id = models.CharField(max_length=100, null=True, blank=True)
    authorization_case_id = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'documents_document'
        ordering = ['-upload_timestamp']

    def __str__(self):
        return self.original_filename
