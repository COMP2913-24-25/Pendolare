"""
Parse JUnit XML or TRX test report and update wiki/tests.md with the results.

Author: James Kinley
Date: 2025-10-04
"""

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

TICK = "✅"
CROSS = "❌"

def parse_pytest_junit(path: Path):
    tree = ET.parse(path)
    root = tree.getroot()
    tests = []
    for tc in root.iter("testcase"):
        name = tc.attrib.get("name")
        passed = tc.find("failure") is None and tc.find("error") is None
        tests.append((name, TICK if passed else CROSS))
    return tests

def parse_nunit_trx(path: Path):
    tree = ET.parse(path)
    root = tree.getroot()
    ns = {"trx": "http://microsoft.com/schemas/VisualStudio/TeamTest/2010"}
    tests = []
    for result in root.findall(".//trx:UnitTestResult", ns):
        name = result.attrib["testName"]
        outcome = result.attrib["outcome"]
        tests.append((name, TICK if outcome == "Passed" else CROSS))
    return tests

def render_md_table(tests):
    lines = ["| Test Name | Status |", "|-----------|:------:|"]
    for name, status in tests:
        lines.append(f"| `{name}` | {status} |")
    return "\n".join(lines)

def replace_section_by_header(content: str, service: str, table_md: str) -> str:
    heading = f"### Pendo.{service}"
    lines = content.splitlines()
    out = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == heading:
            out.append(lines[i])
            out.extend(table_md.splitlines())
            out.append("") 
            i += 1

            while i < len(lines) and not lines[i].startswith("### "):
                i += 1
        else:
            out.append(lines[i])
            i += 1
    return "\n".join(out).rstrip() + "\n"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--service",   required=True, help="e.g. AdminService")
    p.add_argument("--report",    required=True, help="path to JUnit XML or TRX")
    p.add_argument("--wiki-file", required=True, help="path to wiki/tests.md")
    args = p.parse_args()

    report = Path(args.report)
    tests = parse_nunit_trx(report) if report.suffix.lower() == ".trx" else parse_pytest_junit(report)
    table_md = render_md_table(tests)

    wiki_path = Path(args.wiki_file)
    content = wiki_path.read_text(encoding="utf-8")
    new_content = replace_section_by_header(content, args.service, table_md)

    if new_content != content:
        wiki_path.write_text(new_content, encoding="utf-8")
        print(f"[update_tests_md] updated Pendo.{args.service}")
    else:
        print(f"[update_tests_md] no changes for Pendo.{args.service}")

if __name__ == "__main__":
    main() 