#!/usr/bin/env python3
"""Self-test for tools/bla-check.

Standard library only and no test framework: this repository must not gain a
manifest. The CLI is invoked as a subprocess with sys.executable, never imported —
the contract under test is the exit code and the printed lines, and only a
subprocess exercises that.

Run from anywhere: python3 tools/tests/run.py
"""

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

    tail = "%d passed, %d failed" % (passed, failed)
    if skipped:
        tail += ", %d skipped" % skipped
    print(tail)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
