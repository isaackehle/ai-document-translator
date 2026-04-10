---
tags: [ai, llm, local, ollama, lmstudio, continue, cline, opencode]
---

# AI Tools Configuration (Continue, Cline, OpenCode)

Configuration and setup guide for local AI coding assistants including Continue, Cline, and OpenCode with Ollama and LM Studio.

## Configuration Overview

### Continue.dev Configuration
- **File**: `~/continue.yaml` or `~/.continue/config.yaml`
- **Provider**: LM Studio
- **Endpoint**: http://127.0.0.1:1234/v1

### OpenCode Configuration
- **File**: `~/.config/opencode/opencode.jsonc`
- **Provider**: LM Studio
- **Endpoint**: http://127.0.0.1:1234/v1

## Model Management

### Ollama Models
To pull models for Ollama:

```shell
# Pull Qwen Coder models
ollama pull qwen3.2-coder:7b
ollama pull qwen3.2-coder:1.5b
ollama pull nomic-embed-text:latest

# Pull Phi-4 model
ollama pull phi4

# Pull Gemma 3 model
ollama pull gemma3:12b

# Pull DeepSeek Coder model
ollama pull deepseek-coder:6.7b

# Pull Codestral model
ollama pull codestral:22b
```

### LM Studio Models
To pull models for LM Studio:

```shell
# Search and download models via LM Studio UI:
# - Open LM Studio App
# - Go to Models tab → + icon → Search for model name (e.g., qwen2.5-coder:7b)
# - Click download and wait for completion

# Common Qwen models for LM Studio:
# - qwen/qwen3-coder-30b@4bit
# - qwen2.5-coder:7b
# - qwen2.5-coder:1.5b
# - qwen/qwen3.5-35b-a3b
# - qwen/qwen3.5-9b
```

## Ollama Model List

To see available models in Ollama:

```shell
# List all downloaded models
ollama list

# Get model tags from API (if Ollama server is running)
curl http://localhost:11434/api/tags
```

## LM Studio Model List

To see available models in LM Studio:

```shell
# Check models via API (if LM Studio server is running)
curl http://localhost:1234/v1/models

# Models available in LM Studio UI:
# - qwen/qwen3-coder-30b@4bit
# - qwen2.5-coder:7b
# - qwen2.5-coder:1.5b
# - deepseek/deepseek-r1-0528-qwen3-8b
# - qwen/qwen3.5-35b-a3b
# - qwen/qwen3.5-9b
```

## Continue Configuration Example

```yaml
name: "Qwen Models Configuration"
version: "1.0.0"
schema: "v1"

models:
  # Agent model for general use
  - name: "qwen/qwen3-coder-30b@4bit"
    provider: "lmstudio"
    model: "qwen/qwen3-coder-30b@4bit"
    roles:
      - "chat"
      - "edit"
      - "apply"
      - "summarize"
  
  # Chat model (same as agent for consistency)
  - name: "qwen/qwen3-coder-30b@4bit"
    provider: "lmstudio"
    model: "qwen/qwen3-coder-30b@4bit"
    roles:
      - "chat"
  
  # Autocomplete model for code completion
  - name: "qwen2.5-coder-1.5b"
    provider: "lmstudio"
    model: "qwen2.5-coder-1.5b"
    roles:
      - "autocomplete"
  
  # Apply model for code application
  - name: "fast-apply-1.5b-v1.0_gguf"
    provider: "lmstudio"
    model: "fast-apply-1.5b-v1.0_gguf"
    roles:
      - "apply"
  
  # Embedding model for semantic search
  - name: "text-embedding-nomic-embed-text-v1.5"
    provider: "lmstudio"
    model: "text-embedding-nomic-embed-text-v1.5"
    roles:
      - "embed"
  
  # Reranking model (using zerank-2 as specified)
  - name: "zerank-2"
    provider: "lmstudio"
    model: "zerank-2"
    roles:
      - "rerank"
```

## OpenCode Configuration Example

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "lmstudio": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LM Studio (Local)",
      "options": {
        "baseURL": "http://127.0.0.1:1234/v1"
      },
      "models": {
        "qwen/qwen3-coder-30b@4bit": {
          "name": "Qwen 3 Coder 30B 4bit"
        },
        "deepseek/deepseek-r1-0528-qwen3-8b": {
          "name": "DeepSeek R1 Qwen3 8B"
        },
        "qwen/qwen3.5-35b-a3b": {
          "name": "Qwen 3.5 35B A3B"
        },
        "qwen/qwen3.5-9b": {
          "name": "Qwen 3.5 9B"
        }
      }
    }
  },
  "default_agent": "code",
  "model": "lmstudio/qwen/qwen3-coder-30b@4bit",
  "small_model": "lmstudio/qwen/qwen3.5-9b",
  "permission": {
    "read": "allow",
    "glob": "allow",
    "grep": "allow",
    "list": "allow",
    "webfetch": "allow",
    "edit": "ask",
    "bash": "ask"
  }
}
```

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
```