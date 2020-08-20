import os

def get_postgres_uri():
    host = os.environ.get('DB_HOST', 'localhost')
    port = 5432
    password = os.environ.get('DB_PASSWORD', 'abc123')
    user, db_name = 'postgres', 'allocation'

    return f'postgres://{user}:{password}@{host}:{port}/{db_name}'

def get_api_url():
    host = os.environ.get('API_HOST', 'localhost')
    port = 5000

    return f'http://{host}:{port}'
