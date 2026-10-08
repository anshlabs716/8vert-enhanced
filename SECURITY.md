# Security Policy

## Supported Versions

Enhanced is a small, actively maintained personal tool. Security fixes land on the
default branch and are released with the latest commit rather than tagged patch
series.

| Version | Supported |
| ------- | --------- |
| `main` (latest) | :white_check_mark: |
| Older commits | :x: |

There are no tagged releases, so "latest `main`" is the only supported version.

## Threat Model

Enhanced runs entirely on your machine as a desktop GUI. It **makes no network
requests** — the source imports only `tkinter`, `math`, `re`, `json`, `os`, and
`datetime`, with no socket, HTTP, or subprocess usage. There is no server, no
account, and no telemetry.

The realistic risks are therefore local, not remote:

| Surface | Where | Notes |
| ------- | ----- | ----- |
| Calculator expression evaluation | `enhanced.py` (`eval`) | Input is filtered to `[0-9+\-*/.()% ]` and evaluated with `__builtins__` removed, so no name or attribute access is possible. |
| Filesystem writes | `~/.enhanced/` | Config, history, and saved notes. A malicious or corrupted file here could affect the app on next launch. |
| Imported files | Notes you open in the editor | Notes are text only; nothing is executed on open. |

If you find a way to escape the calculator sandbox or make the app execute code
from a file, that is a genuine vulnerability — please report it.

## Reporting a Vulnerability

**Do not open a public issue for security problems.**

Use GitHub's private reporting:

1. Go to <https://github.com/anshlabs716/8vert-enhanced/security/advisories/new>
2. Describe the issue and include the steps needed to reproduce it.

Please include:

- Operating system and Python version (`python3 --version`)
- The exact steps to reproduce
- What you expected versus what actually happened
- Any error output

### What to expect

- **Acknowledgement:** within 7 days
- **Assessment:** within 14 days, with severity and whether a fix is planned
- **Fix:** for confirmed issues, as soon as practical. Coordinated disclosure is
  appreciated — please allow a reasonable window before publicising.

Because this is a single-maintainer personal project, response time is best-effort
rather than guaranteed. If a report is time-sensitive, say so in the advisory and it
will be prioritised.

## Scope

**In scope:** code in `enhanced.py`, sandbox escapes, unsafe file handling, crashes
caused by malformed input.

**Out of scope:** vulnerabilities in Python itself or the standard library,
issues requiring an already-compromised system, and reports generated solely by an
automated scanner with no demonstrated impact.

## License

Distributed under the Apache License 2.0. See [`LICENSE`](LICENSE).
