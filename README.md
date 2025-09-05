# Open Password Leak Check (OPLC)

**A privacy‑preserving, open‑source web app that lets anyone check if a password appears in known breach corpora without sending the password to the server.**

Live App: **https://huggingface.co/spaces/r3ddkahili/oplc-ui**  
API Docs: **https://r3ddkahili-oplc-api.hf.space/docs**

> TL;DR: Your browser hashes the password with SHA‑1 and only sends the first **5 hex characters** of the hash (k‑anonymity). The API replies with a bucket of suffixes and counts; the match happens locally in your browser. No plaintext passwords, no full hashes, no cookies.

---

## ✨ Features
- **Client‑side hashing** (Web Crypto): the full password never leaves the browser.
- **k‑Anonymity range lookup**: only a 5‑char SHA‑1 prefix is sent to the API.
- **Response padding**: reduces information leakage by normalizing response sizes.
- **Simple, accessible UI**: one page, keyboard friendly, includes a *Show password* toggle.
- **OSS + Cloud‑only**: built and deployed with Hugging Face Spaces; code lives in GitHub.

---

## 🧭 How it works
1. You type a password into the UI (client only).
2. The UI computes SHA‑1 and splits into **prefix (first 5)** + **suffix (remaining 35)**.
3. The UI calls `GET /range/{prefix}` on the API.
4. The API returns lines `SUFFIX:COUNT` for that range (optionally padded to ≥800 lines).
5. The UI searches locally for the suffix and shows the count (if any).

No password or full hash is ever transmitted or stored.

---

## 📚 Dataset
- **Upstream dataset:** **Pwned Passwords** (Have I Been Pwned). This is a publicly available corpus of **SHA‑1 hashed passwords with breach counts**. We use it in two ways:
  - **Proxy mode (default):** the API forwards k‑anonymous range lookups to the official **Pwned Passwords Range API** with response padding enabled. No dataset hosting is required on our side.
  - **Self‑hosted mirror (optional):** for research/independence, you can ingest the latest Pwned Passwords into **prefix‑grouped shards** and publish them as a **Hugging Face Dataset** (`data/pp-XX.jsonl.zst`, records: `{prefix, suffix, count}`). The API can then serve from this mirror by setting `BACKEND_MODE=hf`.
- **Notes & ethics:** Use the dataset for **defensive purposes** only. Review the upstream terms before mirroring. This project does **not** store plaintext passwords and never transmits full hashes.

---

## ⚠️ Important disclaimer
**This project is an assistive tool only. Do not rely on it as your sole security check.** A result of “Not found” does **not** guarantee safety, and a positive result only indicates the password has appeared in public breach corpora. Always use a password manager to generate unique, strong passwords, and enable multi‑factor authentication (MFA). Consider additional defenses like breach monitoring and device security.

### Why this project exists (caveat)
This is **not a replacement** for existing services like Have I Been Pwned (HIBP). It’s a transparent, open‑source **reference implementation** you can audit, learn from, and self‑host.

- **Education & capstone value:** shows end‑to‑end k‑anonymity, padding, strict CSP, and CI/monitoring.
- **Trust & transparency:** 100% open code, no cookies or tracking; everything verifiable.
- **Customization:** change UX copy, language, policy guidance, or integrate into your org.
- **Independence option:** mirror mode (HF Datasets) if upstream is rate‑limited/unavailable.
- **Research playground:** try enhancements (e.g., stronger padding, PIR) without depending on third‑party releases.

If you just want a ready service, you can use HIBP directly; see **References** below. If you want an **auditable, forkable, cloud‑only blueprint**, use this project.

## 🔐 Privacy & Security
- **No plaintext**: your password never leaves your device.
- **No full hashes**: the server only sees a 5‑char prefix.
- **No cookies**: the UI/API set **no cookies** and avoid localStorage/sessionStorage.
- **CSP**: a strict Content‑Security‑Policy is applied in the UI.
- **Minimal logging**: server runs without access logs; never log prefixes/body.

**Important:** “Not found” ≠ safe. Always use unique, strong passwords (ideally via a password manager) and enable multi‑factor authentication.

---

## 🧱 Architecture
- **UI (Static Space):** `r3ddkahili/oplc-ui` → serves `index.html` (hashing, fetch, display)
- **API (Docker Space):** `r3ddkahili/oplc-api` → FastAPI service exposing:
  - `GET /healthz` → liveness probe
  - `GET /range/{prefix}` → suffix list for 5‑char SHA‑1 prefix
  - `GET /docs` → OpenAPI/Swagger
- **Two backends supported by the API**
  - **proxy** (default): forwards the range request upstream (with padding header)
  - **hf** (optional): serves from a self‑hosted mirror on Hugging Face Datasets

