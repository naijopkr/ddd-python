import pytest

from allocation.adapters import repository
from allocation.domain import model
from allocation.service_layer import services

class FakeRepository(repository.AbstractRepository):

    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return (next(
            b for b in self._batches if b.reference == reference
        ))

    def list(self):
        return list(self._batches)


class FakeSession():
    committed = False

    def commit(self):
        self.committed = True


def test_returns_allocation():
    line = model.OrderLine('o1', 'lamp', 10)
    batch = model.Batch('b1', 'lamp', 100, eta=None)

    repo = FakeRepository([batch])

    result = services.allocate(line, repo, FakeSession())
    assert result == 'b1'


def test_error_for_invalid_sku():
    line = model.OrderLine('o1', 'fake_sku', 10)
    batch = model.Batch('b1', 'real_sku', 100, eta=None)
    repo = FakeRepository([batch])

    with pytest.raises(
        services.InvalidSku,
        match='Invalid sku fake_sku'
    ):
        services.allocate(line, repo, FakeSession())


def test_commits():
    line = model.OrderLine('o1', 'mirror', 10)
    batch = model.Batch('b1', 'mirror', 100, eta=None)
    repo = FakeRepository([batch])
    session = FakeSession()

    services.allocate(line, repo, session)
    assert session.committed is True
