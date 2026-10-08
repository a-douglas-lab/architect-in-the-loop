# Development outcomes

Status: agreed 5 Oct 2026

Outcomes used to build and dry-run the Ordering exemplar (backlog P9). They may be built by hand, with Claude Code, as reference implementations, and the capability may iterate against them during development. The held-out evaluation outcomes are kept elsewhere and are not used for development.

| ID | Outcome | Main areas touched | Use-case rung |
| --- | --- | --- | --- |
| D1 | Customers can add a note to their order at checkout | Ordering (order and create-order request), storefront checkout | Rung 2: add a field |
| D2 | Record a carrier and tracking number when an order ships | Ordering (ship command, order, shipped event), webhook payload for shipped orders | Rung 2–3: field plus event contract change |
| D3 | Orders not paid within 24 hours are cancelled automatically | Ordering, including OrderProcessor (background processing) | Rung 1: single domain, existing cancel transition |

Each development outcome follows the agreed sequence: visible acceptance examples and tests written first, confirmed failing against unmodified eShop, then implemented and verified.
