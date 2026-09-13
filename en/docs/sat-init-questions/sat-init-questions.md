# sat-init-questions

​                   * Good framing — that's exactly what the cascade spec calls for ("sat init reads each node's children to   decide what to descend into, rather than carrying a fixed five-tier shape... the self-referencing tiers are configuration, not a special case in the code"). One shared node-creation operation, invoked at whatever role you start from. Here's what I'd want settled or supplied before writing it, grouped by what kind of decision each is.

  Spec conflicts this mechanism can't stay silent on. The cascade spec lists these as genuinely open, and a general init routine has to pick an answer rather than special-case around them:
  - How many author folders the instance root carries — "one" is what we built satx with (matches every worked example), but it's still listed as an unresolved conflict between two decided statements. Worth formally ruling before init encodes it, so the doc and the code agree.
  - Whether directory and content belong in sat's children — decides whether sat init can produce a bare instance with a directory or content node directly under root, or only ever collections/archives.
  - Whether roles is declared at every node or only the root — decides what init writes into a non-root node's own config.yml.
  - Whether a collection may hold both collections and archives as children at once, or one kind per collection — decides what a preseed for a collection is allowed to ask for.

  The shape of the mechanism itself. This is really your call, not something the spec answers:
  - One command that inspects where it's pointed and infers the role to create, or a family of thin per-role commands (sat init, collection init, archive init, directory init, content new) sharing one library function underneath? The old sat/ repo used the latter shape.
  - Does creating a tier build everything beneath it in one pass from a preseed manifest (the old repo leaned hard on these — collection-preseed.yml.example, archives-parent.yml), or does each tier get created one command at a time as you descend? This is the biggest scope decision: a preseed format is a new thing to design from the sidecar spec, not something satx's docs already specify.

  What seeding actually writes, per role, since the two specs describe genuinely different behavior at each level and I want real values rather than guessing:
  - At sat (a brand-new instance): config's root defaults already ship populated, so seeding is nearly silent — mostly just sat_version and whatever interface_language/default_metadata you want it to ship with.
  - At collection/archive/directory: language at an archive is the one field that's genuinely mandatory and locked, so that always prompts. Anything else (rights, publisher) is your call whether to prompt or leave inherited.
  - At content: this is real prompting territory — title, date, and friends seed as <notset> and drive the prompt-on-<notset> rule directly.

  Identity minting, which the spec states at a level of generality that leaves a gap: "sat mints for sat, then passes requirements and defaults to collection, which mints collections" — but identifier/isVersionOf are explicitly content-node concepts. What does minting concretely produce for a collection or archive? Just a slug, or some other identity the work index's "nearest collection root" scoping depends on? I'd want this pinned down before writing the mint step.

  Concrete inputs for the actual test HANDOVER names (satx/bin/sat init ../saty): a target path, and whether saty should ship the same rights/publisher/interface_language as satx or deliberately different values, so the test proves init isn't just hardcoding satx's own specifics.

  Given where credits stand, I'd suggest scoping the first version to exactly HANDOVER's test — sat init producing a bare new instance skeleton, no collections or archives yet — and treating the
  preseed/bulk-creation question as a separate decision once that's working. Want to go that route, or do you already have answers to the bigger design questions above?