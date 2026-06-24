export const EVIDENCE_CATEGORY_LABELS = {
  DIAGNOSIS: 'Diagnoses',
  DOCUMENT: 'Documentation',
  CLINICAL_FINDING: 'Clinical Findings',
  IMAGING: 'Imaging',
  MEDICATION: 'Medications',
  PROVIDER_TYPE: 'Provider',
  CONSERVATIVE_TREATMENT: 'Conservative Treatment',
  LAB_RESULT: 'Lab Results',
  INSURANCE: 'Insurance',
};

export const RISK_COLORS = {
  LOW: {
    badge: 'bg-emerald-500/15 text-emerald-400 ring-1 ring-emerald-500/30',
    dot: 'bg-emerald-400',
  },
  MEDIUM: {
    badge: 'bg-amber-500/15 text-amber-400 ring-1 ring-amber-500/30',
    dot: 'bg-amber-400',
  },
  HIGH: {
    badge: 'bg-orange-500/15 text-orange-400 ring-1 ring-orange-500/30',
    dot: 'bg-orange-400',
  },
  CRITICAL: {
    badge: 'bg-rose-500/15 text-rose-400 ring-1 ring-rose-500/30',
    dot: 'bg-rose-400',
  },
};

export const RISK_GAUGE_COLORS = {
  LOW: '#10b981',
  MEDIUM: '#f59e0b',
  HIGH: '#f97316',
  CRITICAL: '#ef4444',
};

export const PROCEDURES = [
  { value: '72148', label: 'MRI Lumbar Spine without contrast' },
  { value: '70450', label: 'CT Head/Brain without contrast' },
  { value: '73221', label: 'MRI Joint of Lower Extremity (Knee)' },
  { value: '71046', label: 'X-Ray Chest, 2 views' },
  { value: '70553', label: 'MRI Brain with and without contrast' },
  { value: '74177', label: 'CT Abdomen and Pelvis with contrast' },
  { value: '73722', label: 'MRI Joint of Lower Extremity without contrast' },
  { value: '77067', label: 'Screening Mammography, bilateral' },
];

export const PROCESSING_STEPS = [
  {
    id: 'parse',
    label: 'Parsing Clinical Document',
    description: 'Extracting text from PDF',
    delay: 0,
  },
  {
    id: 'extract',
    label: 'Extracting Medical Knowledge',
    description: 'Running AI entity extraction',
    delay: 2500,
  },
  {
    id: 'template',
    label: 'Loading Procedure Guidelines',
    description: 'Matching payer requirement template',
    delay: 6000,
  },
  {
    id: 'gap',
    label: 'Running Gap Analysis',
    description: 'Identifying missing clinical evidence',
    delay: 10000,
  },
  {
    id: 'rules',
    label: 'Evaluating Payer Rules',
    description: 'Cross-referencing insurance criteria',
    delay: 14000,
  },
  {
    id: 'score',
    label: 'Computing Readiness Score',
    description: 'Generating final authorization package',
    delay: 18000,
  },
];
