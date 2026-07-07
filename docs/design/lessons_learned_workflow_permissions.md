# Non-Obvious Lessons Learned: CI Workflow Token Permissions

## Context

GitHub Advanced Security (Code Scanning) flagged multiple workflow files in `.github/workflows/` with the alert: "Workflow does not contain permissions." Specifically, files like `freshness-check.yml`, `pytest.yml`, `release-cooldown.yml`, and `spec-consistency.yml` were operating without explicitly declared `permissions` blocks.

## The Challenge

The absence of a `permissions` block does not mean a workflow executes without permissions; it means the workflow executes with the default permissions granted to the `GITHUB_TOKEN`. Depending on repository settings, this default can silently escalate to broad read/write access across the entire repository. This violates the principle of least privilege and introduces a latent confused-deputy vector if a third-party Action is compromised.

## The Resolution (Topological Novelty)

While the parsimonious (Occam's) approach would be to ignore the alert because "the builds were passing," this allows the runtime environment to dictate the security posture rather than the codebase.

The antifragile solution implemented explicitly bounds the execution perimeter:
1. **Explicit Scoping**: The `permissions: contents: read` block (or `pull-requests: read` / `issues: write` as specifically required) was explicitly added to the top level of all 14 workflow files.
2. **Deterministic Infrastructure**: CI workflows are now treated as deterministic infrastructure contracts. The authorization boundary is hardcoded, eradicating the interpretive fracture of implicit default settings.

## Symbolic Scar Registry (SSR) Entry

```yaml
SSR-20260706-001:
  trigger: "GitHub Actions workflow executed without explicit `permissions` block defined at the top level."
  failure_mode: "Code Scanning Alert — Workflow does not contain permissions. Latent privilege escalation vector via default `GITHUB_TOKEN` provisioning."
  prevention_directive: |
    ⚠️ WARNING SSR-20260706-001:
    Every workflow MUST explicitly declare its `GITHUB_TOKEN` permissions.
    Implicit scoping is treated as an Epistemic Void.
    Minimum baseline for standard workflows:
    ```yaml
    permissions:
      contents: read
    ```
  severity: "HIGH"
```

## Future Directives

All future CI/CD orchestration files must abide by this explicit boundary enforcement. Implicit token scoping is forbidden. Any new workflow introduced to `.github/workflows/` must pass a structural review ensuring the `permissions` block is defined with the absolute minimum scope required for its operation.
