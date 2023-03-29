import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render

from ..auth.decorators import deny_restricted
from .forms import GroupForm
from .models import Group

logger = logging.getLogger(__name__)


@deny_restricted
def groups_view(request):
    if not request.user.has_admin_permission("groups"):
        raise Http404
    if "user" in request.GET:
        try:
            user = get_user_model().objects.get(id=request.GET.get("user"))
        except get_user_model().DoesNotExist:
            messages.error(request, f"Requested user ID {request.GET.get('user')} does not exist.")
            user = request.user
    else:
        user = request.user
    return render(request, "groups/groups.html", {"user": user, "all_groups": Group.objects.all(), "group_admin": True})

# Create individual views for each form action
@deny_restricted
def add_group_view(request):
    if not request.user.has_admin_permission("groups"):
        raise Http404
    success = False
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
    else:
        form = GroupForm()

    context = {"form": form, "action": "add", "success": success}
    return render(request, "groups/addmodify.html", context)
