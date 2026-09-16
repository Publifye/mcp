# Rates and conversion

**What was this worth, in that currency, on that date?** 5 Currency MCP tools, listed below with the exact description and input
schema the server itself returns. Endpoint: `https://currency.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | What it does |
|---|---|
| [`get_rate`](#get-rate) | Get the exchange rate between any two currencies on a specific date. Returns the rate and its in… |
| [`convert`](#convert) | Convert a monetary amount from one currency to another using Norges Bank exchange rates. Support… |
| [`get_all_rates`](#get-all-rates) | Get all 38 currency rates for a single date. Returns each currency code, full name, and rate (NO… |
| [`get_rates_range`](#get-rates-range) | Get daily exchange rates for a single currency over a date range. Returns an array of {date, rat… |
| [`list_currencies`](#list-currencies) | List all 38 available currency codes with their full names. Returns the base currency (NOK) and … |

---

## `get_rate`

**Get Rate** — read-only, idempotent, closed-world.

Get the exchange rate between any two currencies on a specific date. Returns the rate and its inverse. Supports all 38 Norges Bank currencies plus NOK. Cross-rates (e.g. USD→EUR) are computed via NOK as intermediary. If date is omitted, returns the most recent available rate.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date` | string | no | Date in YYYY-MM-DD format. Omit or set to 'latest' for the most recent available rate. |
| `from` | string | yes | Source currency code, e.g. USD, EUR, GBP (case-insensitive) |
| `to` | string | yes | Target currency code, e.g. NOK, SEK, DKK (case-insensitive) |

## `convert`

**Convert** — read-only, idempotent, closed-world.

Convert a monetary amount from one currency to another using Norges Bank exchange rates. Supports all 38 currencies plus NOK. Cross-currency conversion (e.g. USD→EUR) is computed via NOK. If date is omitted, uses the most recent available rate.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `amount` | number | yes | Amount to convert (zero or greater) |
| `date` | string | no | Date in YYYY-MM-DD format. Omit or set to 'latest' for the most recent available rate. |
| `from` | string | yes | Source currency code, e.g. USD (case-insensitive) |
| `to` | string | yes | Target currency code, e.g. NOK (case-insensitive) |

## `get_all_rates`

**Get All Rates** — read-only, idempotent, closed-world.

Get all 38 currency rates for a single date. Returns each currency code, full name, and rate (NOK per unit). If date is omitted, returns the most recent available rates. Useful for dashboards and bulk comparisons.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date` | string | no | Date in YYYY-MM-DD format. Omit or set to 'latest' for the most recent available rates. |

## `get_rates_range`

**Get Rates Range** — read-only, idempotent, closed-world.

Get daily exchange rates for a single currency over a date range. Returns an array of {date, rate} points sorted chronologically. Useful for charts, trend analysis, and historical comparisons. Rates are NOK per unit of the specified currency.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `currency` | string | yes | Currency code, e.g. USD (case-insensitive) |
| `from_date` | string | yes | Start date in YYYY-MM-DD format (inclusive) |
| `to_date` | string | yes | End date in YYYY-MM-DD format (inclusive) |

## `list_currencies`

**List Currencies** — read-only, idempotent, closed-world.

List all 38 available currency codes with their full names. Returns the base currency (NOK) and data source (Norges Bank). Use this to discover valid currency codes for get_rate and convert.

*No parameters.*

---

*Generated from the service's own tool registry on the source serving production on
2026-09-16. Regenerate rather than edit by hand.*
