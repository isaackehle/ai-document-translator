# AWS Implementation Plan for Hebrew Translation Review Workflow

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

## Project Overview

This document outlines the AWS implementation plan for the Hebrew Translation Review Workflow, focusing on the integration of AWS services as separate deliverable phases.

## Core Requirements

Based on the AWS refresh plan, this implementation focuses on:

1. **Event-driven architecture** using S3, SQS, and Lambda
2. **Document translation pipeline** with local LLM as initial implementation  
3. **Production-ready AWS patterns** for Python backend systems
4. **Local testing capabilities** before cloud migration

## Phase Structure

### Phase 0: AWS Project Setup and Local Testing
**Goal**: Establish local development environment with AWS service mocking

### Phase 1: AWS Service Integration - S3 and SQS
**Goal**: Implement S3 storage and SQS queue services for document handling

### Phase 2: AWS Service Integration - Lambda Workers
**Goal**: Create Lambda workers for document translation processing

### Phase 3: AWS Service Integration - Database and Secrets
**Goal**: Implement RDS PostgreSQL and Secrets Manager for metadata storage

### Phase 4: AWS Service Integration - Observability
**Goal**: Add CloudWatch logging and monitoring capabilities

### Phase 5: Full AWS Migration and Testing
**Goal**: Complete migration to production AWS services with end-to-end testing

---

## Phase 0: AWS Project Setup and Local Testing

**Goal**: Establish local development environment with AWS service mocking

### Status
✅ Complete - Local testing infrastructure established

### Tasks Completed:
- Created local development environment with Docker containers
- Configured LocalStack for S3, SQS, and Lambda service mocking
- Integrated minio for local S3-compatible storage
- Implemented moto library for boto3 service mocking in tests
- Set up pytest configuration with local AWS services

### Local Testing Tools:
- **LocalStack**: Full AWS service simulation in development
- **minio**: S3-compatible local storage for document handling
- **moto**: boto3 library for AWS service mocking
- **Docker containers**: Isolated local testing environments

### Success Criteria:
- Local development environment ready for AWS integration
- All AWS services mocked locally with realistic behavior
- Testing framework supports local and cloud environments

---

## Phase 1: AWS Service Integration - S3 and SQS

**Goal**: Implement S3 storage and SQS queue services for document handling

### Status
❌ Incomplete - Requires implementation

### Tasks:
- [ ] **S3 Integration Setup**
  - Configure S3 buckets for source and translated documents
  - Implement document upload/download operations
  - Add local minio integration for development testing

- [ ] **SQS Queue Implementation**  
  - Create SQS queues for job processing
  - Implement queue message publishing and consumption
  - Add local SQS simulation using LocalStack

### Implementation Approach:
1. **S3 Integration**:
   - Create S3 client with localstack/minio configuration
   - Implement document storage and retrieval operations
   - Add error handling for S3 service failures

2. **SQS Integration**:
   - Create SQS queue with proper naming conventions
   - Implement job message format and processing logic
   - Add retry logic and dead-letter queue handling

### Success Criteria:
- S3 storage works for document uploads
- SQS queues can queue translation jobs
- Local testing with mocked AWS services functions correctly

---

## Phase 2: AWS Service Integration - Lambda Workers

**Goal**: Create Lambda workers for document translation processing

### Status
❌ Incomplete - Requires implementation

### Tasks:
- [ ] **Lambda Function Development**
  - Create Lambda handler for translation job processing
  - Implement job message parsing and validation
  - Add local Lambda simulation capability

- [ ] **Translation Worker Integration**
  - Connect Lambda to S3 for document retrieval
  - Implement translation API call to local Ollama (or Bedrock)
  - Add result storage back to S3

### Implementation Approach:
1. **Worker Design**:
   - Create Lambda function with proper timeout handling
   - Implement idempotent processing logic
   - Add proper error handling and retry mechanisms

2. **Integration with Existing System**:
   - Configure Lambda to read from SQS queue
   - Implement result storage back to S3 with metadata
   - Add proper logging and metrics collection

### Success Criteria:
- Lambda function processes translation jobs successfully
- Integration with S3 and SQS works in local environment
- Error handling and retry logic functions properly

---

## Phase 3: AWS Service Integration - Database and Secrets

**Goal**: Implement RDS PostgreSQL and Secrets Manager for metadata storage

### Status
❌ Incomplete - Requires implementation

### Tasks:
- [ ] **PostgreSQL Database Setup**
  - Configure RDS PostgreSQL instance for job metadata
  - Create database schema for job tracking and status
  - Implement connection pooling and proper configuration

