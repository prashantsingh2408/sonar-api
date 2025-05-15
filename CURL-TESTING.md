# Perplexity API Test Cases

## Available Models Overview

### Search Models (with web search)
- sonar (128k context) - Lightweight search model, best for quick factual queries
- sonar-pro (200k context) - Advanced search model, best for complex queries and follow-ups
  - Max output tokens: 8k

### Reasoning Models (with web search)
- sonar-reasoning (128k context) - Fast reasoning model with Chain of Thought
- sonar-reasoning-pro (128k context) - Premier reasoning model powered by DeepSeek R1

### Research Models (with web search)
- sonar-deep-research (128k context) - Expert research model for comprehensive reports
  - Note: May take 30+ minutes for complex tasks

### Offline Models (no web search)
- r1-1776 (128k context) - Offline chat model for creative content
  - Note: Post-trained for uncensored, unbiased, and factual information

## Model Performance Specifications
- Context Windows:
  - sonar: 128k tokens
  - sonar-pro: 200k tokens
  - sonar-reasoning: 128k tokens
  - sonar-reasoning-pro: 128k tokens
  - sonar-deep-research: 128k tokens
  - r1-1776: 128k tokens

## Complete API Request Examples

### 1. Search Models

#### Sonar - Basic Query
```bash
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "sonar",
    "messages": [
      {
        "role": "user",
        "content": "What is the latest news about AI?"
      }
    ]
  }'
```

#### Sonar Pro - Complex Query with Follow-up
```bash
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "sonar-pro",
    "messages": [
      {
        "role": "system",
        "content": "You are a research expert providing detailed analysis."
      },
      {
        "role": "user",
        "content": "What are the latest developments in quantum computing?"
      },
      {
        "role": "assistant",
        "content": "[Previous detailed analysis]"
      },
      {
        "role": "user",
        "content": "Based on these developments, what are the most promising applications?"
      }
    ],
    "temperature": 0.3,
    "max_tokens": 4000
  }'
```

### 2. Reasoning Models

#### Sonar Reasoning - Step-by-Step Analysis
```bash
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "sonar-reasoning",
    "messages": [
      {
        "role": "system",
        "content": "You are a logical reasoning assistant that shows your thinking process step by step."
      },
      {
        "role": "user",
        "content": "Explain how blockchain technology works, showing your reasoning process"
      }
    ],
    "temperature": 0.5
  }'
```

#### Sonar Reasoning Pro - Complex Analysis
```bash
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "sonar-reasoning-pro",
    "messages": [
      {
        "role": "system",
        "content": "You are an expert analyst providing detailed reasoning with Chain of Thought."
      },
      {
        "role": "user",
        "content": "Analyze the potential impact of artificial general intelligence on society, showing your reasoning process"
      }
    ],
    "temperature": 0.3,
    "max_tokens": 2000
  }'
```

### 3. Research Models

#### Sonar Deep Research - Comprehensive Analysis
```bash
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "sonar-deep-research",
    "messages": [
      {
        "role": "system",
        "content": "You are a research expert conducting comprehensive analysis."
      },
      {
        "role": "user",
        "content": "Research and analyze the impact of climate change on global agriculture over the next decade"
      }
    ],
    "temperature": 0.2,
    "max_tokens": 4000
  }'
```

### 4. Offline Models

#### R1-1776 - Creative Content
```bash
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "r1-1776",
    "messages": [
      {
        "role": "system",
        "content": "You are a creative writing assistant."
      },
      {
        "role": "user",
        "content": "Write a short story about a future where AI and humans coexist peacefully"
      }
    ],
    "temperature": 0.8,
    "max_tokens": 1000
  }'
```

### 5. Advanced Features

#### Streaming Response
```bash
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --header 'Accept: text/event-stream' \
  --data '{
    "model": "sonar",
    "messages": [
      {
        "role": "user",
        "content": "Explain the concept of quantum computing"
      }
    ],
    "stream": true
  }'
```

## Model Selection Guide
- sonar: Best for quick factual queries, summaries, and current events
- sonar-pro: Best for complex queries, follow-ups, and detailed analysis
- sonar-reasoning: Best for quick problem-solving with step-by-step reasoning
- sonar-reasoning-pro: Best for complex reasoning tasks with detailed analysis
- sonar-deep-research: Best for comprehensive research and detailed reports
- r1-1776: Best for creative content generation without web search

## Common Parameters
- temperature: Controls randomness (0.0 to 1.0)
- max_tokens: Maximum length of response
- top_p: Nucleus sampling parameter
- stream: Enable streaming response
- system: Define model behavior
- messages: Array of conversation messages

## Notes
- Replace `YOUR_API_KEY` with your actual Perplexity API key
- All models support streaming responses (`stream: true`)
- sonar-pro has a max output token limit of 8k
- sonar-reasoning and sonar-reasoning-pro provide Chain of Thought (CoT) responses
- sonar-deep-research may take 30+ minutes for complex tasks
- r1-1776 is an offline model that does not use web search
- For detailed model information, visit: https://docs.perplexity.ai/models/model-cards