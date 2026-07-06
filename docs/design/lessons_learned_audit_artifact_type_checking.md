# Non-Obvious Lessons Learned: Audit Artifact Type Checking

## The Challenge

During the implementation of Phase 6.3 validation logic, an implicit coercion was discovered in the way the Material Passport's `audit_artifact` was handled. The `_load_passport_audit_artifacts` function in `scripts/_next_verified_at_ms.py` was silently coercing an `audit_artifact` that was present but malformed (not a list) into an empty list (`[]`).

## The Resolution (Topological Novelty)

While this silent coercion provided a "forgiving" behavior, it fundamentally eroded the structural integrity of the Material Passport contract (specifically Rule §3.7 E2). By masking the structural error, it allowed malformed passports to persist unnoticed.

The antifragile solution implemented here rejects this parsimonious (Occam's) approach of silent correction. Instead, we enforce strict type checking:

1.  **Fail-Fast Enactment**: In `scripts/_next_verified_at_ms.py`, if `audit_artifact` is present but is not a list, we now raise a deliberate `ValueError`, triggering a loud failure rather than silent corruption.
2.  **Structural Governance**: In `scripts/check_audit_artifact_consistency.py`, we implemented a dedicated linting trap (Rule E2) that explicitly catches this exact structural violation and reports it back to the orchestrator layer.

## Paraconsistent Epistemic Weaving

This update recognizes that a missing field (`None`) and a malformed field (e.g., a string or an object instead of a list) are fundamentally different states. A missing field implies a new or clean passport, whereas a malformed field indicates a breakdown in the upstream generation process. By creating distinct handling paths for these states, we've increased the Topological Novelty of our validation matrix while enforcing absolute Structural Conservation (β0 > 0.9).

## Future Directives

All future validators must abide by this strict type-boundary enforcement. Silent coercion of complex types into empty iterables is now treated as an Epistemic Void and must be rejected at the boundary layer.
