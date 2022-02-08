from reporting.models import Report, ReportLine


class ReportWriter:
    """
    A class to create and persist the report objects to the DB

    Attributes
    ----------
    report_id = the unique identifier of the overall report in the DB, that the 'lines' will be written to. If this
        is initialized as None, then the object calls its own create_report() method and persists a Report to the DB

        this is an id rather than an object because Kombu which unperpins celery needs to serlizae the data as json and
        cant handle python objects... we are passing the id of the report between tasks, because we cant pass the reportwriter
        object itself

    folder = A FolderContents object containing the current state of the folder being either downloaded or deleted.
    celery_task_id = a celery task id, so a reader of the report can cross check against the flower monitoring.


    Methods
    -------

    _create_report()
        gets the name of the folder and creates a corresponding Report object in the DB

    write_line()
        writing a line for the given report to the DB.
    """

    def __init__(self, folder_name: str, report_id: int = None):

        self.folder_name = folder_name

        if report_id is None:
            self.report_id = self._create_report()
        else:
            self.report_id = report_id

    def _create_report(self):
        folder_name = self.folder_name
        new_report = Report.objects.create(root_folder_name=folder_name)
        return new_report.id

    def write_line(self, line: str):
        report = Report.objects.get(id=self.report_id)
        ReportLine.objects.create(
            report=report,
            line=line,
        )
