"""Thin per-provider adapters. Each one returns a ModelResponse with the fields
needed for reproducibility and cost tracking: raw text, token usage as reported by
the provider's own API (never a local tokenizer, see docs/methodology.md), and
latency. Add a new provider by adding one function and registering it in PROVIDERS.
"""

import time
from dataclasses import dataclass


@dataclass
class ModelResponse:
    text: str
    input_tokens: int
    output_tokens: int
    latency_ms: int


def call_anthropic(model, system_prompt, user_prompt, temperature=1.0, max_tokens=4096):
    import anthropic

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    start = time.monotonic()
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    latency_ms = int((time.monotonic() - start) * 1000)
    text = "".join(block.text for block in response.content if block.type == "text")
    return ModelResponse(
        text=text,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
        latency_ms=latency_ms,
    )


PROVIDERS = {
    "anthropic": call_anthropic,
}
