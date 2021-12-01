import django_filters
from .models import Workspace


class WorkspaceFilter(django_filters.FilterSet):
    members = django_filters.NumberFilter(
        name="members",
        lookup_type="contains",
    )

    class Meta:
        model = Workspace
        fields = (
            "classroom__id",
            "members",
        )
