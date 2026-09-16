# Buying power

**What should this USD price be in that country?** 2 Currency MCP tools, listed below with the exact description and input
schema the server itself returns. Endpoint: `https://currency.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | What it does |
|---|---|
| [`get_buying_power`](#get-buying-power) | Get the buying-power multiplier for one country, for pricing a USD list price in a local market.… |
| [`list_buying_power`](#list-buying-power) | List the buying-power multiplier for every country the World Bank publishes GNI per capita (PPP)… |

---

## `get_buying_power`

**Get Buying Power** — read-only, idempotent, closed-world.

Get the buying-power multiplier for one country, for pricing a USD list price in a local market. Returns TWO numbers. `factor` is the RECOMMENDED multiplier on the USD price: 1.0 means full price, and it is NEVER above 1.0 because the USD price is the maximum anyone pays regardless of local wealth; it is clamped to a floor of 0.35 because payment fees make smaller charges uneconomic. `raw_factor` is the honest, uncapped MEASUREMENT (GNI per capita PPP relative to the USA, square-root compressed) and CAN exceed 1.0 for countries richer than the United States — Norway measures about 1.10. `ratio` is the plain GNI ratio before that compression, for a consumer that wants to apply its own curve. The `capped` and `floored` flags say whether policy moved `factor` away from `raw_factor`. If in doubt, use `factor`. An unknown country, missing data or an upstream outage fails safe: factor 1.0 with `unknown` or `fallback` set and the reason in `note`.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `country` | string | yes | ISO 3166-1 alpha-2 country code, e.g. DE, IN, NO, BR (case-insensitive). NOT a currency code — the eurozone spans very different economies on one currency. |
| `history` | boolean | no | Also return the country's full year-to-GNI series and the United States' series alongside it, for trend analysis. Off by default: the history is ~36 years per country and most callers only need the current factor. Years with no observation are absent, not zero — do not interpolate across them. |

## `list_buying_power`

**List Buying Power** — read-only, idempotent, closed-world.

List the buying-power multiplier for every country the World Bank publishes GNI per capita (PPP) for, sorted lowest buying power first. Each row carries both numbers: `factor`, the recommended multiplier on a USD list price (1.0 = full price, never above 1.0, floored at 0.35), and `raw_factor`, the uncapped measurement which exceeds 1.0 for countries richer than the United States. The consumer chooses which to use; if in doubt, use `factor`. Also returns `reference_year` (the World Bank's release year — published annually, around July), `fetched_at` (when this service last pulled it — NOT the same thing), and `data_origin`/`fallback` saying whether the data is a live pull or the table embedded in the binary.

*No parameters.*

---

*Generated from the service's own tool registry on the source serving production on
2026-09-16. Regenerate rather than edit by hand.*
