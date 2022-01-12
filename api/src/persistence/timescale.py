import logging
from uuid import UUID, uuid4
from contextlib import contextmanager
from enum import Enum
from datetime import datetime
from typing import List, NamedTuple, Union

import psycopg2
from psycopg2.extras import register_uuid, DictCursor, NamedTupleCursor
from pydantic import BaseModel, SecretStr

LOGGER = logging.getLogger(__name__)


class CursorFactory(Enum):
    DICT_CURSOR = DictCursor
    NAMED_TUPLE_CURSOR = NamedTupleCursor


class PostgresCredentials(BaseModel):
    """Data class containing fields used to
    store postgres connection settings"""

    PG_HOST: str
    PG_DATABASE: str
    PG_USER: str
    PG_PASSWORD: SecretStr
    PG_PORT: int = 5432


@contextmanager
def get_cursor(credentials: PostgresCredentials,
               cursor_factory: CursorFactory = CursorFactory.NAMED_TUPLE_CURSOR):
    """Returns a cursor as context manager.
    Returns a cursor as a context manager using the credentials
    matching the `connection_name` from the PostgresCredentialsManager.
    Args:
        connection_name (str): The database name in the PostgresCredentialManager.
        cursor_factory (CursorFactory): The cursor factory to user.
    Returns:
        cursor (psycopg2.cursor): A cursor to be used as a context manager.
    """

    with get_connection(credentials) as connection:
        cursor = connection.cursor(cursor_factory=cursor_factory.value)
        try:
            yield cursor
            connection.commit()
        finally:
            cursor.close()


@contextmanager
def get_connection(credentials: PostgresCredentials):
    connection = psycopg2.connect(
        dbname=credentials.PG_DATABASE,
        user=credentials.PG_USER,
        host=credentials.PG_HOST,
        password=credentials.PG_PASSWORD.get_secret_value(),
        port=credentials.PG_PORT
    )
    register_uuid(conn_or_curs=connection)

    try:
        yield connection
    finally:
        connection.close()


def insert_network(creds: PostgresCredentials,
                   network_name: str,
                   network_description: str) -> UUID:
    """Function used to insert new network entry
    into database

    Args:
        creds (PostgresCredentials): [description]
        network_name (str): [description]
        network_description (str): [description]

    Returns:
        UUID: [description]
    """

    network_id = uuid4()
    with get_cursor(creds) as db:
        db.execute('INSERT INTO networks(network_id,network_name,network_description) '
                   'VALUES(%s,%s,%s)', (network_id, network_name, network_description))
    return network_id

def get_networks(creds: PostgresCredentials) -> List:
    """Function used to insert new network entry
    into database

    Args:
        creds (PostgresCredentials): [description]
        network_name (str): [description]
        network_description (str): [description]

    Returns:
        UUID: [description]
    """

    with get_cursor(creds) as db:
        db.execute('SELECT network_id,network_name,network_description FROM networks')
        results = db.fetchall()
    return list(results) if results else []


def get_network_details(creds: PostgresCredentials, network_id: UUID) -> Union[NamedTuple, None]:
    """Function used to insert new network entry
    into database

    Args:
        creds (PostgresCredentials): [description]
        network_name (str): [description]
        network_description (str): [description]

    Returns:
        UUID: [description]
    """

    with get_cursor(creds) as db:
        db.execute('SELECT network_id,network_name,network_description FROM networks '
                   'WHERE network_id = %s', (network_id,))
        result = db.fetchone()
    return result if result else None


def insert_network_stat(creds: PostgresCredentials,
                        network_id: UUID,
                        event_timestamp: datetime,
                        download_speed: float,
                        exec_time: float,
                        upload_speed: float = None):
    """DB function used to insert new network stat
    into database

    Args:
        network_id (UUID): [description]
        download_speed (float): [description]
        exec_time (float): [description]
        upload_speed (float, optional): [description]. Defaults to None.
    """

    with get_cursor(creds) as db:
        db.execute('INSERT INTO network_stats(network_id,download_speed,upload_speed,exec_time,event_timestamp) '
                   'VALUES(%s,%s,%s,%s,%s)', (network_id, download_speed, upload_speed, exec_time,event_timestamp))


def get_timeseries(creds: PostgresCredentials,
                   network_id: UUID,
                   start: datetime,
                   end: datetime) -> List:
    """Function to retrieve network timeseries
    for a given network ID, start and end date

    Args:
        creds (PostgresCredentials): [description]
        network_id (UUID): [description]
        start (datetime): [description]
        end (datetime): [description]

    Returns:
        List: [description]
    """

    end = end if end else datetime.utcnow()
    with get_cursor(creds) as db:
        db.execute('SELECT download_speed,upload_speed,exec_time,event_timestamp '
                   'FROM network_stats WHERE network_id = %s AND event_timestamp > %s '
                   'AND event_timestamp < %s', (network_id, start, end))
        results = db.fetchall()
    return results if results else []
