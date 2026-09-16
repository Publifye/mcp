# Currency Exchange — Norges Bank exchange rate MCP server for Claude, Cursor and any MCP client

**Currency gives an AI assistant Norges Bank's daily reference rates as structured data: the rate
between any two of 38 currencies on any date back to about 1980, conversion of an amount, a daily
series for charting — and World Bank buying-power multipliers for pricing one list price into many
markets. It runs as a hosted MCP server over HTTPS.**

| | |
|---|---|
| Endpoint | `https://currency.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open · no API keys |
| Registry | `pro.publifye/currency` ([server.json](server.json)) |
| Product site | <https://currency.publifye.com> |
| What it solves | <https://publifye.com/currency> |
| Capability tools | **7** ([full schemas](tools.json)) |

## Connect

```jsonc
{ "mcpServers": { "currency": { "type": "http", "url": "https://currency.publifye.com/mcp" } } }
```

Claude Code: `claude mcp add --transport http currency https://currency.publifye.com/mcp`, then
`/mcp` to sign in.

The OAuth flow runs in the browser on first use, with a Publifye account. Access is granted through
that sign-in only; there is no API key to create, copy or rotate. The discovery chain is the same as
for the other servers: **[../../docs/connect.md](../../docs/connect.md)**.

## Where the rates come from

The rates are **Norges Bank's own daily reference rates**, quoted against the Norwegian krone. This
service syncs and serves them. It does not compute, estimate or interpolate a rate.

That last sentence is the one that matters when an AI is asking. Norges Bank publishes once per
business day, at about 16:00 CET, so weekends, Norwegian public holidays and any day the bank did
not publish simply have no rate. A date with no published rate returns the series **as published**
rather than an invented value — no carry-forward, no interpolation, no nearest-neighbour. A model
that wants a number for a Sunday has to decide for itself what to do about it, which is the correct
place for that decision to be made.

Cross-rates — USD→EUR, say — are derived through NOK, because NOK is the only pair Norges Bank
quotes. The derivation is arithmetic on two published rates, not a third source.

## The buying-power tools return two numbers, and the difference matters

`get_buying_power` and `list_buying_power` exist for one job: pricing a USD list price into a local
market. They return **`factor`** and **`raw_factor`**, and they are not the same thing.

- **`factor`** is the recommended multiplier. It is never above 1.0 — the USD price is the maximum
  anyone pays regardless of how wealthy the local market is — and it is floored at 0.35 because
  payment fees make smaller charges uneconomic.
- **`raw_factor`** is the honest, uncapped measurement: GNI per capita (PPP) relative to the USA,
  square-root compressed. It **can** exceed 1.0. Norway measures about 1.10.

Applying `raw_factor` to a Norwegian price charges about 10% **above** list. That is exactly the
mistake the cap exists to prevent, which is why both numbers are returned with `capped` and
`floored` flags saying whether policy moved one away from the other. If in doubt, use `factor`.

An unknown country, missing data or an upstream outage fails safe: `factor` 1.0, with `unknown` or
`fallback` set and the reason in `note` — never a silent guess.

## What the tools do

Every tool is documented with its exact description, annotations and input schema — 7 in all,
generated from the service's own registry, never written by hand.

| Area | The question it answers | Tools |
|---|---|---|
| **[Rates and conversion](tools/rates.md)** | What was this worth, in that currency, on that date? | 5 |
| **[Buying power](tools/buying-power.md)** | What should this USD price be in that country? | 2 |

Machine-readable: **[tools.json](tools.json)** carries all 7 callable tools with full JSON Schema,
plus every excluded bucket listed by name so the count is auditable.

All seven are read-only and idempotent. None is marked open-world: every answer is served from data
this service has already synced, so the same call on the same day gives the same answer.

## What it does not do

- **No live or intraday rates.** One publication per business day, about 16:00 CET. A day's rates
  are stable once published, and therefore cacheable.
- **No currency Norges Bank does not quote.** 38 plus NOK, and no more.
- **No invented values.** No interpolation across a gap, no carry-forward into a weekend.
- **No trading, no execution, no advice.** These are reference rates, not dealable prices, and a
  reference rate is not what you will be charged by a bank or a card network.
- **Not a full annual-accounts or economics source.** The buying-power figures are one World Bank
  indicator, not a model of an economy.

## Data and licence

Exchange rates are published by **Norges Bank**. Buying-power figures are **World Bank** GNI per
capita (PPP), released annually, around July. Results carry `reference_year` — the World Bank's
release year — separately from `fetched_at`, which is when this service last pulled it. Those are
not the same thing and conflating them is how a stale figure gets reported as current.

`data_origin` and `fallback` say whether a buying-power answer came from a live pull or from the
table embedded in the binary, so a degraded answer is never indistinguishable from a fresh one.

Currency Exchange is operated by Publifye AS and is not affiliated with, or endorsed by, Norges Bank
or the World Bank.

## Plans

A free Publifye account grants a small daily allowance on a trial; Currency Access lifts it to a
monthly quota. Plans and prices can change; **the current ones are always on
<https://currency.publifye.com>**, and where this page and the site differ, the site is right.
