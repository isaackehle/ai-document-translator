# Hebrew Translation Review Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a bilingual English ↔ Hebrew document translation and review workflow with side-by-side review and token highlighting.

**Architecture:** FastAPI backend with Ollama LLM integration for translation, React frontend for review UI. Single repo with `backend/` and `frontend/` directories, progressing through 7 phases from minimal scaffold to production-ready review tool.

**Tech Stack:** FastAPI, Python, Ollama (local LLM), React, Vite, TypeScript, PostgreSQL (optional for persistence)

**Source Document:** `docs/hebrew-translation-workflow-plan.md` (AI-generated exploration with Perplexity)

---

## Phase Overview

This plan is divided into **7 phases**, each producing working, testable software:

- **Phase 0**: Scope definition ✅ (complete)
- **Phase 1**: Minimal backend scaffold (5-7 tasks)
- **Phase 2**: Minimal frontend scaffold (5-7 tasks)
- **Phase 3**: Better segmentation (2-3 tasks)
- **Phase 4**: Token scaffolding (3-4 tasks)
- **Phase 5**: Side-by-side review UI (5-6 tasks)
- **Phase 6**: Click-to-highlight alignment (3-4 tasks)
- **Phase 7**: Reviewer workflow (4-5 tasks)

**Total Estimated Tasks:** ~30-35 discrete GitHub issues

---

## Phase 1: Minimal Backend Scaffold

**Goal:** Build the smallest working FastAPI backend with translation endpoint

**Success Criteria:**
- `/translate` endpoint works from FastAPI docs
- Both language directions (en→he, he→en) supported
- Errors handled cleanly with proper HTTP status codes

### Task 1.1: Project Structure and Dependencies

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/.env.example`
- Create: `backend/app/__init__.py`

- [ ] **Step 1: Create requirements.txt**

```text
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-dotenv>=1.0.0
httpx>=0.26.0
```

- [ ] **Step 2: Create .env.example**

```bash
# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# Application
APP_NAME=Hebrew Translation API
DEBUG=true
```

- [ ] **Step 3: Create app package init**

```python
"""Hebrew Translation API - FastAPI Backend"""
```

- [ ] **Step 4: Commit**

```bash
git add backend/requirements.txt backend/.env.example backend/app/__init__.py
git commit -m "feat(backend): add project structure and dependencies"
```

### Task 1.2: FastAPI Application Scaffold

**Files:**
- Create: `backend/app/main.py`

- [ ] **Step 1: Create main.py with health endpoint**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Hebrew Translation API",
    description="Bilingual English ↔ Hebrew translation with review workflow",
    version="0.1.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

- [ ] **Step 2: Test health endpoint**

```bash
cd backend
uvicorn app.main:app --reload
# In another terminal:
curl http://localhost:8000/health
# Expected: {"status":"healthy","version":"0.1.0"}
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/main.py
git commit -m "feat(backend): add FastAPI app with health endpoint"
```

### Task 1.3: Translation Schemas

**Files:**
- Create: `backend/app/schemas.py`

- [ ] **Step 1: Define request/response schemas**

```python
from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime

LanguageCode = Literal["en", "he"]

class TranslationRequest(BaseModel):
    """Request schema for translation endpoint."""
    source_lang: LanguageCode = Field(..., description="Source language code")
    target_lang: LanguageCode = Field(..., description="Target language code")
    text: str = Field(..., min_length=1, description="Text to translate")
    filename: str | None = Field(None, description="Optional filename")

class Segment(BaseModel):
    """Single translation segment."""
    id: str = Field(..., description="Unique segment identifier")
    source: str = Field(..., description="Source text")
    target: str = Field(..., description="Translated text")

class TranslationResponse(BaseModel):
    """Response schema for translation endpoint."""
    source_lang: LanguageCode
    target_lang: LanguageCode
    segments: List[Segment]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    filename: str | None = None
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/schemas.py
git commit -m "feat(backend): add Pydantic schemas for translation API"
```

### Task 1.4: Segmenter Service

**Files:**
- Create: `backend/app/services/__init__.py`
- Create: `backend/app/services/segmenter.py`

- [ ] **Step 1: Create services package**

```python
"""Backend services package."""
```

- [ ] **Step 2: Implement paragraph-based segmenter**

```python
"""Text segmentation service."""
import re
from typing import List

