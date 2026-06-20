# Model Toolkit

Use this file to select, formalize, and check game theory models.

## Model Identity Report

Always classify the model before solving:

1. Can players make binding agreements?
   - Yes: cooperative game; consider core, Shapley value, bargaining.
   - No: non-cooperative game.
2. Are key decisions simultaneous or sequential?
   - Simultaneous: static game.
   - Sequential/observable stages: dynamic game.
3. Do players know payoffs, types, and rules?
   - Complete information: NE or SPNE depending on timing.
   - Incomplete information: BNE or PBE depending on timing.
4. Do players observe previous actions?
   - Perfect information: use backward induction/SPNE when dynamic.
   - Imperfect information: use information sets and beliefs; PBE may be needed.
5. Are strategies discrete or continuous?
   - Discrete: payoff matrix, dominance, mixed strategies.
   - Continuous: optimization, best responses, FOCs, SOCs, fixed points.
6. How many players?
   - Two players for a clean first model.
   - N players if N itself matters.
   - Large population if evolution or mean-field effects matter.

## Common Model Families

- **Cournot**: quantity competition, strategic substitutes, continuous strategies, NE.
- **Bertrand**: price competition, differentiated products/capacity constraints often needed for nontrivial results.
- **Stackelberg**: leader-follower timing, commitment, backward induction, SPNE.
- **Hotelling**: spatial/product/political positioning with differentiation.
- **Repeated game**: cooperation, punishment, reputation, discount factor thresholds.
- **Signaling game**: hidden type + costly signal + receiver action, PBE, separating/pooling equilibria.
- **Principal-agent**: hidden action/type, incentive compatibility, participation constraint, contract design.
- **Auction/mechanism design**: rule design under private information, IC/IR, revenue/welfare.
- **Evolutionary game**: bounded rational populations, replicator dynamics, evolutionary stability.
- **Differential game**: continuous-time controls and state variables, HJB, feedback equilibrium.
- **Network game**: peer effects, diffusion, centrality, local/global interactions.
- **Cooperative game**: surplus allocation, coalition stability, Shapley/core.

## Function Choice Principles

Choose function forms by three criteria:

1. **Analytical tractability**: the model must yield interpretable equilibrium conditions. Prefer linear demand, linear/quadratic cost, or linear-quadratic dynamic forms for first drafts.
2. **Economic intuition**: the function's implicit assumptions must match the phenomenon. Quadratic cost implies increasing marginal cost; log utility often implies diminishing marginal utility/risk aversion; Cobb-Douglas captures input trade-offs and scale properties.
3. **Literature continuity**: standard forms help readers compare your model with established results. Deviate only when the new function is central to the contribution.

When using a nonstandard form, justify it with either real-world mechanism, literature precedent, or robustness motivation.

## Baseline Payoff Patterns

Use these patterns as starting points and adapt notation to the research question:

- Profit: `pi_i = revenue_i - cost_i - penalty_i + subsidy_i`.
- Demand with preference: `Q_i = market_size - own_price_effect + cross_price_effect + preference_effect`.
- Effort/investment cost: convex cost such as `(k/2) e_i^2`.
- Welfare: `W = consumer_surplus + producer_surplus + external_benefit - external_damage - policy_cost`.
- Principal-agent utility: principal payoff from output minus transfer; agent utility from transfer minus effort cost, with IC and IR constraints.
- Signaling payoff: type-dependent benefit minus signal cost, with receiver belief updating.
- Dynamic state: `dot S = accumulation from effort/investment - depreciation/decay`.

## Solving Checklist

For continuous strategy models:

1. Define domains and parameter restrictions.
2. Write each player's objective.
3. Derive FOCs or best responses.
4. Check SOCs, concavity, or Hessian conditions.
5. Solve the system.
6. State equilibrium and parameter restrictions.
7. Perform comparative statics on key parameters.
8. Interpret each derivative economically.

For sequential games:

1. Draw or describe timing.
2. Solve final stage first.
3. Substitute follower reaction functions backward.
4. Solve leader decisions.
5. State SPNE/PBE and beliefs if incomplete information exists.

For signaling/screening:

1. Define types, priors, messages/signals, actions, payoffs.
2. Specify beliefs and updating.
3. Check incentive compatibility for each type.
4. Check participation/individual rationality if contracts are used.
5. Distinguish separating, pooling, and semi-separating candidates.

For differential games:

1. Define state variable and law of motion.
2. Define controls and instantaneous payoffs.
3. Choose open-loop or feedback equilibrium.
4. Write HJB equations for feedback equilibrium.
5. Guess value function only when justified by linear-quadratic structure.
6. Solve control rules and steady state.
7. Interpret dynamic paths, not just steady states.

## Comparative Statics

Choose 3-5 parameters that map to the paper's mechanism:

- Market size or baseline demand.
- Cost or investment efficiency.
- Preference/sensitivity.
- Policy instrument: tax, subsidy, penalty, audit intensity.
- Information quality or signal precision.
- Discount factor.
- Externality intensity.
- Network effect.

For each result, output: derivative sign, threshold condition if any, economic intuition, and implication for theory/policy/management.

## Robustness And Extensions

Use extensions to test the main mechanism, not to start a new paper.

Good robustness moves:

- Replace linear demand with a more general decreasing demand and show the sign condition still holds.
- Add cost heterogeneity.
- Add a third player such as regulator/auditor/platform only if it tests the mechanism.
- Compare complete vs incomplete information.
- Convert one-shot to repeated game if reputation or long-term cooperation matters.
- Add numerical simulation when closed-form results are too complex.

## Intractability Triage

If the model is hard to solve:

1. Diagnose the issue: algebraic complexity, non-concavity, multiple local optima, no pure-strategy equilibrium, or incompatible timing/information.
2. Prefer strategic simplification for a first draft:
   - Use linear demand.
   - Use linear or quadratic costs.
   - Reduce players to two.
   - Discretize strategy space.
   - Move extra mechanisms to extensions.
3. If complexity is the contribution, shift to numerical equilibrium and visualize comparative statics.
4. If equilibrium nonexistence is real, prove nonexistence and frame instability as the result.

## Red Flags

- A new parameter changes notation but not equilibrium logic.
- Payoff terms have no economic interpretation.
- Parameter restrictions are missing.
- The claimed policy implication is not backed by welfare analysis.
- A model assumes complete information while the motivation is information asymmetry.
- A dynamic phenomenon is forced into a static model without justification.
- A result relies entirely on a special function but no robustness check is offered.
