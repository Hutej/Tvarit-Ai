# Tvarit AI – AI Architecture Blueprint

## 1. Mission and Philosophy

### 1.1 Mission
**"Reduce Prior Authorization rejection on the FIRST submission."**

Our primary KPI is **First-Time Approval Success Rate**. Tvarit AI operates purely as a proactive, pre-submission intelligence layer. It is not an approval system, a conversational chatbot, or a document summarizer. Its single purpose is to intercept a prior authorization (PA) request *before* it reaches the payer, behaving as an expert Clinical PA Specialist. By validating requirements, detecting gaps, and compiling airtight evidence, we eliminate rejections before they happen.

### 1.2 System Philosophy
**Documents are temporary. Knowledge is permanent.**
The AI must *never* reason directly over raw PDFs or unstructured text chunks. Direct LLM-to-PDF reasoning is susceptible to context loss, hallucinations, and inability to track provenance. Instead, every document is deterministically parsed, structured, and assimilated into a **Patient Knowledge Base**. The AI reasons exclusively over structured, canonical medical data.

---

## 2. Overall Pipeline Architecture

### 2.1 The Data Flow

```text
[ Hospital Documents ]
          │
          ▼
[ Storage & Triage ] ─── (Sorts by type, patient, request)
          │
          ▼
[ Document Parsing ] ─── (PyMuPDF / pdfplumber)
          │
          ▼
[ OCR / Layout ] ─────── (RapidOCR for images/scans, Layout understanding)
          │
          ▼
[ Cleaning & Normalization ]
          │
          ▼
[ Deep Extraction ] ──── (Table extraction, Handwriting parsing)
          │
          ▼
[ Entity Extraction ] ── (Clinical NER via LLM / Specialized models)
          │
          ▼
[ Standard Mapping ] ─── (ICD-10, SNOMED, RxNorm, CPT mappings)
          │
          ▼
[ Canonical Schema ] ─── (The core Tvarit AI Knowledge Graph)
          │
          ▼
[ Patient Knowledge Base ]
          │
          ▼
[ LangGraph Orchestration ]
          │
    ┌─────┴─────┐
    │           │
[ Rule Engine ] [ Evidence Matching ]
    │           │
    └─────┬─────┘
          │
          ▼
[ Gap Detection ] ────── (Identifies missing clinical criteria)
          │
          ▼
[ Decision Engine ] ──── (Scores readiness, necessity, confidence)
          │
          ▼
[ Prior Authorization Package ]
```

### 2.2 Pipeline Rationale
- **Decoupling Parsing from Reasoning**: OCR and layout analysis are computationally heavy and brittle. Moving them to the edge ensures the LLM only deals with clean text and tables.
- **Entity & Standard Mapping before LangGraph**: The LangGraph agents shouldn't waste tokens figuring out if "Heart Attack" and "Myocardial Infarction" are the same. Standard mapping normalizes this upfront.
- **Canonical Schema**: Acts as the single source of truth. If the schema is populated correctly, the AI reasoning step becomes a deterministic logic puzzle rather than a creative text generation task.

---

## 3. Medical Document Processing Strategy

Medical submissions are chaotic arrays of structured forms, unstructured notes, and semi-structured tables. Tvarit AI will extract **everything**, ignoring nothing.

### 3.1 Document Typologies & Targets
- **Prescriptions/Medication Lists**: Extract drug name, dosage, frequency, start/end dates, prescribing physician.
- **Discharge Summaries & Clinical Notes**: Extract chief complaint, history of present illness (HPI), diagnoses, clinical course, discharge instructions.
- **Radiology/Pathology Reports**: Extract findings, impressions, measurements, technique, anomalies.
- **Lab Reports**: Extract biomarkers, exact values, units, reference ranges, flags (High/Low).
- **Insurance Forms/Referral Letters**: Extract policy numbers, referring providers, requested procedures (CPT).

