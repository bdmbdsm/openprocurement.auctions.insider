# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import get_now
from openprocurement.auctions.core.validation import (
    update_logging_context,
    validate_data,
    validate_patch_auction_data,
)


def validate_auction_auction_data(request, **kwargs):
    data = validate_patch_auction_data(request)
    auction = request.validated['auction']
    if auction.status != 'active.auction':
        request.errors.add('body', 'data', 'Can\'t {} in current ({}) auction status'.format('report auction results' if request.method == 'POST' else 'update auction urls', auction.status))
        request.errors.status = 403
        return
    if data is not None:
        bids = data.get('bids', [])
        auction_bids_ids = [i.id for i in auction.bids]
        data['bids'] = [x for (y, x) in sorted(zip([auction_bids_ids.index(i['id']) for i in bids], bids))]
    else:
        data = {}
    if request.method == 'POST':
        now = get_now().isoformat()
        data['auctionPeriod'] = {'endDate': now}
    request.validated['data'] = data


def validate_item_data(request, error_handler, **kwargs):
    update_logging_context(request, {'item_id': '__new__'})
    context = request.context
    model = type(context).items.model_class
    validate_data(request, model, "item")


def validate_patch_item_data(request, error_handler, **kwargs):
    update_logging_context(request, {'item_id': '__new__'})
    context = request.context
    model = context.__class__
    validate_data(request, model)
