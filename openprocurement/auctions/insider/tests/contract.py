# -*- coding: utf-8 -*-
import unittest
from datetime import timedelta

from openprocurement.auctions.core.tests.contract import (
    AuctionContractResourceTestMixin,
    AuctionContractDocumentResourceTestMixin
)
from openprocurement.auctions.core.plugins.contracting.v3.tests.contract import (
    AuctionContractV3ResourceTestCaseMixin
)
from openprocurement.auctions.core.utils import get_now

from openprocurement.auctions.insider.tests.base import (
    BaseInsiderAuctionWebTest, test_bids,
)


class InsiderAuctionContractResourceTest(
    BaseInsiderAuctionWebTest,
    AuctionContractResourceTestMixin,
    AuctionContractV3ResourceTestCaseMixin,
):
    initial_status = 'active.auction'
    initial_bids = test_bids

    def setUp(self):
        super(InsiderAuctionContractResourceTest, self).setUp()
        # Create award
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('auction', ''))
        response = self.app.get('/auctions/{}'.format(self.auction_id))
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        value_threshold = auction['value']['amount'] + auction['minimalStep']['amount']

        now = get_now()
        auction_result = {
            'bids': [
                {
                    "id": b['id'],
                    "date": (now - timedelta(seconds=i)).isoformat(),
                    "value": {"amount": value_threshold * 2},

                }
                for i, b in enumerate(self.initial_bids)
            ]
        }

        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        self.app.authorization = authorization
        self.award = auction['awards'][0]
        self.award_id = self.award['id']
        self.award_value = self.award['value']
        self.award_suppliers = self.award['suppliers']

        self.set_status('active.qualification')

        response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, self.award_id, self.auction_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']

        response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, self.award_id, doc_id, self.auction_token), {"data": {
            "description": "auction protocol",
            "documentType": 'auctionProtocol'
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')
        self.assertEqual(response.json["data"]["author"], 'auction_owner')

        self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
            self.auction_id, self.award_id, self.auction_token
        ), {"data": {"status": "active"}})
        response = self.app.get('/auctions/{}'.format(self.auction_id))
        auction = response.json['data']
        self.award_contract_id = auction['contracts'][0]['id']


class InsiderAuctionContractDocumentResourceTest(BaseInsiderAuctionWebTest, AuctionContractDocumentResourceTestMixin):
    #initial_data = auction_data
    initial_status = 'active.auction'
    initial_bids = test_bids
    docservice = True

    def setUp(self):
        super(InsiderAuctionContractDocumentResourceTest, self).setUp()
        # Create award
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('auction', ''))
        response = self.app.get('/auctions/{}'.format(self.auction_id))
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        value_threshold = auction['value']['amount'] + auction['minimalStep']['amount']

        now = get_now()
        auction_result = {
            'bids': [
                {
                    "id": b['id'],
                    "date": (now - timedelta(seconds=i)).isoformat(),
                    "value": {"amount": value_threshold * 2},

                }
                for i, b in enumerate(self.initial_bids)
            ]
        }

        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        self.app.authorization = authorization
        self.award = auction['awards'][0]
        self.award_id = self.award['id']
        self.award_value = self.award['value']
        self.award_suppliers = self.award['suppliers']

        self.set_status('active.qualification')

        response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, self.award_id, self.auction_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']

        response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, self.award_id, doc_id, self.auction_token), {"data": {
            "description": "auction protocol",
            "documentType": 'auctionProtocol'
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')
        self.assertEqual(response.json["data"]["author"], 'auction_owner')

        self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
            self.auction_id, self.award_id, self.auction_token
        ), {"data": {"status": "active"}})
        # Getting contract for award
        response = self.app.get('/auctions/{}/contracts'.format(self.auction_id))
        contract = response.json['data'][0]
        self.contract_id = contract['id']


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(InsiderAuctionContractResourceTest))
    tests.addTest(unittest.makeSuite(InsiderAuctionContractDocumentResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
