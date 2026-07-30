# Creating a Toy Universe With Nothing In It, Except Proteins

*AlphaFold and protein language models give an atomic-resolution picture of what a protein
looks like. Function is motion. This is a research program about whether the second thing is
recoverable from the first — and about building a universe where the answer is known by
construction, so that an interpretability method can be calibrated instead of merely
demonstrated.*

---

## The core ideas

**1. The counting argument.** A system's equilibrium distribution says how much time it spends
in each state. Its generator says how fast it hops between them — the generator *is* the
dynamics. There are far more generators than there are equilibrium distributions consistent
with them, so knowing where a system sits does not tell you how it moves. Generically, many
distinct dynamics produce identical static data. This is arithmetic, not a modeling
limitation, and it is the load-bearing observation of the whole program.

**2. Two failure modes that look identical in a loss curve and are different in kind.** This
distinction is the actual contribution.

- **Gauge — the dynamics is unidentified.** Several generators are exactly consistent with
  everything the data can see. A model trained on that data will commit confidently to one of
  them. Signature: well-calibrated, and wrong. It is not uncertain, because nothing in its
  training data gave it a reason to be.
- **Channel — the information was deleted en route to the dataset.** The universe was fine; the
  observation process censored it. Signature: wrong in a specific *region*, and if the model is
  well-behaved, unconfident there.

Conflating these is the standard error. They demand different fixes — better priors versus
better instruments — and one of them is unfixable.

**3. Tilt versus truncation.** Censoring splits, and the split has teeth. **Tilt** reweights:
some states are over-represented, but every state still appears, so the distortion is invertible
in principle. **Truncation** deletes: a region has exactly zero probability of being observed,
positivity fails, and no amount of data or cleverness recovers it. Tilt is a hard estimation
problem. Truncation is an impossibility theorem. Knowing which one you have is the difference
between "try harder" and "stop."

**4. The toy universe is a calibration standard, not a small protein.** The naive framing —
build a tiny protein, study it — invites a fatal and correct objection: your toy is not a
protein. The reframe kills the objection outright. A known-mass weight is not a scale model of
the thing you plan to weigh; it is the object you check the scale against. Apply an
interpretability method where the answer is known exactly, and you measure that method's
sensitivity and false-positive rate. That is a result *about the method*, and it travels
wherever the method is used without any resemblance argument.

This also redefines difficulty, usefully: you tune the universe to break the **interpretability
method**, not the model. Those are different axes. A universe can be trivially easy to learn
and adversarial to a sparse autoencoder — and nobody can currently measure the second axis at
all.

**5. The matched grid.** Two things can be varied independently, so the minimum viable design is
2×2, not a pair. The **gauge** axis changes the dynamics while holding fixed everything the data
can see — detailed-balance versus circulating, same equilibrium distribution. The **channel**
axis holds the universe fixed and changes what gets recorded — uncensored versus dwell-censored.
One axis alone confounds the two failure modes above. Every cell has an exactly known answer,
which is the entire reason for building a universe rather than using a real dataset.

**6. The ground-truth ladder — always know which rung you're on.** *Exact*: small enough to
enumerate, so the generator is an explicit matrix and mean first-passage times and the full
relaxation spectrum come from linear algebra, with no error bars. *Sampled*: too big to
enumerate, so long trajectories and bootstrap intervals. *Asymptotic*: too big for that, but a
limit theorem applies — barrier-crossing asymptotics, escape rates, critical-point counting.
*Universal*: only exponents survive, but they survive provably.

One correction matters and is easy to get wrong: the universal rung must use **dynamic**
exponents. Static exponents are *constructed* to be insensitive to dynamics — using them to
certify a claim about the generator is circular. Static exponents check that your sampler works.
That is a different job.

**7. Channel-indexed transfer beats universality-class transfer.** The usual physics transfer
argument requires the toy and the target to share a universality class — a strong claim, usually
unverifiable for a protein, and the first thing a reviewer attacks. A result of the form
"channel *M* at severity *λ* costs *f(λ)* in recovering quantity *Q*" instead travels to any
domain that shares the **channel**, and channels are far more portable than Hamiltonians.
Dwell-time-weighted observation is dwell-time-weighted observation whether the objects are
proteins, galaxies, patients, or hedge funds — the same structure appears as Malmquist bias in
astronomy, ascertainment bias in epidemiology, publication bias in meta-analysis, and
survivorship bias in finance. That is a structural upgrade, not a rhetorical one.

**8. The prize is impossibility, not a benchmark win.** "Our models did badly" invites "you
didn't try hard enough." "The information is not present in the data" does not — it constrains
every future method, including ones nobody has built, and cannot be defeated by a better
architecture. Truncation supplies exactly this: provable non-identifiability rather than
empirical failure. Existence results are nearly as good, since one concrete counterexample kills
a universal claim regardless of whether the toy resembles anything real. The ambition when the
rig produces a failure is to characterize the *geometry* causing it, not to report the loss
curve.

**9. The honest boundary condition.** State this early, because it pre-empts the sharpest
available objection: **near equilibrium, statics genuinely does determine dynamics.** The
fluctuation–dissipation theorem and the Green–Kubo relations are theorems, not loopholes — nudge
a system gently and its response is fixed by its equilibrium fluctuations. So the program's claim
is not that static data is uninformative. It is that the far-from-equilibrium content — rare
events, barrier crossings, the shape of the transition network — is where identifiability breaks,
and that this is precisely the content that protein *function* lives in.

---

## Why proteins

Because it is the field where the gap is most consequential and most visible. Structure
prediction is essentially solved as a static problem, and the community has largely absorbed the
lesson that function is dynamics. What has not been absorbed is that the static-to-dynamic
inference has a *measurable* information budget, and that some of it is provably empty. The
statistical-mechanics literature on foldability and rugged landscapes provides analytic ground
truth about exactly the objects censoring destroys — saddles and shallow minima — at system
sizes far past enumeration. That lets one say quantitatively what is in the hole in the dataset,
rather than merely noting that there is a hole.

## Status

Active, at the specification-and-design stage. The idea catalogue runs to roughly a hundred
entries across seven tiers — substrates for toy universe design, measure theory, generator and
dynamics theory, missing-data and identifiability, experimental design, and transfer arguments.
Known open problems include a space mismatch in the neural-tangent-kernel-as-mobility conjecture
(the kernel acts on function space, the mobility on probability measures over state space), an
imprecision in the persistent-homology-to-circulation link (topological cycles of sublevel sets
are not cycles of the transition graph), and a gauge-choice risk in the cycle probe's
rate-extraction step, which argues for reporting two independent extraction methods as a control.

Collaborators and critics both welcome, the second more urgently: nathan16@ucla.edu

