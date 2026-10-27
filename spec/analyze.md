# Task, Risk, and Dependency Analysis

**Review date**: 2026-10-27
**Status**: Analysis of draft planning artifacts; no requirements or policy decisions are approved by this review.
**Reviewed**: [constitution.md](./constitution.md), [specification.md](./specification.md), [clarify.md](./clarify.md), [plan.md](./plan.md), and [tasks.md](./tasks.md), with the original [project_spec.md](../project_spec.md) and [backlog.md](../backlog.md) as scope references.

## Executive Assessment

The task list has strong safety intent, broad phase coverage, and a useful decision-first structure. It contains **45 tasks** across eight phases. The largest risks are unresolved policy decisions (catalog ownership, identity, runner boundary, environments, Jira access, and artifact handling), incomplete user-interface coverage for catalog exchange and AI drafting, and acceptance criteria that do not yet define the security/deployment boundary or measurable release evidence.

Complexity ratings below estimate implementation and coordination difficulty, not elapsed time. “High” commonly reflects a broad cross-boundary task or unsettled policy; it is not a request to begin work before its gate is approved. Dependencies reproduce the task list's declared dependencies. Risks call out the main delivery or safety concern, not every shared cross-cutting criterion.

## Task-by-Task Assessment

### Phase 0 — Product Decisions and Delivery Baseline

| Task | Complexity | Declared dependencies | Main risks and watchpoints |
|---|---|---|---|
| T0.1 Approve product scope and release boundaries | Medium | — | Product/QA owners and a named acceptance authority are not yet identified. Broad product branding may continue to imply Confluence functionality beyond this feature. |
| T0.2 Approve environment and production safety policy | High | T0.1 | Owner-confirmed origins and production-denial criteria are blocking inputs. Browser boundary, DNS behavior, redirects, and policy distribution need security/environment-owner agreement. |
| T0.3 Approve identity, roles, and authorization | High | T0.1 | SSO/session/API identity, role grants, self-approval, revocation, and audit evidence span organization and application decisions. |
| T0.4 Decide catalog authority and concurrency semantics | High | T0.1 | PostgreSQL versus shared workbook authority changes persistence, imports, exports, conflict handling, and team workflow. Choosing without QA/product approval risks rework or data loss. |
| T0.5 Define runner execution boundary and lifecycle | High | T0.1, T0.3 | Local process, service, and user-operated CLI have different deployment, authentication, failure, cancellation, and support models. |
| T0.6 Confirm Jira scope and query policy | Medium | T0.1, T0.3 | Project/site, issue types, allowed fields, JQL limits, credentials, and canonical link validation require Jira-owner approval. |
| T0.7 Record AI and Confluence decisions | High | T0.1, T0.3, T0.6 | Provider/data approval, prompt data limits, usage controls, and Confluence exclusion need distinct governance decisions; approval may remain unavailable. |
| T0.8 Approve data, artifacts, privacy, and service targets | High | T0.1, T0.3 | Storage, retention, redaction, audit, backup, SLO, supported platforms, and data classification require security/operations decisions and measurable definitions. |
| T0.9 Finalize contracts and pilot acceptance checklist | High | T0.1–T0.8 | This is a large synthesis task; unresolved inputs must become explicit disabled/blocking decisions rather than guessed contracts. The evidence checklist should be traceable to every success criterion. |

### Phase 1 — Platform Foundation

| Task | Complexity | Declared dependencies | Main risks and watchpoints |
|---|---|---|---|
| T1.1 Scaffold React 18/Vite client | Low | T0.1 | Low implementation risk; ensure package/runtime constraints and build checks match the eventual repository layout. |
| T1.2 Scaffold Node.js/Express API and shared contracts | Medium | T0.1, T0.9 | Contract versioning and stable error shape can be costly to change after clients depend on them. Health/readiness must not expose configuration secrets. |
| T1.3 Configure Docker PostgreSQL 15 and migrations | Medium | T0.4, T0.8, T0.9 | Database lifecycle, test isolation, credentials, migration failure recovery, and local-versus-production assumptions are not yet operationally settled. |
| T1.4 Establish test, quality, and local setup baseline | Medium | T1.1–T1.3 | “Quality commands” are not enumerated; no explicit CI validation pipeline or supported developer-platform matrix is assigned. Avoid confusing test automation CI with out-of-scope scheduled product runs. |

