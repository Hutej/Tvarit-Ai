# API Reference

This document exhaustively details the backend APIs required to implement the Tvarit AI frontend. All endpoints are prefixed with `/api`.

---

## 1. Document Upload API

**Purpose:** Securely uploads a raw medical document to the system and initiates the document lifecycle. Returns a tracking ID needed for the workflow.
**Method:** `POST`
**URL:** `/api/documents/upload`
**Headers:** `Content-Type: multipart/form-data`
**Authentication:** Assumed None for Hackathon (or standard Bearer token if configured later).

### Request Parameters
*   **Path:** None
*   **Query:** None

### JavaScript Request Payload Example (FormData)
```javascript
const formData = new FormData();
formData.append('file', fileObject); // fileObject from input type="file"
```

### Response Body Example (200 OK - Success)
```json
{
  "id": "e4b3b1f2-5b9c-4d8e-9b2c-1b2c3d4e5f6a",
  "filename": "clinical_note.pdf",
  "document_type": "UNKNOWN",
  "status": "UPLOADED",
  "upload_date": "2026-06-23T12:00:00Z"
}
```
**Response Field Explanation:**
*   `id`: The unique UUID of the document. Crucial for the next API step.
*   `status`: Initial lifecycle stage.

### Error Examples
```json
// 400 Bad Request
{
  "error": "VALIDATION_ERROR",
  "details": "File size exceeds 10MB limit."
}
```

### Axios Implementation Example (`src/services/api.js`)
```javascript
import api from './apiConfig';

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};
```

### React Query Integration Example (`src/hooks/useWorkflow.js`)
```jsx
import { useMutation } from '@tanstack/react-query';
import { uploadDocument } from '../services/api';

export const useUploadDocument = () => {
  return useMutation({
    mutationFn: uploadDocument,
    onSuccess: (data) => {
      console.log('Document uploaded successfully, ID:', data.id);
    },
    onError: (error) => {
      console.error('Upload failed:', error.response?.data || error.message);
    }
  });
};
```

### Frontend Notes
*   **Retry Behavior:** Do not automatically retry uploads to prevent duplicate storage. Notify the user to retry.
*   **Loading Expectations:** Fast (< 1s), but depends on file size and network. Use a progress bar via Axios `onUploadProgress` if possible.

---

## 2. Workflow Orchestration API

**Purpose:** Triggers the complete LangGraph orchestration pipeline (Parse → Extract → Build Auth → Load Template → Gap Analysis → Rule Engine).
**Method:** `POST`
**URL:** `/api/workflow/run`
**Headers:** `Content-Type: application/json`

### JavaScript Request Payload Example
```javascript
const payload = {
  document_id: "e4b3b1f2-5b9c-4d8e-9b2c-1b2c3d4e5f6a",
  procedure_code: "72148",
  procedure_name: "MRI Lumbar Spine without contrast"
};
```

### Response Body Example (200 OK - Success)
```json
{
  "authorization_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
  "procedure": "MRI Lumbar Spine without contrast",
  "patient_name": "John Doe",
  "readiness_score": 65,
  "risk_level": "HIGH",
  "matched_evidence_count": 5,
  "missing_evidence_count": 2,
  "recommendations": [
    "Upload or provide evidence for imaging: X-Ray Lumbar Spine (within 6 months)"
  ],
  "summary": "Submission is incomplete. Missing 2 critical elements."
}
```

### Axios Implementation Example
```javascript
export const runWorkflow = async (payload) => {
  const response = await api.post('/workflow/run', payload);
  return response.data;
};
```

### React Query Integration Example
```jsx
import { useMutation } from '@tanstack/react-query';
import { runWorkflow } from '../services/api';
import { useNavigate } from 'react-router-dom';

export const useRunWorkflow = () => {
  const navigate = useNavigate();

  return useMutation({
    mutationFn: runWorkflow,
    onSuccess: (data) => {
      // Route immediately to the dashboard on success
      navigate(`/dashboard/${data.authorization_id}`);
    }
  });
};
```

### Frontend Notes
*   **Expected Latency:** High (10–30 seconds). The backend performs complex AI extraction via OpenAI.
*   **Loading Expectations:** The UI *must* display a robust, staged loading animation to keep the user engaged. Do not just show a spinner. Show simulated progress steps.
*   **Timeout Handling:** Set the Axios timeout to at least 60000ms (60 seconds) for this specific endpoint.
*   **Retry Behavior:** Do not auto-retry 500s. You may auto-retry 502s once.

---

## 3. Dashboard API

**Purpose:** Retrieves the comprehensive, frontend-friendly dashboard data for a processed authorization request.
**Method:** `GET`
**URL:** `/api/workflow/dashboard/{authorization_id}`
**Headers:** `Accept: application/json`

### Request Parameters
*   **Path:** `authorization_id` (String UUID, Required)

### Response Body Example (200 OK - Success)
```json
{
  "authorization_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
  "patient_name": "John Doe",
  "procedure_name": "MRI Lumbar Spine without contrast",
  "readiness_score": 65,
  "risk_level": "HIGH",
  "completion_percentage": 71.4,
  "matched_evidence": [
    {
      "category": "DIAGNOSIS",
      "requirement": "Low Back Pain",
      "status": "MATCHED",
      "matched_value": "Patient presents with severe low back pain.",
      "reason": "Exact or substring match found."
    }
  ],
  "missing_evidence": [
    {
      "category": "IMAGING",
      "requirement": "X-Ray Lumbar Spine (within 6 months)",
      "status": "MISSING",
      "matched_value": null,
      "reason": "Missing required imaging."
    }
  ],
  "recommendations": [
    "Upload or provide evidence for imaging: X-Ray Lumbar Spine (within 6 months)"
  ],
  "summary": "Submission is incomplete. Missing critical elements."
}
```
**Response Field Explanation:**
*   `readiness_score` (0-100): Determines the primary gauge chart value.
*   `risk_level` (LOW, MEDIUM, HIGH, CRITICAL): Determines badge colors.
*   `matched_evidence` & `missing_evidence`: Arrays driving the core split-view UI.

### Axios Implementation Example
```javascript
export const getDashboard = async (authorizationId) => {
  const response = await api.get(`/workflow/dashboard/${authorizationId}`);
  return response.data;
};
```

### React Query Integration Example
```jsx
import { useQuery } from '@tanstack/react-query';
import { getDashboard } from '../services/api';

export const useDashboard = (authorizationId) => {
  return useQuery({
    queryKey: ['dashboard', authorizationId],
    queryFn: () => getDashboard(authorizationId),
    enabled: !!authorizationId,
    staleTime: Infinity, // Data is immutable once processed
  });
};
```

### Frontend Notes
*   **Expected Latency:** Low (< 200ms). This is a fast retrieval query.
*   **Retry Behavior:** Standard React Query retry (3 retries).
*   **Caching:** Cache this heavily using React Query.

---

## Complete API Call Sequence

1. User Drops File -> `POST /api/documents/upload` -> Returns `document_id`.
2. User Selects Procedure -> `POST /api/workflow/run` (Payload: `document_id`, `procedure_code`) -> Wait 15s -> Returns `authorization_id`.
3. Route changes to `/dashboard/{authorization_id}`.
4. Page Mounts -> `GET /api/workflow/dashboard/{authorization_id}` -> Renders UI.
