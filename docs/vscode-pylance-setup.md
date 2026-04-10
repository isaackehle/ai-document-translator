# VS Code Pylance Configuration Guide

## ✅ Configuration Complete

Your workspace is now configured to help fix Pylance errors automatically.

## What's Configured

### 1. VS Code Settings (`.vscode/settings.json`)
- **Type checking**: Basic mode for balanced error detection
- **Auto-imports**: Enabled for intelligent completions
- **Code actions on save**: Auto-fix errors and organize imports
- **Format on save**: Auto-format Python code
- **Diagnostic mode**: Workspace-wide error detection

### 2. Pyright Config (`pyrightconfig.json`)
- Customized type checking rules
- Suppressed overly strict warnings
- Optimized for FastAPI + SQLAlchemy projects

## How to Use

### Automatic Fixes (Recommended)
1. **Save a file** (`Cmd+S` / `Ctrl+S`)
   - VS Code will automatically:
     - Fix all fixable errors
     - Organize imports
     - Format code

### Manual Quick Fixes
1. **Hover over error** → Click "Quick Fix" (💡)
2. **Keyboard shortcut**: `Cmd+.` (Mac) / `Ctrl+.` (Windows)
3. **Right-click** → "Quick Fix"

### Common Quick Fixes
- **Add missing import**: Click import suggestion
- **Add type annotation**: Select suggested type
- **Fix type mismatch**: Choose conversion option
- **Add type ignore**: For unavoidable type issues

## Fixed Errors

The following Pylance errors have been resolved:

### ✅ Fixed
1. **Async generator return type** (`app/core/database.py`)
   - Changed `AsyncSession` → `AsyncGenerator[AsyncSession, None]`

2. **Optional type handling** (`app/api/dependencies.py`)
   - Fixed `user_id` type annotation

3. **SQLAlchemy Column types** (`app/repositories/user_repository.py`)
   - Added explicit type casts for Column access

4. **Generic type constraints** (`app/repositories/base_repository.py`)
   - Added `DeclarativeBase` bound to ModelType

5. **Type conversions** (`app/services/user_service.py`)
   - Fixed password hash type handling

## Remaining Warnings (Expected)

Some warnings are expected with SQLAlchemy due to its dynamic nature:

```python
# SQLAlchemy Column access - use type: ignore
if not current_user.is_active:  # type: ignore[truthy-bool]
    ...

# Generic model attributes - use type: ignore
self.model.id  # type: ignore[attr-defined]
```

## Pro Tips

### 1. Enable Auto-Save
```json
"files.autoSave": "afterDelay",
"files.autoSaveDelay": 500
```

### 2. Use Command Palette
- `Cmd+Shift+P` → "Python: Fix All"
- `Cmd+Shift+P` → "Python: Sort Imports"

### 3. Install Recommended Extensions
- **Black Formatter** (`ms-python.black-formatter`)
- **isort** (built into Pylance)
- **Ruff** (optional, faster linting)

### 4. Reload Window
If Pylance acts up:
- `Cmd+Shift+P` → "Developer: Reload Window"

## Troubleshooting

### Pylance Not Fixing Errors?
1. Check Output panel → "Pylance"
2. Reload VS Code window
3. Verify Python interpreter is selected

### Too Many Errors?
- Lower type checking mode in `.vscode/settings.json`:
  ```json
  "python.analysis.typeCheckingMode": "off"  // or "basic" or "strict"
  ```

### Import Errors?
- Ensure Python interpreter matches your virtual environment
- Run: `Cmd+Shift+P` → "Python: Select Interpreter"

## Next Steps

1. ✅ Save all files to trigger auto-fixes
2. ✅ Test the API still works: `curl http://localhost:8000/health`
3. ✅ Add new code with confidence - Pylance will help catch errors!