### 3.2 Handling Complexities
- **Tables**: Standard text extraction destroys table hierarchies. We must use bounding-box layout parsing (e.g., LayoutParser, Docling, or specialized LLM vision models) to reconstruct tables into JSON/Markdown before entity extraction.
- **Scanned PDFs & Handwriting**: Processed via RapidOCR. Handwritten physician notes will be flagged for low-confidence extraction and validated cross-document.
- **Duplicate Merging & Deduplication**: Resolved during the Canonical Schema instantiation. If Doc A says "Aspirin 81mg" and Doc B says "Aspirin 81mg", the schema retains one entity but links **two provenance traces**. If they conflict, the newer timestamp or more authoritative source (e.g., Discharge Summary over Intake Form) wins.

---

## 4. Healthcare Standards & FHIR Strategy

### 4.1 Adopted Standards
- **ICD-10-CM**: For Diagnoses/Conditions. (Internal & External)
- **CPT / HCPCS**: For Procedures/Treatments requested. (Internal & External)
- **SNOMED CT**: For deep clinical terminology and semantic equivalence mapping. (Reference Only)
- **RxNorm**: For Medications. (Internal & External)
- **LOINC**: For Lab Results and Observations. (Reference Only)

### 4.2 FHIR Strategy: The Hybrid Architecture
**Strategy**: We will **NOT** store only FHIR, nor will we store only a proprietary schema. We will use a **Hybrid Architecture**.

*Why?* FHIR (Fast Healthcare Interoperability Resources) is perfect for interoperability (EHR integrations) but terrible for LLM reasoning. FHIR JSONs are heavily nested, deeply verbose, and consume massive context windows. 

**Implementation**:
1. **Ingestion Layer**: Can accept FHIR bundles from EHRs.
2. **Canonical Layer**: Data is mapped into a flattened, heavily optimized Python Pydantic-based Canonical Schema designed specifically for LLM context limits and vectorization.
3. **Export Layer**: The final PA Package can export the clinical data back into FHIR for the hospital's EHR.

---

## 5. The Canonical Internal Schema

The master internal schema represents the complete medical reality of the patient. Every object strictly adheres to **Provenance Tracking** to guarantee explainability and eliminate hallucination.

### 5.1 Base Provenance Interface
Every node in the schema inherits this:
```python
class Provenance:
    source_document_id: str
    page_number: int
    paragraph_or_bounding_box: str
    extraction_confidence: float
    timestamp: datetime
    extracted_by: str # Agent/Model name
```

### 5.2 Core Entities
- **Patient**: Demographics, Risk Factors.
- **Encounters & Timeline**: Chronological tracking of hospital visits, duration, and severity.
- **Conditions/Diagnoses**: ICD-10 code, status (Active/Resolved), date of onset.
- **Procedures**: CPT codes, dates, outcomes, provider.
- **Medications**: RxNorm, dosage, response (tolerated/failed - *crucial for step-therapy rules*).
- **Observations/Vitals/Labs**: Specific quantitative values needed for payer threshold rules (e.g., "BMI > 35" or "HbA1c > 7.0").
- **Authorization State**: The requested procedure, medical necessity arguments, satisfied vs. missing evidence.

---

## 6. Knowledge Representation & Flow

**Raw PDF ➔ Extracted Text ➔ FHIR/NER ➔ Canonical Schema ➔ Patient Knowledge Base ➔ LangGraph State ➔ Decision**

**Why this is superior:**
By the time the data reaches the LangGraph State, the AI is no longer reading a 50-page PDF. It is querying a structured Knowledge Base. If a payer rule states: *"Patient must have tried and failed NSAIDs for 6 weeks,"* the Rule Engine doesn't have to read the PDF. It simply queries the Canonical Schema for `Medications` where `type == 'NSAID'` and `response == 'failed'` and calculates the `duration`. This shifts the architecture from "Stochastic Text Generation" to "Deterministic Graph Querying."

---

## 7. LangGraph Multi-Agent Workflow

Our intelligence operates as a coordinated team of expert agents, managed via LangGraph.

