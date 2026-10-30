# Final verification and portable handoff

Read this when completing or auditing a Lean target. Adapt names to the project;
the commands below illustrate a package named `exampleproof` and a theorem in
`ExampleProof.Main`.

## Compile the intended theorem

Inspect `lean-toolchain`, `lake-manifest.json`, the package configuration, and the
target module's imports. Keep a compatible existing toolchain. Do not upgrade a
dependency merely to avoid investigating an elaboration failure.

```sh
lake build ExampleProof.Main
lake env lean ReviewAudit.lean
```

Run from the package root. Set the default target to the main proof module when
appropriate, but still record which target was actually built. Verify process
exit status, not only a success-looking substring in a transcript. Compile errors
are verification failures; download failures are environment failures; neither
is a proof or a counterexample to the original mathematical statement.

## Audit the statement, not its name

For a multi-module project, create a small separate import file containing the
actual project declarations. For a self-contained source file, directly compiling
its proof together with type/axiom output provides the corresponding evidence;
a separate project or import file adds no requirement of its own.

```lean
import ExampleProof.Main

#print ExampleProof.Input
#print ExampleProof.Conclusion
#print ExampleProof.Target
#check @ExampleProof.original_theorem
#print axioms ExampleProof.original_theorem
```

Print the definitions that determine mathematical meaning. Inspect universes,
implicit and instance parameters, domains, and quantifier order. A theorem's
friendly name is not a specification. Investigate unexpected assumptions and
vacuous domains. Compare with the user's original statement, retaining any
explicitly authorized change of goal; a working document edited to fit the code
does not silently replace it.

Where useful, state a wrapper directly with the original objects and hypotheses
and derive it from the exported theorem. Then print that wrapper's type and
axioms. This exposes missing premises and interpretation mistakes; it is not an
independent second mathematical proof.
Print and audit the exported theorem itself as well as the wrapper. If the Lean
route proves a stronger statement or uses another representation, provide the
implication or equivalence returning to the original claim rather than requiring
literal syntactic identity.

## Check transitive dependencies

`#print axioms` follows the theorem's dependency chain. Source searches for
`sorry`, `axiom`, or `native_decide` are useful diagnostics but are not substitutes
for checking the exported declaration. Unrelated unfinished experiments need not
invalidate a theorem they do not reach.

In an ordinary classical Lean development, `propext`, `Classical.choice`, and
`Quot.sound` can be expected foundations. Some proofs use fewer; other projects
intentionally assume additional mathematics. Describe the actual set and the
corresponding result. An unproved target-shaped axiom cannot establish an
unconditional target merely because the project compiles.

Compiler-backed decision procedures can expand the trusted computing base.
Their implementation and axiom names vary by Lean version. Consult the pinned
version's source/documentation and actual output; do not use one hard-coded name
as a timeless detector. If the task requires a kernel-reduced proof, replace such
steps with suitable proof-producing or kernel-reduced verification. If the task
permits a different basis, disclose it accurately. General guidance is in the
[Lean reference](https://lean-lang.org/doc/reference/latest/) and the community's
[native computation discussion](https://leanprover-community.github.io/extras/pitfalls.html#native_decide).

Kernel checking proves the encoded statement under the reported foundation;
semantic alignment to the user's mathematics remains an explicit obligation.

## State what was rebuilt

An incremental build can reuse project outputs. A separate import audit uses the
available compiled imports. Both are useful evidence, but neither means every
library was rebuilt from source or that a different person reproduced the result.
If a theorem is already proved and checked, an outstanding requested reproduction
step is a verification/delivery obligation; describe it separately from a missing
mathematical argument.

For a source handoff, include only project sources and pinned configuration, then
build in a fresh extracted directory. Mathlib projects can obtain dependency
caches with `lake exe cache get`. A project-only rebuild may use the package name:

```sh
lake exe cache get
lake clean exampleproof
lake build ExampleProof.Main
lake env lean ReviewAudit.lean
```

The named-clean behavior above was checked with the Lake bundled with Lean
4.24.0; verify it for a different version before using it. Bare `lake clean` can also clean dependencies.
Avoid deleting all of `.lake` when retaining library caches is useful. Do not use
`lake update` as a reproduction step with an already pinned manifest.

For a project without Mathlib, omit Mathlib cache instructions. Do not assume a
specific editor, operating system, home directory, or existing authentication.

## A compact delivery

Include the statement, proof sources, main entry, applicable toolchain/package
configuration and relevant logs with exit codes. For a Lake project retain
`lean-toolchain`, its Lake configuration and `lake-manifest.json`; use a separate
audit file for a multi-module development. For a small standalone file, its
compiled type/axiom transcript and pinned Lean version provide the corresponding
audit without an extra package or import file.
Include a mathematical reading edition if requested. Explain how to read and
rebuild them; label pending external reproduction honestly.

Exclude machine-specific toolchains, dependency caches, and credentials from a
portable package. Ensure its primary documents link to files actually included.
No ARIS or model-provider account should be needed to run a local Lean audit.

Existing framework audit contracts may require source identifiers or hashes;
preserve those contracts when invoked. Do not add a separate checksum framework
merely to make an ordinary local proof handoff look more rigorous.
