import logging
import pytest
import time

from threading import Thread

from Api.server_connect import create_server_connect_session, run_dservices_service, stop_server_session

@pytest.fixture(scope='class')
def setup_class():
    server_connect_session = create_server_connect_session()
    server_thread = Thread(target=run_dservices_service, args=[server_connect_session])
    server_thread.start()
    time.sleep(10)

    yield

    stop_server_session(server_connect_session)
    server_thread.join(10)