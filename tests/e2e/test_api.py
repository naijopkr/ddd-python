import pytest
import requests
import uuid

from allocation import config

def random_sufix():
    return uuid.uuid4().hex[:6]

def random_sku(name=''):
    return f'sku-{name}-{random_sufix()}'

def random_batchref(name=''):
    return f'batch-{name}-{random_sufix()}'

def random_orderid(name=''):
    return f'order-{name}-{random_sufix()}'


@pytest.mark.usefixtures('restart_api')
def test_api_returns_allocation(add_stock):
    sku, othersku = random_sku(), random_sku('other')
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)

    add_stock([
        (laterbatch, sku, 100, '2020-09-02'),
        (earlybatch, sku, 100, '2020-09-01'),
        (otherbatch, othersku, 100, None)
    ])

    data = {
        'orderid': random_orderid(),
        'sku': sku,
        'qty': 3
    }

    url = config.get_api_url()

    r = requests.post(f'{url}/allocate', json=data)

    assert r.status_code == 201
    assert r.json()['batchref'] == earlybatch
