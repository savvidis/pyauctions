#  Based on: http://www.djangosnippets.org/snippets/73/
#
#  Modified by Sean Reifschneider to be smarter about surrounding page
#  link context.  For usage documentation see:
#
#     http://www.tummy.com/Community/Articles/django-pagination/

from django import template

register = template.Library()

def paginator(context, adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    """
    page_numbers = [n for n in range(context['page'] - adjacent_pages, context['page'] + adjacent_pages + 1) \
                    if n > 0 and n <= context['pages']]
    # page_numbers = context['page_numbers']

    return {
        # 'hits': context['hits'],
        'results_per_page': context['results_per_page'],
        'page': context['page'],
        'pages': context['pages'],
        'page_numbers': page_numbers,
        'next': context['next'],
        'previous': context['previous'],
        'has_next': context['has_next'],
        'has_previous': context['has_previous'],
        'show_first': 1 not in page_numbers,
        'show_last': context['pages'] not in page_numbers,
    }

    # return {
    #     'page_obj': page_obj,
    #     'paginator': paginator,
    #     # 'hits': context['hits'],
    #     'results_per_page': context['results_per_page'],
    #     'page': context['page'],
    #     'pages': context['pages'],
    #     'page_numbers': page_numbers,
    #     'next': context['next'],
    #     'previous': context['previous'],
    #     'has_next': context['has_next'],
    #     'has_previous': context['has_previous'],
    #     'show_first': 1 not in page_numbers,
    #     'show_last': context['pages'] not in page_numbers,
    # }

register.inclusion_tag('auctionapp/public/paginator.html', takes_context=True)(paginator)
