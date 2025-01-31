import logging
import pytest

from Api.session_management import Session

from assertpy import assert_that

from constants import login_params

class TestSessionManagement:
    def test_vdser_2030_create_correct_session(self, setup_class, schedule_window=100, as_run_log_window =100):
        logging.info(f"Step 1: Create session with vaild credential.")
        session = Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Verify that session was created with session ID = {session.session_id}.")
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

        logging.info(f"Step 2: Verify that request statue cod is {session.session_response.status_code}.")
        (assert_that(session.session_response.status_code, "Error: unexpected request status").
         is_equal_to(expected_status))

        logging.info(f"Step 3: Verify that response contains {expected_response_body}")
        (assert_that(session.session_response_body, "Error: unexpected response").
         contains(expected_response_body))

    def test_ping_session_positive(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        session = Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send ping session request.")
        session_response_code = Session.ping_session(session.session_id, login_params)

        logging.info(f"Step 3: Verify that ping session request status is 200")
        assert_that(session_response_code, "Error: the session ID is not exists").is_equal_to(200)

    def test_delete_session_positive(self, setup_class, schedule_window=16, as_run_log_window=16):
        logging.info(f"Step 1: Create session.")
        session = Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Step 2: Send delete session request.")
        session_response_code = Session.delete_session(session.session_id)

        logging.info(f"Step 3Veify that delete session request status is 200")
        assert_that(session_response_code, "Error: the session ID is not exists").is_equal_to(200)

        logging.info(f"Step 4: Send ping session request.")
        session_response_code = Session.ping_session(session.session_id, login_params)

        logging.info(f"Step 5: Verify that ping session request status is 404")
        assert_that(session_response_code, "Error: the session ID is not exists").is_equal_to(404)
