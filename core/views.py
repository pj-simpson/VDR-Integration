from celery import group
from celery.result import GroupResult
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.forms import SettingsForm
from core.http_handlers.site_http_handlers import get_all_sites, get_single_site
from core.models import RemoteSystemSettings
from core.site_migration.site_migrations import (
    recursive_remote_storage_site_builder_task,
    recursive_site_builder_task,
    recursive_site_permanent_delete_task,
    recursive_site_shallow_delete_task,
)
from vdr_storage_integration.celery import app


class Home(TemplateView):
    template_name = "home.html"


def settings_view(request):
    """

    :param request:
    :return:

    """

    form = SettingsForm()

    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("/settings/")
        else:
            # redirect with errors
            return redirect("/settings/")
    else:
        try:
            # Singleton object
            instance = RemoteSystemSettings.objects.get(id=1)
            form = SettingsForm(instance=instance)
        except RemoteSystemSettings.DoesNotExist:
            form = SettingsForm()
        return TemplateResponse(
            request,
            "settings.html",
            {
                "form": form,
            },
        )


def sites_view(request):

    """
    Displays a list of all VDR Sites the logged in user has access to

    ** Context **
    an instance of VDRSiteList

    ** Template **
    site_list.html

    """
    all_sites = get_all_sites(request.user, request.GET)

    return TemplateResponse(request, "site_list.html", {"context_data": all_sites})


def site_detail_view(request, id: int):

    """
    Displays the detail of a single VDR Site which the logged in user has access to

    ** Path Parameters **
    The unique identifier of the site in the external System

    ** Context **
    an instance of VDRSiteDetail

    ** Template **
    site_detail.html

    """

    site = get_single_site(request.user, id)

    return TemplateResponse(request, "site_detail.html", {"context_data": site})


@csrf_exempt
def replicate_site(request):

    """
    Dispatches the celery jobs (as a group task) to save the VDR Site to the local server and replicate it in the AWS S3 Bucket

    ** Parameters **
    POST['rootFolderId'] : The folder id of the root folder of the VDR Site.

    ** Return Value **
    {"group_task_id": unique identifier of the celery group task}

    """
    if request.POST:
        user_id = request.user.id
        root_folder_id = request.POST.get("rootFolderId")
        group_task = group(
            recursive_site_builder_task.s(user_id, root_folder_id),
            recursive_remote_storage_site_builder_task.s(user_id, root_folder_id),
        )
        group_result = group_task()
        group_result.save()
        return JsonResponse({"group_task_id": group_result.id}, status=202)


@csrf_exempt
def soft_delete_site(request):

    """
    Dispatches the celery job (as a group task) to soft delete contents of the VDR Site.

    ** Parameters **
    POST['rootFolderId'] : The folder id of the root folder of the VDR Site.

    ** Return Value **
    {"group_task_id": unique identifier of the celery group task}

    """
    if request.POST:
        user_id = request.user.id
        root_folder_id = request.POST.get("rootFolderId")
        group_task = group(
            recursive_site_shallow_delete_task.s(user_id, root_folder_id),
        )
        group_result = group_task()
        group_result.save()
        return JsonResponse({"group_task_id": group_result.id}, status=202)


@csrf_exempt
def hard_delete_site(request):

    """
    Dispatches the celery job (as a group task) to permanently delete contents of the VDR Site.

    ** Parameters **
    POST['rootFolderId'] : The folder id of the root folder of the VDR Site.

    ** Return Value **
    {"group_task_id": unique identifier of the celery group task}

    """

    if request.POST:
        user_id = request.user.id
        root_folder_id = request.POST.get("rootFolderId")
        group_task = group(
            recursive_site_permanent_delete_task.s(user_id, root_folder_id),
        )
        group_result = group_task()
        group_result.save()
        return JsonResponse({"group_task_id": group_result.id}, status=202)


@csrf_exempt
def get_status(request, group_task_id):
    """
    Fetches the GroupResult object for the celery tasks and checks whether or not they were ALL successful.

    ** Path Parameters **
    The unique identifier of the celery group task

    ** Return Value **
    {
        "group_task_id": unique identifier of the celery group task,
        "group_task_success": truthly value of whether or not the tasks have completed
    }

    """

    group_task_result = GroupResult.restore(id=group_task_id, app=app)
    all_successful = str((group_task_result.successful()))
    result = {"group_task_id": group_task_id, "group_task_success": all_successful}
    return JsonResponse(result, status=200)
