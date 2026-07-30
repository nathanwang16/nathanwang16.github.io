# Nobody Opts In — An Involuntary, Retroactive Prediction Ledger for Public Discourse

*People make falsifiable claims about the future constantly, in public, for free. Almost none
of it is ever scored. LLM claim extraction just made scoring it cheap enough to be worth
doing.*

## The thesis

There are two existing ways to hold a prediction accountable, and both have the same blind
spot.

**Prediction markets** produce excellent calibration data, but only about people who chose to
enter — a self-selected population of the already-calibrated. **Fact-checking** covers
everyone, but adjudicates claims about the *past*, where the disagreement is usually about
values or framing rather than about who saw further.

The gap is the enormous volume of forward-looking, falsifiable, involuntary public claims:
earnings calls, op-eds, podcasts, timelines, threads. Statements with a truth condition and a
horizon, made without any expectation of being scored. Extracting and resolving them at scale
used to cost more than the answer was worth. That constraint just moved.

So: ingest organic public claims, compile them into structured propositions with explicit
resolution criteria and horizons, resolve them against ground truth when they mature, and
aggregate per-source track records using statistics that don't lie about how thin the evidence
is.

## Why the statistics are the hard part

Every naive version of this project produces a leaderboard that is mostly noise wearing a
number. The failure modes are specific and each needs a structural answer, not a caveat:

- **Luck versus skill.** Small samples generate impressive track records for free. Effective
  sample size replaces raw claim count everywhere; shrinkage toward a prior is mandatory, not
  optional; and there is a display floor below which no score is shown at all.
- **No null baseline is not neutral.** A source's score means nothing without a null
  forecaster to beat. In some domains that null is easy to construct and in others it is
  arguably impossible — which is itself a finding worth measuring before building on top of it.
- **Void is a measurement, not a shrug.** Claims that never resolve are the majority in some
  domains. Treating them as neutral is a choice that quietly rewards vagueness. Void is
  promoted to a first-class measured quantity with a bounding analysis.
- **Deletion survivorship.** Wrong predictions get deleted. Any ledger built on live scrapes
  is reading a curated record.
- **Temporal leakage.** An LLM asked to resolve a 2023 claim may already know the answer from
  pretraining. If the extraction model has seen the outcome, the pipeline is measuring
  contamination.
- **Popularity is not a sampling frame.** If discovery follows engagement, the ledger measures
  reach. A hard floor of ingest volume is reserved for popularity-orthogonal discovery.

## Non-negotiable data integrity

Five invariants, enforced in code rather than convention, because data collected without them
cannot be retroactively repaired:

**append-only ledger** · **blind extraction** (the extractor never sees the outcome window) ·
**resolution criteria frozen before resolution** · **archived source snapshots** ·
**versioned extraction epochs**

A related rule with teeth: retrospective and prospective claims are split at the schema level
by an epoch flag, and the code *refuses* to score retrospectively-collected claims as though
they were prospective. That refusal being a hard error rather than a guideline is the whole
point.

## Where it is going

**Tier 1 is a test harness, not the product.** The earnings-call wedge exists because
resolution is mechanical and ground truth is unambiguous — the right place to debug a pipeline,
and the wrong place to look for anything interesting about discourse.

**Tier 2 is the substance.** Domains like AI progress, where claims are dense, horizons are
long, and nobody is keeping score. The current phase is a deliberate parameter-measurement
study rather than a system build: measure claim density, horizon extractability, adjudication
reliability, null constructability, and cost per resolved claim — *then* decide on the
architecture.

There is a genuine architectural fork ahead, and the honest position is that it is not yet
decided. **Branch S** scores sources and produces track records. **Branch C** abandons
per-source scoring and measures properties of the discourse itself. The pre-registered
expectation is that Tier 2 source populations will be too small for powered population-level
claims — which makes Branch C the modal outcome and Branch S a per-source description with wide
intervals rather than a ranking. Pre-registering that expectation before seeing the data is the
only way the eventual answer means anything.

## Two options, held open

Not commitments. Trigger conditions, written down in advance so that enthusiasm doesn't get to
make the call:

- **Epistemic credentials as a portable, opt-in asset** — the involuntary ledger becomes
  voluntary once being in it is worth something.
- **AI-evals and AI-for-epistemics infrastructure** — the claim-resolution pipeline is
  general-purpose measurement machinery, and the market for that is arriving independently.

There are also explicit project-level kill criteria, including a passion-decay tripwire.
Knowing in advance what would make this not worth continuing is a feature.