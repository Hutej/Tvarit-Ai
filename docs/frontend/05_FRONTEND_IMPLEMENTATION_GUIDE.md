# Frontend Implementation Guide

This document serves as the absolute source of truth for the Tvarit AI React Frontend. It combines architecture, design systems, application lifecycle, and practical implementation guidelines using JavaScript (JSX). NO TypeScript is to be used.

## 1. Complete Folder Structure
*(Refer to 04_FRONTEND_DATA_MODELS.md for the directory tree)*

## 2. Component Tree & Page Hierarchy
```text
App (React Router)
└── MainLayout
    ├── Sidebar
    ├── Header
    └── Outlet (Page Content)
        ├── UploadPage
        │   ├── ProcedureSelector (Combobox)
        │   └── DocumentDropzone (react-dropzone)
        ├── ProcessingPage
        │   └── ProcessingSteps (Framer Motion sequence)
        └── DashboardPage
            ├── SummaryCards
            │   ├── ReadinessGauge (Recharts)
            │   ├── RiskBadge
            │   └── CompletionProgress
            ├── LeftColumn
            │   ├── NextActionsList
            │   └── MissingEvidenceCard (mapped list)
            └── RightColumn
                └── EvidenceAccordion (mapped list)
```

## 3. Application Lifecycle
1. **Initial Load:** User lands on `UploadPage`. No server data is fetched yet.
2. **Action 1:** User drops file. Call `useUploadDocument` mutation. Update local state with `document_id`.
3. **Action 2:** User selects procedure from hardcoded list. Clicks "Analyze". Call `useRunWorkflow` mutation.
4. **Transition:** Immediately route to `ProcessingPage`. Wait for mutation to resolve.
5. **Resolution:** Mutation resolves with `authorization_id`. Route to `DashboardPage/:id`.
6. **Data Fetch:** `DashboardPage` mounts, triggers `useDashboard(id)` query. Displays data.

## 4. React Query & State Strategy
*   **No Global State Libraries:** Do not use Redux, Zustand, or Jotai. 
*   **React Query:** Handles all async data, caching, and loading/error states. 
*   **Local State:** `useState` is sufficient for forms and UI toggles.

## 5. Sample Component Implementations (JSX)

### React Router Example (`src/App.jsx`)
```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import UploadPage from './pages/UploadPage';
import ProcessingPage from './pages/ProcessingPage';
import DashboardPage from './pages/DashboardPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<MainLayout />}>
          <Route path="/" element={<UploadPage />} />
          <Route path="/processing" element={<ProcessingPage />} />
          <Route path="/dashboard/:id" element={<DashboardPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

### Framer Motion Example (`src/pages/ProcessingPage.jsx`)
```jsx
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';

export default function ProcessingPage() {
  const steps = [
    "Parsing Clinical Document...",
    "Extracting Medical Knowledge with AI...",
    "Loading Procedure Guidelines...",
    "Running Gap Analysis..."
  ];

  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh]">
      <Loader2 className="w-12 h-12 text-blue-500 animate-spin mb-8" />
      <motion.ul
        initial="hidden"
        animate="visible"
        variants={{
          visible: { transition: { staggerChildren: 1.5 } },
        }}
        className="space-y-4 text-lg"
      >
        {steps.map((step, idx) => (
          <motion.li
            key={idx}
            variants={{
              hidden: { opacity: 0, y: 10 },
              visible: { opacity: 1, y: 0 }
            }}
            className="flex items-center space-x-3 text-slate-700 dark:text-slate-300"
          >
            <div className="w-2 h-2 rounded-full bg-blue-500" />
            <span>{step}</span>
          </motion.li>
        ))}
      </motion.ul>
    </div>
  );
}
```

### Recharts Example (`src/components/features/dashboard/ReadinessGauge.jsx`)
```jsx
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

