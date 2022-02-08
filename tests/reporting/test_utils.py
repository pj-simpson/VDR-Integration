import pytest

from core.site_migration.utilities import utils
from reporting.models import Report, ReportLine
from reporting.utils import ReportWriter
from tests.test_utilities.conftest import folder_contents_object, report_factory
from tests.test_utilities.dataclass_responses import vdr_folder_detail


@pytest.mark.django_db
def test_simple_report_writer_init(report_factory):

    report = report_factory()

    report_writer = ReportWriter(folder_name="a folder name", report_id=report.id)

    assert type(report_writer) == ReportWriter


@pytest.mark.django_db
def test_report_writer_init_report_creation():

    # if we initialize the report writer w/o a report id, it will call its create_report method.
    report_writer = ReportWriter(
        folder_name="a folder name",
    )

    assert Report.objects.get(id=1).id == report_writer.report_id


@pytest.mark.django_db
def test_report_writer_write_report_line():

    # if we initialize the report writer w/o a report id, it will call its create_report method.
    report_writer = ReportWriter(
        folder_name="a folder name",
    )
    report_writer.write_line("Currently replicating blah blah blah")

    latest_line_from_db = ReportLine.objects.latest("timestamp")
    assert latest_line_from_db.line == "Currently replicating blah blah blah"