- [ ] **Secrets Management Integration**
  - Configure AWS Secrets Manager for API keys and credentials
  - Implement secure credential loading in local environment
  - Create SSM Parameter Store integration as alternative

### Implementation Approach:
1. **Database Design**:
   - Create jobs table with proper indexing
   - Implement status tracking and transition logic
   - Add proper constraints and data validation

2. **Security Implementation**:
   - Configure Secrets Manager with proper IAM policies
   - Implement secure credential loading in Lambda workers
   - Add environment variable fallback for local development

### Success Criteria:
- PostgreSQL database stores job metadata correctly
- Secrets Manager securely handles configuration
- Local development environment supports both local and AWS configurations

---

## Phase 4: AWS Service Integration - Observability

**Goal**: Add CloudWatch logging and monitoring capabilities

### Status
❌ Incomplete - Requires implementation

### Tasks:
- [ ] **Logging Configuration**
  - Implement structured CloudWatch logging
  - Add custom metrics and alarms for system health
  - Configure log retention and monitoring

- [ ] **Monitoring Implementation**
  - Set up CloudWatch metrics for job processing
  - Create dashboard for system performance monitoring
  - Implement alerting for error conditions

### Implementation Approach:
1. **Logging Framework**:
   - Implement structured logging with proper context
   - Add error tracking and exception handling
   - Configure log levels for different environments

2. **Monitoring Setup**:
   - Create CloudWatch metrics for job success/failure rates
   - Set up dashboard with key performance indicators
   - Implement alerting for system degradation

### Success Criteria:
- Comprehensive logging in both local and AWS environments
- System monitoring dashboard available
- Alerting configured for critical system failures

---

## Phase 5: Full AWS Migration and Testing

**Goal**: Complete migration to production AWS services with end-to-end testing

### Status
❌ Incomplete - Requires implementation

### Tasks:
- [ ] **Production Migration**
  - Deploy Lambda functions to AWS
  - Migrate database to production RDS instance
  - Configure proper IAM roles and permissions

- [ ] **End-to-End Testing**
  - Validate complete document translation pipeline
  - Test error handling and recovery scenarios
  - Perform load testing with realistic workloads

### Implementation Approach:
1. **Deployment Strategy**:
   - Use Infrastructure-as-Code (Terraform or CloudFormation)
   - Implement CI/CD pipeline for AWS deployments
   - Configure proper environment variables and configuration

2. **Testing Strategy**:
   - Comprehensive end-to-end testing of full pipeline
   - Validate performance and scalability in production
   - Document system behavior under various load conditions

### Success Criteria:
- Complete migration to production AWS services
- End-to-end pipeline works correctly in cloud environment
- All tests pass with realistic production workloads

---

## Testing Strategy

### Local Development Testing:
```bash
# Test local environment setup
docker-compose up -d localstack minio

# Run tests with mocked AWS services
pytest tests/ --aws-mock

# Verify all services are working locally
curl http://localhost:4566/health
```

### Production Migration Testing:
```bash
# Test actual AWS service integration
terraform apply -auto-approve

# Validate end-to-end pipeline
curl https://api.example.com/translate \
  -H "Content-Type: application/json" \
  -d '{"source_lang": "en", "target_lang": "he", "text": "Hello world"}'
```

### Manual Testing Checklist:
- [ ] Local development environment configured
- [ ] AWS services mocked successfully in local environment  
- [ ] S3 storage works for document uploads
- [ ] SQS queue processing functions correctly
- [ ] Lambda workers process jobs successfully
- [ ] Database stores job metadata correctly
- [ ] Secrets manager loads credentials properly
- [ ] CloudWatch logging works in local and AWS environments
- [ ] Production deployment completes successfully

---

## Deployment Notes

### Local Development:
```bash
# Start local AWS services for testing
docker-compose up -d localstack minio

# Run tests with mocked services  
pytest tests/ --aws-mock --verbose

# Verify local setup
curl http://localhost:4566/health
```

### Production Deployment:
```bash
# Deploy to AWS using infrastructure-as-code
terraform init
terraform apply -auto-approve

# Validate production environment
aws cloudformation describe-stacks --stack-name translation-pipeline
```

### AWS Services Configuration:
```bash
# S3 bucket setup (local and production)
aws s3 mb s3://translation-source-bucket --region us-east-1

# SQS queue setup (local and production)
aws sqs create-queue --queue-name translation-job-queue

# Lambda function deployment
aws lambda create-function --function-name translation-worker \
  --runtime python3.9 --handler lambda_function.lambda_handler \
  --role arn:aws:iam::123456789012:role/translation-worker-role
```

---

## References

- [[Hebrew Translation Review Workflow Implementation Plan]]
- [[AWS Refresh Plan for Revalia Prep]]