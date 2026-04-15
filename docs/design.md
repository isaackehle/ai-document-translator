---
tags: [ai, llm, aws, translation]
---

# Hebrew Translation Review Workflow - Design Document

## Project Overview

This document outlines the design and architecture of the Hebrew Translation Review Workflow, an AI-powered bilingual English ↔ Hebrew translation tool with side-by-side review capabilities. The project combines local LLM integration with a web-based review interface to enable efficient document translation and quality assurance.

## Project Intent

The primary intent of this project is to upskill AI capabilities while building a practical tool for bilingual document translation and review. The system enables users to:

1. Upload English or Hebrew documents for translation between languages
2. Review translations side-by-side with original text
3. Interactively highlight and compare tokens between source and target languages
4. Build comprehensive review workflows for translation quality assurance

This project serves as both a technical skill-building exercise and a functional tool for working with bilingual documents.

## Architecture Overview

### Core Components

The system follows a two-tier architecture:

**Backend Layer:**
- FastAPI server handling API requests
- Ollama integration for local LLM translation
- PostgreSQL database (optional) for persistence
- Text segmentation and token processing services

**Frontend Layer:**
- React/TypeScript web interface
- Side-by-side document visualization
- Real-time token highlighting and alignment
- Hebrew RTL (Right-To-Left) text rendering support

### AWS Integration Framework

Based on the AWS refresh plan, this project can be extended to leverage AWS services:

**Current Local Implementation:**
- FastAPI backend with Ollama LLM integration
- File-based operations and local storage
- Simple in-memory state management

**AWS Extension Points:**
- **Storage**: S3 for document uploads and translated outputs
- **Queue**: SQS for background job processing
- **Compute**: Lambda or ECS containers for translation workers
- **Database**: RDS PostgreSQL for job metadata and status tracking
- **Secrets**: Secrets Manager or SSM Parameter Store
- **Observability**: CloudWatch logs and basic metrics/alarms
- **Containers**: Docker for API and worker

## Local Testing and Development Tools

To enable comprehensive testing and validation before AWS migration, the system supports local AWS service mocking:

### Local AWS Service Mocking

**LocalStack** - Provides local emulation of key AWS services:
- S3-compatible storage for document handling
- SQS queue service for job processing
- Lambda function execution environment
- RDS-compatible database for metadata storage

**boto3 + moto** - Python library for AWS service mocking:
- Mocks S3, SQS, Lambda operations
- Enables unit and integration testing without AWS credentials
- Supports local development with realistic service behavior

### Local Development Environment

The system supports local testing with:
- **minio** - S3-compatible local storage for document uploads
- **localstack** - Full AWS service simulation in development
- **pytest + moto** - Comprehensive test suite with mocked AWS services
- **Docker containers** - Isolated local testing environments

## Technical Design

### Backend Architecture

#### API Endpoints
- `/health` - System health check
- `/api/v1/translate` - Translation endpoint with language validation

#### Core Services
1. **Segmentation Service**:
   - Paragraph-based text segmentation
   - Markdown-aware content handling
   - Support for custom segmentation strategies

2. **Translation Service**:
   - Ollama-based LLM integration
   - Language pair validation (en↔he)
   - Error handling and retry mechanisms

3. **Data Management**:
   - Translation response formatting
   - Segment tracking and ID management

### Frontend Architecture

#### UI Components
1. **Upload Form**:
   - Language selection (English/Hebrew)
   - Text input area with validation
   - Translation trigger

2. **Review Interface**:
   - Side-by-side text display
   - RTL support for Hebrew text rendering
   - Token-level highlighting capabilities

3. **Segment Display**:
   - Individual paragraph/unit display
   - Segment identification and metadata
   - Status indicators (draft/completed)

### Data Flow

1. **Document Upload**: User provides text in source language
2. **Segmentation**: Text is broken into manageable units (paragraphs)
3. **Translation**: Each segment sent to Ollama for translation
4. **Rendering**: Original and translated segments displayed side-by-side
5. **Review**: Users can interact with segments and tokens

