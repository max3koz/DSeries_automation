import logging

from Api.session_management import create_session, ping_session, delete_session

from assertpy import assert_that

class TestSessionManagement:
    def test_create_session_positive(self, schedule_window=100, as_run_log_window =100):
        session_id = create_session(schedule_window, as_run_log_window)
        logging.info(f"Session ID = {session_id}.")
        assert_that(session_id, "Error: the session ID is not exists").is_not_empty()

    def test_ping_session_positive(self, schedule_window=16, as_run_log_window=16):
        session_id = create_session(schedule_window, as_run_log_window)
        session_response_code = ping_session(session_id)
        logging.info(session_response_code)
        assert_that(session_response_code, "Error: the session ID is not exists").is_equal_to(200)

    def test_delete_session_positive(self, schedule_window=16, as_run_log_window=16):
        session_id = create_session(schedule_window, as_run_log_window)
        session_response_code = delete_session(session_id)
        logging.info(session_response_code)
        assert_that(session_response_code, "Error: the session ID is not exists").is_equal_to(200)
        session_response_code = ping_session(session_id)
        logging.info(session_response_code)
        assert_that(session_response_code, "Error: the session ID is not exists").is_equal_to(404)