def segment_by_paragraph(text: str) -> List[str]:
    """
    Segment text by paragraphs (double newlines).

    Args:
        text: Input text to segment

    Returns:
        List of paragraph segments
    """
    # Split by double newlines (paragraph breaks)
    paragraphs = re.split(r'\n\s*\n', text)

    # Filter out empty segments and strip whitespace
    segments = [p.strip() for p in paragraphs if p.strip()]

    return segments

def segment_markdown(text: str) -> List[str]:
    """
    Segment markdown text, preserving headings.

    Args:
        text: Markdown text to segment

    Returns:
        List of segments with headings attached to following content
    """
    # First segment by paragraphs
    segments = segment_by_paragraph(text)

    # TODO: Enhance to preserve heading structure
    # For now, return paragraph segments
    return segments
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/services/__init__.py backend/app/services/segmenter.py
git commit -m "feat(backend): add paragraph-based segmentation service"
```

### Task 1.5: Ollama Translation Service

**Files:**
- Create: `backend/app/services/translator.py`
- Create: `backend/app/core/__init__.py`
- Create: `backend/app/core/config.py`

- [ ] **Step 1: Create config module**

```python
"""Application configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    APP_NAME: str = os.getenv("APP_NAME", "Hebrew Translation API")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
```

- [ ] **Step 2: Implement Ollama translator**

```python
"""Ollama translation service."""
import httpx
from typing import List
from app.core.config import settings
from app.services.segmenter import segment_by_paragraph

async def translate_text(source_lang: str, target_lang: str, text: str) -> List[dict]:
    """
    Translate text using Ollama.

    Args:
        source_lang: Source language code (en/he)
        target_lang: Target language code (en/he)
        text: Text to translate

    Returns:
        List of translation segments with source and target
    """
    segments = segment_by_paragraph(text)
    results = []

    async with httpx.AsyncClient(timeout=60.0) as client:
        for i, segment in enumerate(segments, 1):
            # Build translation prompt
            prompt = f"Translate the following {source_lang} text to {target_lang}. Only output the translation, nothing else:\n\n{segment}"

            # Call Ollama API
            response = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()

            translation = response.json()["response"].strip()

            results.append({
                "id": f"seg-{i:03d}",
                "source": segment,
                "target": translation
            })

    return results
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/core/__init__.py backend/app/core/config.py backend/app/services/translator.py
git commit -m "feat(backend): add Ollama translation service"
```

### Task 1.6: Translation API Endpoint

**Files:**
- Create: `backend/app/api/__init__.py`
- Create: `backend/app/api/routes_translate.py`
- Modify: `backend/app/main.py:15` (add router)

- [ ] **Step 1: Create API package**

```python
"""API routes package."""
```

- [ ] **Step 2: Implement translation route**

```python
"""Translation API routes."""
from fastapi import APIRouter, HTTPException
from app.schemas import TranslationRequest, TranslationResponse
from app.services.translator import translate_text

router = APIRouter(prefix="/api/v1", tags=["Translation"])

@router.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translate text from source to target language.

    - **source_lang**: Source language code (en/he)
    - **target_lang**: Target language code (en/he)
    - **text**: Text to translate
    - **filename**: Optional filename for reference
    """
    # Validate language pair
    if request.source_lang == request.target_lang:
        raise HTTPException(
            status_code=400,
            detail="Source and target languages must be different"
        )

    # Validate language direction
    valid_pairs = [("en", "he"), ("he", "en")]
    if (request.source_lang, request.target_lang) not in valid_pairs:
        raise HTTPException(
            status_code=400,
            detail="Only English ↔ Hebrew translation is supported"
        )

    try:
        segments = await translate_text(
            request.source_lang,
            request.target_lang,
            request.text
        )

        return TranslationResponse(
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            segments=segments,
            filename=request.filename
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(e)}"
        )
```

- [ ] **Step 3: Register router in main.py**

```python
from app.api.routes_translate import router as translate_router

# ... existing code ...

app.include_router(translate_router)
```

- [ ] **Step 4: Test endpoint**

```bash
# Start server
cd backend && uvicorn app.main:app --reload

# Test translation
curl -X POST http://localhost:8000/api/v1/translate \
  -H "Content-Type: application/json" \
  -d '{
    "source_lang": "en",
    "target_lang": "he",
    "text": "The report is due tomorrow."
  }'
