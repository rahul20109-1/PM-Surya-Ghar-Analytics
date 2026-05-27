## Core Thesis

Vibe coding fails not because AI is bad, but because developers provide vague intent, no structure, and no constraints. AI is a translator, not a mind reader. When fundamentals, documentation, and rules are missing, AI guesses—and those guesses compound into broken systems. Vibe coding works only when you supply clarity, locked constraints, and persistent context.

---

## Most Important Ideas

### 1. Documentation Is the Real Product

Code is a downstream artifact. The real foundation is a **documentation-first system** that defines scope, flows, tech, design, data, and execution order before coding begins. Without this, AI hallucinates architecture, UI, and logic.

### 2. Six Canonical Docs Define Everything

A complete project requires six markdown files as immutable sources of truth:

* **PRD.md** – What is being built, for whom, success criteria, scope, and non-goals.
* **APP_FLOW.md** – Pages, routes, navigation paths, success/error states.
* **TECH_STACK.md** – Exact frameworks, tools, and versions.
* **FRONTEND_GUIDELINES.md** – Design system, tokens, responsive rules.
* **BACKEND_STRUCTURE.md** – Database schema, APIs, auth rules.
* **IMPLEMENTATION_PLAN.md** – Step-by-step build order.

These documents cross-reference each other and eliminate ambiguity.

### 3. AI Needs Persistent Memory

AI has no session memory. Two files solve this:

* **CLAUDE.md** – Global rules, constraints, patterns, forbidden actions.
* **progress.txt** – What’s done, in progress, next, and broken.

Together, they prevent context loss and repeated mistakes.

### 4. Interrogation Before Building

Before documentation, AI must aggressively question the idea to expose assumptions. Clear answers become raw inputs for the canonical docs. Clarity ends hallucinations.

### 5. Fundamentals Matter More Than Prompts

Key concepts you must understand to communicate with AI:

* Components
* Layout
* State
* Styling and design tokens
* Responsive design
* Pages vs routes
* Frontend vs backend
* APIs, databases, authentication

Prompt quality depends on conceptual understanding, not clever wording.

### 6. UI ≠ UX

* **UI**: visual appearance.
* **UX**: usability and flow.
  AI must be told explicitly which one to improve. Visual references (screenshots) outperform verbal descriptions.

### 7. Consistency Comes From Locked Rules

Design tokens, component patterns, folder structure, and dependency versions must be fixed in documentation. Consistency collapses if AI is allowed to improvise.

### 8. Tooling Is Phase-Specific

Different tools excel at different stages:

* **Claude**: thinking, interrogation, documentation.
* **Cursor (Ask → Plan → Agent → Debug)**: implementation workflow.
* **Kimi K2.5**: pixel-accurate frontend from visuals.
* **Codex**: debugging, refactoring, stabilization.
* **GitHub + Vercel + Supabase**: version control, deployment, backend.

### 9. Markdown Is a Control Mechanism

Markdown files are not for humans—they are constraints for AI. More markdown = less guessing = fewer failures.

---

## High-Level Summary

The document presents a complete operating system for AI-assisted software development. It argues that “vibe coding” fails when developers skip fundamentals and documentation, forcing AI to guess. The solution is a rigid, documentation-first workflow where canonical markdown files define product scope, user flows, tech stack, design system, backend schema, and build order. Persistent context files (CLAUDE.md and progress.txt) replace AI memory. Clear conceptual understanding (components, state, layout, UX/UI) enables precise instructions. Proper tool usage by phase and strict version control complete the system. When constraints are explicit, AI stops hallucinating and becomes a reliable builder.

---

## Actionable Steps

### Before Any Coding

1. Run an **AI interrogation** of your idea until no assumptions remain.
2. Answer explicitly: users, core action, data, success/failure states, auth, mobile needs.
3. Generate and manually review the six canonical markdown docs.
4. Lock all docs as the single source of truth.

### Project Setup

5. Create the standard folder structure.
6. Add **CLAUDE.md** with rules, conventions, and references.
7. Create **progress.txt** and update it continuously.
8. Initialize Git and commit documentation first.

### During Development

9. Follow the sequence: **Interrogation → Documentation → Code**.
10. Build only one step at a time from **IMPLEMENTATION_PLAN.md**.
11. Always specify:

    * Components to build
    * Layout rules
    * State changes
    * Routes and pages
12. Reference the relevant markdown file in every AI request.
13. Update **progress.txt** after every completed feature.

### Design & UI

14. Define design tokens (colors, spacing, typography) upfront.
15. Choose 1–2 design styles and document them.
16. Use screenshots as visual references instead of descriptions.
17. Design mobile-first and define breakpoints explicitly.

### Backend & Data

18. Define database schema before writing backend code.
19. Use managed auth (Clerk or Supabase Auth).
20. Never hardcode secrets; use `.env` and environment configs.

### Debugging & Shipping

21. Commit frequently with clear messages.
22. Use Codex or Debug mode for systematic bug fixing.
23. Deploy via GitHub → Vercel.
24. Fix deploy issues using logs, not guesses.

### Continuous Improvement

25. When AI makes a mistake, update **CLAUDE.md** to prevent repetition.
26. Maintain a **lessons.md** file for recurring patterns and fixes.
27. Optionally adopt parallel git worktrees for faster builds once experienced.

---}
