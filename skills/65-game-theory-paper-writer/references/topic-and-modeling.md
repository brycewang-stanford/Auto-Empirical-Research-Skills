# Topic And Modeling

Use this file when the user provides only a topic, a phenomenon, one or more anchor papers, or asks for a new game theory paper idea.

## Integrity Boundary

Transform ideas through transparent research practice:

- Cite every anchor paper or borrowed mechanism.
- Explain what is kept, changed, and newly contributed.
- Re-derive the model instead of copying algebra or prose.
- Avoid cosmetic renaming as a contribution. A valid contribution changes scene, player structure, assumptions, timing, information, method, or key factor in a way that changes interpretation or equilibrium implications.

## Five Research Question Routes

1. **Theory migration**: apply a mature model to a new domain whose strategic logic matches the model. Good for first papers when the mapping is strong.
2. **Model modification**: start from an important anchor model and relax, replace, or add one key assumption. Good when the anchor has clear structure and known limitations.
3. **Phenomenon driven**: start from a puzzling real case and build the smallest model that reproduces the core mechanism. Good for new technologies, platforms, regulation, AI, sustainability, and digital markets.
4. **Method fusion**: combine two compatible tools, such as repeated game + signaling, principal-agent + market competition, evolutionary game + platform governance, or game theory + empirical estimation.
5. **Conclusion rebuttal**: identify a canonical result and show the conditions under which it weakens, reverses, or disappears after adding a realistic mechanism.

Score each route from 1-5 on tractability, novelty, literature fit, real-world importance, and ability to produce clear propositions.

## A-F Deconstruction Framework

Use this to read an anchor paper or build a new model.

- **A Scene**: market, organization, policy regime, network, platform, supply chain, environmental governance, AI ecosystem, etc.
- **B Players**: firms, consumers, platforms, workers, creators, government, regulator, auditor, investor, principal, agent, sender, receiver.
- **C Conditions**: information, rationality, risk preference, cost/demand forms, capacity, liability, observability, commitment, regulation.
- **D Process**: simultaneous, sequential, finite repeated, infinite repeated, continuous time, dynamic state transition.
- **E Methods**: NE, SPNE, BNE, PBE, HJB/MPE, replicator dynamics, mechanism design, Shapley/core, numerical simulation.
- **F Factors**: market size, cost, sensitivity, preference, discount factor, audit accuracy, penalty, subsidy, externality, network effect, algorithm quality.

Innovation usually comes from changing one or two modules while keeping the rest simple enough to solve.

## One-Anchor Literature Workflow

Use when the user provides one paper or asks to build from a known model.

1. Identify the anchor's A-F modules.
2. List the anchor assumptions that are both important and simplifying.
3. Choose one legitimate change:
   - New scene with the same strategic logic.
   - New player, such as government, platform, auditor, consumer association, AI agent, insurer, or data intermediary.
   - New condition, such as incomplete information, bounded rationality, capacity constraint, limited liability, heterogeneity, or risk aversion.
   - New process, such as converting static to sequential, one-shot to repeated, or discrete time to continuous time.
   - New factor, such as ESG preference, privacy concern, data quality, carbon penalty, audit accuracy, reputation, or network externality.
4. Rebuild notation and payoff functions from the new economic logic.
5. Re-solve the model and compare with the anchor result.
6. State contribution as: "Compared with [anchor], this paper changes [module], which makes [mechanism] endogenous and yields [new implication]."

## Multi-Paper Synthesis Workflow

Use when the user provides several papers or asks to integrate models.

1. Pick one **base model** as the spine. It should be foundational, structurally clear, and extendable.
2. Extract one mechanism from each additional paper, not the whole paper.
3. Check compatibility before combining:
   - Same or convertible timing?
   - Same information assumptions, or a deliberate transition?
   - Same level of rationality?
   - Units and signs consistent?
   - Concavity/second-order conditions still plausible?
   - Additional mechanism changes equilibrium predictions, not just notation?
4. Add mechanisms one at a time. After each addition, verify solvability and contribution.
5. Prefer a clean two-module synthesis over an overloaded model.

Common synthesis modules:

- Preference insertion: add ESG, fairness, privacy, risk, reputation, or quality preference to demand/utility.
- Competition insertion: turn monopoly into duopoly/oligopoly with cross effects.
- Sequential insertion: add leader-follower timing, contract then market competition, or regulation then firm decisions.
- Behavioral insertion: replace pure money payoff with fairness, loss aversion, social image, or bounded rationality.
- Uncertainty insertion: add state probability, type distribution, audit error, demand shock, or technology success probability.
- Dynamic insertion: add a state variable such as reputation, data stock, goodwill, pollution stock, trust, or knowledge capital.
- Signal insertion: add costly signaling, audit, certification, disclosure, or screening constraints.

## Reality-To-Model Workflow

Use when the user gives a phenomenon such as AIGC, platform governance, digital labor, green supply chain, blockchain tracing, data privacy, algorithm regulation, or market quality screening.

1. **Reality deconstruction**
   - Background: What happened and why now?
   - Players: Who chooses strategically?
   - Actions: What are the few key decisions?
   - Payoffs: What does each player maximize or avoid?
   - Conflict: What trade-off, externality, information asymmetry, or time inconsistency drives the puzzle?
   - Observable implication: What real behavior should the model explain?
2. **Candidate model screening**
   - Static simultaneous game: use for one-shot symmetric competition.
   - Stackelberg/dynamic game: use when one actor commits first or regulates first.
   - Principal-agent: use when effort/action is hidden and incentives matter.
   - Signaling/screening: use when type/quality is hidden and costly signals matter.
   - Repeated game: use when future punishment/reputation sustains cooperation.
   - Evolutionary game: use when bounded rational groups update strategies over time.
   - Differential game: use when a state stock evolves continuously, such as data quality, pollution, goodwill, trust, or knowledge.
   - Mechanism design/auction: use when the research question is optimal rule or contract design.
3. **Choose the smallest viable model**
   - Keep only the players and variables needed to reproduce the core phenomenon.
   - Use standard linear/quadratic forms unless the phenomenon requires otherwise.
   - Add complexity as robustness or extension, not in the main model.
4. **Produce research question**
   - "How does [new mechanism] affect [player decisions/equilibrium/welfare] in [scene]?"
   - "Under what conditions does [counterintuitive outcome] emerge?"
   - "What policy/contract/platform rule maximizes [welfare/profit/sustainability] when [information/timing/externality] exists?"

## Candidate Topic Output Template

For each candidate topic, output:

- Title.
- Research question.
- Real-world motivation.
- Closest literature family and required citations.
- Model type and equilibrium concept.
- Players, strategies, timing, information, payoffs.
- Core mechanism.
- Expected propositions.
- Comparative statics.
- Possible simulation or case.
- Why this is new relative to the anchor literature.
- Main risk and how to simplify if needed.