### Phase 2 — Catalog, Case Authoring, and Human Review

| Task | Complexity | Declared dependencies | Main risks and watchpoints |
|---|---|---|---|
| T2.1 Implement test case and catalog persistence model | High | T0.4, T0.9, T1.2, T1.3 | Many fields, relationships, versioning, and approval invalidation rely on approved contracts. Schema changes after import/export implementation cause migration and compatibility rework. |
| T2.2 Enforce user and role authorization | High | T0.3, T1.2 | API authorization is required, but the login/session/identity-provider integration and security controls are not separate implementation tasks. |
| T2.3 Implement review state transitions and audit history | High | T2.1, T2.2 | Incorrect transition or content-edit invalidation can allow stale approval or lose decision history. Race conditions need atomic state-change semantics. |
| T2.4 Implement catalog and field validation | Medium | T0.9, T2.1 | Jira-link canonicalization, numbered-step grammar, and API-vs-workbook diagnostic formats must be identical and testable. |
| T2.5 Implement safe Excel import | High | T0.4, T0.9, T2.1, T2.4 | Workbook parsing has file-size, macro/external-link, formula, malformed-file, and atomicity concerns. The all-or-nothing versus partial-import choice must be fixed first. |
| T2.6 Implement Excel export and round-trip behavior | Medium | T0.4, T0.9, T2.1, T2.4 | Exported review/identity metadata and workbook version compatibility may expose sensitive information or create stale, misleading edits. |
| T2.7 Implement concurrent edit/version conflict handling | High | T0.4, T0.9, T2.1, T2.5 | Concurrency semantics span database updates, imports, and stale workbooks. A two-writer test alone may not represent import-versus-edit races. |
| T2.8 Implement React authoring and review workflows | High | T2.1–T2.4, T2.7 | User-facing authorization, history, conflict recovery, and accessibility are broad. Declared scope does not include workbook import/export screens or authentication/login UI. |

### Phase 3 — Read-Only Jira Integration and Controlled Drafting

| Task | Complexity | Declared dependencies | Main risks and watchpoints |
|---|---|---|---|
| T3.1 Implement Jira credential loading and read-only authentication | Medium | T0.3, T0.6, T1.2 | Secret-manager adapter, rotation, request logging, and read-only enforcement need to match the approved deployment model. |
| T3.2 Implement constrained Jira issue-key retrieval | Medium | T3.1 | Inaccessible, malformed, or out-of-scope issue behavior and browse-link host validation must remain explicit and safely redacted. |
| T3.3 Implement approved JQL search and pagination | High | T0.6, T3.1 | JQL restriction is a security/data-scope boundary; encoding alone is not a policy validator. Rate limits and pagination caps need agreed behavior. |
| T3.4 Build Jira story selection interface | Medium | T3.2, T3.3, T2.8 | Needs authenticated UI integration and consistent loading, permission, and rate-limit states. The app must not leak fields outside the approved Jira scope. |
| T3.5 Implement manual Draft authoring from Jira stories | Medium | T2.8, T3.4 | The path should remain useful with AI disabled. Source freshness, duplicate case creation, and traceability cardinality are not explicit. |
| T3.6 Implement AI provider adapter behind explicit approval gate | High | T0.7, T3.4, T3.5 | Data minimization, untrusted Jira content, schema validation, cost/time controls, provider failures, and revocation need a true feature gate. No corresponding AI drafting UI task is declared. |

### Phase 4 — Safety-Gated Runner Integration and Reporting

