## Task — difference-in-differences

We have a state-year panel recording, for each state and year, whether a policy
was in force and the level of the outcome. Implement a difference-in-differences
design appropriate for state-year panel data, accounting for time-invariant unit
characteristics and common year shocks.

Data: `{data}`

- Treatment: `treat` (1 = policy in force)
- Outcome: `y` (standardised)
- Identifiers: `unit`, `year`, `region`
- Covariates: `x1`–`x4`, `pop`
