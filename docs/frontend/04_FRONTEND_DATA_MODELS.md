# Frontend Data Structures & Architecture

This document contains all required JavaScript object structures, expected API shapes, and architectural suggestions for the React developer. No TypeScript interfaces are used; instead, we define expected object shapes and validation rules for JavaScript.

## 1. JavaScript Object Structures & API Shapes

### Enum Constants (src/constants/enums.js)
```javascript
export const RiskLevel = {
  LOW: 'LOW',
  MEDIUM: 'MEDIUM',
  HIGH: 'HIGH',
  CRITICAL: 'CRITICAL'
};

export const EvidenceCategory = {
  DIAGNOSIS: 'DIAGNOSIS',
  DOCUMENT: 'DOCUMENT',
  CLINICAL_FINDING: 'CLINICAL_FINDING',
  IMAGING: 'IMAGING',
  MEDICATION: 'MEDICATION',
  PROVIDER_TYPE: 'PROVIDER_TYPE',
  CONSERVATIVE_TREATMENT: 'CONSERVATIVE_TREATMENT',
  LAB_RESULT: 'LAB_RESULT',
  INSURANCE: 'INSURANCE'
};

export const EvidenceStatus = {
  MATCHED: 'MATCHED',
  MISSING: 'MISSING',
  PARTIAL: 'PARTIAL',
  CONFLICTING: 'CONFLICTING'
};
```

### 1.1 Document Upload API
**Expected Request Payload:** `FormData` containing the file.
**Example Response Object:**
```javascript
const uploadResponse = {
  id: "uuid-string",           // Required: String
  filename: "file.pdf",        // Required: String
  document_type: "UNKNOWN",    // Optional: String
  status: "UPLOADED",          // Required: String
  upload_date: "2026-06-23T"   // Required: ISO Date String
};
```

### 1.2 Workflow Run API
**Expected Request Payload:**
```javascript
const workflowRunRequest = {
  document_id: "uuid-string",  // Required: String (from Upload API)
  procedure_code: "72148",     // Required: String
  procedure_name: "MRI Lumbar" // Required: String
};
```
**Example Response Object:**
```javascript
const workflowResponse = {
  authorization_id: "uuid",    // Required: String
  procedure: "MRI Lumbar",     // Required: String
  patient_name: "John Doe",    // Required: String
  readiness_score: 65,         // Required: Number (0-100)
  risk_level: "HIGH",          // Required: String (Matches RiskLevel constant)
  matched_evidence_count: 5,   // Required: Number
  missing_evidence_count: 2,   // Required: Number
  recommendations: ["rec 1"],  // Required: Array of Strings
  summary: "Text summary"      // Required: String
};
```

### 1.3 Dashboard API
**Example Dashboard Evidence Item:**
```javascript
const dashboardEvidenceItem = {
  category: "IMAGING",         // Required: String (Matches EvidenceCategory constant)
  requirement: "X-Ray",        // Required: String
  status: "MISSING",           // Required: String (Matches EvidenceStatus constant)
  matched_value: null,         // Optional: String or null
  reason: "Not found"          // Optional: String or null
};
```

**Example Dashboard Response Object:**
```javascript
const dashboardResponse = {
  authorization_id: "uuid",    // Required: String
  patient_name: "John Doe",    // Required: String
  procedure_name: "MRI Lumbar",// Required: String
  readiness_score: 65,         // Required: Number (0-100)
  risk_level: "HIGH",          // Required: String (RiskLevel enum)
  completion_percentage: 71.4, // Required: Number
  matched_evidence: [          // Required: Array of DashboardEvidenceItem
    // ... items
  ],
  missing_evidence: [          // Required: Array of DashboardEvidenceItem
    // ... items
  ],
  recommendations: [           // Required: Array of Strings
    "Recommendation 1"
  ],
  summary: "Summary text"      // Required: String
};
```

## 2. Recommended React Query Hooks (`src/hooks/useWorkflow.js`)

```jsx
import { useMutation, useQuery } from '@tanstack/react-query';
import { api } from '../services/apiConfig';

export const useUploadDocument = () => {
  return useMutation({
    mutationFn: async (file) => {
      const formData = new FormData();
      formData.append('file', file);
      const { data } = await api.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return data;
    }
  });
};

export const useRunWorkflow = () => {
  return useMutation({
    mutationFn: async (payload) => {
      const { data } = await api.post('/workflow/run', payload);
      return data;
    }
  });
};

export const useDashboard = (authorizationId) => {
  return useQuery({
    queryKey: ['dashboard', authorizationId],
    queryFn: async () => {
      const { data } = await api.get(`/workflow/dashboard/${authorizationId}`);
      return data;
    },
    enabled: !!authorizationId, // Only fetch when ID is present
    staleTime: Infinity,        // Data is immutable once processed
    gcTime: 1000 * 60 * 30,     // Keep in cache for 30 minutes
    retry: 1
  });
};
```

## 3. Suggested Project Structure

```text
src/
├── components/
│   ├── features/
│   │   ├── dashboard/
│   │   │   ├── EvidenceAccordion.jsx
│   │   │   ├── MissingEvidenceCard.jsx
│   │   │   ├── ReadinessGauge.jsx
│   │   │   └── SummaryCards.jsx
│   │   ├── upload/
│   │   │   ├── DocumentDropzone.jsx
│   │   │   └── ProcedureSelector.jsx
│   │   └── workflow/
│   │       └── ProcessingSteps.jsx
│   ├── ui/                   // shadcn components (.jsx)
├── constants/
│   ├── index.js              // Procedure lists, Color maps
│   └── enums.js              // JavaScript Enums
├── contexts/
│   └── ThemeProvider.jsx
├── hooks/
│   └── useWorkflow.js
├── layouts/
│   ├── Header.jsx
│   ├── Sidebar.jsx
│   └── MainLayout.jsx
├── pages/
│   ├── DashboardPage.jsx
│   ├── ProcessingPage.jsx
│   └── UploadPage.jsx
├── services/
│   └── apiConfig.js          // Axios instance
└── utils/
    └── helpers.js            // cn() utility for Tailwind, data formatters
```

## 4. Suggested API Service Layer (`src/services/apiConfig.js`)

```javascript
import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 60000, // 60 seconds crucial for the workflow endpoint
});

// Optional: Interceptor for generic error handling/toasts
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // You can trigger a global toast here if desired
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);
```

## 5. Suggested Constants (`src/constants/index.js`)

```javascript
export const RISK_COLORS = {
  LOW: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400',
  MEDIUM: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400',
  HIGH: 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400',
  CRITICAL: 'bg-rose-100 text-rose-800 dark:bg-rose-900/30 dark:text-rose-400',
};

// Mock list of procedures for the Combobox
export const PROCEDURES = [
  { value: '72148', label: 'MRI Lumbar Spine without contrast' },
  { value: '70450', label: 'CT Head/Brain without contrast' },
  { value: '73221', label: 'MRI Joint of Lower Extremity (Knee)' }
];
```
