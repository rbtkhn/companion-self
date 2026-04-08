# Inference modes

The companion stack supports three **inference modes** that control where the LLM runs. This axis is **orthogonal** to runtime modes (`adjunct_runtime` / `primary_runtime` / `portable_bundle_only` in architecture.md), which control what gets packaged for export.

---

## Modes

| Mode | Where inference runs | When to use |
|------|---------------------|-------------|
| **`cloud`** | Remote API (OpenAI, Anthropic, etc.) | Default. Full capability, requires network and API key. |
| **`local-first`** | On-device model (Google AI Edge, Ollama, etc.) | Privacy-first, zero-cost, offline. Escalates to cloud only with explicit user approval. |
| **`hybrid`** | Local for most tasks, cloud for heavy ones | Balanced. Local handles chat and lightweight reasoning; cloud handles web search, large context, low-confidence tasks. |

All three modes preserve the same governance guarantees: Seed Phase, Change Review, Authority Map, observability, and contradiction preservation remain mandatory regardless of where inference happens.

---

## Configuration

Set in **`runtime_config.json`** under the **`inference`** block:

```json
"inference": {
  "mode": "cloud",
  "local": {
    "provider": "google_ai_edge",
    "model": "gemini-nano-4b",
    "fallback": "gemini-nano-2b",
    "context_budget_tokens": 32000
  },
  "cloud": {
    "provider": "openai",
    "model": "gpt-4o",
    "analyst_model": "gpt-4o-mini"
  },
  "hybrid_escalation": {
    "require_user_approval": true,
    "escalation_triggers": ["web_search", "large_context", "low_confidence"]
  }
}
```

| Field | Purpose |
|-------|---------|
| **`mode`** | Active inference mode: `"cloud"` \| `"local-first"` \| `"hybrid"`. |
| **`local.provider`** | Local inference backend: `"google_ai_edge"` \| `"ollama"`. |
| **`local.model`** | Primary local model identifier. |
| **`local.fallback`** | Smaller model to use if the primary is unavailable or device is constrained. |
| **`local.context_budget_tokens`** | Max tokens the local model can handle. Drives prompt compression. |
| **`cloud.provider`** | Cloud inference backend: `"openai"` \| `"anthropic"`. |
| **`cloud.model`** | Primary cloud model for Voice chat. |
| **`cloud.analyst_model`** | Separate model for analyst/governance tasks (can be cheaper). |
| **`hybrid_escalation.require_user_approval`** | If `true`, the companion must surface an approval dialog before escalating to cloud. |
| **`hybrid_escalation.escalation_triggers`** | List of conditions that trigger cloud escalation: `"web_search"`, `"large_context"`, `"low_confidence"`. |

---

## Env-var override (grace-mar instance)

For the grace-mar bot, inference mode can also be set via environment variables (useful for Render, Docker, CI):

| Env var | Overrides | Default |
|---------|-----------|---------|
| `LLM_PROVIDER` | `inference.*.provider` | `openai` |
| `OPENAI_MODEL` | `inference.cloud.model` | `gpt-4o` |
| `OPENAI_ANALYST_MODEL` | `inference.cloud.analyst_model` | `gpt-4o-mini` |
| `EDGE_MODEL` | `inference.local.model` | `gemini-nano-4b` |
| `OLLAMA_MODEL` | `inference.local.model` (when provider is ollama) | — |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |

Env vars take precedence over `runtime_config.json` when both are present.

---

## Hybrid escalation protocol

In `local-first` or `hybrid` mode, certain tasks may exceed the local model's capability. The escalation flow:

1. The provider detects an escalation trigger (e.g. user asks for a web search, context exceeds `context_budget_tokens`, or model confidence is low).
2. If `require_user_approval` is `true`, the companion surfaces a clear message: *"This requires internet access. Allow one-time cloud escalation?"*
3. On approval, the request routes to the cloud provider for that single call.
4. The response is tagged `execution_mode: hybrid` in observability logs.
5. Without approval, the companion answers with its local capability or abstains.

Cloud escalation is governed by the `cloud_escalation: review_required` surface in `config/authority-map.json`.

---

## Relation to runtime modes

| Runtime mode | Inference mode | Typical use |
|-------------|---------------|-------------|
| `primary_runtime` | `cloud` | Standard deployment (Telegram bot on Render) |
| `primary_runtime` | `local-first` | Privacy-first desktop companion (Python + Ollama) |
| `portable_bundle_only` | `local-first` | Fully offline export (future mobile app) |
| `adjunct_runtime` | `hybrid` | Companion supports another app, local when possible |

The two axes are independent. Changing inference mode does not affect what gets packaged; changing runtime mode does not affect where inference runs.

---

## Context budget and prompt compression

Local models have smaller context windows than cloud models. When `inference.mode` is `local-first` or `hybrid`, the system uses `context_budget_tokens` to:

- Select a compressed system prompt (shorter IX-A/B/C summaries, no lookup/rephrase scaffolding)
- Limit conversation history depth
- Prioritize recent evidence in retrieval

The `scripts/compress_system_prompt.py` script generates compressed prompt variants. See `bot/prompt_compressed.py` for the grace-mar instance output.
