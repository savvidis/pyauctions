from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView, DetailView
from .models import *
import json

# Create your views here.


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


class AuctionDetailView(DetailView):
    model = Auction
    template_name = "auctionapp/public/auction_detail.html"


class AuctionListView(ListView):
    model = Auction
    template_name = "auctionapp/public/auction_list.html"

    def get_queryset(self):
        if self.request.GET.get('type'):
            print(self.request.GET['type'])
        if self.request.user.is_staff:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(price_num__gt=1000000)

    def get_context_data(self, **kwargs):
        context = super(AuctionListView, self).get_context_data(**kwargs)

        # Manipulate the query with functions in the model

        # events_queryset = self.model.objects.future()
        # if not self.request.user.is_staff:
        #     events_queryset = events_queryset.published()
        #
        # context['events'] = events_queryset[:3]

        return context

# class AuctionDetailView(DetailView):
#     model = Auction
#     template_name = "auctionapp/public/auction_detail.html"
