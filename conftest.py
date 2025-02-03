import logging
import pytest
import time

from threading import Thread

from Api.server_connect import create_server_connect_session, run_dservices_service, stop_server_session
from Api.setup_update_management import (delete_file_on_server, verify_service_run, create_file_on_dservices_server,
                                         update_config_dict)
from constants import system_cfg_dict


@pytest.fixture(scope='class')
def setup_class():
    server_connect_session = create_server_connect_session()
    update_config_dict(system_cfg_dict, {'GENERAL': {'SESSION_TIMEOUT': '1200'}})
    create_file_on_dservices_server(server_connect_session, "system.cfg", system_cfg_dict)
    server_thread = Thread(target=run_dservices_service, args=[server_connect_session])
    server_thread.start()
    time.sleep(5)
    process_status = verify_service_run(server_connect_session, "d-services host")
    if process_status:
        yield
    else:
        logging.error(f"The process \"d-services host.exe\' is not started!!!")
    delete_file_on_server(server_connect_session, "system.cfg")
    stop_server_session(server_connect_session)
    server_thread.join(10)

@pytest.fixture(scope='function')
def setup_module_max():
    server_connect_session = create_server_connect_session()
    update_config_dict(system_cfg_dict, {'GENERAL': {'SESSION_TIMEOUT': '2147483647'}})
    create_file_on_dservices_server(server_connect_session, "system.cfg", system_cfg_dict)
    server_thread = Thread(target=run_dservices_service, args=[server_connect_session])
    server_thread.start()
    time.sleep(5)
    process_status = verify_service_run(server_connect_session, "d-services host")
    if process_status:
        yield
    else:
        logging.error(f"The process \"d-services host.exe\' is not started!!!")
    delete_file_on_server(server_connect_session, "system.cfg")
    stop_server_session(server_connect_session)
    server_thread.join(10)

@pytest.fixture(scope='function')
def setup_module_min():
    server_connect_session = create_server_connect_session()
    update_config_dict(system_cfg_dict, {'GENERAL': {'SESSION_TIMEOUT': '0'}})
    create_file_on_dservices_server(server_connect_session, "system.cfg", system_cfg_dict)
    server_thread = Thread(target=run_dservices_service, args=[server_connect_session])
    server_thread.start()
    time.sleep(5)
    process_status = verify_service_run(server_connect_session, "d-services host")
    if process_status:
        yield
    else:
        logging.error(f"The process \"d-services host.exe\' is not started!!!")
    delete_file_on_server(server_connect_session, "system.cfg")
    stop_server_session(server_connect_session)
    server_thread.join(10)

@pytest.fixture(scope='function')
def setup_module_negative():
    server_connect_session = create_server_connect_session()
    update_config_dict(system_cfg_dict, {'GENERAL': {'SESSION_TIMEOUT': '-30'}})
    create_file_on_dservices_server(server_connect_session, "system.cfg", system_cfg_dict)
    server_thread = Thread(target=run_dservices_service, args=[server_connect_session])
    server_thread.start()
    time.sleep(5)
    process_status = verify_service_run(server_connect_session, "d-services host")
    if process_status:
        yield
    else:
        logging.error(f"The process \"d-services host.exe\' is not started!!!")
    delete_file_on_server(server_connect_session, "system.cfg")
    stop_server_session(server_connect_session)
    server_thread.join(10)
