from django_filters import FilterSet, CharFilter

from .models import Group


class GroupFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")

    class Meta:
        model = Group
        fields = ('title', )
