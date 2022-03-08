import django_filters
from .models import Contact


class ContactFilter(django_filters.FilterSet):
    # search_by = django_filters.CharFilter(method='search_by_name_phone_email_family_filter')

    class Meta:
        model = Contact
        fields = {
            'name': ['icontains'],
            'tel_work': ['icontains'],
            'phone': ['icontains'],
            'comment': ['icontains'],
            'tel_home': ['icontains']
        }

    # def search_by_name_phone_email_family_filter(self, queryset, name, value):
    #     return queryset.filter(**{
    #         name: value,
    #     })

    # @property
    # def qs(self):
    #     parent = super().qs
    #     author = getattr(self.request, 'user', None)
    #     # print(self.search_by)
    #
    # #
    # #     return parent.filter(is_published=True) \
    # #            | parent.filter(author=author)
