from django.contrib import admin
from django.urls import include, path

from core.views import (
    Home,
    get_status,
    hard_delete_site,
    replicate_site,
    settings_view,
    site_detail_view,
    sites_view,
    soft_delete_site,
)
from reporting.views import report_detail, report_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", Home.as_view(), name="home"),
    path("reports/", report_list, name="reports"),
    path("reports/<int:id>", report_detail, name="report_detail"),
    path("sites/", sites_view, name="sites"),
    path("settings/", settings_view, name="settings"),
    path("sitereplicator/", replicate_site, name="site_downloader"),
    path("sitesoftdeleter/", soft_delete_site, name="soft_deleter"),
    path("siteharddeleter/", hard_delete_site, name="hard_deleter"),
    path("tasks/<str:group_task_id>/", get_status, name="get_status"),
    path("site/<int:id>", site_detail_view, name="site"),
]
