# A-P intake — independent package/history/oracle audit

Target: `v0.3.7-candidate.2`

Frozen source: `bda470e0a6b170cec61225a905957a501454a2fe`

Frozen candidate subtree: `d5fefc8c786d7e40b3e9a59211ee7045bccee5bf`

Prior A-S content seal has been independently verified and persisted externally before this A-P stage was exposed.

## Task

Audit the full frozen candidate package now present under `releases/v0.3.7-candidate/`.

A-P is not a second blind A-S. Its job is to inspect package-local material that was intentionally withheld from A-S, including where present:

- candidate self-description, identity and status claims;
- lineage and repair/history narrative;
- fixtures, selftests, regression oracles and expected outcomes;
- package claims versus actual frozen bytes;
- contradictions, stale claims, misleading confidence, or package-local evidence that materially changes interpretation of the frozen candidate.

You may run the package's own tests and inspect all files in this repository state.

Preserve the already sealed A-S attack tree as fixed occurrence truth. You may note whether package-local material confirms, contextualizes, contradicts, or adds to it, but do not rewrite the A-S report.

Do not perform project-manager Phase B, do not classify author/shared blind spots on behalf of the project manager, do not repair the candidate, and do not seek the source project repository or external project history.

## Output

Produce one final report named conceptually `candidate2-independent-a-p-primary-r3.md` containing:

1. review identity and boundary;
2. package/self-description/oracle findings;
3. any confirmation/context relevant to the fixed A-S findings;
4. final A-P disposition;
5. explicit statement that Phase B was not performed.

After the report is final, compute SHA-256 over the exact report bytes and return that digest **externally** (or in a sibling `.sha256` sidecar). Do not embed the digest inside the bytes being hashed.

Then STOP.
