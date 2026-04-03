# Hebrew Translation Review Workflow

## Goal
Build a bilingual English ↔ Hebrew document translation and review workflow that starts small and grows into a product-style system with side-by-side review and token highlighting.

## Project framing
This project is meant to help position you for Python + AI workflow roles. The public/core version should show:
- FastAPI backend design
- Local LLM integration with Ollama
- Document ingestion and segmentation
- React review UI
- English ↔ Hebrew language handling, including RTL concerns

Potential private/commercial extensions can include advanced alignment, premium review tools, analytics, customer integrations, and hosted deployment.

## Phase 0 — Define the smallest version
Objective: keep scope under control.

Deliverables:
- One repo with `backend/` and `frontend/`
- Input support for `.txt` and `.md`
- Two supported language directions: `en -> he` and `he -> en`
- Output returned as aligned segment JSON

Success criteria:
- Upload a file
- Choose source and target language
- Receive translated segment pairs
- Display them side by side in the browser

---

## Phase 1 — Minimal backend scaffold
Objective: build the smallest backend that works.

Suggested structure:

```text
backend/
  app/
    main.py
    schemas.py
    api/
      routes_translate.py
    services/
      translator.py
      segmenter.py
  requirements.txt
  .env.example
```

Core tasks:
- Create FastAPI app
- Add `GET /health`
- Add `POST /translate`
- Validate `source_lang` and `target_lang`
- Read uploaded text or markdown file
- Segment text by paragraph first
- Call Ollama for translation
- Return JSON response

Suggested response shape:

```json
{
  "source_lang": "en",
  "target_lang": "he",
  "segments": [
    {
      "id": "seg-1",
      "source": "The report is due tomorrow.",
      "target": "הדוח אמור להימסר מחר."
    }
  ]
}
```

Success criteria:
- `/translate` works from FastAPI docs
- Both directions are supported
- Errors are handled cleanly

---

## Phase 2 — Minimal frontend scaffold
Objective: make the backend visible and reviewable.

Suggested structure:

```text
frontend/
  src/
    main.tsx
    App.tsx
    api/
      client.ts
    components/
      UploadForm.tsx
      SegmentRow.tsx
    types/
      translation.ts
    styles.css
  package.json
  vite.config.ts
```

Core tasks:
- Create React + Vite app
- Build upload form
- Add source/target language selectors
- Call backend `POST /translate`
- Render segment rows in two columns
- Set Hebrew side to `dir="rtl"` and `lang="he"`

Success criteria:
- Upload works from browser
- Source and target render side by side
- Hebrew display works correctly

---

## Phase 3 — Better segmentation and structure
Objective: improve quality without changing the product concept.

Core tasks:
- Move from paragraph-only segmentation to sentence-aware segmentation where useful
- Preserve headings and blank-line structure better
- Add basic request logging, timing, and file size limits
- Improve prompt to preserve markdown structure

Possible additions:
- Add filename metadata to response
- Add counts for segments and character lengths

Success criteria:
- Longer files remain readable
- Segment boundaries are more useful for review
- Backend behavior is easier to debug

---

## Phase 4 — Token scaffolding for future alignment
Objective: prepare the backend/frontend contract for interactive review.

Update response shape to include token arrays:

```json
{
  "id": "seg-1",
  "source": "The report is due tomorrow.",
  "target": "הדוח אמור להימסר מחר.",
  "source_tokens": ["The", "report", "is", "due", "tomorrow", "."],
  "target_tokens": [".", "הדוח", "אמור", "להימסר", "מחר"],
  "token_links": []
}
```

Core tasks:
- Tokenize source and target text per segment
- Return tokens in API response
- Update React UI to render tokens instead of raw text blocks

Success criteria:
- Tokens render cleanly
- No alignment yet required
- Frontend is ready for interaction logic

---

## Phase 5 — Side-by-side review UI
Objective: make it feel like a real workflow product.

Core tasks:
- Create a scrollable segment review list
- Label source and target columns clearly
- Add segment IDs or row numbers
- Add room for future controls like edit, split, merge, approve

Possible additions:
- Show simple status badges like `draft`, `reviewed`
- Add search/filter by segment text

Success criteria:
- Reviewer can compare source and target quickly
- UI feels like a review tool, not just raw output

---

## Phase 6 — Click-to-highlight token alignment
Objective: implement the differentiating feature.

Suggested response contract:

```json
{
  "token_links": [
    { "sourceIndex": 1, "targetIndex": 0 },
    { "sourceIndex": 4, "targetIndex": 3 }
  ]
}
```

Future-friendly range format:

```json
{
  "token_links": [
    {
      "sourceStart": 1,
      "sourceEnd": 2,
      "targetStart": 0,
      "targetEnd": 1
    }
  ]
}
```

React suggestion:
- Use a custom token-highlighting UI, not a generic diff viewer
- Render each token as a clickable span
- Store active selection in component or page state
- Highlight linked tokens on the opposite side
- Support hover preview and click-to-lock later

Suggested components:
- `AlignedText.tsx`
- `SegmentRow.tsx`
- shared selection state in `App.tsx`

Success criteria:
- Clicking a token on one side highlights mapped token(s) on the other side
- Hebrew tokens render correctly in RTL
- Imperfect alignment is still useful for review

---

## Phase 7 — Reviewer workflow improvements
Objective: make the app more product-like.

Core tasks:
- Allow manual segment editing
- Add split/merge segment actions
- Add reviewer notes per segment
- Add export back to markdown or HTML

Potential commercial/private features:
- Better alignment algorithms
- Team review and approval workflow
- Glossary/terminology enforcement
- Customer-specific translation memory
- Analytics and audit trail

Success criteria:
- Project feels like a true translation-review workflow
- Public repo still remains understandable and portfolio-friendly

---

## Public vs private split
Suggested public:
- Core FastAPI backend
- React review UI
- Basic bilingual translation
- Basic token highlighting
- README and screenshots

Suggested private:
- Advanced alignment logic
- Premium review tools
- Customer connectors and auth
- Hosted deployment setup
- Business logic for monetization

---

## Resume/interview framing
Possible summary:

> Built a bilingual English ↔ Hebrew translation-review workflow with a FastAPI backend and React frontend. The system ingests text/Markdown files, segments and translates content with a local LLM via Ollama, and presents aligned source/target text side by side with support for interactive token highlighting.
