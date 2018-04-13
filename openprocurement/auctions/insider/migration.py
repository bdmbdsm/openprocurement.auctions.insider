# -*- coding: utf-8 -*-
import logging

from openprocurement.auctions.core.plugins.awarding.v3.migration import (
    migrate_awarding2_to_awarding3
)
from openprocurement.auctions.core.traversal import Root
from openprocurement.auctions.core.utils import get_now


LOGGER = logging.getLogger(__name__)
SCHEMA_VERSION = 1
SCHEMA_DOC = 'openprocurement_auctions_insider_schema'


def get_db_schema_version(db):
    schema_doc = db.get(SCHEMA_DOC, {"_id": SCHEMA_DOC})
    return schema_doc.get("version", SCHEMA_VERSION - 1)


def set_db_schema_version(db, version):
    schema_doc = db.get(SCHEMA_DOC, {"_id": SCHEMA_DOC})
    schema_doc["version"] = version
    db.save(schema_doc)


def migrate_data(registry, destination=None):
    existing_plugins = ['auctions.insider' in registry.settings['plugins'].split(',')]
    if registry.settings.get('plugins') and not any(existing_plugins):
        return
    cur_version = get_db_schema_version(registry.db)
    if cur_version == SCHEMA_VERSION:
        return cur_version
    for step in xrange(cur_version, destination or SCHEMA_VERSION):
        LOGGER.info("Migrate openprocurement auction schema from {} to {}".format(step, step + 1), extra={'MESSAGE_ID': 'migrate_data'})
        migration_func = globals().get('from{}to{}'.format(step, step + 1))
        if migration_func:
            migration_func(registry)
        set_db_schema_version(registry.db, step + 1)


def from0to1(registry):
    class Request(object):
        def __init__(self, registry):
            self.registry = registry

    results = registry.db.iterview('auctions/all', 2 ** 10, include_docs=True)

    request = Request(registry)
    root = Root(request)

    docs = []
    for i in results:
        auction = i.doc
        changed = migrate_awarding2_to_awarding3(auction, registry.server_id, (auction['procurementMethodType']))
        if not changed:
            continue
        model = registry.auction_procurementMethodTypes.get(auction['procurementMethodType'])
        if model:
            try:
                auction = model(auction)
                auction.__parent__ = root
                auction = auction.to_primitive()
            except: # pragma: no cover
                LOGGER.error("Failed migration of auction {} to schema 1.".format(auction.id), extra={'MESSAGE_ID': 'migrate_data_failed', 'AUCTION_ID': auction.id})
            else:
                auction['dateModified'] = get_now().isoformat()
                docs.append(auction)
        if len(docs) >= 2 ** 7:  # pragma: no cover
            registry.db.update(docs)
            docs = []
    if docs:
        registry.db.update(docs)
