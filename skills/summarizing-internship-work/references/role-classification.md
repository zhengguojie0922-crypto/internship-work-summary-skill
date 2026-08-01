# Role Classification

Classify work nonexclusively. Assign one primary role from the dominant evidence chain and zero or more secondary roles from meaningful supporting evidence. Do not force a single label onto cross-functional work.

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

Route to every applicable role file directly: `role-frontend.md`, `role-backend.md`, `role-client.md`, `role-testing.md`, `role-devops.md`, `role-data-analytics.md`, and `role-algorithm.md`. Use the primary role to order career material and secondary roles to frame collaboration or breadth.
