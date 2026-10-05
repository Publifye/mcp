# Place and distance

**Who is registered near here, and how far apart are they?** 2 Brreg MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://brreg.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | What it does |
|---|---|
| [`entity_nearby`](#entity_nearby) | Entities registered near a place: the same snapshot as entity_search, ordered nearest first |
| [`entity_distance`](#entity_distance) | How far apart two organisations are, and which of several is closest |

---

## `entity_nearby`

**Entity Nearby** — read-only, idempotent, closed-world.

Entities registered near a place: the same snapshot as entity_search, ordered nearest first.
ARGS: radius_km, plus ONE centre — orgnr (that entity's own registered address: who is near this company) or lat and lon. Both, or neither, is refused by name. For a named place use entity_search with municipality, city or postcode.
ANCHOR: an orgnr centre is NOT in its own results (diagnostics: anchor_orgnr, anchor_excluded). An anchor with no coordinate (c/o, PO box, foreign or unmatched address) is REFUSED naming that reason, never answered as an empty list; a sole proprietorship cannot be a customer's anchor, its address being personal data.
CAP: 10 km for a bare radius, 50 km when another filter narrows it (status and kind:all do not count); over it is invalid_filter naming the cap.
FILTERS: kind, org_form, municipality, postcode, city, nace, sector, status (active by default), public_body, vat_registered, parent_orgnr, employees_min/max.
ITEMS: the entity_search summary (including forced_dissolution=true for a state-compelled tvangsavvikling/tvangsoppløsning inside status "dissolving") plus distance_km (2 decimals, straight line) and location. Diagnostics add order, radius_cap_km, shared_points, distinct_points_in_page and unlocated_excluded.
PLACE: the point is the REGISTERED address matched to a Kartverket address point, never where the business operates; entities without a located address are excluded and counted.
REFUSALS: personal-data records (ENK and their establishments) and c/o addresses are never members of a radius result. Answers carry the Kartverket CC BY 4.0 block beside the NLOD attribution.
Example: entity_nearby orgnr="964338531" radius_km=2 org_form=["AS"]. Next: entity_distance from={orgnr} to=[{orgnr}]. [END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `city` | string | no | Postal city name. |
| `compact` | boolean | no | One-line text summary, not duplicated JSON. |
| `cursor` | string | no | Next-page token; send it alone (+max_bytes, compact). |
| `employees_max` | integer | no | Maximum employees. |
| `employees_min` | integer | no | Minimum employees. |
| `fields` | array of string | no | Item fields to return (orgnr kept). |
| `kind` | string | no | Default all. |
| `lat` | number | no | Centre latitude, decimal degrees. Coordinates only — for a place use entity_search with municipality, city or postcode. |
| `limit` | integer | no | Items per page (1-100, default 20). |
| `lon` | number | no | Centre longitude, decimal degrees. |
| `max_bytes` | integer | no | Response byte budget (default 24576). |
| `municipality` | string | no | Municipality number or name. |
| `nace` | string | no | NACE code prefix, e.g. 84 or 84.110. |
| `org_form` | array of string | no | Org form codes, e.g. AS, ENK (see code_list). |
| `orgnr` | string | no | Anchor: centre on THIS entity's registered address instead of lat/lon. It is never in its own results. |
| `parent_orgnr` | string | no | Only direct children of this orgnr. |
| `postcode` | string | no | Four-digit postcode. |
| `public_body` | boolean | no | Public bodies only (true) or none (false). |
| `radius_km` | number | yes | Km; max 10 alone, 50 with another filter. |
| `sector` | string | no | Institutional sector code prefix. |
| `snapshot_id` | string | no | Pin a snapshot (else snapshot_expired). |
| `status` | string | no | Default active. |
| `vat_registered` | boolean | no | VAT-registered (true) or not (false). |

## `entity_distance`

**Entity Distance** — read-only, idempotent, closed-world.

How far apart two organisations are, and which of several is closest — e.g. which supplier is nearest our office.
STRAIGHT LINE ONLY: distance_km is the straight-line distance between two registered address points. It is NOT travel, driving or walking distance and NOT a travel time. Across a Norwegian fjord or a mountain the road is often many times longer, so never present this number as how far someone drives or how long it takes. There is no road network and no routing here.
ARGS: from, one place; to, a list of places (up to 50; the schema you were served carries the cap your plane actually has). A place is {orgnr} or {lat, lon}, never both, with an optional label echoed back.
ITEMS: one per `to` entry, nearest first: {index, label, orgnr, name, located, distance_km, point, location}. Order is distance; ties and unlocated entries keep input order.
REFUSALS: a `to` place with no usable point is still answered, with located=false and a stated reason (no_coordinate + location_reason, personal_data, not_in_snapshot, removed, invalid_orgnr) — never silently left out. A `from` that cannot be resolved refuses the whole call, because nothing could be measured. A sole proprietorship's address is personal data: for customers it is refused as a place, not answered.
PLACE: every point is the REGISTERED address matched to a Kartverket address point, not where the business operates; answers carry the Kartverket CC BY 4.0 block beside the NLOD attribution.
Example: entity_distance from={"orgnr":"964338531","label":"office"} to=[{"orgnr":"973210009"},{"lat":60.39,"lon":5.32}]. Next: entity_nearby orgnr=<orgnr> radius_km=5. [END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `compact` | boolean | no | One-line text summary, not duplicated JSON. |
| `cursor` | string | no | Next-page token; send it alone (+max_bytes, compact). |
| `from` | object | yes | Measure from here: {orgnr} or {lat, lon} (optional label). |
| `max_bytes` | integer | no | Response byte budget (default 24576). |
| `snapshot_id` | string | no | Pin a snapshot (else snapshot_expired). |
| `to` | array of object | yes | Measure to these, answered nearest first: [{orgnr}] or [{lat, lon}]. |

---

*Generated from the live `tools/list` of the release serving production (0.3.32) on 2026-09-29. Regenerate rather than edit by hand.*
