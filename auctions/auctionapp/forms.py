from django import forms

from .models import Auction

CATEGORIES = [(1, "Apartment"), (2, "House"), (3, "Villara")]


class AuctionForm(forms.ModelForm):

    class Meta:
        model = Auction
        fields = ('category_major', )
        category_major = forms.ChoiceField(choices=CATEGORIES, required=True)

    # def __init__(self, *args, **kwargs):
    #     super(AuctionForm, self).__init__(*args, **kwargs)
    #     self.fields["category"].required = True
