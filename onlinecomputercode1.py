#!/usr/bin/env python

### ON COMPUTER 1 (CONNECTED TO THE INTERNET) ###

api_key = ""  ### API key available from https://chainz.cryptoid.info/api.dws ###
rpc_user = "" ### rpcuser= in .conf file ###
rpc_pass = "" ### rpcpassword= in .conf file ###
rpc_port = "" ### standard rpc port for this coin ###
coin_iso = "" ### three digit ISO (eg btc, ltc) in the Chainz API URL ###

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

def get_utxos(api_key, from_address):
        url = "https://chainz.cryptoid.info/{}/api.dws?q=unspent&key={}&active={}".format(coin_iso, api_key, from_address)
        payload = json.dumps({"address": from_address})
        headers = {'content-type': "application/json", 'cache-control': "no-cache"}
        try:
                response = s.request("POST", url, data=payload, headers=headers)
                return json.loads(response.text)
        except requests.exceptions.RequestException as e:
                print e
                print 'Unable to Connect, is Chainz API available?  Backing off for 10 seconds'
                time.sleep(10)
        return get_utxos(api_key, from_address)

def get_balance(api_key, from_address):
        url = "https://chainz.cryptoid.info/{}/api.dws?q=getbalance&key={}&a={}".format(coin_iso, api_key, from_address)
        payload = json.dumps({"address": from_address})
        headers = {'content-type': "application/json", 'cache-control': "no-cache"}
        try:
                response = s.request("POST", url, data=payload, headers=headers)
                return json.loads(response.text)
        except requests.exceptions.RequestException as e:
                print e
                print 'Unable to Connect, is Chainz API available?  Backing off for 10 seconds'
                time.sleep(10)
        return get_balance(api_key, from_address)

s = requests.Session()

from_address=raw_input("Spend from which address?: ")
from_address_balance = get_balance(api_key, from_address)
print "Available balance: {}".format(from_address_balance)
spend_amount=round(float(raw_input("Amount of coins to spend?: ")), 8)
amount_inc_fee=spend_amount + 0.0001
if from_address_balance < amount_inc_fee:
  print "Error: Insufficient balance in address (after minimum fee of 0.0001)"	
	sys.exit()
to_address=raw_input("Send to which address?: ")

available_utxos=get_utxos(api_key, from_address)['unspent_outputs']
transaction_list=[]
utxo_input_amount=float(0)

# try to find single UTXO larger than the send amount including fee
try:
	utxo_input = [utxo for utxo in available_utxos if utxo['value'] > amount_inc_fee*100000000]
	# use the smallest one	
	utxo_input = min(utxo_input, key=lambda utxo:utxo['value'])
	transaction_list=[{"txid":utxo_input['tx_hash'],"vout":utxo_input['tx_ouput_n']}]
	utxo_input_amount = float(utxo_input['value'])/100000000
except:
	# iterate over largest values and sum to get enough inputs
	while True:
		utxo_input = max(available_utxos, key=lambda utxo:utxo['value'])
		tx_hash = utxo_input['tx_hash']
		vout = utxo_input['tx_ouput_n']
		utxo_value = float(utxo_input['value'])/100000000
		available_utxos.remove(utxo_input)
		transaction_list.append({"txid":tx_hash,"vout":vout})
		utxo_input_amount = utxo_input_amount + utxo_value
		if utxo_input_amount >= amount_inc_fee:
			break

change_amount = round(utxo_input_amount - amount_inc_fee, 8)
print "Change from transaction: {}".format(change_amount)

# create a rawtransaction
if from_address == to_address:
	print "Error: Send From and Send To addresses cannot be the same"
	sys.exit()
else:
	if change_amount == 0:
		raw_transaction = instruct_wallet('createrawtransaction', [transaction_list, {to_address:spend_amount}])
	else:
		raw_transaction = instruct_wallet('createrawtransaction', [transaction_list, {to_address:spend_amount, from_address:change_amount}])

if raw_transaction['error'] != None:
	print "Error in raw transaction: {}".format(raw_transaction['error']['message'])
else:
	print "Raw Transaction HEX: {}".format(raw_transaction['result'])

print "******************************************************************"
print "Transfer the Raw Transaction HEX to airgapped computer for signing"
print "******************************************************************"
