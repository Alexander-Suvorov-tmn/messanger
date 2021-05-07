import json


def write_order_to_json(it, qu, pr, bu, da):
    d = {}

    d['item'] = it
    d['quanty'] = qu
    d['price'] = pr
    d['buyer'] = bu 
    d['data'] = da

    with open('orders.json', 'w') as f_n:
        json.dump(d, f_n, indent=4)


write_order_to_json('SA', 5, 20, 'DFG', 17.05)