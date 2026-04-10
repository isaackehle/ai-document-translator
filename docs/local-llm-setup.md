---
tags: [ai, llm, local, ollama, lmstudio, continue, cline]
---

# Local LLM Setup for AI Coding Assistants (Ollama + LM Studio)

This guide covers configuring Continue and Cline AI coding assistants to use local LLMs via **Ollama** or **LM Studio** for private, cost-effective coding assistance.

## Table of Contents
- [LM Studio Setup](#lm-studio-setup)
- [Continue Configuration](#continue-configuration)
- [Cline Configuration](#cline-configuration)
- [Recommended Models](#recommended-models)
- [Verification](#verification)

---


## LM Studio Setup

LM Studio is a graphical interface for local LLMs with integrated UI and chat.

### Installation

- Mac/Windows/Linux: Download from https://lmstudio.ai
- Run the application and follow the onboarding wizard

### Configuration

1. Install Model:

  - Click Models tab → + icon → Search for model (e.g., qwen2.5-coder:7b)
  - Click download and wait for completion

2. Start Server:

```shell
# Open LM Studio App
# Go to "Servers" tab → Click ▶️ Run / Start server
# Default port: 1234
```
3. Access API Endpoint:

  - URL: http://localhost:1234/v1
  - Keep server running in background or set to launch on startup via app settings

## Continue Configuration

Continue is an open-source AI code assistant that integrates with VS Code and JetBrains IDEs.

### Installation

```shell
# Install via VS Code marketplace
# In VS Code: Extensions → Search for "Continue" → Install
```

### Configuration for Ollama OR LM Studio

   1. Open Continue settings (click the Continue icon in sidebar → Settings)
   2. Under "Models", select "Ollama" or "OpenAI Compatible Provider"
   3. Set endpoint and choose provider below:

#### For Ollama:

  - Provider: Ollama
  - Endpoint: http://localhost:11434
  - Model: qwen2.5-coder:7b

#### For LM Studio:

  - Provider: OpenAI Compatible
  - Endpoint: http://localhost:1234/v1
  - API Key: Blank or none
  - Model ID: Model name from app (e.g., qwen2.5-coder:7b)

## Configuration via ~/.continue/config.yaml:

```yaml
name: Local Only
version: 1.0.0
schema: v1
  - name: Nomic Embed
    provider: lmstudio
    model: nomic-embed-text-v2-moe-GGUF:latest
    roles:
      - embed
    autocompleteOptions:
      debounceDelay: 200
      maxPromptTokens: 1024
      onlyMyCode: true
      maxSuffixPercentage: 0.2
      prefixPercentage: 0.3
  - name: LM Studio - Autodetect
    provider: lmstudio
    model: AUTODETECT
    apiBase: http://localhost:1234/v1/
  - name: Qwen2.5-Coder-1.5B-Q8_0-GGUF
    provider: lmstudio
    model: ggml-org/Qwen2.5-Coder-1.5B-Q8_0-GGUF
    apiBase: http://localhost:1234/v1
    roles:
      - autocomplete
    capabilities:
      - tool_use
    defaultCompletionOptions:
      contextLength: 8192
      temperature: 0.1
    autocompleteOptions:
      debounceDelay: 200
      maxPromptTokens: 1024
      onlyMyCode: true
      maxSuffixPercentage: 0.2
      prefixPercentage: 0.3
  - name: Qwen2.5 Coder 7B
    provider: lmstudio
    model: qwen2.5-coder:7b
    apiBase: http://localhost:1234/v1
    roles: [chat, edit]
    capabilities:
      - tool_use
    defaultCompletionOptions:
      contextLength: 8192
      temperature: 0.5
    autocompleteOptions:
      debounceDelay: 200
      maxPromptTokens: 1024
      onlyMyCode: true
      maxSuffixPercentage: 0.2
      prefixPercentage: 0.3
  - name: GPT-OSS 20B
    provider: lmstudio
    model: openai/gpt-oss-20b
    apiBase: http://localhost:1234/v1
    roles: [apply]
    capabilities:
      - tool_use
    defaultCompletionOptions:
      contextLength: 8192
      temperature: 0.5
    autocompleteOptions:
      debounceDelay: 200
      maxPromptTokens: 1024
      onlyMyCode: true
      maxSuffixPercentage: 0.2
      prefixPercentage: 0.3
```

### Roles

| Role         | Purpose                 | Notes                              |
| ------------ | ----------------------- | ---------------------------------- |
| chat         | Main chat / Q&A         | Works on both Ollama & LM Studio   |
| edit         | Inline edit suggestions | Best with strong models (≥7B)      |
| apply        | Apply /diffs to files   | Requires explicit confirmation     |
| autocomplete | Tab completion          | Best with smaller models (1.5B–3B) |


## Recommended Models

### For Ollama:

```shell
ollama pull qwen2.5-coder:7b
ollama pull qwen2.5-coder:1.5b-base
ollama pull nomic-embed-text:latest
```

### For LM Studio:

- Search and download models from the UI
- Recommended sizes: qwen2.5-coder:7b, qwen2.5-coder:1.5b, nomic-embed-text

## Verification

### Ollama Health Check:

```shell
ollama list
curl http://localhost:11434/api/tags
```

### LM Studio Health Check:

```shell
curl http://localhost:1234/v1/models
```

### Continue Test:

1. Open VS Code
2. Trigger chat command (e.g., @explain this)
3. Verify response comes from local model

## Troubleshooting

### Slow Responses

- Model might be too large for your hardware
- Consider smaller models like qwen2.5-coder:1.5b for quick tasks

### Firewall Issues

- Ensure ports 11434 (Ollama) and 1234 (LM Studio) are open
- Check system firewall settings or proxy configuration

### Memory Issues

- Ollama defaults to using available RAM
- Adjust via OLLAMA_NUM_GPU or LM Studio model quantization settings