# UI Flow & UX Specification

This document provides the definitive UX specifications for the React developer to implement.

---

## 1. Upload Page

**Purpose:** Entry point for users to upload clinical documents and select the target procedure.

**Wireframe (Desktop)**
```text
+-------------------------------------------------------------+
| [Logo] Tvarit AI                                            |
+-------------------------------------------------------------+
|                                                             |
|   Select Procedure                                          |
|   [ Combobox: Type to search procedures... ]                |
|                                                             |
|   Upload Clinical Documentation                             |
|   +-----------------------------------------------------+   |
|   |                                                     |   |
|   |         (Icon) Drag & Drop clinical PDF here        |   |
|   |                                                     |   |
|   +-----------------------------------------------------+   |
|                                                             |
|                  [ Analyze Submission ]                     |
|                                                             |
+-------------------------------------------------------------+
```

**Layouts:**
*   **Desktop:** Centered narrow container (max-w-2xl).
*   **Mobile:** Full width, stacked.

**Components Used:** `Card`, `Dropzone` (react-dropzone), `Combobox` (shadcn), `Button`.
**Animations:** Hover state on dropzone (scale up slightly, border color change).
**States:**
*   **Empty:** Standard dropzone.
*   **Success (File Selected):** Show file icon, filename, file size, and a "Remove" button. Enable "Analyze Submission" button.
*   **Loading:** Button shows spinner. Disable dropzone.

---

## 2. Processing Page

**Purpose:** Provide engaging feedback during the 10-30 second LangGraph orchestration execution.

**Wireframe (Desktop)**
```text
+-------------------------------------------------------------+
|                                                             |
|      [Spinner] Analyzing Submission...                      |
|                                                             |
|      (v) Parsing Document                                   |
|      (v) Extracting Clinical Knowledge                      |
|      (O) Matching Procedure Templates                       |
|      ( ) Running Gap Analysis                               |
|                                                             |
+-------------------------------------------------------------+
```

**Components Used:** Framer Motion `motion.ul`, `motion.li`, `Loader2` (Lucide).
**Animations:** Staggered fade-in of list items. Use Framer Motion's `AnimatePresence`. Automatically transition list items from gray -> blue -> green (completed) using a `useEffect` timer, simulating progress while waiting for the API.
**Error State:** If the API fails, immediately show a critical `Alert` with the error message and a "Go Back" button.

---

## 3. Dashboard Page

**Purpose:** The core product view. Displays the readiness of the prior authorization request.

**Wireframe (Desktop)**
```text
+-------------------------------------------------------------------------+
| Patient: John Doe | Procedure: MRI Lumbar Spine | Status: Review Needed |
+-------------------------------------------------------------------------+
|  [ Readiness Score Gauge ]  | [ Risk Level ]     | [ Completion % ]     |
|          65%                |   HIGH (Badge)     |   [====    ] 71%     |
+-------------------------------------------------------------------------+
| Next Best Actions                     | Matched Evidence                |
| - Upload X-Ray Lumbar Spine           | > Diagnoses (3)                 |
| - Include PT Note                     |   - Low Back Pain               |
|                                       |   - Sciatica                    |
| Missing Critical Evidence             | > Imaging (0)                   |
| +-----------------------------------+ | > Conservative Tx (1)           |
| | (X) X-Ray Lumbar Spine            | |   - NSAIDs                      |
| | Reason: Required within 6 months. | |                                 |
| +-----------------------------------+ |                                 |
+-------------------------------------------------------------------------+
```

**Layouts:**
*   **Desktop:** CSS Grid. Top row (3 columns) for summary cards. Bottom row split 50/50 (Actions/Missing vs. Matched).
*   **Tablet/Mobile:** Single column stacked layout. Summary cards become 2x2 or 1x3 grid.

**Major Components:**
### 1. Readiness Gauge (Summary Card)
*   **Props:** `score` (number).
*   **Visual:** `Recharts` PieChart configured as a half-circle gauge.
*   **Colors:** Red (<70), Yellow (70-89), Green (90+).

### 2. Evidence Panel (Missing)
*   **Props:** `items` (DashboardEvidenceItem[]).
*   **Visual:** Stack of Cards.
*   **Variants:** If critical, apply `border-red-500` and `bg-red-50/10` (dark mode adjusted). Icon: `AlertTriangle`.

### 3. Evidence Panel (Matched)
*   **Props:** `items` (DashboardEvidenceItem[]).
*   **Visual:** `Accordion` grouped by `category`.
*   **Interaction:** Clicking category expands to show matched values and extraction reasons. Icon: `CheckCircle2` (green).

**Dark Mode Behaviour:**
Ensure slate/zinc colors are used for backgrounds. Avoid pure black. Adjust red/green/yellow indicators to be softer (e.g., pastel variants or reduced opacity backgrounds) so they don't clash or cause eye strain in dark mode.

---

## 4. Top Navigation & Sidebar

**Wireframe (Sidebar)**
```text
[ Logo ]
- New Request (Active)
- History (Disabled)
- Settings (Disabled)
[ Theme Toggle ]
```
**Responsive Behaviour:** On mobile, Sidebar collapses into a Hamburger menu (shadcn `Sheet`). On desktop, it is a persistent left-side rail (w-64).
