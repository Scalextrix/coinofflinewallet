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

signed_transaction_hex = raw_input("Type the Signed Transaction HEX: "
		
# send the transaction
sent_transaction = instruct_wallet('sendrawtransaction', [signed_transaction_hex])
if sent_transaction['error'] != None:
	print "Error in transaction broadcast: {}".format(sent_transaction['error']['message'])
else:
	print "Transaction Sent: {}".format(sent_transaction['result'])
