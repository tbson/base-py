from typing import Any, Callable, Optional

from django.core.paginator import Paginator
from ninja import ModelSchema, Schema
from type.general import QuerySet

PAGE_SIZE = 10


class PagesMetaData(Schema):
    next: Optional[int]
    prev: Optional[int]


class PagingResponse(Schema):
    items: Optional[list[Any]]
    pages: PagesMetaData
    count: int
    extra: dict
    page_size: int
    total_pages: int


class PagingUtil:
    @staticmethod
    def get_paging(schema: ModelSchema, page: int = 1) -> Callable:
        def inner(queryset: QuerySet[Any], extra: dict = {}) -> dict:
            total = queryset.count()
            total_pages = total // PAGE_SIZE + 1
            paginator = Paginator(queryset, PAGE_SIZE)
            items = [schema.from_orm(i) for i in paginator.get_page(page).object_list]
            next_page = page + 1 if page < total_pages else None
            prev_page = page - 1 if page > 1 else None
            pages = dict(next=next_page, prev=prev_page)
            return dict(
                count=total,
                extra=extra,
                items=items,
                pages=pages,
                page_size=PAGE_SIZE,
                total_pages=total_pages,
            )

        return inner
