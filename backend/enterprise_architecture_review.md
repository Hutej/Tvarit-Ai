# Tvarit AI – Enterprise Architecture Review & Blueprint

**Role:** Principal AI Architect, Healthcare Systems  
**Objective:** Critical validation, refinement, and enterprise-grade restructuring of the Tvarit AI Prior Authorization Platform.  
**KPI Focus:** First-Time Approval Success Rate (Accuracy) + Latency/Cost (Speed).

---

## QUESTION 1: The Reasoning Substrate
**Hypothesis:** Reason over Raw PDFs vs. FHIR vs. Canonical Schema.  
**Verdict:** **Canonical Schema (LLM-Optimized).**

*Critique:* 
- **Raw PDFs** are toxic for AI reasoning. They force the LLM to perform OCR error-correction, layout reconstruction, and logical deduction simultaneously, bloating token counts and triggering hallucinations.
- **FHIR** is an interoperability protocol, not an AI reasoning format. It is deeply nested, overly verbose, and packed with transport-level metadata (`valueCodeableConcept`, `coding`, `system`). Feeding raw FHIR to an LLM wastes 60% of the context window on JSON syntax.
- **The Optimal Architecture:** The LLM must reason over a flattened, highly dense, temporally ordered **Universal Canonical Schema**. The reasoning engine should only see pure clinical facts stripped of layout and transport noise.

---

## QUESTION 2: Multi-Modal Ingestion
**Hypothesis:** Treat PDFs as only ONE ingestion source alongside FHIR, HL7, APIs, etc.  
**Verdict:** **Absolutely Correct.**

*Critique:* If you hardcode your pipeline around PDFs, you build a glorified OCR tool, not a healthcare platform. By moving to a **Ports and Adapters (Hexagonal)** architecture, the core system is agnostic to the data origin. 
- A faxed PDF goes through the `PDFAdapter` (OCR + LLM Extraction).
- An Epic integration goes through the `FHIRAdapter` (JSON mapping).
- Both output the exact same Canonical Schema objects. This future-proofs the system for enterprise EHR integration.

---

## QUESTION 3: FHIR Strategy (Storage vs. Import/Export)
**Hypothesis:** FHIR as internal storage vs. import/export format.  
**Verdict:** **FHIR must strictly be an Edge Layer (Import/Export).**

*Critique:* Storing data internally as FHIR is a common anti-pattern that cripples performance. Querying a FHIR data store to answer "Has the patient failed 6 weeks of conservative therapy?" requires complex graph traversals across `Condition`, `MedicationStatement`, `Procedure`, and `Encounter` resources. 
**Internal storage must be optimized for query speed and LLM context limits.** FHIR should be translated into the Canonical Schema upon ingestion, and the final Prior Authorization payload translated back to a FHIR `Claim` or `Task` resource at the exit node.

---

## QUESTION 4: The Pipeline Architecture
**Hypothesis:** `Input -> Adapter -> Universal Medical Schema -> Validation -> Knowledge Base -> LangGraph -> Decision Engine -> Export to FHIR`  
**Verdict:** **Strong, but needs an Entity Resolution layer.**

*Critique:* The proposed pipeline is 90% correct. However, mapping raw input to the Universal Schema directly assumes the input data is clean. It omits **Semantic Merging**. 
*Refined Pipeline:*
`Input -> Classifier -> Adapter/Extractor -> Semantic Entity Resolution (Deduplication/Terminology Mapping) -> Universal Medical Schema -> Patient Knowledge Base (Graph Update) -> LangGraph Agents -> Decision Engine -> Output/FHIR`

---

## QUESTION 5: Universal Medical Schema Design
**Verdict:** An enterprise schema requires a strict base class emphasizing Provenance, Confidence, and Temporal tracking.

### Core Entity Design Pattern
```python
class Provenance:
    source_id: str           # e.g., 'doc_789' or 'fhir_encounter_12'
    source_type: str         # 'pdf', 'hl7', 'manual_entry'
    locator: str             # Page 2, Bounding Box, or JSON path
    timestamp: datetime      # When this fact was recorded
    extractor_confidence: float

class MedicalEntity:
    entity_id: str
    provenance: List[Provenance]  # An entity can be backed by multiple documents
    is_conflicted: bool
```

### Schema Domains
1. **Administrative:** `Patient`, `Provider`, `Organization`, `Insurance`, `Coverage`.
2. **Clinical Core:** `Condition` (Diagnoses, Problems, Symptoms), `Medication` (Current, History, Failures), `Procedure`, `Allergy`.
3. **Clinical Diagnostics:** `Observation`, `Vital`, `LaboratoryResult`, `ImagingStudy`, `DiagnosticReport`.
4. **Encounters & Workflow:** `Encounter`, `Appointment`, `Referral`, `TimelineEvent`.
5. **Authorization Specifics:** `AuthorizationRequest`, `RequestedProcedure`, `MedicalNecessityArgument`, `SupportingEvidence`, `MissingEvidence`, `PayerRule`, `Conflict`.
6. **Documentation:** `ClinicalNote`, `OperativeNote`, `PathologyReport`, `DischargeSummary`, `DocumentReference`.

*Architectural Rule:* Every time a new document mentions "Type 2 Diabetes," we do not create a new `Condition` object. We append a new `Provenance` to the existing `Condition` object.

---

## QUESTION 6: Resolving Merges, Duplicates, and Conflicts
**Verdict:** Do not overwrite data. Use a deterministic Semantic Merger.

