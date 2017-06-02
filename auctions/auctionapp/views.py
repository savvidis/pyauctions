from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView, DetailView, FormView
from django_filters.views import FilterView
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import *
import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from utility import *


# Create your views here.

categories = ["Apartment", "House", "Maisonette", "Detached House"]

types = ["realestate", "auction"]

class AuctionDetailView(DetailView):
    model = TranAuction
    template_name = "auctionapp/public/auction_detail.html"
    context_object_name = 'auction'

class AuctionListView(FilterView):
    model = TranAuction
    template_name = "auctionapp/public/auction_list.html"
    paginate_by = 10
    filterset_class = AuctionFilter

    def get_queryset(self):
        queryset = super(AuctionListView, self).get_queryset()
        # queryset = self.form_filter(queryset, self.request)
        try:
            queryset = AuctionFilter(request.GET, queryset=queryset)
            return render_to_response(template_name, {'filter': queryset,'page':10})
        except:
            pass
        return queryset

    def get_context_data(self, *args, **kwargs):
        # print("$" * 30)
        context = super(AuctionListView, self).get_context_data(**kwargs)

        paginator = Paginator(TranAuction.objects.all(), 1)

        try:
            page_number = int(self.request.GET.get('page'))
            page = paginator.page(page_number)
        except:
            page_number = 1
            page = paginator.page(page_number)

        context['page'] = page_number

        max_index = len(paginator.page_range)
        context['pages'] = max_index
        context['results_per_page'] = 10
        context['next'] = page.next_page_number()

        if page_number==1:
            context['previous'] = 0
        else:
            context['previous'] = page.previous_page_number()

        context['has_next'] = page.has_next()
        context['has_previous'] = page.has_previous()
        context['types'] = types
        # context['page_range'] = page_range

        # context['categories'] = [x[0] for x in cat]
        # context['cities'] = [x[0] for x in cities]

        return context

    @classmethod
    def form_filter(cls, queryset, request):
        q = None
        if request.GET.get('category'):
            q = request.GET['category']
            # self.request.GET.pop(u'csrfmiddlewaretoken')
            print(request.GET)
            criterial = request.GET
        if q:
            return queryset.filter(category_major=criterial['category'])
        else:
            return queryset


class AuctionTypeView(AuctionListView):

    def get_queryset(self):
        print("-" * 30)
        print(self.args)
        print(self.kwargs)
        print("-" * 30)
        # queryset = super(AuctionTypeView, self).get_queryset()

        value = self.kwargs.get('asset_type')
        print value
        if value == None:
            self.kwargs['asset_type'] == "commercial"

        if self.kwargs['asset_type'] == "auction":
            # queryset = self.model.objects.filter(transaction_type=self.kwargs['asset_type'])
            queryset = TranAuction.objects
        else:
            # queryset = self.model.objects.filter(asset_type=self.kwargs['asset_id'])
            queryset = TranCommercial.objects

        # queryset = self.form_filter(queryset, self.request)
        return queryset


class AuctionFormView(AuctionDetailView):

    def get_queryset(self):
        queryset = super(AuctionFormView, self).get_queryset()
        q = self.request.GET.get("q")
        if q:
            return queryset.filter(category=q)
        else:
            return queryset


class ActionSearch(FormView):
    # template_name = 'auctionapp/public/auction_list.html'
    form_class = AuctionForm

    def form_valid(self, form):
        return super(ActionSearch, self).form_valid(form)


class CommercialDetailView(DetailView):
    model = TranCommercial
    template_name = "auctionapp/public/commercial_detail.html"
    # context_object_name = 'commercial'

    def get_context_data(self, **kwargs):
        context = super(CommercialDetailView, self).get_context_data(**kwargs)

        t = TranCommercial.objects.get(pk=self.kwargs['pk'])
        context['commercial'] = t

        a = AssetProperty.objects.get(pk=t.asset_id)
        context['asset_type'] = a.asset_type
        context['asset_embadon'] = a.embadon
        context['latitude'] = a.latitude
        context['longitude'] = a.longitude

        return context

