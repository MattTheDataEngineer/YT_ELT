import os
import pytest
import psycopg2
from unittest import mock
from airflow.models import Variable, Connection, DagBag


@pytest.fixture
def api_key():
    with mock.patch.dict("os.environ", AIRFLOW_VAR_API_KEY="MOCK_KEY1234"):
        yield Variable.get("API_KEY")


@pytest.fixture
def channel_handle():
    with mock.patch.dict("os.environ", AIRFLOW_VAR_CHANNEL_HANDLE="MRCHEESE"):
        yield Variable.get("CHANNEL_HANDLE")


@pytest.fixture
def mock_postgres_conn_vars():
    conn = Connection(
        login="mock_username",
        password="mock_password",
        host="mock_host",
        port=1234,
        schema="mock_db_name",  # schema is the db name
    )
    conn_uri = conn.get_uri()

    with mock.patch.dict("os.environ", AIRFLOW_CONN_POSTGRES_DB_YT_ELT=conn_uri):
        yield Connection.get_connection_from_secrets(conn_id="POSTGRES_DB_YT_ELT")


@pytest.fixture()
def dagbag():
    yield DagBag()


@pytest.fixture()
def airflow_variable():
    def get_airflow_variable(variable_name):
        env_var = f"AIRFLOW_VAR_{variable_name.upper()}"
        return os.getenv(env_var)

    return get_airflow_variable


@pytest.fixture
def real_postgres_connection():
    dbname = os.getenv("ELT_DATABASE_NAME")
    user = os.getenv("ELT_DATABASE_USERNAME")
    password = os.getenv("ELT_DATABASE_PASSWORD")
    host = os.getenv("POSTGRES_CONN_HOST")
    port = os.getenv("POSTGRES_CONN_PORT")

    conn = None

    try:
        conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )

        yield conn

    except psycopg2.Error as e:
        pytest.fail(f"Failed to connect to the database: {e}")

    finally:
        if conn:
            conn.close()
