import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ArrowRight,
  Loader2,
  ShieldCheck,
  Zap,
  ClipboardList,
  AlertCircle,
} from 'lucide-react';
import DocumentDropzone from '../components/features/upload/DocumentDropzone';
import ProcedureSelector from '../components/features/upload/ProcedureSelector';
import { useUploadDocument } from '../hooks/useWorkflow';

const features = [
  {
    icon: Zap,
    title: 'AI Extraction',
    desc: 'LangGraph multi-agent clinical NER pipeline',
  },
  {
    icon: ClipboardList,
    title: 'Rule Matching',
    desc: 'Cross-references 50+ payer criteria automatically',
  },
  {
    icon: ShieldCheck,
    title: 'Gap Detection',
    desc: 'Catches missing evidence before submission',
  },
];

const container = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.07 } },
};
const item = {
  hidden: { opacity: 0, y: 14 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.35, ease: 'easeOut' } },
};

export default function UploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [procedure, setProcedure] = useState(null);
  const [error, setError] = useState(null);

  const uploadMutation = useUploadDocument();
  const isLoading = uploadMutation.isPending;
  const canAnalyze = !!file && !!procedure && !isLoading;

  const handleAnalyze = async () => {
    setError(null);
    try {
      const uploadResult = await uploadMutation.mutateAsync(file);
      navigate('/processing', {
        state: {
          documentId: uploadResult.id,
          procedureCode: procedure.value,
          procedureName: procedure.label,
        },
      });
    } catch (err) {
      setError(err.userMessage || 'Upload failed. Please try again.');
    }
  };

  return (
    <div className="max-w-2xl mx-auto pt-2 pb-12">
      <motion.div
        variants={container}
        initial="hidden"
        animate="visible"
        className="space-y-5"
      >
        {/* Heading */}
        <motion.div variants={item} className="space-y-1 pb-1">
          <h2
            className="text-xl font-bold tracking-tight"
            style={{ color: 'hsl(var(--foreground))' }}
          >
            Submit for Analysis
          </h2>
          <p className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>
            Upload clinical documentation to identify gaps before payer submission.
          </p>
        </motion.div>

        {/* Feature strip */}
        <motion.div variants={item} className="grid grid-cols-3 gap-2.5">
          {features.map((f) => {
            const Icon = f.icon;
            return (
              <div
                key={f.title}
                className="flex flex-col gap-2 p-3 rounded-lg border"
                style={{
                  background: 'hsl(var(--card))',
                  borderColor: 'hsl(var(--border))',
                }}
              >
                <div
                  className="w-6 h-6 flex items-center justify-center rounded-md"
                  style={{ background: 'hsl(var(--highlight))' }}
                >
                  <Icon size={13} style={{ color: 'hsl(var(--foreground))' }} />
                </div>
                <p
                  className="text-xs font-semibold leading-snug"
                  style={{ color: 'hsl(var(--foreground))' }}
                >
                  {f.title}
                </p>
                <p
                  className="text-xs leading-snug"
                  style={{ color: 'hsl(var(--muted-foreground))' }}
                >
                  {f.desc}
                </p>
              </div>
            );
          })}
        </motion.div>

        {/* Form card */}
        <motion.div
          variants={item}
          className="rounded-xl border p-5 space-y-5"
          style={{
            background: 'hsl(var(--card))',
            borderColor: 'hsl(var(--border))',
          }}
        >
          {/* Procedure */}
          <div className="space-y-1.5">
            <label
              className="block text-xs font-semibold uppercase tracking-wider"
              style={{ color: 'hsl(var(--muted-foreground))' }}
            >
              Target Procedure
            </label>
            <ProcedureSelector value={procedure?.value} onChange={setProcedure} />
          </div>

          {/* Divider */}
          <div className="zinc-separator" />

          {/* Upload */}
          <div className="space-y-1.5">
            <label
              className="block text-xs font-semibold uppercase tracking-wider"
              style={{ color: 'hsl(var(--muted-foreground))' }}
            >
              Clinical Documentation
            </label>
            <DocumentDropzone
              file={file}
              onFileSelect={setFile}
              onFileRemove={() => setFile(null)}
              disabled={isLoading}
            />
          </div>

          {/* Error */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -4 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-start gap-2.5 px-3.5 py-2.5 rounded-lg text-sm border"
              style={{
                background: 'hsl(var(--destructive) / 0.08)',
                color: 'hsl(var(--destructive))',
                borderColor: 'hsl(var(--destructive) / 0.2)',
              }}
            >
              <AlertCircle size={14} className="mt-0.5 flex-shrink-0" />
              <span>{error}</span>
            </motion.div>
          )}

          {/* Submit */}
          <button
            type="button"
            onClick={handleAnalyze}
            disabled={!canAnalyze}
            className="w-full flex items-center justify-center gap-2 py-2.5 px-5 rounded-lg text-sm font-semibold transition-all duration-150 border"
            style={{
              background: canAnalyze ? 'hsl(var(--foreground))' : 'hsl(var(--highlight))',
              color: canAnalyze ? 'hsl(var(--background))' : 'hsl(var(--muted-foreground))',
              borderColor: canAnalyze ? 'transparent' : 'hsl(var(--border))',
              opacity: canAnalyze ? 1 : 0.7,
              cursor: canAnalyze ? 'pointer' : 'not-allowed',
            }}
          >
            {isLoading ? (
              <>
                <Loader2 size={14} className="animate-spin" />
                <span>Uploading document…</span>
              </>
            ) : (
              <>
                <span>Analyze Submission</span>
                <ArrowRight size={14} />
              </>
            )}
          </button>

          {/* Hint */}
          {(!file || !procedure) && !isLoading && (
            <p
              className="text-xs text-center"
              style={{ color: 'hsl(var(--muted-foreground))' }}
            >
              {!procedure && !file
                ? 'Select a procedure and upload a document to continue'
                : !procedure
                ? 'Select a target procedure to continue'
                : 'Upload a clinical document to continue'}
            </p>
          )}
        </motion.div>

        {/* Footer note */}
        <motion.p
          variants={item}
          className="text-xs text-center"
          style={{ color: 'hsl(var(--muted-foreground))' }}
        >
          Documents are processed securely. Analysis typically completes in 15–30 seconds.
        </motion.p>
      </motion.div>
    </div>
  );
}