| Task | Complexity | Declared dependencies | Main risks and watchpoints |
|---|---|---|---|
| T4.1 Define and version fixed automation registry | Medium | T0.5, T0.9 | Registry ownership, rollout/version compatibility, and retirement behavior must avoid executing stale mappings or losing traceability. |
| T4.2 Implement URL parsing, environment allowlist, and production denial | High | T0.2, T0.5 | A parser and origin check may not protect popups, subresources, downloads, service workers, DNS changes, or browser-level bypasses. The enforcement boundary must be specified and tested. |
| T4.3 Implement case preflight and trusted booking policy | High | T2.3, T2.4, T4.1, T4.2 | Approval, mapping, environment, and booking classification must be read from trusted/versioned data; stale approval and mixed-environment semantics remain critical. |
| T4.4 Implement Node-to-Python runner adapter | High | T0.5, T1.2, T4.1–T4.3 | Process/service isolation, authentication, payload integrity, timeout, runner loss, and safe secret delivery depend on the unresolved deployment boundary. |
| T4.5 Implement run confirmation and lifecycle | High | T0.5, T0.9, T4.3, T4.4 | Confirmation must be enforced server-side and tied to the exact immutable selection/policy, not just displayed in the UI. Idempotency and partial failure need deterministic semantics. |
| T4.6 Persist run and case result records | High | T1.3, T0.9, T4.4, T4.5 | Runner retries/duplicate deliveries and partial results can corrupt totals unless writes are idempotent and run transitions atomic. |
| T4.7 Generate and securely store run artifacts | High | T0.8, T4.6 | Access control, retention/deletion, screenshot/trace policy, redaction completeness, and storage outage behavior are unresolved operational risks. |
| T4.8 Build React run selection, confirmation, and results views | High | T4.3–T4.7 | Requires accessible, trustworthy confirmation and clear asynchronous/partial-result behavior. Run history, artifact access control, and cancellation UX need explicit scope. |

### Phase 5 — Search and Comparison Pilot

| Task | Complexity | Declared dependencies | Main risks and watchpoints |
|---|---|---|---|
| T5.1 Provision approved pilot prerequisites | Medium | T0.2, T0.8, T0.9 | Accounts, login instructions, synthetic data, and owner-approved targets may be external schedule blockers; secrets must use an approved channel. |
| T5.2 Implement approved search and comparison automations | High | T5.1, T4.1–T4.5 | UI stability, selectors, cleanup after all failures, and safe live-environment checks require coordination with the application owner. |
| T5.3 Execute end-to-end pilot acceptance | High | T5.1, T5.2, T3.4–T3.5, T4.5–T4.8 | This is a multi-system release gate; it needs test accounts, a versioned evidence package, defect handling, and authorized go/no-go sign-off. |

### Phase 6 — Configuration and Sandbox Booking Expansion

| Task | Complexity | Declared dependencies | Main risks and watchpoints |
|---|---|---|---|
| T6.1 Approve configuration journey scope and test data | Medium | T5.3 | “Configuration” may include consequential actions; scope must distinguish safe selections from any purchase/booking commitment. |
| T6.2 Implement configuration automation | High | T6.1, T4.1–T4.5 | Needs approved scenarios, repeatable fixtures, and consistent enforcement. Result persistence/artifact dependencies are implicit rather than declared. |
| T6.3 Approve Sandbox booking behavior | High | T5.3 | Non-production status and permitted booking/payment-simulation actions require explicit, auditable owner/security approval and stop/rollback criteria. |
| T6.4 Implement and separately accept Sandbox booking automation | High | T6.3, T4.1–T4.7 | Highest consequence feature. Any uncertainty in origin, redirects, metadata, or mixed runs must remain fail-closed. It does not explicitly depend on the run-selection/results UI T4.8. |

### Phase 7 — Team Adoption and Operational Readiness

| Task | Complexity | Declared dependencies | Main risks and watchpoints |
|---|---|---|---|
| T7.1 Validate team concurrency and service targets | High | T2.7, T4.6, T5.3 | Requires quantified and approved targets plus representative workloads; artifact access, backup/restore, and run concurrency are not fully represented by a simple two-writer test. |
| T7.2 Complete operational documentation and support handoff | Medium | T5.3; T6.4 when booking is enabled | Operational ownership, escalation, deployment, monitoring, recovery, and secret rotation need named owners; documentation should be maintained incrementally, not deferred to handoff. |
| T7.3 Review adoption and decide future scope | Medium | T7.1, T7.2 | Feedback needs measurable outcomes and a decision record; future proposals should not be confused with approval to implement them. |

