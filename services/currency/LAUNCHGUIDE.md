# Currency Exchange

## Tagline
Norges Bank exchange rates for AI: 38 currencies against NOK since ~1980, plus buying power

## Description
Currency gives an AI assistant Norges Bank's daily reference rates as structured data: the rate between any two of 38 currencies on any date back to about 1980, conversion of an amount, and a daily series for charting. It also serves World Bank buying-power multipliers for pricing one list price into many markets.

It is a hosted server with a Streamable HTTP endpoint at https://currency.publifye.com/mcp, so there is nothing to install. Sign in once in the browser. The service syncs and serves the rates; it does not compute, estimate or interpolate one. A date with no published rate returns the series as published, with no carry-forward and no invented value.

It is for developers, finance staff, publishers and anyone who needs an assistant to use real reference rates instead of a remembered figure. These are reference rates, not dealable prices, and not advice.

## Setup Requirements
No setup required — sign in with OAuth in the browser on first use.

## Category
Finance

## Use Cases
Currency conversion, historical exchange rates, NOK exchange rates, exchange-rate charts, regional pricing, price localisation, accounting reference rates, buying-power pricing

## Features
- Norges Bank daily reference rates for 38 currencies plus NOK, back to about 1980
- Rate between any two currencies on a date, with its inverse
- Cross-rates such as USD to EUR derived through NOK
- Conversion of an amount at a given date or the most recent rate
- Daily rate series over a date range, sorted chronologically, for charts and trends
- All 38 currency rates for a single date in one call, for dashboards and bulk comparisons
- World Bank buying-power multipliers (GNI per capita, PPP) for pricing a USD list price per country
- Returns both a recommended `factor` (never above 1.0, floored at 0.35) and an uncapped `raw_factor`, with `capped` and `floored` flags
- Fails safe on unknown country or missing data: `factor` 1.0 with the reason in `note`
- No interpolation and no carry-forward across weekends, holidays or days the bank did not publish
- `reference_year` and `fetched_at` reported separately, so a stale figure is not reported as current
- `data_origin` and `fallback` say whether a buying-power answer is live or from the embedded table
- All seven tools are read-only and idempotent

## Getting Started
- "Convert 2,500 NOK to US dollars at the latest Norges Bank rate"
- "What was the EUR to NOK rate on 15 March 2020?"
- "Give me the daily USD to NOK rates for the first half of 2024 so I can chart them"
- "What multiplier should I apply to a USD list price for Brazil?"
- Tool: get_rate — rate between two currencies on a date, with its inverse
- Tool: convert — convert an amount between currencies at a given date
- Tool: get_rates_range — daily series for one currency over a date range
- Tool: get_all_rates — all 38 currency rates for a single date
- Tool: get_buying_power — recommended price multiplier for one country
- Tool: list_currencies — the available currency codes and their names

## Tags
currency, exchange-rates, norges-bank, nok, forex, conversion, finance, historical-rates, pricing, buying-power, world-bank, localisation, reference-rates, norway, rates

## Documentation URL
https://github.com/Publifye/mcp/tree/main/services/currency

## Health Check URL
https://currency.publifye.com/health
