from django.test import TestCase

# Create your tests here.
from auctions.auctionapp.models import *


class EntryTestCase(TestCase):
    def test_auctionapp_insert(self):
        TypeDemo = dict()
        SourceDemo = dict()
        TypeDemo['asset_type'] = "Real Estate"
        t = Type(**TypeDemo)
        t.save()

        SourceDemo['source_site'] = "www.eurobank.gr"
        s = Source(**SourceDemo)
        s.save()

        AssetDemo = dict()

        AssetDemo['unique_code'] = "34234sdf"
        AssetDemo['name'] = "Katoikia sta diabata"
        AssetDemo['date_imported'] = datetime.now()
        AssetDemo['asset_type'] = Type.objects.get(asset_type="Real Estate")
        AssetDemo['debtor_name'] = "Spros"
        AssetDemo['debtor_vat_number'] = "123"
        AssetDemo['auctioneer_name'] = "Eurobank"
        AssetDemo['auctioneer_vat_number'] = "324"
        AssetDemo['offer_price'] = 23333
        AssetDemo['published_date'] = datetime.strptime('02/06/2015', '%d/%m/%Y')
        AssetDemo['description'] = 'the bast place to be'
        AssetDemo['source'] = Source.objects.get(source_site="www.eurobank.gr")

        a = Auction(**AssetDemo)
        a.save()
        auction_1 = Auction.objects.get(name="Katoikia sta diabata")
        print(auction_1.description)
        self.assertEqual(auction_1.description, 'the bast place to be')
