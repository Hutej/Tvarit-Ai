import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, FileText, X, AlertCircle } from 'lucide-react';
import { cn, formatFileSize } from '../../../utils/helpers';
import { motion, AnimatePresence } from 'framer-motion';

const ACCEPTED = { 'application/pdf': ['.pdf'], 'image/jpeg': ['.jpg', '.jpeg'], 'image/png': ['.png'] };
const MAX_BYTES = 10 * 1024 * 1024;

export default function DocumentDropzone({ file, onFileSelect, onFileRemove, disabled }) {
  const onDrop = useCallback(
    (accepted) => { if (accepted[0]) onFileSelect(accepted[0]); },
    [onFileSelect]
  );

  const { getRootProps, getInputProps, isDragActive, isDragReject, fileRejections } =
    useDropzone({ onDrop, accept: ACCEPTED, maxFiles: 1, maxSize: MAX_BYTES, disabled: disabled || !!file });

  const rejection = fileRejections[0]?.errors[0]?.message;

  return (
    <div className="space-y-2">
      <AnimatePresence mode="wait">
        {file ? (
          <motion.div key="selected"
            initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -4 }}
            transition={{ duration: 0.15 }}
            className="flex items-center gap-3 px-3.5 py-3 rounded-md border"
            style={{ background: 'hsl(var(--surface-1))', borderColor: 'hsl(var(--border-strong))' }}>
            <div className="flex items-center justify-center w-8 h-8 rounded-md flex-shrink-0"
              style={{ background: 'hsl(var(--highlight))' }}>
              <FileText size={14} style={{ color: 'hsl(var(--foreground))' }} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-semibold truncate" style={{ color: 'hsl(var(--foreground))' }}>{file.name}</p>
              <p className="text-[11px]" style={{ color: 'hsl(var(--muted-foreground))' }}>{formatFileSize(file.size)}</p>
            </div>
            {!disabled && (
              <button type="button" onClick={onFileRemove}
                className="flex-shrink-0 p-1 rounded transition-colors"
                style={{ color: 'hsl(var(--muted-foreground))' }}
                onMouseEnter={e => { e.currentTarget.style.color = 'hsl(var(--foreground))'; e.currentTarget.style.background = 'hsl(var(--border))'; }}
                onMouseLeave={e => { e.currentTarget.style.color = 'hsl(var(--muted-foreground))'; e.currentTarget.style.background = 'transparent'; }}>
                <X size={12} />
              </button>
            )}
          </motion.div>
        ) : (
          <motion.div key="empty"
            initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -4 }}
            transition={{ duration: 0.15 }}
            {...getRootProps()}
            className={cn('dropzone-base flex flex-col items-center justify-center text-center px-6 py-9',
              isDragActive && !isDragReject && 'dropzone-active',
              isDragReject && 'dropzone-rejected',
              disabled && 'opacity-40 pointer-events-none')}>
            <input {...getInputProps()} />
            <motion.div
              animate={isDragActive ? { scale: 1.1, y: -2 } : { scale: 1, y: 0 }}
              transition={{ type: 'spring', stiffness: 300, damping: 20 }}
              className="flex items-center justify-center w-10 h-10 rounded-xl mb-3"
              style={{ background: 'hsl(var(--highlight))' }}>
              <UploadCloud size={18} style={{ color: isDragActive ? 'hsl(var(--foreground))' : 'hsl(var(--muted-foreground))' }} />
            </motion.div>
            <p className="text-sm font-semibold mb-1" style={{ color: 'hsl(var(--foreground))' }}>
              {isDragActive ? 'Release to upload' : 'Drop clinical document here'}
            </p>
            <p className="text-xs mb-3" style={{ color: 'hsl(var(--muted-foreground))' }}>PDF, JPG or PNG — max 10 MB</p>
            <span className="inline-flex items-center px-3 py-1 rounded-md text-xs font-medium border"
              style={{ background: 'hsl(var(--highlight))', color: 'hsl(var(--foreground))', borderColor: 'hsl(var(--border-strong))' }}>
              browse files
            </span>
          </motion.div>
        )}
      </AnimatePresence>

      {rejection && (
        <div className="flex items-center gap-2 px-3 py-2 rounded-md border text-xs"
          style={{ background: 'hsl(var(--danger) / 0.08)', color: 'hsl(0 72% 62%)', borderColor: 'hsl(var(--danger) / 0.2)' }}>
          <AlertCircle size={12} /><span>{rejection}</span>
        </div>
      )}
    </div>
  );
}
