# TLC Skills

Agent skills for product delivery, adaptive triathlon planning, and funding proposals for waste picker cooperatives.

```text
TLC Spec → TLC Delivery
```

| Skill | Purpose |
| --- | --- |
| `tlc-spec` | Turns a request into testable requirements, implementation decisions, and atomic tasks. |
| `tlc-delivery` | Implements an approved handoff with TDD, focused commits, verification, and a pull request. |
| `triathlon-trainingpeaks-planner` | Plans only the next triathlon-training week from Strava trends and a user-provided Runna plan, then publishes approved sessions to TrainingPeaks. |
| `projetos-catadores-editais` | Writes funding proposals for waste picker cooperatives (cooperativas de catadores) applying to private calls, checks them against the call and Brazilian waste legislation, and exports a .docx. |

## Installation

Clone this repository and copy the skills you want into your agent's skills directory:

```bash
git clone https://github.com/matheusteixeira7/tlc-skills.git
mkdir -p ~/.codex/skills
cp -R tlc-skills/skills/tlc-spec tlc-skills/skills/tlc-delivery tlc-skills/skills/triathlon-trainingpeaks-planner tlc-skills/skills/projetos-catadores-editais ~/.codex/skills/
```

Restart the agent session after installing so it discovers the new skills. For other compatible agent environments, copy the skill directories under that environment's configured skills directory.

## Usage

Start with `$tlc-spec` when a request needs product clarification, a design decision, or task breakdown. It produces a closed handoff in the issue and creates the delivery sub-issue.

Use `$tlc-delivery` only when that handoff is ready. It follows the agreed scope, writes and runs tests, makes atomic Conventional Commits, and opens a pull request without merging it.

Use `$triathlon-trainingpeaks-planner` to prepare a single upcoming week for a triathlon event. It reviews the completed week and the preceding three to four weeks in Strava, receives the next week's running sessions manually from Runna, proposes the schedule for approval, and only then updates TrainingPeaks. Bike sessions are always built fully in TrainingPeaks' **Build Workout** editor.

Use `$projetos-catadores-editais` to write a proposal for a cooperativa or associação de catadores applying to a private funding call (foundations, corporate institutes, ESG or reverse-logistics programs). It reads the call PDF, builds a requirements matrix, cites only verified legislation from its reference file, checks character limits, and generates a .docx with no external dependencies.

## Boundaries

- `tlc-spec` plans; it does not change repository code or open pull requests.
- `tlc-delivery` delivers a closed spec; it does not redo discovery or silently make product or architecture decisions.
- `triathlon-trainingpeaks-planner` plans and publishes only the next approved training week; it does not create multi-week schedules or invent Runna running sessions.
- `projetos-catadores-editais` covers private funding calls only; it does not write PGRS/PGRSS/PMGIRS plans, landfill engineering, or public calls (FUNASA, Transferegov), and it never invents cooperative data or legal citations.
- All skills respond in the member's language, while code and repository-facing artifacts remain in English.

## License

[MIT](LICENSE)
