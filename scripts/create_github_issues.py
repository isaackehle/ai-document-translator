#!/usr/bin/env python3
"""Create GitHub issues from implementation plan."""

import subprocess
import sys


def run_gh_command(args):
    """Run gh command and return result."""
    try:
        result = subprocess.run(
            ["gh"] + args, capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def create_issue(title, body, labels):
    """Create a GitHub issue."""
    print(f"Creating: {title}")

    # Write body to temp file to avoid shell escaping issues
    with open("/tmp/issue_body.md", "w") as f:
        f.write(body)

    args = ["issue", "create", "--title", title, "--body-file", "/tmp/issue_body.md"]
    for label in labels:
        args.extend(["--label", label])

    success, stdout, stderr = run_gh_command(args)

    if success:
        print(f"  ✓ Created successfully")
        if stdout:
            print(f"  {stdout.strip()}")
    else:
        print(f"  ✗ Failed: {stderr}")

    return success


def main():
    """Create all Phase 1 issues."""

    issues = [
        {
            "title": "Phase 1: Project Structure and Dependencies",
            "labels": ["phase-1", "backend", "good first issue"],
            "body": """## Goal
Set up the minimal backend project structure with dependencies and configuration.

## Tasks
- [ ] Create `backend/requirements.txt` with FastAPI, uvicorn, python-dotenv, httpx
- [ ] Create `backend/.env.example` with Ollama configuration
- [ ] Create `backend/app/__init__.py` package init
- [ ] Verify dependencies install correctly

## Files to Create
- `backend/requirements.txt`
- `backend/.env.example`
- `backend/app/__init__.py`

## Acceptance Criteria
- [ ] `pip install -r backend/requirements.txt` succeeds
- [ ] Environment variables documented in `.env.example`
- [ ] Python package structure is valid

## Implementation Details

### requirements.txt
```text
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-dotenv>=1.0.0
httpx>=0.26.0
```

### .env.example
```bash
# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# Application
APP_NAME=Hebrew Translation API
DEBUG=true
```

## References
- Parent plan: `docs/plans/hebrew-translation-implementation.md`
- Phase: Phase 1 - Minimal Backend Scaffold
""",
        },
        {
            "title": "Phase 1: FastAPI Application Scaffold",
            "labels": ["phase-1", "backend", "good first issue"],
            "body": """## Goal
Create the base FastAPI application with health check endpoint.

## Tasks
- [ ] Create `backend/app/main.py` with FastAPI app
- [ ] Add CORS middleware configuration
- [ ] Implement `GET /health` endpoint
- [ ] Test health endpoint returns correct response

## Files to Create
- `backend/app/main.py`

## Acceptance Criteria
- [ ] Application starts with uvicorn
- [ ] `GET /health` returns {"status": "healthy", "version": "0.1.0"}
- [ ] CORS configured for frontend origin

## Implementation Details

### main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Hebrew Translation API",
    description="Bilingual English ↔ Hebrew translation with review workflow",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}
```

## Testing
```bash
cd backend
uvicorn app.main:app --reload
curl http://localhost:8000/health
```

## References
- Parent plan: `docs/plans/hebrew-translation-implementation.md`
- Depends on: #1
""",
        },
        {
            "title": "Phase 1: Translation Schemas",
            "labels": ["phase-1", "backend", "good first issue"],
            "body": """## Goal
Define Pydantic schemas for translation API request/response.

## Tasks
- [ ] Create `backend/app/schemas.py`
- [ ] Define `TranslationRequest` schema
- [ ] Define `Segment` schema
- [ ] Define `TranslationResponse` schema

## Files to Create
- `backend/app/schemas.py`

## Acceptance Criteria
- [ ] All schemas properly typed
- [ ] Language codes restricted to "en" and "he"
- [ ] Response includes timestamp

## Implementation Details

### schemas.py
```python
from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime

LanguageCode = Literal["en", "he"]

class TranslationRequest(BaseModel):
    source_lang: LanguageCode
    target_lang: LanguageCode
    text: str = Field(..., min_length=1)
    filename: str | None = None

class Segment(BaseModel):
    id: str
    source: str
    target: str

class TranslationResponse(BaseModel):
    source_lang: LanguageCode
    target_lang: LanguageCode
    segments: List[Segment]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

## References
- Parent plan: `docs/plans/hebrew-translation-implementation.md`
- Depends on: #1
""",
        },
        {
            "title": "Phase 1: Segmenter Service",
            "labels": ["phase-1", "backend"],
            "body": """## Goal
Implement paragraph-based text segmentation service.

## Tasks
- [ ] Create `backend/app/services/__init__.py`
- [ ] Create `backend/app/services/segmenter.py`
- [ ] Implement `segment_by_paragraph()` function
- [ ] Add unit tests

## Files to Create
- `backend/app/services/__init__.py`
- `backend/app/services/segmenter.py`

## Implementation Details

### segmenter.py
```python
import re
from typing import List

def segment_by_paragraph(text: str) -> List[str]:
    paragraphs = re.split(r'\\n\\s*\\n', text)
    segments = [p.strip() for p in paragraphs if p.strip()]
    return segments
```

## References
- Parent plan: `docs/plans/hebrew-translation-implementation.md`
- Depends on: #1
""",
        },
        {
            "title": "Phase 1: Ollama Translation Service",
            "labels": ["phase-1", "backend", "help wanted"],
            "body": """## Goal
Integrate Ollama API for translation calls.

## Tasks
- [ ] Create `backend/app/core/config.py`
- [ ] Create `backend/app/services/translator.py`
- [ ] Implement `translate_text()` async function
- [ ] Handle timeouts and errors

## Files to Create
- `backend/app/core/__init__.py`
- `backend/app/core/config.py`
- `backend/app/services/translator.py`

## Prerequisites
- Ollama must be running locally
- Model (llama3.1) must be pulled

## References
- Parent plan: `docs/plans/hebrew-translation-implementation.md`
- Depends on: #3, #4
""",
        },
        {
            "title": "Phase 1: Translation API Endpoint",
            "labels": ["phase-1", "backend"],
            "body": """## Goal
Create the main translation endpoint with validation.

## Tasks
- [ ] Create `backend/app/api/__init__.py`
- [ ] Create `backend/app/api/routes_translate.py`
- [ ] Implement `POST /api/v1/translate` endpoint
- [ ] Add language pair validation
- [ ] Register router in main.py

## Files to Create
- `backend/app/api/__init__.py`
- `backend/app/api/routes_translate.py`

## Files to Modify
- `backend/app/main.py`

## References
- Parent plan: `docs/plans/hebrew-translation-implementation.md`
- Depends on: #2, #3, #5
""",
        },
        {
            "title": "Phase 1: Error Handling and Logging",
            "labels": ["phase-1", "backend"],
            "body": """## Goal
Add comprehensive error handling and logging to backend.

## Tasks
- [ ] Create `backend/app/core/logging_config.py`
- [ ] Add global exception handler
- [ ] Configure logging levels
- [ ] Log all translation requests

## Files to Create
- `backend/app/core/logging_config.py`

## Files to Modify
- `backend/app/main.py`

## References
- Parent plan: `docs/plans/hebrew-translation-implementation.md`
- Depends on: #2
""",
        },
        {
            "title": "Phase 2: React Project Setup",
            "labels": ["phase-2", "frontend", "good first issue"],
            "body": """## Goal
Initialize React + Vite project for the review UI.

## Tasks
- [ ] Create Vite + React + TypeScript project
- [ ] Install dependencies
- [ ] Configure for development
- [ ] Verify dev server starts

## Files to Create
- `frontend/package.json`
- `frontend/vite.config.ts`
- `frontend/index.html`

## Commands
```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install
npm run dev
```

## References
- Parent plan: `docs/plans/hebrew-translation-implementation.md`
- Phase: Phase 2 - Minimal Frontend Scaffold
""",
        },
        {
            "title": "Phase 2: API Client",
            "labels": ["phase-2", "frontend", "good first issue"],
            "body": """## Goal
Create TypeScript API client for translation endpoint.

## Tasks
- [ ] Create `frontend/src/api/client.ts`
- [ ] Define TypeScript interfaces
- [ ] Implement `translate()` function
- [ ] Handle errors properly

## Files to Create
- `frontend/src/api/client.ts`

## References
- Parent plan: `docs/plans/hebrew-translation-implementation.md`
- Depends on: #8 (React Setup)
""",
        },
        {
            "title": "Phase 2: Upload Form Component",
            "labels": ["phase-2", "frontend"],
            "body": """## Goal
Create upload form with language selectors.

## Tasks
- [ ] Create `frontend/src/components/UploadForm.tsx`
- [ ] Add source/target language dropdowns
- [ ] Add textarea for text input
- [ ] Add submit handler
- [ ] Add loading state

## Files to Create
- `frontend/src/components/UploadForm.tsx`

## References
- Parent plan: `docs/plans/hebrew-translation-implementation.md`
- Depends on: #8 (React Setup)
""",
        },
        {
            "title": "Phase 2: Segment Row Component",
            "labels": ["phase-2", "frontend"],
            "body": """## Goal
Create side-by-side segment display with RTL support.

## Tasks
- [ ] Create `frontend/src/components/SegmentRow.tsx`
- [ ] Display source and target side by side
- [ ] Add RTL support for Hebrew
- [ ] Show segment IDs
- [ ] Style for readability

## Files to Create
- `frontend/src/components/SegmentRow.tsx`

## References
- Parent plan: `docs/plans/hebrew-translation-implementation.md`
- Depends on: #8 (React Setup)
""",
        },
        {
            "title": "Phase 2: Main App Component",
            "labels": ["phase-2", "frontend"],
            "body": """## Goal
Integrate all components in main App.

## Tasks
- [ ] Update `frontend/src/App.tsx`
- [ ] Integrate UploadForm component
- [ ] Integrate SegmentRow component
- [ ] Add state management
- [ ] Connect to API client
- [ ] Handle errors and loading states
- [ ] Test full workflow

## Files to Modify
- `frontend/src/App.tsx`

## Testing
```bash
# Terminal 1 - Backend
cd backend && uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend && npm run dev

# Open http://localhost:5173
```

## References
- Parent plan: `docs/plans/hebrew-translation-implementation.md`
- Depends on: #9, #10, #11
""",
        },
    ]

    print("Creating GitHub issues from implementation plan...\n")
    print("=" * 60)

    created = 0
    failed = 0

    for issue_data in issues:
        if create_issue(issue_data["title"], issue_data["body"], issue_data["labels"]):
            created += 1
        else:
            failed += 1
        print()

    print("=" * 60)
    print(f"\nSummary: {created} created, {failed} failed")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
