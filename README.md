# TLC Skills

Agent skills for product delivery and adaptive triathlon planning.

```text
TLC Spec → TLC Delivery
```

| Skill | Purpose |
| --- | --- |
| `tlc-spec` | Turns a request into testable requirements, implementation decisions, and atomic tasks. |
| `tlc-delivery` | Implements an approved handoff with TDD, focused commits, verification, and a pull request. |
| `triathlon-trainingpeaks-planner` | Plans only the next triathlon-training week from Strava trends and a user-provided Runna plan, then publishes approved sessions to TrainingPeaks. |

## Installation

Clone this repository and copy the skills you want into your agent's skills directory:

```bash
git clone https://github.com/matheusteixeira7/tlc-skills.git
mkdir -p ~/.codex/skills
cp -R tlc-skills/skills/tlc-spec tlc-skills/skills/tlc-delivery tlc-skills/skills/triathlon-trainingpeaks-planner ~/.codex/skills/
```

Restart the agent session after installing so it discovers the new skills. For other compatible agent environments, copy the three directories under that environment's configured skills directory.

## Usage

Start with `$tlc-spec` when a request needs product clarification, a design decision, or task breakdown. It produces a closed handoff in the issue and creates the delivery sub-issue.

Use `$tlc-delivery` only when that handoff is ready. It follows the agreed scope, writes and runs tests, makes atomic Conventional Commits, and opens a pull request without merging it.

Use `$triathlon-trainingpeaks-planner` to prepare a single upcoming week for a triathlon event. It reviews the completed week and the preceding three to four weeks in Strava, receives the next week's running sessions manually from Runna, proposes the schedule for approval, and only then updates TrainingPeaks. Bike sessions are always built fully in TrainingPeaks' **Build Workout** editor.

## Boundaries

- `tlc-spec` plans; it does not change repository code or open pull requests.
- `tlc-delivery` delivers a closed spec; it does not redo discovery or silently make product or architecture decisions.
- `triathlon-trainingpeaks-planner` plans and publishes only the next approved training week; it does not create multi-week schedules or invent Runna running sessions.
- All skills respond in the member's language, while code and repository-facing artifacts remain in English.

## License

[MIT](LICENSE)
