import json
import logging
import pytest

from Api.session_management import Session
from assertpy import assert_that
from constants import login_params


class TestGetServerStatus:
    def test_vdser_2050_get_server_status_valid_session_id(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        session = Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send get server status request.")
        session_response = Session.get_server_status(session.session_id, login_params)

        logging.info(f"Step 3: Verify that get server status is 200")
        assert_that(session_response.status_code,
                    f"Error: the session_response_code is {session_response.status_code}").is_equal_to(200)

    @pytest.mark.parametrize("session_id, request_status, expected_data", [
        pytest.param("2222222222", 404, {"parameter": "session"}, id="not exist session id"),
        pytest.param("", 400, {'description': 'invalid uri or method', 'reference': ''}, id="empty session id"),
        pytest.param("2a2a2a2a2a", 400, {"description": "parse error", "reference": "session"},
                     id="wrong data type session id")
    ])
    def test_vdser_2051_2053_get_server_status_invalid_session_id(self, setup_class, session_id, request_status,
                                                                  expected_data):
        logging.info(f"Step 1: Send get server status request wrong without session ID.")
        ping_session = Session.ping_session(session_id, login_params)

        logging.info(f"Step 2: Verify that get server status request status is \"{request_status}\"")
        logging.info(ping_session)
        assert_that(ping_session.status_code,
                    f"Error: the session_response_code is {ping_session.status_code}").is_equal_to(request_status)

        logging.info(f"Step 3: Verify that server time data errors are: {expected_data}")
        for key, value in expected_data.items():
            data = json.loads(ping_session.text)[key]
            logging.info(f"The server time data error is \"{key}\": \"{value}\"")
            assert_that(data,
                        f"Error: The server time data error is not \"{data}\"").is_equal_to(value)


class TestGetServerTime:
    def test_vdser_2054_get_server_time_valid_session_id(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        session = Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send get server status request.")
        session_response = Session.get_server_status(session.session_id, login_params)

        logging.info(f"Step 3: Verify that get server status is 200")
        assert_that(session_response.status_code,
                    f"Error: the session_response_code is {session_response.status_code}").is_equal_to(200)

        logging.info(f"Step 4: Send get server time request.")
        time_response = Session.get_server_time(session.session_id, login_params)

        logging.info(f"Step 5: Verify that get server time request status is 200")
        assert_that(session_response.status_code,
                    f"Error: the session_response_code is {time_response.status_code}").is_equal_to(200)

        logging.info(f"Step 6: Verify that server time value is not empty")
        server_time = json.loads(time_response.text)['time']["time point"]
        logging.info(f"The server time value is {server_time}")
        assert_that(server_time, f"Error: the server time value is empty").is_not_empty()

    @pytest.mark.parametrize("session_id, request_status, expected_data", [
        pytest.param("2222222222", 404, {"parameter": "session"}, id="not exist session id"),
        pytest.param("", 400, {"description": "parse error", "reference": "session"}, id="empty session id"),
        pytest.param("2a2a2a2a2a", 400, {"description": "parse error", "reference": "session"},
                     id="wrong data type session id")
    ])
    def test_vdser_2055_2057_get_server_time_invalid_session_id(self, setup_class, session_id,
                                                                request_status,expected_data):
        logging.info(f"Step 1: Send get server time request.")
        time_response = Session.get_server_time(session_id, login_params)

        logging.info(f"Step 2: Verify that get server time request status is \"{request_status}\"")
        assert_that(time_response.status_code,
                    f"Error: the session_response_code is {time_response.status_code}").is_equal_to(request_status)

        logging.info(f"Step 3: Verify that server time data errors are: {expected_data}")
        for key, value in expected_data.items():
            data = json.loads(time_response.text)[key]
            logging.info(f"The server time data error is \"{key}\": \"{value}\"")
            assert_that(data,
                        f"Error: The server time data error is not \"{data}\"").is_equal_to(value)
