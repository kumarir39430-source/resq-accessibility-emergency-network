# ResQ — Emergency help that adapts to you (hackathon prototype)
FastAPI backend + Vite frontend. All phases below are already built in this zip; follow them to run and verify.
Everything marked PROTOTYPE SIMULATION is simulated: no real calls to 112, mesh networking, speech/gesture recognition or AI. Demo coordinates are fictional (Chennai).
NOT IMPLEMENTED YET: database, real auth, real maps, WebSockets (state sync uses 0.8 s polling), real speech/camera.

## 🚀 Quick Setup for Collaborators

### 1. Clone the Repository
```bash
git clone https://github.com/kumarir39430-source/resq-accessibility-emergency-network.git
cd resq-accessibility-emergency-network
```

### 2. Backend Setup (FastAPI)
Run from the `backend` folder:
- **Windows (PowerShell)**:
  ```powershell
  cd backend
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  uvicorn main:app --reload --port 8000
  ```
  *(If script activation is blocked on Windows: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*
- **macOS / Linux**:
  ```bash
  cd backend
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  uvicorn main:app --reload --port 8000
  ```
- **Backend URL**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3. Frontend Setup (Vite)
Open a new terminal and run from the `frontend` folder (requires Node.js 18+):
```bash
cd frontend
npm install
npm run dev
```
- **App URL**: [http://127.0.0.1:5173](http://127.0.0.1:5173) (Vite proxies all `/api` calls directly to port 8000)

## Phase 3 — Run the hero demo (2 minutes)
Open THREE browser tabs on http://localhost:5173: Person, Responder, Coordinator (use the top-bar buttons).
1. Person: set your mode, optionally "Simulate no internet", press and hold SOS.
2. Watch countdown, connecting, AI triage (from the backend), incident fusion.
3. Responder tab: ACCEPT INCIDENT -> precise location unlocks.
4. Person tab: live ETA. Responder tab: ARRIVED -> Person sees "Help has arrived".
5. Coordinator tab: live row RQ-10482 updates. Try Accessibility and Simple mode.

## Phase 4 — Git
[POWERSHELL] run from the `resq` project root:
```powershell
git init
git status
git add .
git commit -m "feat: ResQ prototype with FastAPI backend and Vite frontend"
git push
```
(`git push` only after adding a remote. .env and secrets are git-ignored.)

## Troubleshooting
- Port 8000 busy: use `--port 8001` and change the proxy target in frontend/vite.config.js.
- Tabs not syncing: confirm the badge says "backend: connected".

## v2 Additions
- **"▶ Auto-play demo" button (top bar)**: runs the full hero flow automatically with live explanatory captions at the bottom.
- **START RESPONSE**: tracks active responder response state ("✓ Response started. En route.").
- **CONTACT USER**: simulated secure communication channel between Responder and Person with quick message buttons; messages stream directly to the Person's emergency screen in real time.
- **PITCH.md**: Complete pitch kit with 10s / 30s / 2min demo scripts, slide outline, and judge Q&A prep.
- **Direct Role URLs**: Deep-link directly into `?role=user`, `?role=resp`, or `?role=coord`.
- **API Docs Shortcut**: Direct header button to open FastAPI interactive Swagger documentation (`/docs`).
