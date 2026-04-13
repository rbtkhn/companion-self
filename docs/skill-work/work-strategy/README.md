# work-strategy (template stub)

**Companion-self template** does not ship the full grace-mar work-strategy lane. Instance repos (e.g. [Grace-Mar](https://github.com/rbtkhn/grace-mar)) hold the complete strategy notebook, STRATEGY.md, and daily brief machinery.

This folder holds **portable forecast–strategy hooks** only:

- [decision-points/forecast-informed-decision-point-template.md](decision-points/forecast-informed-decision-point-template.md)
- [strategy-notebook/forecast-watch-log.md](strategy-notebook/forecast-watch-log.md)

Full operator copy: [grace-mar work-strategy README](https://github.com/rbtkhn/grace-mar/blob/main/docs/skill-work/work-strategy/README.md).

## Forecast integration

Forecast artifacts from [`docs/skill-work/work-forecast/`](../work-forecast/README.md) may be referenced as planning inputs in instances.

Allowed uses:

- active watch support
- threshold monitoring
- timing judgments
- decision-point framing

Disallowed uses:

- direct Record updates
- converting a forecast into a fact claim
- bypassing proposal and review workflow

Recommended flow:

1. run forecast
2. save artifact
3. write receipt
4. review summary
5. reference in forecast-watch-log or a decision point if useful
6. stage any durable downstream claim separately if needed
