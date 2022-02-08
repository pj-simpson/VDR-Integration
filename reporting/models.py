from django.db import models
from django.urls import reverse


class Report(models.Model):
    id = models.BigAutoField(primary_key=True)
    root_folder_name = models.CharField(max_length=1000)
    task_start = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("report_detail", kwargs={"id": self.id})


class ReportLine(models.Model):
    id = models.BigAutoField(primary_key=True)
    line = models.CharField(max_length=1500)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
