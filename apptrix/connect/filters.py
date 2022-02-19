from django_filters import rest_framework as filters

from connect.models import User


class UserFilter(filters.FilterSet):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOISES = (
        (MALE, 'M'),
        (FEMALE, 'W'),
    )

    gender = filters.ChoiceFilter(choices=GENDER_CHOISES)
    first_name = filters.CharFilter(lookup_expr='contains')
    last_name = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = User
        fields = ['gender', 'first_name', 'last_name']