export default function ReadinessGauge({ score }) {
  const data = [
    { name: 'Score', value: score },
    { name: 'Empty', value: 100 - score }
  ];
  
  const getColor = (s) => {
    if (s >= 90) return '#10b981'; // emerald
    if (s >= 70) return '#f59e0b'; // amber
    return '#ef4444'; // rose
  };

  return (
    <div className="w-full h-48">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="100%"
            startAngle={180}
            endAngle={0}
            innerRadius={60}
            outerRadius={80}
            dataKey="value"
            stroke="none"
          >
            <Cell fill={getColor(score)} />
            <Cell fill="#f1f5f9" /> {/* slate-100 */}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <div className="text-center -mt-10 text-3xl font-bold">
        {score}%
      </div>
    </div>
  );
}
```

## 6. Design System

*   **Colors:** 
    *   Primary Brand: `slate` (clean, professional).
    *   Success/Matched: `emerald` (`text-emerald-600`, `bg-emerald-50`).
    *   Warning/Missing: `rose` (`text-rose-600`, `bg-rose-50`).
    *   Borders: `slate-200` (light mode), `slate-800` (dark mode).
*   **Typography:** Inter (via Google Fonts or Next.js fonts). standard tailwind sizes.
*   **Spacing & Elevation:** Minimal shadows (`shadow-sm`). Flat UI design. Border radius `rounded-lg` or `rounded-xl`.
*   **Icons:** Use `lucide-react`. 
    *   Matched: `CheckCircle2`
    *   Missing: `AlertTriangle`
    *   Procedure: `Activity`

## 7. Loading & Error UX
*   **Upload Failure:** Show a `toast` with a clear message (e.g., "File too large. Max 10MB.").
*   **Workflow Failure / Timeout:** Because the workflow takes 10-30s, network issues can occur. If the mutation errors out, immediately show an error state on the Processing page with a "Try Again" button.
*   **Empty Dashboard:** If `dashboard_response` is somehow empty, show a polite Empty State component ("No data available for this request.").
*   **Skeleton Loaders:** If navigating directly to `/dashboard/:id`, show a skeleton layout matching the Dashboard grid while `useDashboard` is fetching.

## 8. Dashboard Layout Specification
*   **Top Row:** 3 equal-width cards. 
*   **Readiness Gauge:** Must be visually prominent. Use a half-donut pie chart.
*   **Missing Evidence:** Prioritize displaying the `reason` why it's missing (e.g., "Missing required imaging within 6 months"). This proves the engine's intelligence.
*   **Matched Evidence:** Must be grouped by `category` (e.g., DIAGNOSIS, IMAGING) into an accordion so it doesn't overwhelm the user.

## 9. Implementation Order (Sprints)
1.  **Sprint 1:** Scaffold Vite/React project. Install Tailwind, shadcn/ui. Build layout shell (Header/Sidebar). Set up Axios and React Query.
2.  **Sprint 2:** Build Dashboard UI *using hardcoded mock data* based on `02_API_REFERENCE.md`. Perfect the charts and evidence cards.
3.  **Sprint 3:** Build Upload and Processing pages. Connect `useUploadDocument` and `useRunWorkflow` mutations.
4.  **Sprint 4:** Wire Dashboard to actual API. Add dark mode, polish animations, and test error states.

---

## 10. Hackathon Demo Script (Expanded 5-Minute Pitch)

**Role:** Presenter (speaking), Driver (clicking the UI).

**[0:00 - 1:00] The Hook & The Problem**
*   **Speaker:** "80% of prior authorizations are rejected on the first attempt, not because the patient doesn't need care, but because a specific piece of clinical evidence is missing. Providers wait 14 days just to get an administrative denial. Tvarit AI solves this."
*   **Driver:** Shows the clean, empty Upload screen. 

**[1:00 - 2:00] The Ingestion**
*   **Speaker:** "Instead of manually auditing charts, a clinician drops the unstructured clinical note here and selects the target procedure—say, an MRI of the Lumbar Spine."
*   **Driver:** Drags a sample PDF into the dropzone. Selects "MRI Lumbar Spine". Clicks "Analyze".

**[2:00 - 3:00] The Intelligence (Processing Screen)**
*   **Speaker:** "Right now, our LangGraph orchestration engine is actively parsing the PDF, extracting canonical medical knowledge using deterministic AI structured outputs, loading the exact insurance requirements for an MRI, and running a gap analysis."
*   **Driver:** Lets the Processing animation play out.

**[3:00 - 4:00] The Reveal (Dashboard)**
*   **Speaker:** "In 15 seconds, we have our answer. The submission is only 65% ready. The risk of denial is HIGH. Why?"
*   **Driver:** Cursor hovers over the Readiness Gauge, then moves to the "Missing Evidence" column.
*   **Speaker:** "Tvarit AI identifies exactly what's missing. The provider documented conservative treatment, but forgot to attach the previous X-Ray required within the last 6 months. It provides the Next Best Action immediately."

**[4:00 - 5:00] The Trust & Conclusion**
*   **Speaker:** "But why should we trust it? Look at the Matched Evidence."
*   **Driver:** Expands the "Diagnoses" and "Conservative Treatment" accordions in the Matched Evidence panel.
*   **Speaker:** "It flawlessly extracted 'Sciatica' and '6 weeks of Physical Therapy' from the raw text. By identifying gaps *before* submission, Tvarit AI eliminates administrative rework, prevents denials, and accelerates patient care. Thank you."

---

## 11. Cursor AI Prompt

**Instructions for the Developer:** Paste the following prompt into Cursor AI (or your preferred AI IDE) to kickstart the frontend development.

> "You are an expert React developer. I want to build the frontend for the Tvarit AI platform. Please review the documentation in the `docs/frontend` directory (01 through 05). We are using React 19, Vite, JavaScript (JSX), TailwindCSS, shadcn/ui, React Query (TanStack Query), Axios, Recharts, Framer Motion, and Lucide React.
> 
> DO NOT use TypeScript. Do not generate `.tsx` or `.ts` files. Use only `.jsx` and `.js`.
> 
> First, please scaffold the primary layout shell (`MainLayout.jsx`, `Sidebar.jsx`, `Header.jsx`). 
> Second, set up `src/services/apiConfig.js` and `src/hooks/useWorkflow.js` according to the data models in `04_FRONTEND_DATA_MODELS.md`. 
> Finally, create a mock version of the `DashboardPage.jsx` focusing heavily on the Recharts Readiness Gauge and the Split-view Evidence Panels as defined in `03_UI_FLOW.md` and `05_FRONTEND_IMPLEMENTATION_GUIDE.md`. Ensure strict usage of pure JavaScript."