### 7.1 Agents
1. **Document Agent**: Routes and categorizes uploads. Flags unreadable documents.
2. **Extraction Agent**: Converts raw text/layout into raw JSON fragments.
3. **Normalization Agent**: Maps raw JSON into the Canonical Schema, assigning ICD-10/CPT codes and merging duplicates.
4. **Timeline Agent**: Constructs a strict chronological history of the patient's condition. Crucial for "Step Therapy" and "Duration of Treatment" payer rules.
5. **Insurance Agent**: Retrieves and parses the specific payer guidelines (e.g., Aetna Clinical Policy Bulletin) for the requested CPT code.
6. **Evidence Agent**: The cross-referencer. Matches the Canonical Schema against the rules parsed by the Insurance Agent.
7. **Gap Detection Agent**: Identifies rules that have *no* matching evidence. Determines if the evidence is truly missing or just ambiguously worded.
8. **Validator Agent**: Fact-checks the Evidence Agent against the Provenance pointers to prevent hallucinations.
9. **Decision Engine Agent**: Computes the final readiness scores.
10. **Report Agent**: Drafts the final Prior Authorization Package.

### 7.2 State Management
The LangGraph `AgentState` holds the populated Canonical Schema, the Insurance Rules, the identified Gaps, and the current processing status. Agents communicate by mutating this central state.

---

## 8. Rule Engine & Evidence Matching

### 8.1 Payer Rule Representation
Rules will be represented as a **Hybrid of YAML (for logic) and Knowledge Graph (for ontologies)**.
- **YAML Logic**: `requires: {condition: "conservative_therapy", duration_weeks: >= 6, outcome: "failure"}`
- **Ontology**: The system knows that "Physical Therapy", "NSAIDs", and "Chiropractic care" all roll up to the parent concept of "conservative_therapy" via the SNOMED-CT reference graph.

### 8.2 Resolving Conflicts
If Document A states "Patient successfully completed PT" and Document B states "PT was terminated due to pain", the Evidence Agent flags a `Conflict`. The Gap Detection Agent will demand clarification in the final output, recommending the physician provide an addendum.

---

## 9. Decision Engine Scoring

Instead of a binary "Approved/Rejected", the system evaluates **Submission Readiness**. 

### 9.1 The Metrics
- **Medical Necessity Score (0-100%)**: How strongly the extracted conditions justify the requested CPT code based on generic clinical pathways.
- **Clinical Evidence Score (0-100%)**: What percentage of the *specific payer's* criteria are explicitly met in the documentation.
- **Documentation Quality Score (0-100%)**: Legibility, presence of signatures, up-to-date lab work (e.g., labs within the last 30 days).
- **Overall Readiness Score**: A weighted aggregation. A score < 95% means the package is NOT ready for submission.
- **Confidence**: The AI's internal confidence in its own extraction and mapping (based on OCR scores and LLM logprobs).

---

## 10. The Final Output Package

The output generated by the Report Agent is a structured digital package ready for human review and payer submission.

### 10.1 Package Components
1. **Executive Summary**: A 3-bullet-point summary of the request, the primary diagnosis, and the medical necessity.
2. **Clinical Timeline**: A dynamically generated chronological summary proving the patient's journey (proving step-therapy compliance).
3. **Satisfied Requirements Matrix**: A table listing every payer rule alongside the exact quote from the medical record and the PDF page number (Traceability).
4. **Missing Requirements (The Gap Report)**: Crucial for the provider. E.g., *"Aetna requires an MRI within the last 6 months. Found MRI from 8 months ago. Please upload newer imaging."*
5. **Recommended Actions**: Actionable steps for the hospital staff (e.g., "Request physician signature on Page 4", "Upload recent CBC lab").

### 10.2 Explainability & Traceability
Every claim made in the Final Package contains a hyperlink or reference tag (e.g., `[Doc: MRI_Report.pdf, Page: 2, Para: 3]`). This ensures the human-in-the-loop (the hospital's PA specialist) can verify the AI's logic in seconds, fostering absolute trust.
