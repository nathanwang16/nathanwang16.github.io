# A Browser for the Small Web — See the Shape of a Corpus Before You Read It

*Hypergraph knowledge discovery over multi-source crawled corpora. Highly personalized ways
of selecting and absorbing information. Information as means and ends.*

![Infolake interface](images/UI.png)

## The problem it actually solves

Search gives you ranked documents. Feeds give you what engagement predicts you'll click. Both
answer the question "what should I read next," and neither answers "what is out here, and how
is it arranged." For anything genuinely unfamiliar, the second question is the one that
matters — and answering it by reading serially is hopeless, because you cannot know what
you're missing from inside a list.

So: render the corpus as a space, and let the eye do the work it is good at. Dense regions are
consensus or repetition. Bridges between regions are the interesting documents. Sparse regions
are either a real gap or a crawl failure, and telling those two apart is a genuine research
question rather than a UI detail.

The bias toward the **small web** is deliberate. Independent blogs, personal sites, forums,
niche archives, papers — the parts of the internet that platform recommendation has no
incentive to surface. That's where the marginal information is.

## Pipeline

**Acquisition — infocrawl.** A contract-based adapter layer rather than a monolithic crawler.
Every source implements the same protocol and declares its own capabilities as data; the
framework uses that declaration for routing, documentation, and CLI generation, so there is no
parallel document to keep in sync. All adapters emit one unified `DocumentRecord` schema.
Crawl4AI serves as the generic web adapter; API-native sources get purpose-built adapters;
synchronous libraries are first-class rather than second-class. A capability-aware dispatcher
routes static targets to a fast HTTP path instead of spinning up a browser, which is the
single highest-leverage performance decision in the system. Anti-bot handling escalates
through explicit tiers rather than pretending the problem doesn't exist.

**Storage.** A hypergraph in SQLite — hyperedges because the relations that matter between
documents are genuinely n-ary, not pairwise. SQLModel and Alembic for schema and migrations.
Per-adapter sidecar tables hold source-specific engagement metadata so the core document
schema stays clean. Wide metadata retention is a deliberate policy: it is cheap now and the
analyses you'll want in two years are not the ones you can name today.

**Representation.** Sentence embeddings over chunked documents, then UMAP for projection and
HDBSCAN for clustering. HDBSCAN specifically because it declines to assign points it doesn't
believe in — clusters should be allowed to not exist, and "unclustered" is information.

**Interface.** A deck.gl rendering of the hypergraph, built to stay interactive at corpus
scale rather than to look good in a screenshot.

**Taxonomy.** `world_taxonomy_tree` is the backbone for topic classification — a merge of
several open-source taxonomies into one usable spine, so cluster labels can be anchored to
something external instead of being re-invented per corpus.

## Design principles, contractually encoded

1. **Never reinvent the wheel.** The framework is small; almost all functionality lives in
   dependencies. If a mature library does it, wrap it.
2. **Single source of truth.** Documentation, scripts, and contracts derive from one place.
   Capabilities are declared as data, never duplicated in prose.
3. **Optimize within real hardware constraints.** A Mac mini does acquisition; the GPU box
   does embedding and inference. Nothing in the design assumes a cluster that doesn't exist.

## Open and honest

SQLite as the primary store holds to tens of millions of documents in WAL mode with care —
past that the plan is DuckDB or Postgres, and the migration should be designed for before it
is needed rather than after. The unresolved question that matters most is the **discovery /
frontier seam**: where the boundary sits between "the crawler decides what to fetch next" and
"the pipeline decides what is worth having." That is an architectural fork, not a tuning
parameter.

Repository: https://github.com/nathanwang16/infolake
Taxonomy: https://github.com/nathanwang16/world_taxonomy_tree