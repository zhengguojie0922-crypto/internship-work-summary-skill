# Role Classification

Classify work from the dominant direct evidence chain and the confirmed target role. Select exactly one primary role guide. Select at most one secondary role guide only when direct cross-role evidence is necessary to explain a dependency, interface, or collaboration boundary. The target role remains the organizing perspective, and secondary evidence does not establish secondary ownership.

## Role Routing

| Role | Primary evidence | Guide |
|---|---|---|
| Frontend | Browser UI, state, accessibility, rendering, client-side performance | `role-frontend.md` |
| Backend | APIs, services, persistence, consistency, authorization | `role-backend.md` |
| Client | Mobile, desktop, or native lifecycle, platform integration, offline behavior | `role-client.md` |
| Testing | Test strategy, automation, fixtures, quality gates, failure diagnosis | `role-testing.md` |
| DevOps | CI/CD, infrastructure, deployment, observability, operations | `role-devops.md` |
| Data analytics | Data modeling, SQL, metric definitions, reporting, data quality | `role-data-analytics.md` |
| Algorithm | Models, ranking, optimization, evaluation, inference, experimentation | `role-algorithm.md` |

Treat labels as ambiguous when two roles have comparable direct evidence or when only filenames/commit messages imply a role. Retain both candidate classifications and avoid converting target preference into evidence. Route any genuinely material missing target-role information through the main consolidated confirmation process; role classification does not add confirmation rounds.

Load the shared `role-analysis-framework.md` and exactly one primary role guide. Load at most one secondary role guide when direct cross-role evidence meets the boundary above. Use the primary role to order career material and the secondary role only to frame collaboration or breadth. For a target role outside the seven supported categories, choose the closest primary guide and state the mapping reason and unsupported boundary in the final document.