## AWS Integration Design

### Event-Driven Architecture (as per AWS prep plan)

The system can be extended to follow AWS event-driven patterns:

1. **Document Upload**:
   - Client uploads document via API
   - Backend stores file in S3 and writes job to PostgreSQL

2. **Job Processing**:
   - SQS message enqueued with job metadata
   - Worker (Lambda or container) consumes job, processes translation
   - Results stored back in S3, metadata updated in PostgreSQL

3. **API Access**:
   - Status polling and result retrieval
   - Metadata query endpoints

### AWS Service Mapping

| AWS Service         | Usage in System                                    |
| ------------------- | -------------------------------------------------- |
| **S3**              | Store source documents and translated outputs      |
| **SQS**             | Queue translation jobs for asynchronous processing |
| **Lambda/ECS**      | Execute translation workloads                      |
| **RDS/PostgreSQL**  | Store job metadata and status tracking             |
| **Secrets Manager** | Secure storage of configuration and API keys       |
| **CloudWatch**      | Logging, metrics, and observability                |

### Scalability Considerations

The current design supports local operation but can scale to:
- Handle multiple concurrent translation requests
- Process large documents through batch jobs
- Maintain state for complex review workflows

## Implementation Plan Integration

### Phase 1-2: Core Foundation
- Backend scaffolding with FastAPI and Ollama integration
- Frontend React interface for translation display
- Basic text segmentation and translation services

### Phase 3-4: Enhanced Features
- Improved segmentation strategies (sentence-aware)
- Token-level processing and display capabilities
- Enhanced UI with better text rendering and alignment

### Phase 5-7: Review Workflow
- Side-by-side document review interface
- Token highlighting and alignment features
- Complete translation workflow for quality assurance

## AWS Extension Roadmap

### Phase 1: Foundation (Current)
- Local FastAPI + Ollama implementation
- Basic React frontend with RTL support

### Phase 2: AWS Integration (Planned)
- S3 integration for document storage
- SQS queue for job processing
- Lambda or ECS containers for translation workers

### Phase 3: Production Ready (Future)
- RDS PostgreSQL for job metadata
- Secrets Manager for configuration
- CloudWatch for observability and metrics

## Key Design Principles

1. **Modular Architecture**: Services are designed to be independently replaceable
2. **Extensible Design**: Easy to integrate new features and services
3. **User-Centric UI**: Focus on effective translation review workflows
4. **AWS-Ready**: Design supports eventual migration to cloud services
5. **Language-Aware**: Special handling for Hebrew RTL text rendering
6. **Test-Driven Development**: Local mocking enables comprehensive testing

## Technology Stack

### Backend
- FastAPI (Python)
- Ollama (local LLM)
- PostgreSQL (optional)
- HTTPX for API calls

### Frontend
- React with TypeScript
- Vite for build tooling
- CSS Grid/Flexbox for layout

### AWS Services (Planned)
- S3 for storage
- SQS for queueing
- Lambda/ECS for compute
- RDS/PostgreSQL for persistence
- Secrets Manager for configuration

### Local Testing Tools
- LocalStack for AWS service simulation
- moto library for boto3 mocking
- minio for S3-compatible local storage

## Security Considerations

1. **Data Handling**: Sensitive documents should be handled securely
2. **API Security**: Input validation and rate limiting
3. **Secrets Management**: Configuration should not be hard-coded
4. **Access Control**: Authentication and authorization (future enhancement)

## Future Enhancements

1. **Multi-language Support**: Extend beyond English-Hebrew pairs
2. **Advanced Review Tools**: Markdown support, syntax highlighting
3. **Collaborative Features**: Multiple reviewers, comments, versioning
4. **Full AWS Migration**: Complete cloud-native implementation
5. **Performance Optimization**: Caching, parallel processing, better tokenization

## References

- [[Hebrew Translation Review Workflow Implementation Plan]]