## Cross-Document Gaps, Contradictions, and Dependency Findings

### Blocking or high-priority gaps

1. **Catalog authority is still unresolved.** The specification says PostgreSQL holds persistent application records and Excel is required, while leaving authority open. The plan and tasks correctly gate implementation, but no approved decision or versioned decision record exists yet. Resolve C-01/C-12 before T1.3/T2.1/T2.5–T2.7.
2. **Identity implementation is incomplete as a workstream.** T0.3 decides authentication and roles; T2.2 enforces authorization at the API. No explicit task implements the selected login/SSO/session/token lifecycle, user provisioning/revocation, or React authentication flow. Add a task or explicitly constrain an existing task after the identity decision.
3. **Catalog user workflows are incomplete.** T2.5/T2.6 cover backend import/export and T2.8 covers case authoring/review, but no task provides file upload/download, import preview/diagnostic resolution, overwrite confirmation, or conflict recovery in the UI. Yet User Story 2 and pilot acceptance expect Excel-compatible catalog maintenance and import/export.
4. **AI drafting has no end-user workflow task.** T3.6 implements an adapter and checks its disabled/approved behavior, but there is no UI action for requesting drafts, previewing/editing generated cases, showing approval status, or handling provider errors. This leaves User Story 1 only partially deliverable if AI is approved.
5. **Application and runner security boundaries are not fully specified.** T4.2 leaves the effective browser enforcement boundary open; T4.4 leaves process/service deployment dependent on T0.5. C-21 mentions tests, but no explicit threat model, security review, network-isolation design, or proof method for “zero network activity” is required. Define the boundary before enabling live runs.
6. **Production-readiness scope is thin.** T7.1 includes backup/restore and T7.2 documentation, but no explicit deployment/release, monitoring/alerting, database upgrade/rollback, disaster-recovery exercise, access provisioning, or incident-response implementation task. The spec/clarifications raise several of these topics but task coverage is partial.
7. **Acceptance evidence artifacts are not enumerated.** T0.1/T0.9/T5.3/T6.3 require sign-off or evidence, but do not name a canonical decision log, approval record, safety checklist, pilot report, test evidence bundle, or owner for maintaining them.
8. **Work breakdown is not delivery-ready.** Tasks have no owner, estimate, or explicit deliverable artifact field. This is acceptable for a draft analysis, but the team cannot use the list for capacity planning or accountable execution without adding those fields or linking an execution tracker.

### Consistency and dependency observations

- **The React/Express product scope differs from the original backlog's CLI-first plan.** The project specification recommends starting with a command-line interface and considering a team UI later; the constitution/specification now mandate React/Express and the task plan builds a UI in Phases 1–4. This may be an intentional, approved architecture change, but record its rationale and ensure the backlog is updated to avoid two competing delivery plans.
- **Pilot environment is not settled consistently.** The detailed specification/constitution permit Staging, Sandbox, QA, and PreProd generally, while the original backlog recommends a search/comparison pilot in Sandbox and the plan recommends search/comparison without fixing a pilot environment. T0.2/T5.1 must record exactly which environment(s) are enabled.
- **Mixed booking/non-booking behavior remains deliberately unresolved.** The general run request selects one environment, while booking must use Sandbox. T0.2/T0.9/T6.3 need an explicit reject/split/separate-run policy and the confirmation screen must show the effective environment per case.
- **T0.9 is a broad dependency bottleneck.** Nearly all implementation depends directly or indirectly on its contracts and acceptance checklist. Split its outputs into reviewable contract artifacts if decisions can be approved in parallel; do not make a single oversized task block independent scaffolding.
- **T4.8 is not an explicit prerequisite of T6.4.** If booking is enabled through the team UI, add T4.8 to T6.4 or T6.4's acceptance criteria must explicitly verify the end-user run and result path.
- **T2.8 omits the UI dependencies implied by catalog import/export.** Add import/export UI tasks and connect them to T2.5/T2.6/T2.7, T2.8, and T5.3 as appropriate.
- **Story priorities and delivery sequencing are not identical.** User Stories 1–4 are P1, but Jira search/drafting and reporting land in later phases. The plan intentionally establishes catalog foundations first, but the release definition should state which P1 capabilities are deferred from the first usable increment.
- **The constitution and feature scope have different breadth.** The constitution names a Jira/Confluence project; the feature is Vehicle Shop Jira test automation with Confluence disabled. T0.1/T0.7 should keep product branding, feature boundary, and any Confluence work unambiguous.
- **Default test isolation needs a sharper database interpretation.** FR-028 mentions isolating database dependencies while FR-012 requires PostgreSQL persistence. The plan suggests unit tests plus disposable PostgreSQL integration tests, but the requirement should explicitly distinguish mocked/unit tests from integration tests against disposable local PostgreSQL.
- **Some acceptance criteria are qualitative or compound.** Phrases such as “small approved set,” “actionable,” “securely,” “stable,” “approved locations,” and “complete workflow” need concrete limits, examples, or evidence references in T0.9 before they can be objectively accepted.

