rpc_user = "" ### rpcuser= in .conf file ###
rpc_pass = "" ### rpcpassword= in .conf file ###
rpc_port = "" ### standard rpc port for this coin ###

import requests
import json
import sys
import time

def instruct_wallet(method, params):
        url = "http://127.0.0.1:{}/".format(rpc_port)
        payload = json.dumps({"method": method, "params": params})
        headers = {'content-type': "application/json", 'cache-control': "no-cache"}
        try:
                response = s.request("POST", url, data=payload, headers=headers, auth=(rpc_user, rpc_pass))
                return json.loads(response.text)
        except requests.exceptions.RequestException as e:
                print e
                print 'Unable to Connect, is Wallet running?  Backing off for 10 seconds'
                time.sleep(10)
        return instruct_wallet(method, params)

raw_transaction_hex = raw_input("Type the Raw Transaction HEX: "

# sign the transaction
signed_transaction = instruct_wallet('signrawtransaction', [raw_transaction_hex])
if signed_transaction['error'] != None:
	print "Error in transaction signature: {}".format(signed_transaction['error']['message'])
else:
	print "Signed Transaction HEX: {}".format(signed_transaction['result']['hex'])

print "*****************************************************************"
print "Transfer Signed Transaction HEX to networked computer for signing"
print "*****************************************************************"