```

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/__init__.py backend/app/api/routes_translate.py backend/app/main.py
git commit -m "feat(backend): add translation endpoint with language validation"
```

### Task 1.7: Error Handling and Logging

**Files:**
- Modify: `backend/app/main.py` (add exception handler)
- Create: `backend/app/core/logging_config.py`

- [ ] **Step 1: Add logging configuration**

```python
"""Logging configuration."""
import logging
import sys

def setup_logging(debug: bool = False):
    """Configure application logging."""
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )

    logger = logging.getLogger("app")
    logger.setLevel(level)

    return logger
```

- [ ] **Step 2: Add exception handler to main.py**

```python
from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("app")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": type(exc).__name__}
    )
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/core/logging_config.py backend/app/main.py
git commit -m "feat(backend): add logging and error handling"
```

---

## Phase 2: Minimal Frontend Scaffold

**Goal:** Create React frontend to interact with translation API

**Success Criteria:**
- Upload works from browser
- Source and target render side by side
- Hebrew displays correctly (RTL)

### Task 2.1: React Project Setup

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/tsconfig.json`
- Create: `frontend/index.html`

- [ ] **Step 1: Initialize Vite + React project**

```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install
```

- [ ] **Step 2: Verify setup**

```bash
npm run dev
# Should start on http://localhost:5173
```

- [ ] **Step 3: Commit**

```bash
git add frontend/
git commit -m "feat(frontend): initialize React + Vite project"
```

### Task 2.2: API Client

**Files:**
- Create: `frontend/src/api/client.ts`

- [ ] **Step 1: Create API client**

```typescript
const API_BASE_URL = 'http://localhost:8000';

export interface Segment {
  id: string;
  source: string;
  target: string;
}

export interface TranslationResponse {
  source_lang: string;
  target_lang: string;
  segments: Segment[];
  timestamp: string;
  filename?: string;
}

export async function translate(
  sourceLang: string,
  targetLang: string,
  text: string
): Promise<TranslationResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/translate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      source_lang: sourceLang,
      target_lang: targetLang,
      text: text,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Translation failed');
  }

  return response.json();
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/api/client.ts
git commit -m "feat(frontend): add API client for translation endpoint"
```

### Task 2.3: Upload Form Component

**Files:**
- Create: `frontend/src/components/UploadForm.tsx`

- [ ] **Step 1: Create upload form**

```tsx
import { useState } from 'react';

interface UploadFormProps {
  onTranslate: (sourceLang: string, targetLang: string, text: string) => void;
  isLoading: boolean;
}

export function UploadForm({ onTranslate, isLoading }: UploadFormProps) {
  const [sourceLang, setSourceLang] = useState('en');
  const [targetLang, setTargetLang] = useState('he');
  const [text, setText] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onTranslate(sourceLang, targetLang, text);
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
      <div style={{ marginBottom: '10px' }}>
        <label>
          Source:{' '}
          <select value={sourceLang} onChange={(e) => setSourceLang(e.target.value)}>
            <option value="en">English</option>
            <option value="he">Hebrew</option>
          </select>
        </label>
        {' → '}
        <label>
          Target:{' '}
          <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
            <option value="en">English</option>
            <option value="he">Hebrew</option>
          </select>
        </label>
      </div>

      <div style={{ marginBottom: '10px' }}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text to translate..."
          rows={10}
          style={{ width: '100%', padding: '8px' }}
          disabled={isLoading}
        />
      </div>

      <button type="submit" disabled={isLoading || !text.trim()}>
        {isLoading ? 'Translating...' : 'Translate'}
      </button>
    </form>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/components/UploadForm.tsx
git commit -m "feat(frontend): add upload form with language selectors"
```

### Task 2.4: Segment Row Component

**Files:**
- Create: `frontend/src/components/SegmentRow.tsx`

- [ ] **Step 1: Create segment display component**

```tsx
import { Segment } from '../api/client';

interface SegmentRowProps {
  segment: Segment;
  targetLang: string;
}

export function SegmentRow({ segment, targetLang }: SegmentRowProps) {
  const isHebrew = targetLang === 'he';

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: '20px',
      padding: '15px',
      borderBottom: '1px solid #eee',
      marginBottom: '10px'
    }}>
      <div>
        <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>
          {segment.id}
        </div>
        <div>{segment.source}</div>
      </div>

      <div dir={isHebrew ? 'rtl' : 'ltr'} lang={targetLang}>
        <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>
          Translation
        </div>
        <div style={{ fontFamily: isHebrew ? 'Arial, sans-serif' : 'inherit' }}>
          {segment.target}
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/components/SegmentRow.tsx
git commit -m "feat(frontend): add side-by-side segment display with RTL support"
```

### Task 2.5: Main App Component

**Files:**
- Modify: `frontend/src/App.tsx`

- [ ] **Step 1: Update App.tsx**

```tsx
import { useState } from 'react';
import { UploadForm } from './components/UploadForm';
import { SegmentRow } from './components/SegmentRow';
import { translate, Segment } from './api/client';