---

## 🚀 Quick start (use it)
- Visit **https://huggingface.co/spaces/r3ddkahili/oplc-ui**
- Type a password → click **Check** (or press **Enter**)
- Toggle **Show** to verify your input if needed

Demo: try the word `password` and notice the high breach count.

---

## 🛠️ Developer guide

### Project layout
```
spaces/
  oplc-api/           # FastAPI service (Docker Space)
    Dockerfile
    requirements.txt
    app/
      __init__.py
      main.py
      storage.py
  oplc-ui/            # Static UI (Static Space)
    index.html
    style.css         # optional
.github/
  workflows/
    smoke.yml         # CI smoke tests for live Spaces
    deploy-api.yml    # optional: auto deploy API Space from GitHub
    deploy-ui.yml     # optional: auto deploy UI Space from GitHub
```

### Environment variables (API Space)
- `BACKEND_MODE` = `proxy` (default) or `hf`
- `PADDING` = `true` (default)
- `HF_DATASET_REPO` = `<org>/<dataset>` (for `hf` mode only)
- `CACHE_DIR` = `/tmp/oplc-cache` (safe default)

### Run the API locally (optional)
```bash
pip install -r spaces/oplc-api/requirements.txt
uvicorn spaces.oplc_api.app.main:app --reload
# then open http://127.0.0.1:8000/docs
```

### Run the UI locally (optional)
```bash
cd spaces/oplc-ui
python -m http.server 8080
# open http://127.0.0.1:8080/?api=http://127.0.0.1:8000
```

---

## 🔄 CI / Monitoring (GitHub Actions)
- **smoke.yml** checks the live Spaces:
  - API `/healthz` returns `ok`
  - `/range/5BAA6` contains the known suffix for `password`
  - UI home is reachable and contains the project title
- Optional workflows (**deploy-*.yml**) push changes from GitHub → Hugging Face Spaces using a `HF_TOKEN` repository secret.

Add a status badge to your README (replace names as needed):
```md
![smoke](https://github.com/<your-username>/<your-repo>/actions/workflows/smoke.yml/badge.svg)
```

---

## 📦 Deploying to Hugging Face
**UI (Static Space):**
1. Create Space → SDK: **Static** → Public
2. Add `index.html` at the **root** (and `style.css` if used)

**API (Docker Space):**
1. Create Space → SDK: **Docker** → Public
2. Add `Dockerfile`, `requirements.txt`, and the `app/` folder
3. Set Variables: `BACKEND_MODE=proxy`, `PADDING=true`, `CACHE_DIR=/tmp/oplc-cache`
4. Restart Space → visit `/healthz`, `/docs`, and test `/range/5BAA6`

---

## 📚 FAQ
**Q: Do you store passwords or cookies?**  
A: No. Your password never leaves your device; only a 5‑char prefix is sent. The app does not set cookies.

**Q: Is “not found” a guarantee of safety?**  
A: No. It only means the password isn’t in the dataset used. Always use unique, strong passwords and enable MFA.

**Q: Why SHA‑1? Isn’t it broken?**  
A: We’re not using SHA‑1 for security; it’s used as a stable index for range queries compatible with public breach datasets. The *password itself* is never transmitted.

**Q: Can I self‑host without the upstream API?**  
A: Yes. Build a prefix‑grouped mirror on Kaggle and publish as a Hugging Face Dataset; run the API in `hf` mode.

---

## 🗺️ Roadmap
- Externalize UI script (`app.js`) and tighten CSP (drop `'unsafe-inline'`).
- Add strength meter and guidance links.
- Add optional rate limiting and simple analytics **without** identifiers.
- Evaluate Private Information Retrieval (PIR) as a research track.

---

## 🤝 Contributing
Issues and PRs are welcome. Please avoid submitting real passwords in issues.

---

## ⚖️ License
MIT (see `LICENSE`).

---

## 🙏 Acknowledgments
- The password range‑query approach popularized by defenders to reduce exposure risk.
- The open‑source community around privacy‑preserving security tooling.



---

## 📎 References
- Pwned Passwords (Have I Been Pwned): https://haveibeenpwned.com/Passwords
- Pwned Passwords Range API (k‑anonymity): https://haveibeenpwned.com/API/v3#PwnedPasswords
- Example range endpoint: https://api.pwnedpasswords.com/range/5BAA6
- MDN Web Crypto API (SubtleCrypto.digest): https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/digest
- FastAPI documentation: https://fastapi.tiangolo.com/
- Hugging Face Spaces overview: https://huggingface.co/docs/hub/spaces-overview

