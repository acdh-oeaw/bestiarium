# generated by appcreator
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

from browsing.browsing_utils import (BaseCreateView, BaseUpdateView,
                                     GenericListView)

from .filters import *
from .forms import *
from .models import *
from .tables import *


class TeamMemberListView(GenericListView):

    model = TeamMember
    filter_class = TeamMemberListFilter
    formhelper_class = TeamMemberFilterFormHelper
    table_class = TeamMemberTable
    init_columns = [
        'id', 'description',
    ]


class TeamMemberDetailView(DetailView):

    model = TeamMember
    template_name = 'browsing/generic_detail.html'


class TeamMemberCreate(BaseCreateView):

    model = TeamMember
    form_class = TeamMemberForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TeamMemberUpdate(BaseUpdateView):

    model = TeamMember
    form_class = TeamMemberForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TeamMemberDelete(DeleteView):
    model = TeamMember
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('info:teammember_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AboutTheProjectListView(GenericListView):

    model = AboutTheProject
    filter_class = AboutTheProjectListFilter
    formhelper_class = AboutTheProjectFilterFormHelper
    table_class = AboutTheProjectTable
    init_columns = [
        'id', 'description',
    ]


class AboutTheProjectDetailView(DetailView):

    model = AboutTheProject
    template_name = 'browsing/generic_detail.html'


class AboutTheProjectCreate(BaseCreateView):

    model = AboutTheProject
    form_class = AboutTheProjectForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AboutTheProjectUpdate(BaseUpdateView):

    model = AboutTheProject
    form_class = AboutTheProjectForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AboutTheProjectDelete(DeleteView):
    model = AboutTheProject
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('info:about_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProjectInstListView(GenericListView):

    model = ProjectInst
    filter_class = ProjectInstListFilter
    formhelper_class = ProjectInstFilterFormHelper
    table_class = ProjectInstTable
    init_columns = [
        'id', 'description',
    ]


class ProjectInstDetailView(DetailView):

    model = ProjectInst
    template_name = 'browsing/generic_detail.html'


class ProjectInstCreate(BaseCreateView):

    model = ProjectInst
    form_class = ProjectInstForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProjectInstUpdate(BaseUpdateView):

    model = ProjectInst
    form_class = ProjectInstForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProjectInstDelete(DeleteView):
    model = ProjectInst
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('info:projectinst_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
