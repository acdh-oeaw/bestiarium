from django.conf.urls import url

from . import special_views, views

app_name = "infos"
urlpatterns = [
    url(r"^project-team/$", special_views.TeamView.as_view(), name="project-team"),
    url(
        r"^about-the-project/$",
        special_views.SpecialAboutView.as_view(),
        name="about-the-project",
    ),
    url(r"^about/$", views.AboutTheProjectListView.as_view(), name="about_browse"),
    url(
        r"^about/detail/(?P<pk>[0-9]+)$",
        views.AboutTheProjectDetailView.as_view(),
        name="about_detail",
    ),
    url(r"^about/create/$", views.AboutTheProjectCreate.as_view(), name="about_create"),
    url(
        r"^about/edit/(?P<pk>[0-9]+)$",
        views.AboutTheProjectUpdate.as_view(),
        name="about_edit",
    ),
    url(
        r"^about/delete/(?P<pk>[0-9]+)$",
        views.AboutTheProjectDelete.as_view(),
        name="about_delete",
    ),
    url(r"^teammember/$", views.TeamMemberListView.as_view(), name="teammember_browse"),
    url(
        r"^teammember/detail/(?P<pk>[0-9]+)$",
        views.TeamMemberDetailView.as_view(),
        name="teammember_detail",
    ),
    url(
        r"^teammember/create/$",
        views.TeamMemberCreate.as_view(),
        name="teammember_create",
    ),
    url(
        r"^teammember/edit/(?P<pk>[0-9]+)$",
        views.TeamMemberUpdate.as_view(),
        name="teammember_edit",
    ),
    url(
        r"^teammember/delete/(?P<pk>[0-9]+)$",
        views.TeamMemberDelete.as_view(),
        name="teammember_delete",
    ),
    url(
        r"^projectinst/$",
        views.ProjectInstListView.as_view(),
        name="projectinst_browse",
    ),
    url(
        r"^projectinst/detail/(?P<pk>[0-9]+)$",
        views.ProjectInstDetailView.as_view(),
        name="projectinst_detail",
    ),
    url(
        r"^projectinst/create/$",
        views.ProjectInstCreate.as_view(),
        name="projectinst_create",
    ),
    url(
        r"^projectinst/edit/(?P<pk>[0-9]+)$",
        views.ProjectInstUpdate.as_view(),
        name="projectinst_edit",
    ),
    url(
        r"^projectinst/delete/(?P<pk>[0-9]+)$",
        views.ProjectInstDelete.as_view(),
        name="projectinst_delete",
    ),
    url(
        r"^about-the-project/methodology$",
        views.Methodology.as_view(),
        name="projectinst_delete",
    ),
]
