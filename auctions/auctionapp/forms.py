from django import forms

from .models import Auction


class AuctionForm(forms.Form):
    type = forms.CharField(label='type', max_length=100)