class CommercialListView(FilterView):
    # model = Auction
    model = TranCommercial
    template_name = "auctionapp/public/commercial_list.html"
    paginate_by = 10
    filterset_class = AuctionFilter

    def get_queryset(self):
        queryset = super(CommercialListView, self).get_queryset()
        # queryset = self.form_filter(queryset, self.request)
        try:
            queryset = AuctionFilter(request.GET, queryset=queryset)
            return render_to_response(template_name, {'filter': queryset,'page':10})
        except:
            pass
        return queryset

    def get_context_data(self, *args, **kwargs):
        # print("$" * 30)
        context = super(CommercialListView, self).get_context_data(**kwargs)

        paginator = Paginator(TranCommercial.objects.all(), 1)

        try:
            page_number = int(self.request.GET.get('page'))
            page = paginator.page(page_number)
        except:
            page_number = 1
            page = paginator.page(page_number)

        context['page'] = page_number
        # try:
        #     blogs = paginator.page(page)
        # except(EmptyPage):
        #     blogs = paginator.page(1)
        #
        # # Get the index of the current page
        # index = blogs.number - 1  # edited to something easier without index
        # # This value is maximum index of your pages, so the last page - 1
        max_index = len(paginator.page_range)
        context['pages'] = max_index
        context['results_per_page'] = 10
        context['next'] = page.next_page_number()

        if page_number==1:
            context['previous'] = 0
        else:
            context['previous'] = page.previous_page_number()

        # # You want a range of 7, so lets calculate where to slice the list
        # start_index = index - 10 if index >= 10 else 0
        # end_index = index + 10 if index <= max_index - 10 else max_index
        # # My new page range
        # context['page_numbers'] = paginator.page_range
        # page_range = page_range[start_index:end_index]
        context['has_next'] = page.has_next()
        context['has_previous'] = page.has_previous()
        context['types'] = types

        # context['page_range'] = page_range

        # context['categories'] = [x[0] for x in cat]
        # context['cities'] = [x[0] for x in cities]

        return context

    @classmethod
    def form_filter(cls, queryset, request):
        q = None
        if request.GET.get('category'):
            q = request.GET['category']
            # self.request.GET.pop(u'csrfmiddlewaretoken')
            print(request.GET)
            criterial = request.GET
        if q:
            return queryset.filter(category_major=criterial['category'])
        else:
            return queryset

class DashboardView(DetailView):
    model = TranCommercial
    template_name = "auctionapp/sbadmin/sb_admin_dashboard.html"
    # context_object_name = 'commercial'


@staff_member_required
def synchro(request):
    if 'update_properties' in request.POST:
        try:
            update_properties()
            msg = _('Properties tables updated.')
            messages.add_message(request, messages.INFO, msg)
        except Exception as e:

            msg = _('An error occured: %(msg)s (%(type)s)') % {'msg': str(e),
                                                               'type': e.__class__.__name__}
            messages.add_message(request, messages.ERROR, msg)

    elif 'delete_properties' in request.POST:
        try:
            delete_properties()
            msg = _('Properties tables deleted.')
            messages.add_message(request, messages.INFO, msg)
        except Exception as e:
            msg = _('An error occured: %(msg)s (%(type)s)') % {'msg': str(e),
                                                               'type': e.__class__.__name__}
            messages.add_message(request, messages.ERROR, msg)

    elif 'update_transactions' in request.POST:
        try:
            update_transactions()
            msg = _('Transaction tables updated.')
            messages.add_message(request, messages.INFO, msg)
        except Exception as e:

            msg = _('An error occured: %(msg)s (%(type)s)') % {'msg': str(e),
                                                               'type': e.__class__.__name__}
            messages.add_message(request, messages.ERROR, msg)

    elif 'delete_transactions' in request.POST:
        try:
            delete_transactions()
            msg = _('Transactions tables deleted.')
            messages.add_message(request, messages.INFO, msg)
        except Exception as e:
            msg = _('An error occured: %(msg)s (%(type)s)') % {'msg': str(e),
                                                               'type': e.__class__.__name__}
            messages.add_message(request, messages.ERROR, msg)


    elif 'update_search_sources_coops' in request.POST:
        try:
            update_search_sources_coops()
            msg = _('Search, sources, cooperators updated.')
            messages.add_message(request, messages.INFO, msg)
        except Exception as e:

            msg = _('An error occured: %(msg)s (%(type)s)') % {'msg': str(e),
                                                               'type': e.__class__.__name__}
            messages.add_message(request, messages.ERROR, msg)

    elif 'delete_search_sources_coops' in request.POST:
        try:
            delete_search_sources_coops()
            msg = _('Search_sources_coops tables deleted.')
            messages.add_message(request, messages.INFO, msg)
        except Exception as e:
            msg = _('An error occured: %(msg)s (%(type)s)') % {'msg': str(e),
                                                               'type': e.__class__.__name__}
            messages.add_message(request, messages.ERROR, msg)

    elif 'add_pois' in request.POST:
        try:
            add_pois()
            msg = _('Added new POIs.')
            messages.add_message(request, messages.INFO, msg)
        except Exception as e:
            msg = _('An error occured: %(msg)s (%(type)s)') % {'msg': str(e),
                                                               'type': e.__class__.__name__}
            messages.add_message(request, messages.ERROR, msg)

    return TemplateResponse(request, 'auctionapp/synchro.html')
