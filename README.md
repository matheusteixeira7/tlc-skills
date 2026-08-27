# TLC Skills

Two complementary agent skills for taking a product request from a closed implementation plan to a reviewed pull request.

```text
TLC Spec → TLC Delivery
```

| Skill | Purpose |
| --- | --- |
| `tlc-spec` | Turns a request into testable requirements, implementation decisions, and atomic tasks. |
| `tlc-delivery` | Implements an approved handoff with TDD, focused commits, verification, and a pull request. |

## Installation

Clone this repository and copy the skills you want into your agent's skills directory:

```bash
git clone https://github.com/matheusteixeira7/tlc-skills.git
mkdir -p ~/.codex/skills
cp -R tlc-skills/skills/tlc-spec tlc-skills/skills/tlc-delivery ~/.codex/skills/
```

Restart the agent session after installing so it discovers the new skills. For other compatible agent environments, copy the two directories under that environment's configured skills directory.

## Usage

Start with `$tlc-spec` when a request needs product clarification, a design decision, or task breakdown. It produces a closed handoff in the issue and creates the delivery sub-issue.

Use `$tlc-delivery` only when that handoff is ready. It follows the agreed scope, writes and runs tests, makes atomic Conventional Commits, and opens a pull request without merging it.

## Boundaries

- `tlc-spec` plans; it does not change repository code or open pull requests.
- `tlc-delivery` delivers a closed spec; it does not redo discovery or silently make product or architecture decisions.
- Both skills respond in the member's language, while code and repository-facing artifacts remain in English.

## License

[MIT](LICENSE)