function App() {
  const [segments, setSegments] = useState<Segment[]>([]);
  const [targetLang, setTargetLang] = useState('he');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTranslate = async (
    sourceLang: string,
    target: string,
    text: string
  ) => {
    setIsLoading(true);
    setError(null);
    setTargetLang(target);

    try {
      const response = await translate(sourceLang, target, text);
      setSegments(response.segments);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Translation failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
      <h1>Hebrew Translation Review</h1>

      <UploadForm onTranslate={handleTranslate} isLoading={isLoading} />

      {error && (
        <div style={{
          padding: '10px',
          backgroundColor: '#fee',
          border: '1px solid #f99',
          marginBottom: '20px'
        }}>
          Error: {error}
        </div>
      )}

      {segments.length > 0 && (
        <div>
          <h2>Translation Results</h2>
          {segments.map((segment) => (
            <SegmentRow
              key={segment.id}
              segment={segment}
              targetLang={targetLang}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
```

- [ ] **Step 2: Test full workflow**

```bash
# Terminal 1 - Backend
cd backend && uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend && npm run dev

# Open http://localhost:5173
# Test translation from English to Hebrew
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/App.tsx
git commit -m "feat(frontend): integrate upload form and segment display"
```

---

## Next Phases (Outline)

### Phase 3: Better Segmentation (Tasks 3.1-3.3)
- Sentence-aware segmentation
- Preserve markdown structure
- Add logging and file size limits

### Phase 4: Token Scaffolding (Tasks 4.1-4.4)
- Add tokenization to backend
- Update API response schema
- Render tokens in UI
- Prepare for alignment

### Phase 5: Side-by-Side Review UI (Tasks 5.1-5.6)
- Scrollable segment list
- Segment IDs and row numbers
- Status badges (draft/reviewed)
- Search and filter
- Keyboard navigation

### Phase 6: Click-to-Highlight Alignment (Tasks 6.1-6.4)
- Token mapping logic
- Click handlers
- Bidirectional highlighting
- RTL-compatible rendering

### Phase 7: Reviewer Workflow (Tasks 7.1-7.5)
- Manual segment editing
- Split/merge segments
- Reviewer notes
- Export functionality
- Final polish

---

## Testing Strategy

### Backend Tests
```bash
# Run all tests
pytest backend/tests -v

# Run specific test file
pytest backend/tests/test_translator.py -v

# With coverage
pytest backend/tests --cov=app --cov-report=html
```

### Frontend Tests
```bash
# Run tests
npm test

# With coverage
npm test -- --coverage
```

### Manual Testing Checklist
- [ ] Health endpoint responds
- [ ] Translation works en→he
- [ ] Translation works he→en
- [ ] Error handling for invalid language pairs
- [ ] File upload works
- [ ] Segments display side-by-side
- [ ] Hebrew renders RTL correctly
- [ ] Loading states work
- [ ] Error messages display

---

## Deployment Notes

### Backend
```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend
```bash
# Development
npm run dev

# Production build
npm run build
```

### Ollama
```bash
# Ensure Ollama is running
ollama serve

# Pull model if needed
ollama pull llama3.1
```

---

## GitHub Issues Mapping

This plan maps to the following GitHub issue labels:

- `phase-1` through `phase-7` - Phase tracking
- `backend` - Backend tasks
- `frontend` - Frontend tasks
- `good first issue` - Simple tasks (setup, schemas)
- `help wanted` - Complex tasks (token alignment)

Each task above can become a standalone GitHub issue with the checklist items as subtasks.
