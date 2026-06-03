Do not run the README commands on your laptop as written.

Safe protocol:

1. Treat the anonymous package as untrusted code. Download `setup.sh` as a file,
   do not pipe it directly into `bash`.
2. Inspect `setup.sh`, `run_all.sh`, and every script they call before execution.
   Look for network writes, credential reads, shell escapes, deletion commands,
   and attempts to modify files outside the project directory.
3. Create an isolated environment: a disposable container or VM with a fresh
   checkout, no personal files mounted, and network disabled unless a specific
   data fetch has been reviewed and approved.
4. Do not put real AWS credentials, production credentials, tokens, or personal
   secrets in `.env`. If the code genuinely needs cloud access, use dummy
   credentials for dry runs first, then a temporary least-privilege credential
   scoped to a read-only bucket and revoke it after the test.
5. Run the package in stages after inspection: environment setup, data download,
   data build, tables, figures. Log stdout/stderr and file hashes after each
   stage so failures are reproducible.

Only after the scripts are inspected and a sandboxed dry run succeeds should the
package be considered for a trusted replication machine.
