# ai-document-translator

AI Document translator; AI Pipeline demo

## 📚 Documentation

### Learning & Planning Documents

- **[docs/project-overview.md](docs/project-overview.md)** - AI-generated workflow plan created with Perplexity to explore the ins and outs of building a simple AI translation tool. This document breaks down all the pieces, jargon, and considerations involved in creating an AI-powered document translation pipeline. Great for understanding the landscape and terminology.

- **[docs/vscode-pylance-setup.md](docs/vscode-pylance-setup.md)** - Complete guide to configuring VS Code and Pylance for Python type checking, including how to handle false positives from SQLAlchemy and Alembic.

### Project Documentation

All project documentation is stored in the `docs/` directory.

## FastAPI Application Scaffold

This project includes a production-ready FastAPI application scaffold with:

- Async/await support with SQLAlchemy and PostgreSQL
- JWT authentication with bcrypt password hashing
- Repository and service layer patterns
- Pydantic validation for requests/responses
- Alembic database migrations
- Comprehensive API documentation

See the FastAPI application structure in the `app/` directory.

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
