import django_filters
from .models import Workspace


class WorkspaceFilter(django_filters.FilterSet):
    cities = django_filters.CharFilter(
        name="members",
        lookup_type="contains",
    )

    class Meta:
        model = Workspace
        fields = (
            "classroom",
            "members",
        )
