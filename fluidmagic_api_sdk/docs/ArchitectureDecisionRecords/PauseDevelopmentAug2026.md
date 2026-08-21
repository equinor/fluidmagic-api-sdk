# ADR-001: Pause SDK development

## Status
Accepted

## Date
2026-08-21

## Context
The original motivation for building the SDK was that running a calculation against FluidMagic required several sequential steps: saving an EOS, saving a fluid, saving a process, saving all of these to a configuration, and finally running the calculation on that configuration. Because this multi-step workflow was cumbersome for consumers of the API, the SDK was meant to encapsulate the steps behind a single high-level interface.

Since then, the direction of FluidMagic has changed: it will no longer maintain a database and will instead operate as a pure, stateless calculator. As a result, the multi-step "save → save → save → run" workflow collapses to a single stateless call. This removes most of the complexity that the SDK was designed to hide, which in turn reduces both the necessity of the SDK and the incremental value it provides over calling the API directly.

## Decision
Pause development of the SDK due to a lack of clear value creation and lack of funding to continue the work.

"Paused" here means:

- No new features will be developed.
- No routine maintenance releases will be published.
- The repository remains available for reference and may be resumed later (see *Trigger to revisit*).

## Alternatives Considered

### 1. Continue development as-is
Keep investing in the SDK at the current pace. Rejected because the underlying problem the SDK was designed to solve (multi-step, stateful API usage) is being removed at the API level, and there is no funding to justify continued investment.

### 2. Repurpose the SDK
The SDK could be reshaped into a different kind of integration layer (for example, higher-level workflows, domain helpers, or opinionated defaults on top of the stateless API). This is potentially valuable, but requires identified users and use cases to guide the redesign, as well as funding to execute. Neither is available today, so this option is deferred rather than pursued.

### 3. Convert to a thin examples / client-samples repository
Strip the SDK down to request/response models and example scripts that demonstrate how to call the API directly, without maintaining a full SDK abstraction. Rejected for now because it still requires ongoing maintenance effort and a decision on packaging, and the same effect can be achieved by pointing users at the existing `examples/` directory.

### 4. Deprecate and archive publicly
Publish a final release with a clear deprecation notice, mark the repository read-only, and remove the package from PyPI (or mark it as yanked/deprecated). Rejected at this time because we want to preserve the option to resume; a hard deprecation would signal a stronger commitment than "paused."

## Consequences

### Positive
- Refocuses the team on completing the FluidMagic API within the project's scope.
- Avoids sunk-cost investment in an abstraction whose original justification has been removed.
- Leaves the door open to resume the SDK (or repurpose it) if a concrete use case and funding appear.

### Negative / neutral
- The repository will not receive new features or routine maintenance while paused.
- Existing users (if any) will need to call the API directly; there is no active migration support.
- Open issues and pull requests will not be actively triaged during the pause.

