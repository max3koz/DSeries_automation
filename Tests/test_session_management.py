import json
import logging
import time

import pytest

from Api.session_management import Session
from assertpy import assert_that
from constants import login_params


class TestCreateSession:
    def test_vdser_2030_create_correct_session(self, setup_class, schedule_window=100, as_run_log_window =100):
        logging.info(f"Step 1: Create session with vaild credential.")
        session = Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Verify that session was created with session ID.")
        assert_that(session.session_id, "Error: the session ID is not exists").is_not_empty()

    @pytest.mark.parametrize("invalid_credentials, expected_status, expected_response_body", [
        pytest.param({'user name': '1', 'password': '1'}, 403, "bad credentials",
                     id="unexpected login and password"),
        pytest.param({'user name': '1', 'password': ''}, 403, "bad credentials", id="unexpected login"),
        pytest.param({'user name': '0', 'password': '1'}, 403, "bad credentials", id="unexpected password")
    ])
    def test_vdser_2031_create_invalid_session(self, setup_class, invalid_credentials, expected_status,
                                               expected_response_body, schedule_window=100, as_run_log_window=100):
        logging.info(f"Step 1: Create session with invaild credential: {invalid_credentials}.")
        session = Session(invalid_credentials, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Verify that request statue code is {session.session_response.status_code}.")
        (assert_that(session.session_response.status_code, "Error: unexpected request status").
         is_equal_to(expected_status))

        logging.info(f"Step 3: Verify that response contains {expected_response_body}")
        (assert_that(session.session_response_body,
                     f"Error: unexpected response {session.session_response_body}").
         contains(expected_response_body))


class TestSessionLimitTime:
    def test_vdser_2032_create_session_with_min_limit_time(self, setup_module_min,
                                                       schedule_window=100, as_run_log_window =100):
        logging.info(f"Step 1: Create session with vaild credential.")
        session = Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Verify that session was created with session ID = {session.session_id}.")
        assert_that(session.session_id, "Error: the session ID is not exists").is_not_empty()
        time.sleep(5)

        logging.info(f"Step 3: Send ping session request.")
        session_response = Session.ping_session(session.session_id, login_params)

        logging.info(f"Step 4: Verify that session was dropped")
        assert_that(session_response.status_code,
                    f"Error: the session response code is {session_response.status_code}").is_equal_to(404)

    def test_vdser_2033_create_session_with_max_limit_time(self, setup_module_max,
                                                       schedule_window=100, as_run_log_window =100):
        logging.info(f"Step 1: Create session with vaild credential.")
        session = Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Verify that session was created with session ID = {session.session_id}.")
        assert_that(session.session_id, "Error: the session ID is not exists").is_not_empty()

    def test_vdser_2034_create_session_with_negative_limit_time(self, setup_module_negative,
                                                       schedule_window=100, as_run_log_window =100):
        logging.info(f"Step 1: Create session with vaild credential.")
        session = Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Verify that session was created with session ID = {session.session_id}.")
        assert_that(session.session_id, "Error: the session ID is not exists").is_not_empty()

        logging.info(f"Step 3: Send ping session request.")
        session_response = Session.ping_session(session.session_id, login_params)

        logging.info(f"Step 4: Verify that session was dropped")
        assert_that(session_response.status_code,
                    f"Error: the session_response_code is {session_response.status_code}").is_equal_to(404)

    def test_vdser_2043_ping_session_id_after_life_time(self, setup_module_min, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        session = Session(login_params, schedule_window, as_run_log_window)
        time.sleep(5)

        logging.info(f"Step 2: Send ping session request.")
        ping_session = Session.ping_session(session.session_id, login_params)

        logging.info(f"Step 3: Verify that ping session request status is 404")
        logging.info(ping_session)
        assert_that(ping_session.status_code,
                    f"Error: the session_response_code is {ping_session.status_code}").is_equal_to(404)

        logging.info("Step 4: Verify that response contains: {'parameter': 'session'}")
        expected_json = {'parameter': 'session'}
        response_body_content = json.loads(ping_session.content.decode("utf-8"))
        logging.info(response_body_content)
        assert_that(response_body_content,
                    f"Error: unexpected response {response_body_content}").is_equal_to(expected_json)


class TestDestroySession:
    def test_vdser_2035_destroy_available_session(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        session = Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send delete session request.")
        session_response = Session.delete_session(session.session_id)

        logging.info(f"Step 3: Verify that delete session request status is 200")
        assert_that(session_response.status_code,
                    f"Error: the session response code {session_response.status_code}").is_equal_to(200)

        logging.info(f"Step 4: Send ping session request.")
        session_response = Session.ping_session(session.session_id, login_params)

        logging.info(f"Step 5: Verify that ping session request status is 404")
        assert_that(session_response.status_code,
                    f"Error: the session_response_code is {session_response.status_code}").is_equal_to(404)

    def test_vdser_2036_destroy_wrong_session_id(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send delete session request.")
        destroy_session = Session.delete_session("2161583127")

        logging.info(f"Step 3: Verify that delete session request status is 404")
        assert_that(destroy_session.status_code,
                    f"Error: the session response code is {destroy_session.status_code}").is_equal_to(404)

        logging.info(f"Step 4: Verify that response contains \"session\"")
        expected_json = {'parameter': 'session'}
        response_body_content = json.loads(destroy_session.content.decode("utf-8"))
        logging.info(response_body_content)
        assert_that(response_body_content,
                    f"Error: unexpected response {response_body_content}").is_equal_to(expected_json)

    def test_vdser_2037_destroy_empty_session_id(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send delete session request.")
        destroy_session = Session.delete_session("")

        logging.info(f"Step 3: Verify that delete session request status is 400")
        assert_that(destroy_session.status_code,
                    "Error: the session_response_code is {session_response_code}").is_equal_to(400)

        logging.info(f"Step 4: Verify that response contains \"invalid uri or method\"")
        expected_json = {'description': 'invalid uri or method', 'reference': ''}
        response_body_content = json.loads(destroy_session.content.decode("utf-8"))
        logging.info(response_body_content)
        assert_that(response_body_content,
                    f"Error: unexpected response {response_body_content}").is_equal_to(expected_json)

    def test_vdser_2038_destroy_empty_session_id(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send delete session request.")
        destroy_session = Session.delete_session("aa222222")

        logging.info(f"Step 3: Verify that delete session request status is 400")
        assert_that(destroy_session.status_code,
                    "Error: the session_response_code is {session_response_code}").is_equal_to(400)

        logging.info(f"Step 4: Verify that response contains:  \"description\": \"parse error\", "
                     f"\"reference\": \"session\"")
        expected_json = {"description": "parse error", "reference": "session"}
        response_body_content = json.loads(destroy_session.content.decode("utf-8"))
        logging.info(response_body_content)
        assert_that(response_body_content,
                    f"Error: unexpected response {response_body_content}").is_equal_to(expected_json)


class TestPingSession:
    def test_vdser_2040_ping_valid_session(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        session = Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send ping session request.")
        session_response = Session.ping_session(session.session_id, login_params)

        logging.info(f"Step 3: Verify that ping session request status is 200")
        assert_that(session_response.status_code,
                    f"Error: the session_response_code is {session_response.status_code}").is_equal_to(200)

    def test_vdser_2041_ping_empty_session_id(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send ping session request without session ID.")
        ping_session = Session.ping_session("", login_params)

        logging.info(f"Step 3: Verify that ping session request status is 404")
        logging.info(ping_session)
        assert_that(ping_session.status_code,
                    f"Error: the session_response_code is {ping_session.status_code}").is_equal_to(400)

        logging.info("Step 4: Verify that response contains: {'description': 'invalid uri or method', 'reference': ''}")
        expected_json = {'description': 'invalid uri or method', 'reference': ''}
        response_body_content = json.loads(ping_session.content.decode("utf-8"))
        logging.info(response_body_content)
        assert_that(response_body_content,
                    f"Error: unexpected response {response_body_content}").is_equal_to(expected_json)

    def test_vdser_2042_ping_wrong_session_id(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send ping session request without session ID.")
        ping_session = Session.ping_session("22222222", login_params)

        logging.info(f"Step 3: Verify that ping session request status is 404")
        logging.info(ping_session)
        assert_that(ping_session.status_code,
                    f"Error: the session_response_code is {ping_session.status_code}").is_equal_to(404)

        logging.info("Step 4: Verify that response contains: {'parameter': 'session'}")
        expected_json = {'parameter': 'session'}
        response_body_content = json.loads(ping_session.content.decode("utf-8"))
        logging.info(response_body_content)
        assert_that(response_body_content,
                    f"Error: unexpected response {response_body_content}").is_equal_to(expected_json)

    def test_vdser_2039_ping_wrong_session_id_data(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send ping session request wrong session id data.")
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
