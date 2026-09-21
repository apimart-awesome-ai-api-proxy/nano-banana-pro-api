# Nano Banana Pro API (gemini-3-pro-image-preview)

<!-- conv-kit:v1 -->

<p align="center">
  <img src="assets/badges/price.svg" alt="observed unit price"> <img src="assets/badges/billing.svg" alt="billing model"> <img src="assets/badges/compat.svg" alt="OpenAI-compatible endpoint">
</p>

<p align="center">
  <img src="assets/01-product-hero-perfume.jpg" width="820" alt="Nano Banana Pro (gemini-3-pro-image-preview) output generated through APIMart">
</p>

> **$0.03 per image** at default resolution — one OpenAI-compatible endpoint at `https://api.apimart.ai/v1`, no monthly plan required. *(observed 2026-09-17)*

**[Get an API key](https://go.apimart.ai/k-f7f7df)** · **[Live pricing](https://go.apimart.ai/k-4e1a1b)** · **[Model page](https://go.apimart.ai/k-72d37a)** · [⚡ 60-second quickstart](#quickstart)

**Why teams call Nano Banana Pro (`gemini-3-pro-image-preview`) through APIMart**

- **One key, entire catalog.** The same `https://api.apimart.ai/v1` base URL and `Authorization` header reach Nano Banana Pro (`gemini-3-pro-image-preview`) and 300+ other image, video and language models — switch the `model` field, not your client.
- **$1 minimum, pay as you go.** No subscription and no prepaid plan to size up front: top up from $1 and spend it on calls. There is no free quota to burn through first, so the price in this table is the price you pay.
- **The charge comes back in the response.** Every call reports the amount billed (`cost` / `credits_cost`), so a spend number is read per call instead of guessed at month end.
- **Async by design.** Submit, take the `task_id`, poll `GET /v1/tasks/{id}` — batching and retries are ordinary queue work, not a bespoke integration.

<!-- /conv-kit:v1 -->

Nano Banana Pro is the highest-fidelity Gemini image route on APIMart: one asynchronous endpoint, 1K/2K/4K output, eleven aspect ratios including `auto`, and reference images for editing.

## Model id and routes

| Route | `model` value | Billing | Notes |
| --- | --- | --- | --- |
| Per-image (default here) | `gemini-3-pro-image-preview` | per delivered image, by resolution | alias `nano-banana-pro-ext` is documented as equivalent |
| Token-billed official | `gemini-3-pro-image-preview-official` | per million tokens | no `official_fallback` on this id |

Endpoint: `POST https://api.apimart.ai/v1/images/generations` (OpenAI-compatible), then poll `GET /v1/tasks/{task_id}`.
Result links are valid for 24 hours.

## Pricing

<!-- pricing:model:start -->
| Output | List price | Effective price |
| --- | --- | --- |
| default | $0.0375 | $0.03 |
| 4K | $0.05 | $0.04 |

The token-billed official route bills per million tokens instead: `text_input` $1.60, `cached_text_input` free, `image_input` $1.60, `cached_image_input` free, `text_output` $9.60, `image_output` $96.00.
<!-- pricing:model:end -->

Prices are a snapshot; the [pricing page](https://go.apimart.ai/k-4e1a1b) and [`data/model.json`](data/model.json) are refreshed by
CI, and a completed task reports the exact amount in its `cost` field.

## Request parameters

| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| `model` | string | required | `gemini-3-pro-image-preview` (alias `nano-banana-pro-ext` is equivalent) |
| `prompt` | string | required | must not be empty after trimming |
| `size` | string | `auto` | `auto`, `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` |
| `resolution` | string | `1K` | `1K`, `2K`, `4K` — 4K with base64 output takes longer |
| `n` | integer | `1` | must be `1` on this route; a quoted string errors |
| `image_urls` | string[] | — | reference images for image-to-image or editing (URL or base64 data URL) |
| `nsfw_check` | boolean | `false` | `true` runs `omni-moderation-latest` before submitting, adding latency |
| `official_fallback` | boolean | `false` | `true` falls back to the official channel; not available on the `-official` model id |

Supported aspect ratios: `auto`, `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`.

## Quickstart

```bash
curl --request POST --url https://api.apimart.ai/v1/images/generations \
  --header "Authorization: Bearer $APIMART_API_KEY" --header 'Content-Type: application/json' \
  -d '{"model":"gemini-3-pro-image-preview","prompt":"A bamboo forest path under moonlight","size":"1:1","resolution":"1K","n":1}'
```

```python
import os, time, requests

BASE = "https://api.apimart.ai/v1"
HEADERS = {"Authorization": f"Bearer {os.environ['APIMART_API_KEY']}", "Content-Type": "application/json"}

created = requests.post(f"{BASE}/images/generations", headers=HEADERS, timeout=60, json={
    "model": "gemini-3-pro-image-preview", "prompt": "A bamboo forest path under moonlight",
    "size": "1:1", "resolution": "1K", "n": 1,
}).json()
task_id = created["data"]["id"]

while True:
    task = requests.get(f"{BASE}/tasks/{task_id}", headers=HEADERS, timeout=60).json()["data"]
    if task["status"] in ("completed", "failed"):
        break
    time.sleep(5)
print(task.get("cost"), task.get("result", {}).get("images", [{}])[0].get("url"))
```

```javascript
const res = await fetch("https://api.apimart.ai/v1/images/generations", {
  method: "POST",
  headers: { Authorization: `Bearer ${process.env.APIMART_API_KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({ model: "gemini-3-pro-image-preview", prompt: "A bamboo forest path under moonlight",
                          size: "1:1", resolution: "1K", n: 1 }),
});
const { data } = await res.json();      // data.id is the task id — poll /v1/tasks/<id>
```

Runnable versions: [`examples/`](examples). The task lifecycle is `pending → processing → completed | failed`, and the
finished task carries `cost`, `credits_cost` and expiring result URLs.

## Sample outputs

Every render below came from a single call with the model id above, at the ratio shown; the cost column is what the task
reported.

| Output | Recipe | Ratio | Cost | Prompt |
| --- | --- | --- | --- | --- |
| <img src="assets/01-product-hero-perfume.jpg" width="220" alt="Nano Banana Pro sample output"> | Product / e-commerce | 1:1 | $0.03 | `Studio hero shot of a frosted glass perfume bottle on a wet black stone slab, single softbox from the left, faint mist, deep charcoal background, crisp label text, commercial product photography` |
| <img src="assets/03-cinematic-street-rain.jpg" width="220" alt="Nano Banana Pro sample output"> | Cinematic still | 16:9 | $0.03 | `Rain soaked Kyoto alley at night, paper lantern reflections on wet stone, a lone figure with a transparent umbrella walking away, cinematic 35mm still, shallow depth of field, film grain` |
| <img src="assets/02-food-overhead-ramen.jpg" width="220" alt="Nano Banana Pro sample output"> | Food photography | 4:3 | $0.03 | `Overhead flat lay of a spicy miso ramen bowl with soft boiled egg, nori and scallions, dark ceramic table, chopsticks resting on the rim, natural window light, editorial food photography` |
| <img src="assets/04-architectural-dusk.jpg" width="220" alt="Nano Banana Pro sample output"> | Architecture | 16:9 | $0.03 | `Minimalist concrete villa on a cliff at dusk, warm interior light, infinity pool reflecting a violet sky, architectural photography, 24mm perspective, ultra sharp` |
| <img src="assets/06-illustration-layered-paper.jpg" width="220" alt="Nano Banana Pro sample output"> | Illustration | 1:1 | $0.03 | `Layered paper cut illustration of a mountain lake at sunrise, five depth layers, soft pastel palette, subtle drop shadows, art print composition, clean vector edges` |
| <img src="assets/05-fashion-editorial-studio.jpg" width="220" alt="Nano Banana Pro sample output"> | Fashion portrait | 3:4 | $0.03 | `Editorial fashion portrait of a model in an oversized ivory wool coat, seamless light grey studio backdrop, crisp high key lighting, medium format detail, calm expression` |
| <img src="assets/08-macro-botanical-detail.jpg" width="220" alt="Nano Banana Pro sample output"> | Macro nature | 3:2 | $0.03 | `Macro photograph of a dew covered dandelion seed head against deep black background, focus stacked detail, iridescent droplets, studio lighting` |
| <img src="assets/07-infographic-dashboard.jpg" width="220" alt="Nano Banana Pro sample output"> | Design / UI | 16:9 | $0.03 | `Flat vector dashboard panel showing three gauge dials and abstract latency curves, muted blue and sand palette, generous white space, crisp geometric cards, no placeholder text` |

Recipes and measured costs are also in [`data/samples.json`](data/samples.json).

<!-- conv-kit:v1:fix -->
## First-call troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `401` / `invalid api key` | key missing, truncated, or a stray newline pasted into the header | Re-copy it from the console; the header is `Authorization: Bearer $APIMART_API_KEY` |
| balance / credit error | the account has no balance | Top up from $1 in the console — there is no free quota to fall back on |
| `429` | concurrent requests on one key | Back off, then retry the same request with the same `Idempotency-Key` |
| `400` / model not found | wrong route for the id: the per-unit alias needs its `version`, the official id must not send one | Copy the exact `model` value from the route table above |
| task ends `failed` | prompt rejected by the filter, or a reference image URL expired | Re-submit with a **new** `Idempotency-Key` and re-host the reference image |
| result URL stops working | result links expire | Download the file as soon as the task reports `completed` |
<!-- /conv-kit:v1:fix -->

## FAQ

**What is the Nano Banana Pro API model id?**

`gemini-3-pro-image-preview`. The alias `nano-banana-pro-ext` is documented as equivalent and produces identical results, so either string works in the `model` field.

**How much does one Nano Banana Pro image cost?**

On the per-image route the table above lists the effective price per resolution tier and the token-billed official route (`gemini-3-pro-image-preview-official`) is priced per million tokens; both are refreshed daily by CI and verified against the `cost` field of a completed task.

**Can I generate more than one image per request?**

No. `n` is 1 on this route; fan out client-side for batches. Passing a quoted number also fails — the field must be a bare integer.

**How do I edit an existing image?**

Send the source image in `image_urls` (public URL or base64 data URL) and describe what to preserve and what to change in `prompt`. With `size: auto` the output follows the upstream aspect ratio, so pin a ratio when the layout matters.

**How long do the result links live?**

The generated links are valid for 24 hours, so download and store the output as part of the job.

## Related searches

- `nano banana pro api`
- `nano banana pro api pricing`
- `nano banana pro api key`
- `gemini 3 pro image api`
- `nano banana pro vs nano banana 2`
- `image editing api`
- `ai image generation api`

<!-- conv-kit:v1:cta -->
---

**Start with $1.** [Get an API key](https://go.apimart.ai/k-f7f7df) → [check live pricing](https://go.apimart.ai/k-4e1a1b) → [open Nano Banana Pro (`gemini-3-pro-image-preview`) in the model library](https://go.apimart.ai/k-72d37a). The first call is three steps: submit, poll `task_id`, read the charged amount off the response.
<!-- /conv-kit:v1:cta -->

## Attributed links (how this repository is measured)

| Purpose | Attributed link | Target |
| --- | --- | --- |
| Open Nano Banana Pro on APIMart | <https://go.apimart.ai/k-72d37a> | `docs.apimart.ai` model page |
| Current pricing page | <https://go.apimart.ai/k-4e1a1b> | `apimart.ai/pricing` |
| Get an API key | <https://go.apimart.ai/k-f7f7df> | `apimart.ai/keys` |

Outbound APIMart links are minted through the promo link API; hand-made tracking parameters are rejected by
`tools/check_links.py` in CI.

## Disclosure

Nano Banana Pro is a third-party model served through APIMart; this repository documents how to call it and publishes
real outputs, model ids and prices, and does not claim official status. Model names, prices and documentation belong to
their respective owners. Endpoint reference: [https://docs.apimart.ai/en/api-reference/images/gemini-3-pro/generation](https://docs.apimart.ai/en/api-reference/images/gemini-3-pro/generation).

## Repository map

```text
README.md             model id, pricing, parameters, quickstart, samples, FAQ
data/model.json       the pricing record for this model (CI-refreshed)
data/samples.json     prompt recipes with measured cost
tools/snapshot.py     refresh this model's prices from the public pricing payload
tools/check_links.py  attribution guard
examples/             curl, Python and JavaScript clients
assets/               real sample renders (JPEG, resized for the README)
.github/workflows/    daily price refresh + validation
```

## License

MIT — see [LICENSE](LICENSE).
