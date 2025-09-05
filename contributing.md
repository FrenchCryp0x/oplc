# Contributing to OPLC

Thanks for your interest in improving **Open Password Leak Check (OPLC)**! This project aims to be a clear, auditable reference for privacy‑preserving password range checks.

> **Safety first:** Never share real passwords, tokens, or secrets in issues, commits, or tests.

---

## Ways to contribute
- **Bug reports:** Open a GitHub Issue with steps to reproduce, expected/actual behavior, and environment (browser, OS). Attach screenshots or console logs if relevant.
- **Feature proposals:** Describe the problem, not just the solution. Explain the user benefit and privacy impact.
- **Docs:** Fix typos, clarify steps, improve examples.
- **Code:** Send small, focused PRs. Larger changes: open an Issue first for design discussion.

---

## Development setup (quick)
- **API (FastAPI):**
  ```bash
  pip install -r spaces/oplc-api/requirements.txt
  uvicorn spaces.oplc_api.app.main:app --reload
  # http://127.0.0.1:8000/docs
  ```
- **UI (Static):**
  ```bash
  cd spaces/oplc-ui
  python -m http.server 8080
  # http://127.0.0.1:8080/?api=http://127.0.0.1:8000
  ```

---

## Coding standards
- Keep code **simple, readable, testable** (KISS).
- Prefer **explicit names**, small functions, and clear error messages.
- Follow project conventions (PEP8 for Python; semantic HTML; minimal JS).
- Document the **why** in code comments when non‑obvious.

---

## Commit & PR guidelines
- One logical change per PR.
- Include a short description of **what** changed and **why**.
- For UI changes, add a screenshot/GIF.
- Ensure the app still runs and core flows work before submitting.

---

## Issue template (copy/paste)
```
### Summary

### Steps to reproduce
1.
2.
3.

### Actual

### Expected

### Environment
- Browser + version:
- OS:
- API/UI commit SHA:

### Notes
(Logs, screenshots, additional context)
```

---

## Code of Conduct (short)
Be respectful, constructive, and considerate. No harassment, hate speech, or doxxing. Disagreements are fine; personal attacks are not. Moderators may edit/lock threads that violate these principles.

---

## Security & privacy when contributing
- Use **test strings**; never paste real credentials.
- Don’t add analytics or tracking without prior design discussion.
- Keep CSP strict; avoid introducing third‑party scripts.

See **SECURITY.md** for vulnerability reporting.

