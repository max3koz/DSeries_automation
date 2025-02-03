import json
import logging

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

    def test_vdser_2051_get_server_status_wrong_session_id(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send get server status request wrong without session ID.")
        ping_session = Session.ping_session("22222222", login_params)

        logging.info(f"Step 3: Verify that get server status request status is 404")
        logging.info(ping_session)
        assert_that(ping_session.status_code,
                    f"Error: the session_response_code is {ping_session.status_code}").is_equal_to(404)

        logging.info("Step 4: Verify that response contains: {'parameter': 'session'}")
        expected_json = {'parameter': 'session'}
        response_body_content = json.loads(ping_session.content.decode("utf-8"))
        logging.info(response_body_content)
        assert_that(response_body_content,
                    f"Error: unexpected response {response_body_content}").is_equal_to(expected_json)

    def test_vdser_2052_get_server_status_empty_session_id(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send get server status request without empty session ID.")
        ping_session = Session.ping_session("", login_params)

        logging.info(f"Step 3: Verify that get server status request status is 404")
        logging.info(ping_session)
        assert_that(ping_session.status_code,
                    f"Error: the session_response_code is {ping_session.status_code}").is_equal_to(400)



        logging.info("Step 4: Verify that response contains: {'description': 'invalid uri or method', 'reference': ''}")
        expected_json = {'description': 'invalid uri or method', 'reference': ''}
        response_body_content = json.loads(ping_session.content.decode("utf-8"))
        logging.info(response_body_content)
        assert_that(response_body_content,
                    f"Error: unexpected response {response_body_content}").is_equal_to(expected_json)

    def test_vdser_2039_get_server_status_wrong_session_id_data(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send get server status request without wrong session id data.")
        ping_session = Session.ping_session("a22222222", login_params)

        logging.info(f"Step 3: Verify that ping session request status is 404")
        logging.info(ping_session)
        assert_that(ping_session.status_code,
                    f"Error: the session_response_code is {ping_session.status_code}").is_equal_to(400)

        logging.info("Step 4: Verify that response contains: {'description': 'parse error', 'reference': 'session'}")
        expected_json = {'description': 'parse error', 'reference': 'session'}
        response_body_content = json.loads(ping_session.content.decode("utf-8"))
        logging.info(response_body_content)
        assert_that(response_body_content,
                    f"Error: unexpected response {response_body_content}").is_equal_to(expected_json)
