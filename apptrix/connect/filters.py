from django.db.models import Q
from django_filters import rest_framework as filters
import math
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
    distance = filters.NumberFilter(method='filter_by_distance')

    class Meta:
        model = User
        fields = ['gender', 'first_name', 'last_name', 'distance']

    def filter_by_distance(self, queryset, name, value):
        users_list = User.objects.filter(~Q(username=self.request.user.username))
        longitude = self.request.user.longitude
        width = self.request.user.width
        result_list = []
        distance = value
        try:
            for key in users_list:

                check_distance = point_to_distance(width, longitude,
                                                   users_list[key.id].width, users_list[key.id].longitude)
                if check_distance < distance:
                    result_list.append(users_list[key.id].username)

        except IndexError:
            pass
        users_list = User.objects.filter(username__in=result_list)
        return users_list


def point_to_distance(width_1, longitude_1, width_2, longitude_2):
    central_injection = math.acos(
        math.sin(width_1) * math.sin(width_2) +
        math.cos(width_1) * math.cos(width_2) *
        math.cos(longitude_1 - longitude_2)
    )
    distance = 6371.009 * central_injection
    return distance
