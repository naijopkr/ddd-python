import pytest
import requests
import uuid
import time

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
    input()

    assert r.status_code == 201
    assert r.json()['batchref'] == earlybatch


@pytest.mark.usefixtures('restart_api')
def test_allocations_are_persisted(add_stock):
    sku = random_sku()
    batch1, batch2 = random_batchref(1), random_batchref(2)
    order1, order2 = random_orderid(1), random_orderid(2)

    add_stock([
        (batch1, sku, 10, '2020-09-01'),
        (batch2, sku, 10, '2020-09-02'),
    ])

    line1 = {
        'orderid': order1,
        'sku': sku,
        'qty': 10
    }
    line2 = {
        'orderid': order2,
        'sku': sku,
        'qty': 10
    }

    url = config.get_api_url()

    # first order uses all stock in batch
    r = requests.post(f'{url}/allocate', json=line1)
    assert r.status_code == 201
    assert r.json()['batchref'] == batch1

    # second order should go to batch 2
    r2 = requests.post(f'{url}/allocate', json=line2)
    assert r2.status_code == 201
    assert r2.json()['batchref'] == batch2
