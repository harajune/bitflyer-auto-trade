#! encoding: utf-8

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import sys
import datetime


"""
helper functions
"""
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


"""
config
"""

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-52a9ab50-291b-11e5-baaa-0619f8945a4f'

pubnub = PubNub(pnconfig)

class BitflyerSubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presensce):
        pass

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            eprint("unexpected disconecct")

        elif status.category == PNStatusCategory.PNConnectedCategory:
            eprint("connected")

        elif status.category == PNStatusCategory.PNReconnectedCategory:
            eprint("reconnected")

        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            eprint("decryption error")

    def message(self, pubnub, message):
        data = message.message
        data["timestamp"] = datetime.datetime.now().isoformat()
        print(message.message)

pubnub.add_listener(BitflyerSubscribeCallback())
pubnub.subscribe().channels("lightning_board_FX_BTC_JPY").execute()

