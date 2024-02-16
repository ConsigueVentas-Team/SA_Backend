from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class CustomPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data, additional_data=None):
        response_data = OrderedDict({
                    'total': self.page.paginator.count,
                    'per_page': self.page.paginator.per_page,
                    'current_page': self.page.number,
                    'last_page': self.page.paginator.num_pages,
                    'next_page_url': self.get_next_link(),
                    'prev_page_url': self.get_previous_link(),
                    'from': self.page.start_index(),
                    'to': self.page.end_index(),
                    'data': data
                })
        
        if additional_data is not None:
            response_data.update(additional_data)
        
        return Response(response_data)