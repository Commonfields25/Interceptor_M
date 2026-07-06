## 2026-07-06 - [Initial Project Assessment]
**Learning:** The project has two separate Python web entry points (app.py and api/index.py). api/index.py is the primary landing page for Vercel and contains most of the UI logic.
**Action:** Focus UX improvements on api/index.py to ensure the most visible impact.
## 2026-07-06 - [Starlette Middleware Import Pattern]
**Learning:** In the current environment's version of Starlette, `ExceptionMiddleware` must be imported from `starlette.middleware.exceptions` rather than `starlette.exceptions`.
**Action:** Use the specific middleware path for exception handling in Starlette-based projects to avoid AttributeErrors during runtime.
## 2026-07-06 - [High-tech Aerospace Theme & Accessibility Polish]
**Learning:** Transitioning from inline styles to a centralized CSS variable system dramatically improves maintainability and enables seamless system dark mode support. Using 'Inter' and a technical slate/blue palette aligns the UI with the project's aerospace engineering identity.
**Action:** Always prioritize external assets and CSS variables for themeable interfaces to ensure scalability and accessibility.
