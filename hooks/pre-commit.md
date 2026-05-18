# Pre-Commit Hook

## Purpose

Catches issues before code enters the repository. These checks run locally in seconds and prevent common mistakes from reaching code review. Fast, focused, and non-negotiable.

---

## Checks (in order)

### 1. No Secrets in Code

**What**: Scan for hardcoded credentials, API keys, tokens, passwords, or private keys.

**Patterns to detect**:
- AWS access keys (`AKIA[0-9A-Z]{16}`)
- Private keys (`-----BEGIN.*PRIVATE KEY-----`)
- Password assignments (`password\s*=\s*['"][^'"]+['"]`)
- API tokens (high-entropy strings assigned to `token`, `secret`, `api_key` variables)
- Connection strings with embedded credentials

**Action on failure**: Block commit. Display which file and line contains the potential secret.

**Resolution**: Move secret to environment variable, secrets manager, or parameter store. Never commit and then remove—the secret is in git history forever.

---

### 2. No Large Files

**What**: Prevent accidentally committing large binary files, data dumps, or generated artifacts.

**Thresholds**:
- Individual file: >5MB blocked
- Binary files: `.jar`, `.zip`, `.tar`, `.exe`, `.dll`, `.so` — blocked unless in allowlist
- Data files: `.csv`, `.json`, `.sql` >1MB — blocked (use data pipelines, not git)

**Action on failure**: Block commit. Suggest using Git LFS or an artifact repository.

**Resolution**: Add to `.gitignore`, use Git LFS for legitimate large files, or use artifact storage.

---

### 3. Code Formatting

**What**: Enforce consistent code style without manual effort.

**Implementation**:
- Run language-specific formatter (e.g., `prettier`, `black`, `gofmt`, `rustfmt`)
- Auto-fix when possible (format and stage the formatted file)
- Block when auto-fix changes files (so developer reviews the format change)

**Why**: Formatting debates waste review time. Automate the style, review the logic.

---

### 4. Lint Check

**What**: Static analysis for common bugs, style issues, and potential problems.

**Implementation**:
- Language-specific linter (ESLint, pylint, clippy, checkstyle)
- Only check changed files (speed)
- Errors block; warnings are reported but don't block

**Key rules that MUST block**:
- Unused variables (dead code that confuses readers)
- Unreachable code (logic errors)
- Missing error handling (catch without handling)
- Deprecated API usage
- Security-flagged patterns (eval, unsafe deserialization)

---

### 5. Commit Message Format

**What**: Enforce structured commit messages that link to context.

**Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`

**Requirements**:
- Subject line ≤72 characters
- Subject starts with lowercase
- No period at end of subject
- Body wraps at 80 characters
- Footer includes ticket/issue reference

**Example**:
```
feat(auth): add token expiration validation

Tokens are now validated for expiration, issuer, and audience claims.
Previously only signature was checked, allowing stolen tokens to be
used indefinitely.

Resolves: PROJ-1234
```

**Action on failure**: Block commit with format instructions and example.

---

### 6. No TODO Without Ticket

**What**: TODOs in code must reference a tracking ticket.

**Allowed**: `// TODO(PROJ-1234): Optimize this query for large datasets`
**Blocked**: `// TODO: fix this later`

**Why**: TODOs without tickets are never completed. They're lies we tell ourselves.

**Action on failure**: Block commit. Require ticket reference or removal of TODO.

---

### 7. No Merge Conflict Markers

**What**: Detect leftover merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).

**Why**: These occasionally get committed accidentally and break the build or produce confusing behavior.

**Action on failure**: Block commit. Show file and line.

---

### 8. File Permissions Check

**What**: Detect accidentally executable files or overly permissive file modes.

**Rules**:
- Source files (`.py`, `.js`, `.java`, etc.) should not be executable (644, not 755)
- Only scripts in `bin/` or `scripts/` should be executable
- No files with 777 permissions

**Action on failure**: Block commit. Suggest `chmod` command.

---

## Configuration

### Speed Requirement

All pre-commit checks combined MUST complete in <10 seconds on an average developer machine. If checks are slow, developers will disable them.

### Override

In extraordinary circumstances, commits can bypass with:
```bash
git commit --no-verify -m "message"
```

**Policy**: `--no-verify` usage is tracked. More than 2 uses per week triggers a team discussion about why hooks are being skipped.

### Setup

Pre-commit hooks are installed automatically when the repository is cloned (via setup script or git template). No manual installation required. If a developer doesn't have hooks, their first PR will fail CI checks (which run the same validations).

---

## Relationship to CI

Pre-commit catches issues at the developer's desk. CI runs the same checks (and more) on the server. If pre-commit is skipped, CI will still catch it—but the feedback loop is longer. Pre-commit is for developer convenience; CI is for enforcement.
