# coding: utf-8

from __future__ import unicode_literals
from leancloud import client as lc_client, init as lc_init
from time import time

from .metric import wrap_incr, wrap_timing


def init(app_id, master_key):
    lc_init(app_id, master_key=master_key)


@wrap_incr('messages.send')
@wrap_timing('messages.send')
def send_message(conv_id, from_peer, message):
    message.set_attrs(sent_at=time())

    resp = lc_client.post('/rtm/messages', dict(
        conv_id=conv_id,
        from_peer=from_peer,
        no_sync=True,
        transient=False,
        message=message
    ))

    resp.raise_for_status()
    return resp.json()
