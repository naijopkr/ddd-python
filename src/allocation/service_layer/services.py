from allocation.domain import model as m
from allocation.adapters import repository as r


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def allocate(line: m.OrderLine, repo: r.AbstractRepository, session) -> str:
    batches = repo.list()

    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')

    batchref = m.allocate(line, batches)
    session.commit()

    return batchref
