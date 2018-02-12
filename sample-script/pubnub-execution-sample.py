#! encoding: utf-8

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import sys


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
            # print header
        for v in message.message:
            print("%d,%s,%d,%f,%s,%s,%s" % 
                (v["id"],v["side"],v["price"],v["size"],
                v["exec_date"],v["buy_child_order_acceptance_id"],
                v["sell_child_order_acceptance_id"]))


pubnub.add_listener(BitflyerSubscribeCallback())
pubnub.subscribe().channels("lightning_executions_FX_BTC_JPY").execute()

