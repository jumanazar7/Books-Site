from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_query_param = "bet"

    def get_paginated_response(self, data):
        response = Response({
            "betlar": {
                "keyingi": self.get_next_link(),
                "oldingi": self.get_previous_link()
            },
            "count": self.page.paginator.count,
            "results": data
        })
        return response