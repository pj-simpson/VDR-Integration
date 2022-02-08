from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import Report, ReportLine


def report_list(request):

    reports = Report.objects.all().order_by("-task_start")
    paginator = Paginator(reports, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return TemplateResponse(request, "report_list.html", {"report_list": page_obj})


def report_detail(request, id: int):

    report = get_object_or_404(Report, id=id)
    lines = ReportLine.objects.filter(report=report)

    return TemplateResponse(
        request, "report_detail.html", {"report": report, "lines": lines}
    )
