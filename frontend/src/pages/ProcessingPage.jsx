import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, Circle, Loader2, AlertCircle, ArrowLeft } from 'lucide-react';
import { useRunWorkflow } from '../hooks/useWorkflow';
import { PROCESSING_STEPS } from '../constants/index';

export default function ProcessingPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const state = location.state;

  const [completedSteps, setCompletedSteps] = useState([]);
  const [activeStep, setActiveStep] = useState(0);
  const workflowMutation = useRunWorkflow();

  // Guard
  useEffect(() => {
    if (!state?.documentId || !state?.procedureCode) {
      navigate('/', { replace: true });
    }
  }, [state, navigate]);

  // Trigger workflow
  useEffect(() => {
    if (!state?.documentId) return;
    workflowMutation.mutate(
      {
        document_id: state.documentId,
        procedure_code: state.procedureCode,
        procedure_name: state.procedureName,
      },
      {
        onSuccess: (data) => {
          setCompletedSteps(PROCESSING_STEPS.map((s) => s.id));
          setTimeout(() => {
            navigate(`/dashboard/${data.authorization_id}`, { replace: true });
          }, 700);
        },
      }
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Simulated step timer
  useEffect(() => {
    const timers = PROCESSING_STEPS.map((step, idx) =>
      setTimeout(() => {
        setActiveStep(idx);
        if (idx > 0)
          setCompletedSteps((prev) => [...prev, PROCESSING_STEPS[idx - 1].id]);
      }, step.delay)
    );
    return () => timers.forEach(clearTimeout);
  }, []);

  const isError = workflowMutation.isError;
  const errorMessage =
    workflowMutation.error?.userMessage || 'Analysis failed. Please try again.';

  return (
    <div className="max-w-md mx-auto pt-6 pb-12">
      {isError ? (
        /* ── Error ── */
        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          className="rounded-xl border p-8 text-center space-y-5"
          style={{
            background: 'hsl(var(--card))',
            borderColor: 'hsl(var(--destructive) / 0.25)',
          }}
        >
          <div
            className="w-12 h-12 rounded-xl flex items-center justify-center mx-auto"
            style={{ background: 'hsl(var(--destructive) / 0.1)' }}
          >
            <AlertCircle size={22} style={{ color: 'hsl(var(--destructive))' }} />
          </div>
          <div>
            <h3 className="text-sm font-semibold mb-1" style={{ color: 'hsl(var(--foreground))' }}>
              Analysis Failed
            </h3>
            <p className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>
              {errorMessage}
            </p>
          </div>
          <button
            onClick={() => navigate('/')}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium border transition-colors"
            style={{
              background: 'hsl(var(--highlight))',
              color: 'hsl(var(--foreground))',
              borderColor: 'hsl(var(--border))',
            }}
          >
            <ArrowLeft size={13} />
            Go Back
          </button>
        </motion.div>
      ) : (
        /* ── Processing ── */
        <motion.div
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35 }}
          className="rounded-xl border p-7 space-y-7"
          style={{
            background: 'hsl(var(--card))',
            borderColor: 'hsl(var(--border))',
          }}
        >
          {/* Header */}
          <div className="text-center space-y-3">
            <div
              className="flex items-center justify-center w-12 h-12 rounded-xl mx-auto"
              style={{ background: 'hsl(var(--highlight))' }}
            >
              <Loader2
                size={22}
                className="animate-spin"
                style={{ color: 'hsl(var(--foreground))' }}
              />
            </div>
            <div>
              <h2
                className="text-base font-bold"
                style={{ color: 'hsl(var(--foreground))' }}
              >
                Analyzing Submission
              </h2>
              <p className="text-sm mt-0.5" style={{ color: 'hsl(var(--muted-foreground))' }}>
                {state?.procedureName || 'Running AI pipeline'}
              </p>
            </div>
          </div>

          {/* Divider */}
          <div className="divider" />

          {/* Steps */}
          <div className="space-y-0.5">
            <AnimatePresence>
              {PROCESSING_STEPS.map((step, idx) => {
                const isDone = completedSteps.includes(step.id);
                const isActive = activeStep === idx && !isDone;
                const isPending = !isDone && !isActive;

                return (
                  <motion.div
                    key={step.id}
                    initial={{ opacity: 0, x: -6 }}
                    animate={{ opacity: isPending ? 0.35 : 1, x: 0 }}
                    transition={{ duration: 0.25, delay: idx * 0.04 }}
                    className="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all"
                    style={{
                      background: isActive ? 'hsl(var(--highlight))' : 'transparent',
                    }}
                  >
                    {/* Icon */}
                    <div className="flex-shrink-0 w-4 h-4 flex items-center justify-center">
                      {isDone ? (
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          transition={{ type: 'spring', stiffness: 400, damping: 18 }}
                        >
                          <CheckCircle2
                            size={15}
                            style={{ color: 'hsl(var(--success))' }}
                          />
                        </motion.div>
                      ) : isActive ? (
                        <Loader2
                          size={13}
                          className="animate-spin"
                          style={{ color: 'hsl(var(--foreground))' }}
                        />
                      ) : (
                        <Circle size={13} style={{ color: 'hsl(var(--border))' }} />
                      )}
                    </div>

                    {/* Label */}
                    <div className="flex-1 min-w-0">
                      <p
                        className="text-sm font-medium"
                        style={{
                          color: isDone
                            ? 'hsl(var(--success))'
                            : isActive
                            ? 'hsl(var(--foreground))'
                            : 'hsl(var(--muted-foreground))',
                        }}
                      >
                        {step.label}
                      </p>
                      {isActive && (
                        <motion.p
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          className="text-xs mt-0.5"
                          style={{ color: 'hsl(var(--muted-foreground))' }}
                        >
                          {step.description}
                        </motion.p>
                      )}
                    </div>

                    {/* Active badge */}
                    {isActive && (
                      <motion.span
                        initial={{ opacity: 0, scale: 0.85 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="text-xs px-2 py-0.5 rounded-full font-medium border"
                        style={{
                          background: 'hsl(var(--border))',
                          color: 'hsl(var(--foreground))',
                          borderColor: 'hsl(240 5% 22%)',
                          fontSize: '0.65rem',
                          letterSpacing: '0.04em',
                        }}
                      >
                        RUNNING
                      </motion.span>
                    )}
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>

          {/* Footer */}
          <p
            className="text-xs text-center"
            style={{ color: 'hsl(var(--muted-foreground))' }}
          >
            Analysis completes in 15–30 seconds. Please do not close this tab.
          </p>
        </motion.div>
      )}
    </div>
  );
}
