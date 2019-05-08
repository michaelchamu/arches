from arches.app.models.system_settings import settings
from arches.app.search.components.base import BaseSearchFilter
from arches.app.utils.pagination import get_paginator

details = {
    "searchcomponentid": "",
    "name": "Paging",
    "icon": "",
    "modulename": "paging_filter.py",
    "classname": "PagingFilter",
    "type": "paging",
    "componentpath": "views/components/search/paging-filter",
    "componentname": "paging-filter",
    "sortorder": "0",
    "enabled": True
}


class PagingFilter(BaseSearchFilter):

    def append_dsl(self, query_dsl, permitted_nodegroups, include_provisional):
        export = self.request.GET.get('export', None)
        mobile_download = self.request.GET.get('mobiledownload', None)
        page = 1 if self.request.GET.get('page') == '' else int(self.request.GET.get('page', 1))

        if export is not None:
            limit = settings.SEARCH_EXPORT_ITEMS_PER_PAGE
        elif mobile_download is not None:
            limit = self.request.GET['resourcecount']
        else:
            limit = settings.SEARCH_ITEMS_PER_PAGE
        limit = int(self.request.GET.get('limit', limit))
        query_dsl.start = limit*int(page-1)
        query_dsl.limit = limit

    def post_search_hook(results):
        total = results['hits']['total']
        page = 1 if self.request.GET.get('page') == '' else int(self.request.GET.get('page', 1))

        paginator, pages = get_paginator(self.request, results, total, page, settings.SEARCH_ITEMS_PER_PAGE)
        page = paginator.page(page)

        ret = {}
        ret['current_page'] = page.number
        ret['has_next'] = page.has_next()
        ret['has_previous'] = page.has_previous()
        ret['has_other_pages'] = page.has_other_pages()
        ret['next_page_number'] = page.next_page_number() if page.has_next() else None
        ret['previous_page_number'] = page.previous_page_number() if page.has_previous() else None
        ret['start_index'] = page.start_index()
        ret['end_index'] = page.end_index()
        ret['pages'] = pages

        return {'paginator': ret}
