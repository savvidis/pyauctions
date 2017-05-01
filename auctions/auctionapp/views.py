from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView, DetailView, FormView
from django_filters.views import FilterView
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import AuctionFilter
import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from utility import *

# Create your views here.

categories = ["Apartment", "House", "Maisonette", "Detached House"]

types = ["realestate", "auction", "cars"]


class AuctionDetailView(DetailView):
    model = Auction
    template_name = "auctionapp/public/auction_detail.html"


class AuctionListView(FilterView):
    model = Auction
    template_name = "auctionapp/public/auction_list.html"
    paginate_by = 10
    filterset_class = AuctionFilter

    def get_queryset(self):
        queryset = super(AuctionListView, self).get_queryset()
        # queryset = self.form_filter(queryset, self.request)
        try:
            queryset = AuctionFilter(request.GET, queryset=queryset)
            return render_to_response(template_name, {'filter': queryset})
        except:
            pass
        return queryset

    def get_context_data(self, *args, **kwargs):
        print("$" * 30)
        context = super(AuctionListView, self).get_context_data(**kwargs)
        # cat = self.model.objects.order_by().values_list(
        #     'category_major').distinct()  # returns a dictionary
        # cities = self.model.objects.order_by().values_list(
        #     'city').distinct()
        # regions = self.model.objects.order_by().values_list(
        #     'region').distinct()
        # print(regions)
        # Manipulate the query with functions in the model
        # events_queryset = self.model.objects.future()
        # if not self.request.user.is_staff:
        #     events_queryset = events_queryset.published()
        #
        # context['events'] = events_queryset[:3]
        context['types'] = types

        # context['categories'] = [x[0] for x in cat]
        # context['cities'] = [x[0] for x in cities]

        print(context)

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
        if self.kwargs['asset_type'] == "auction":
            queryset = self.model.objects.filter(
                transaction_type=self.kwargs['asset_type'])
        else:
            queryset = self.model.objects.filter(
                asset_type=self.kwargs['asset_type'])
        queryset = self.form_filter(queryset, self.request)
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
    template_name = 'auctionapp/public/auction_list.html'
    form_class = AuctionForm

    def form_valid(self, form):
        return super(ActionSearch, self).form_valid(form)


def AuctionListView2(request):
    template = loader.get_template('auctionapp/public/auction_list.html')
    json_data = open('capitalRE.json')
    data1 = json.load(json_data)
    data2 = json.dumps(data1)

    json_data.close()
    context = {
        'object_list': data1
    }
    return HttpResponse(template.render(context, request))


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

    return TemplateResponse(request, 'auctionapp/synchro.html')
