from datetime import datetime

import pytest
import pytz

from tests.test_utilities.conftest import report_factory, report_line_factory


@pytest.mark.django_db
def test_report_models(report_factory):
    report = report_factory()
    assert report.id == 1
    assert report.root_folder_name == "Testing a Folder"
    assert report.task_start < datetime.now(pytz.utc)


@pytest.mark.django_db
def test_report_lines(report_line_factory):
    report_line = report_line_factory()
    assert report_line.id == 1
    assert report_line.line == "Testing a line"
    assert report_line.report.id == 1
    assert report_line.timestamp < datetime.now(pytz.utc)