- **Merging & Duplication:** Use standard terminology (ICD-10, SNOMED). If the Lab Extractor finds "A1C: 7.2" and the Clinical Note Extractor finds "HbA1c was seven point two", the terminology mapper identifies them as identical. We merge them into one entity with two `Provenance` trails.
- **Conflicts:** If Doc A says "Allergies: Penicillin" and Doc B says "No Known Allergies," the system **creates both**, flags them as `Conflict: True`, and links them via a `ConflictResolution` entity. A LangGraph `Conflict Agent` attempts logical resolution (e.g., temporal precedence—Doc A is from 2018, Doc B is from 2024). If unresolvable, it is escalated to the Human-in-the-Loop gap report.
- **Newer vs. Older:** Medical data is additive. Never delete historical data; it is required to prove chronological compliance (e.g., Step Therapy). Use valid time ranges (`start_date`, `end_date`).

---

## QUESTION 7: Maximizing Speed & Cost Efficiency
**Verdict:** Shift from monolithic LLM calls to a Map-Reduce Routing Architecture.

1. **Document Classification Triage:** Fast, cheap models (or traditional ML) classify documents in milliseconds.
2. **Specialized Map-Reduce:** Parallelize extraction. Don't send a 50-page PDF to GPT-4o. Split it: Labs go to the Lab Extractor, Notes go to the Notes Extractor.
3. **Tiered LLM Strategy:** 
   - Use small, fast models (e.g., GPT-4o-mini or Claude Haiku) for highly structured forms (insurance forms, structured labs).
   - Use heavy models (GPT-4o) *only* for dense, unstructured clinical narratives (Discharge Summaries).
4. **Incremental Updates:** If a hospital uploads a new Lab Report to an existing PA case, *only run the Lab Extractor*. The LangGraph state is updated incrementally. The Decision Engine only re-evaluates the rules affected by the new lab values.
5. **Semantic Caching:** Cache repetitive extractions and payer rule evaluations using vector embeddings.

---

## QUESTION 8: Specialized vs. Generic Extractors
**Verdict:** **Specialized Extractors are mandatory for Enterprise AI.**

*Critique:* A single generic "Extract everything from this document" prompt suffers from the "Lost in the Middle" phenomenon, consumes maximum tokens, and requires a massive JSON schema output that frequently breaks.
*Solution:* 
- **Prescription Extractor:** Prompt is highly tuned for dosage, frequency, and duration.
- **Lab Extractor:** Prompt focuses strictly on tabular data, flags, and units.
- **Result:** Accuracy skyrockets because the LLM focuses on one task. Speed increases due to parallel execution. Cost plummets because smaller LLMs can handle specialized tasks.

---

## QUESTION 9: The Ultimate Ingestion Architecture

```text
[ Data Sources ] (PDF, Images, FHIR API, HL7 Stream)
       │
       ▼
[ Ingestion Gateway ] ───────── (Standardizes transport, queues jobs)
       │
       ▼
[ Pre-Processing / Triage ] ─── (OCR for images, Document Classification)
       │
       ├───► [ Lab Extractor (Tier 1 LLM) ]
       ├───► [ Note Extractor (Tier 2 LLM) ]
       ├───► [ Form Extractor (Rules/Tier 1) ]
       │
       ▼
[ Semantic Normalization ] ──── (Maps extracted text to SNOMED/ICD10/RxNorm)
       │
       ▼
[ Entity Resolution ] ───────── (Deduplicates, identifies Conflicts, links Provenance)
       │
       ▼
[ Patient Knowledge Base ] ──── (The master State Graph is updated)
       │
       ▼
[ LangGraph Event Trigger ] ─── (Wakes up AI Agents upon KB mutation)
       │
       ├───► [ Evidence Agent queries Payer Rules ]
       ├───► [ Timeline Agent builds Step-Therapy graph ]
       ├───► [ Gap Agent detects missing criteria ]
       │
       ▼
[ Decision Engine ] ─────────── (Scores Readiness, Generates Confidence)
       │
       ▼
[ Output API / FHIR Export ]
```

---

## QUESTION 10: Patient Knowledge Base Storage
**Verdict:** **Hybrid Document-Graph Database (e.g., PostgreSQL with JSONB + pgvector).**

*Critique:* 
- **Relational (SQL):** Too rigid. Clinical data is incredibly sparse (a patient might have 100 labs but 0 surgeries).
- **Pure Graph (Neo4j):** Overkill for basic CRUD and creates unnecessary query latency for standard UI rendering.
- **Solution:** Store Canonical Schema entities as Document objects (JSONB in Postgres or MongoDB). This allows schema flexibility. Use foreign keys or explicit edge tables to handle Graph-like relationships (e.g., `Procedure X` -> *resolves* -> `Condition Y`). This gives you the speed of a document database with the relational capability of a graph, perfect for the Timeline Agent.

---

## QUESTION 11: Future EHR Integration Agnosticism
**Verdict:** Decouple LangGraph entirely from Ingestion.

*Critique:* LangGraph should **never** know a document exists. LangGraph should only know that the `PatientKnowledgeBase` has changed. 
If Epic EHR is integrated later via a direct FHIR API push:
1. The `FHIR_Webhook_Adapter` receives the payload.
2. It translates it to the `CanonicalSchema`.
3. It updates the `PatientKnowledgeBase`.
4. It emits an event: `KnowledgeBaseUpdated(patient_id=123)`.
5. LangGraph listens for this event, pulls the current state of the KB, and runs the validation rules. 

Because LangGraph operates strictly on the KB interface, connecting a new $100M hospital EHR system requires zero changes to your AI agents or rule engines. You only build a new Adapter.