## Missing or Recommended Artifacts

These are recommended planning/evidence artifacts, not policy assumptions:

| Artifact | Why it is needed | Suggested owning task |
|---|---|---|
| Approved decision and exception register, with owner/date/status/evidence | Makes Phase 0 gates auditable and distinguishes open, rejected, and approved decisions | T0.1–T0.9 |
| Versioned architecture and trust-boundary diagram, including Node/Python/browser/network boundaries | Clarifies deployment, identity, secrets, and navigation enforcement before execution is enabled | T0.5, T0.9, T4.2, T4.4 |
| Data dictionary, state-transition diagrams, and versioned API/run/result contracts | Reduces ambiguity across UI, API, database, import/export, and runner | T0.9, T1.2, T2.1, T4.4–T4.6 |
| Versioned `.xlsx` template plus valid/invalid golden fixtures and compatibility policy | Supports deterministic validation, round-trip, migration, and regression testing | T0.4, T0.9, T2.5, T2.6 |
| Approved Jira field/JQL policy and canonical-link validation examples | Gives reviewers and tests evidence of least-privilege scope | T0.6, T3.2, T3.3 |
| Environment registry/change approval record and production-denial rules | Makes allowlist inputs owner-approved, reviewable, and safely distributable | T0.2, T4.2, T5.1 |
| Threat model and security/safety verification plan | Defines browser boundary, attacker-controlled inputs, zero-network proof, and release gates | T0.2, T0.5, T0.8, T4.2–T4.5 |
| Synthetic fixture/account setup-reset-cleanup runbook | Makes pilot cases repeatable without real customer/payment data | T5.1, T5.2, T6.1, T6.3 |
| Pilot evidence package and signed go/no-go/booking safety checklist | Preserves test results, owner approvals, residual risks, and expansion decision | T5.3, T6.3, T6.4 |
| Deployment, monitoring, backup/restore, incident response, and support runbook | Covers operational responsibilities that are not fully assigned to current tasks | T0.8, T7.1, T7.2 |

## Recommended Actions Before Implementation

1. Resolve and record the Phase 0 blocking decisions, especially catalog authority, identity, runner deployment, environment/production policy, and artifact handling.
2. Add explicit tasks for authentication UI/identity integration, catalog import/export UI, and the AI drafting UI (or explicitly defer those user workflows).
3. Update the original backlog to the approved React/Express architecture and make the pilot environment and pilot journeys consistent across all documents.
4. Add or reference the security boundary and release-evidence artifacts above; make zero-navigation/network claims measurable at the chosen enforcement boundary.
5. Refine T0.9 and acceptance criteria into versioned contracts, measurable thresholds, and traceable evidence. Then assign owners and estimates in the team's execution tracker.

## Overall Conclusion

The plan is structurally sound for a gated, safety-first project, and the declared dependencies generally follow the planned phase order. It is not yet a complete execution-ready backlog: unresolved decisions block key branches, the UI scope omits catalog file exchange and AI drafting, the original CLI-first backlog conflicts with the newer web-app direction, and security/operational evidence needs more explicit artifacts. Keep live Jira/AI/runner execution and all booking behavior disabled until the relevant decisions, implementation, and sign-offs are recorded.
