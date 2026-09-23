#!/usr/bin/env python3
"""Self-test for tools/bla-check.

Standard library only and no test framework: this repository must not gain a
manifest. The CLI is invoked as a subprocess with sys.executable, never imported —
the contract under test is the exit code and the printed lines, and only a
subprocess exercises that.

Run from anywhere: python3 tools/tests/run.py
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "fixtures")
CLI = os.path.join(os.path.dirname(HERE), "bla-check")

# name, argv after the CLI, expected exit code, substrings that must appear,
# substrings that must NOT appear, reason to skip (None when active)
CASES = [
    ("tasks-clean",
     ["tasks", os.path.join(FIXTURES, "tasks-clean")], 0, [], ["FALHA"], None),
    ("tasks-open-marker",
     ["tasks", os.path.join(FIXTURES, "tasks-open-marker")], 1,
     ["FALHA [task-marker-open]"], [], None),
    ("tasks-blocked-no-reason",
     ["tasks", os.path.join(FIXTURES, "tasks-blocked-no-reason")], 1,
     ["FALHA [task-blocked-no-reason]"], [], None),
    ("tasks-dep-blocked",
     ["tasks", os.path.join(FIXTURES, "tasks-dep-blocked")], 1,
     ["FALHA [task-dep-blocked]"], ["FALHA [task-blocked-no-reason]"], None),
    ("tasks-fenced-legend",
     ["tasks", os.path.join(FIXTURES, "tasks-fenced-legend")], 0, [], ["FALHA"], None),
    ("links-broken",
     ["links", os.path.join(FIXTURES, "links-broken")], 1,
     ["FALHA [link-broken]", "nope.md"], ["a.md (resolved", "also-nope.md"], None),
    ("writes-collision",
     ["tasks", os.path.join(FIXTURES, "writes-collision")], 1,
     ["FALHA [wave-writes-intersection]", "src/api/handler.ts"], [], None),
    ("tasks-evidence-missing",
     ["tasks", os.path.join(FIXTURES, "tasks-evidence-missing")], 1,
     ["FALHA [task-evidence-missing]", "1.2.md does not exist",
      "does not open with"], ["FALHA [tasks-file-absent]", "task 1.1"], None),
    # The AVISO half of the output contract: a warning is reported and the exit code
    # stays 0. Without these three cases the invariant stated at the top of
    # tools/bla-check was asserted nowhere.
    ("tasks-no-graph",
     ["tasks", os.path.join(FIXTURES, "tasks-no-graph")], 0,
     ["AVISO [task-graph-absent]"], ["FALHA"], None),
    ("tasks-partial-graph",
     ["tasks", os.path.join(FIXTURES, "tasks-partial-graph")], 0,
     ["AVISO [task-state-unknown]", "AVISO [wave-writes-undeclared]"], ["FALHA"], None),
    # --wave is the wave-close invocation: an open marker on a task in another wave is
    # out of scope, which is the whole reason the flag exists.
    ("wave-scope-excludes-other-waves",
     ["tasks", os.path.join(FIXTURES, "tasks-open-marker"), "--wave", "2"], 0,
     [], ["FALHA"], None),
    ("wave-scope-keeps-own-wave",
     ["tasks", os.path.join(FIXTURES, "tasks-open-marker"), "--wave", "1"], 1,
     ["FALHA [task-marker-open]"], [], None),
    ("wave-scope-empty",
     ["tasks", os.path.join(FIXTURES, "tasks-open-marker"), "--wave", "9"], 0,
     ["AVISO [wave-scope-empty]"], ["FALHA"], None),
]


def run(argv):
    process = subprocess.Popen(
        [sys.executable, CLI] + argv,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.communicate()[0].decode("utf-8", "replace")
    return process.returncode, output


def main():
    passed = 0
    failed = 0
    skipped = 0
    for name, argv, expected_exit, expect, reject, skip in CASES:
        if skip:
            print("SKIP %s: %s" % (name, skip))
            skipped += 1
            continue
        code, output = run(argv)
        problems = []
        if code != expected_exit:
            problems.append("expected exit %d got %d" % (expected_exit, code))
        for needle in expect:
            if needle not in output:
                problems.append("missing %r in output" % needle)
        for needle in reject:
            if needle in output:
                problems.append("unexpected %r in output" % needle)
        if problems:
            failed += 1
            print("FAIL %s: %s" % (name, "; ".join(problems)))
            for line in output.strip().split("\n"):
                if line:
                    print("     | %s" % line)
        else:
            passed += 1
            print("ok %s" % name)

    code, output = run(["--help"])
    if output.count("not implemented") == 2:
        passed += 1
        print("ok help-registers-unimplemented")
    else:
        failed += 1
        print("FAIL help-registers-unimplemented: expected 2 'not implemented' "
              "entries, got %d" % output.count("not implemented"))

    # The --json contract is documented as mandatory and stable, so it is asserted as
    # a shape and not as a substring: one array, one object per finding, exactly the
    # five declared keys, and nothing printed alongside it.
    code, output = run(["--json", "tasks", os.path.join(FIXTURES, "tasks-open-marker")])
    problems = []
    if code != 1:
        problems.append("expected exit 1 got %d" % code)
    try:
        parsed = json.loads(output)
    except ValueError as error:
        parsed = None
        problems.append("output is not one JSON document: %s" % error)
    if isinstance(parsed, list):
        if len(parsed) != 1:
            problems.append("expected 1 finding, got %d" % len(parsed))
        for item in parsed:
            keys = sorted(item)
            if keys != ["line", "message", "path", "rule", "severity"]:
                problems.append("unexpected key set %r" % keys)
            if item.get("severity") != "FALHA" or item.get("rule") != "task-marker-open":
                problems.append("unexpected finding %r" % item)
    elif parsed is not None:
        problems.append("expected a JSON array, got %s" % type(parsed).__name__)
    if problems:
        failed += 1
        print("FAIL json-contract: %s" % "; ".join(problems))
    else:
        passed += 1
        print("ok json-contract")

    tail = "%d passed, %d failed" % (passed, failed)
    if skipped:
        tail += ", %d skipped" % skipped
    print(tail)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
