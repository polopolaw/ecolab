from wagtail.admin.views.reports import PageReportView
from wagtail.core.models import Page


class UnpublishedChangesReportView(PageReportView):

    def get_queryset(self):
        return Page.objects.filter(has_unpublished_changes=True)