
from enum import StrEnum
import json
import os
from pathlib import Path
import subprocess
from typing import Any, List, Dict, Literal, Optional, Set
from pydantic import BaseModel, Field

from toolguard.data_types import FileTwin


class TestOutcome(StrEnum):
    passed = "passed"
    failed = "failed"

class TracebackEntry(BaseModel):
    path: str
    lineno: int
    message: str

class CrashInfo(BaseModel):
    path: str
    lineno: int
    message: str

class CallInfo(BaseModel):
    duration: float
    outcome: TestOutcome
    crash: Optional[CrashInfo] = None
    traceback: Optional[List[TracebackEntry]] = None
    longrepr: Optional[str] = None

class TestPhase(BaseModel):
    duration: float
    outcome: TestOutcome

class TestResult(BaseModel):
    nodeid: str
    lineno: int
    outcome: TestOutcome
    keywords: List[str]
    setup: TestPhase
    call: CallInfo
    user_properties: Optional[List[Any]] = None
    teardown: TestPhase

class ResultEntry(BaseModel):
    nodeid: str
    type: str
    lineno: Optional[int] = None

class Collector(BaseModel):
    nodeid: str
    outcome: TestOutcome
    result: List[ResultEntry]
    longrepr: Optional[str] = None

class Summary(BaseModel):
    failed: Optional[int] = 0
    total: int
    collected: int

class TestReport(BaseModel):
    created: float
    duration: float
    exitcode: int
    root: str
    environment: Dict[str, str]
    summary: Summary
    collectors: List[Collector] = Field(default=[])
    tests: List[TestResult]

    def all_tests_passed(self)->bool:
        return all([test.outcome == TestOutcome.passed for test in self.tests])
    
    def all_tests_collected_successfully(self)->bool:
        return all([col.outcome == TestOutcome.passed for col in self.collectors])

    def non_empty_tests(self)->bool:
        return self.summary.total > 0

    def list_errors(self)->List[str]:
        errors = set()

        #Python errors in the function under test
        for col in self.collectors:
            if col.outcome == TestOutcome.failed and col.longrepr:
                errors.add(col.longrepr)

        #applicative test failure
        for test in self.tests:
            if test.outcome == TestOutcome.failed:
                error = test.call.crash.message
                if test.user_properties:
                    case_desc = test.user_properties[0].get("docstring")
                    if case_desc:
                        error = f"""Test case {case_desc} failed with the following message:\n {test.call.crash.message}"""
                errors.add(error)
        return list(errors)

def run(folder:str, test_file:str, report_file)->TestReport:
    subprocess.run([
            "pytest",
            test_file,
            # "--verbose",
            "--quiet",
            "--json-report", 
            f"--json-report-file={report_file}"
        ], 
        env={
            **os.environ, 
            "PYTHONPATH": "."
        },
        cwd=folder)
    report = read_test_report(os.path.join(folder, report_file))

    #overwrite it with indented version
    with open(os.path.join(folder, report_file), "w", encoding="utf-8") as f:
        json.dump(report.model_dump(), f, indent=2)

    return report

def configure(folder:str):
    """adds the test function docstring to the output report"""

    hook = """
import pytest

def pytest_runtest_protocol(item, nextitem):
    docstring = item.function.__doc__
    if docstring:
        item.user_properties.append(("docstring", docstring))
"""
    FileTwin(file_name="conftest.py", content=hook).save(folder)


def read_test_report(file_path:str)->TestReport:
    with open(file_path, "r") as file:
        data = json.load(file)
    return TestReport.model_validate(data, strict=False)

