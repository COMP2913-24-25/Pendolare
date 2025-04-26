import argparse
import re
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

        passed = tc.find("failure") is not None or tc.find("error") is not None
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

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--service",   required=True)
    p.add_argument("--report",    required=True) #junit xml or trx
    p.add_argument("--wiki-file", required=True)
    args = p.parse_args()

    report_path = Path(args.report)
    if report_path.suffix.lower() == ".trx":
        tests = parse_nunit_trx(report_path)
    else:
        tests = parse_pytest_junit(report_path)

    table_md = render_md_table(tests)
    placeholder = r"\{\{\s*%s\.TestResults\s*\}\}" % re.escape(args.service)

    wiki = Path(args.wiki_file)
    content = wiki.read_text()
    new_content = re.sub(placeholder, table_md, content, flags=re.MULTILINE)
    if new_content != content:
        wiki.write_text(new_content)
        print(f"[update_tests_md] updated {args.service}")
    else:
        print(f"[update_tests_md] no changes for {args.service}")

if __name__ == "__main__":
    main()