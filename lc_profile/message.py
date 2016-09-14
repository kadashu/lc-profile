from leancloud import client
from time import time


def send_message(conv_id, from_peer, message):
    message['send_at'] = time()

    resp = client.post('/rtm/messages', dict(
        conv_id=conv_id,
        from_peer=from_peer,
        no_sync=True,
        transient=False,
        message=message
    ))

    resp.raise_for_status()
    return resp.json()
