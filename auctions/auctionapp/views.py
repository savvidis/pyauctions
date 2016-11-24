from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView, DetailView
from .models import *


# Create your views here.


def index(request):
    template = loader.get_template('auctionapp/auction_list.html')
    context = {
        'types': Type.objects.all()
    }
    return HttpResponse(template.render(context, request))


class AuctionListView(ListView):
    model = Auction
    template_name = "auctionapp/auction_list.html"


class AuctionDetailView(DetailView):
    model = Auction
    template_name = "auctionapp/auction_detail.html"
