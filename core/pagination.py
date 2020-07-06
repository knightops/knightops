import math

from fastapi import Query
# from link_header import LinkHeader, Link
from starlette.requests import Request
from starlette.responses import Response
from core.functional import cached_property
from math import ceil


class Page:

    def __init__(self, object_list, per_page, orphans=0,
                 allow_empty_first_page=True):
        self.object_list = object_list
        self.per_page = int(per_page)
        self.orphans = int(orphans)
        self.allow_empty_first_page = allow_empty_first_page

    def get_page(self, number):
        """
        Return a valid page, even if the page argument isn't a number or isn't
        in range.
        """
        return self.page(number)

    def page(self, number):
        """Return a Page object for the given 1-based page number."""
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return self.object_list[bottom:top]

    @cached_property
    def count(self):
        """Return the total number of objects, across all pages."""
        try:
            return self.object_list.count()
        except (AttributeError, TypeError):
            # AttributeError if object_list has no count() method.
            # TypeError if object_list.count() requires arguments
            # (i.e. is of type list).
            return len(self.object_list)

    @cached_property
    def num_pages(self):
        """Return the total number of pages."""
        if self.count == 0 and not self.allow_empty_first_page:
            return 0
        hits = max(1, self.count - self.orphans)
        return ceil(hits / self.per_page)


class Pagination:
    """
    A simple page number based style that supports page numbers as
    query parameters. For example:

    http://api.example.org/accounts/?page=4
    http://api.example.org/accounts/?page=4&size=100
    """
    # The default page size.
    # Defaults to `None`, meaning pagination is disabled.
    page_size = None

    # Client can control the page using this query parameter.
    page_query_param = 'page'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = 'size'

    _default_page: int = 1
    _default_per_page: int = 100
    _max_per_page: int = 1000

    def __init__(
            self,
            request: Request,
            response: Response,
            page: int = Query(_default_page, alias=page_query_param, ge=1),
            per_page: int = Query(_default_per_page, alias=page_size_query_param, ge=1, le=_max_per_page),
    ):
        self.page = page
        self.per_page = per_page
        self.request = request
        self.response = response
        self.page_data = []
        self.paginator = None

    def paginate_queryset(self, queryset):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size()
        if not page_size:
            return None

        self.paginator = Page(queryset, page_size)
        page_number = self.get_page_number()

        self.page_data = list(self.paginator.page(page_number))

        return self.page_data

    def get_paginated_response(self, data=None):
        return {
            'count': self.paginator.count,
            'page': self.get_page_number(),
            'size': self.get_page_size(),
            'results': data or self.page_data
        }

    def get_page_size(self):

        return self.per_page

    def get_page_number(self):

        return self.page

    def paginate(self, queryset):
        self.paginate_queryset(queryset)
        return self.get_paginated_response()

