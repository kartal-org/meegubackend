from django_property_filter import PropertyFilterSet, PropertyNumberFilter
from .models_copy import *


class BookFilterSet(PropertyFilterSet):
    class Meta:
        model = ChatRoom
        exclude = ["price"]
        property_fields = [
            ("discounted_price", PropertyNumberFilter, ["lt", "exact"]),
            ("series.book_count.", PropertyNumberFilter, ["gt", "exact"]),
        ]
