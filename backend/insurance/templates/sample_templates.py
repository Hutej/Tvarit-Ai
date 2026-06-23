from insurance.templates.models import ProcedureTemplate
from insurance.templates.registry import TemplateRegistry

mri_lumbar_spine = ProcedureTemplate(
    procedure_code="72148",
    procedure_name="MRI Lumbar Spine without contrast",
    aliases=["MRI L-Spine", "Lumbar MRI", "MR Lumbar Spine"],
    required_diagnoses=["Low Back Pain", "Sciatica", "Radiculopathy"],
    required_documents=["Clinical Note", "Physical Therapy Note"],
    required_clinical_findings=["Neurologic deficit", "Positive straight leg raise", "Pain radiating below knee"],
    required_conservative_treatment=["Physical Therapy (6 weeks)", "NSAIDs (6 weeks)", "Activity Modification"],
    required_imaging=["X-Ray Lumbar Spine (within 6 months)"],
    required_provider_types=["Orthopedic Surgeon", "Neurologist", "Primary Care Physician"],
    required_duration_months=1,
    priority=1
)

ct_brain = ProcedureTemplate(
    procedure_code="70450",
    procedure_name="CT Head/Brain without contrast",
    aliases=["CT Head", "CT Brain", "CAT Scan Head"],
    required_diagnoses=["Head trauma", "Stroke", "Unexplained headaches", "Mental status changes"],
    required_documents=["Clinical Note", "Neurological Exam"],
    required_clinical_findings=["Altered mental status", "Focal neurological deficit", "Severe headache pattern change"],
    required_conservative_treatment=[],
    required_imaging=[],
    required_provider_types=["Neurologist", "Emergency Physician", "Primary Care Physician"],
    custom_notes="Often approved urgently for trauma or suspected stroke.",
    priority=2
)

knee_mri = ProcedureTemplate(
    procedure_code="73221",
    procedure_name="MRI Joint of Lower Extremity (Knee)",
    aliases=["MRI Knee", "Magnetic Resonance Imaging Knee"],
    required_diagnoses=["Knee Pain", "Suspected Meniscal Tear", "Suspected ACL Tear", "Osteoarthritis"],
    required_documents=["Clinical Note"],
    required_clinical_findings=["Joint effusion", "Mechanical locking or catching", "Instability"],
    required_conservative_treatment=["Physical Therapy (4 weeks)", "NSAIDs", "Rest/Ice/Elevation"],
    required_imaging=["X-Ray Knee (weight-bearing)"],
    required_provider_types=["Orthopedic Surgeon", "Sports Medicine", "Primary Care Physician"],
    required_duration_months=1,
    priority=1
)

TemplateRegistry.register(mri_lumbar_spine)
TemplateRegistry.register(ct_brain)
TemplateRegistry.register(knee_mri)
