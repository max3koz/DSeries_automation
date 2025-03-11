import json
import logging
import pytest

from assertpy import assert_that

from Components_Dservises.buses_management import get_bus_configuration, get_bus_status, get_buses
from Components_Dservises.session_management import Session
from constants import login_params, schedule_window, as_run_log_window

class TestBusMNG:
    @classmethod
    def setup_method(cls):
        logging.info(f"Precondition 1: Create session.")
        cls.session = Session(login_params, schedule_window, as_run_log_window)

        logging.info(f"Precondition 2: Send get server status request.")
        session_response = Session.get_server_status(cls.session.session_id, login_params)

        logging.info(f"Precondition 3: Verify that get server status is 200")
        assert_that(session_response.status_code,
                    f"Error: the session_response_code is {session_response.status_code}").is_equal_to(200)

    def test_vdser_2058_get_bus_configuration_valid_data(self, setup_class):
        logging.info(f"Step 1: Send get server status request.")
        session_id = self.session.session_id
        get_bus_configuration_response = get_bus_configuration(session_id, 1, login_params)

        logging.info(f"Step 2: Verify that get bus configuration status is 200")
        assert_that(get_bus_configuration_response.status_code,
                    f"Error: the get bus configuration response is "
                    f"{get_bus_configuration_response.status_code}").is_equal_to(200)

        logging.info(f"Step 3: Verify that responce body with expected data")
        expected_result = {"name": "TYPEC1-2",
                           "description": "TYPE-C 1-2",
                           "permissions": ["control", "edit", "export", "import"],
                           "flags": "128",
                           "timezone": "UTC",
                           "day change": "P0DT0H0M0S",
                           "frame rate": "30",
                           "alternate schedules": ["16", "17"],
                           "machines": [{"category": "none", "monitor name": ""},
                                        {"category": "none", "monitor name": ""},
                                        {"category": "none", "monitor name": ""},
                                        {"category": "none", "monitor name": ""}],
                           "roll under bus": "65535",
                           "color index": "0"}
        response_body = json.loads(get_bus_configuration_response.text)
        assert_that(response_body, f"Error: the get bus configuration response is "
                                   f"{get_bus_configuration_response.status_code}").is_equal_to(expected_result)

    @pytest.mark.parametrize("session_id, bus_id, request_status, expected_data", [
        pytest.param("2222222222", 1, 404, {"parameter": "session"}, id="wrong session id and valid bus ID"),
        pytest.param("valid_session_id", 1000, 404, {"parameter": "bus"},
                     id="valid session id and wrong bus ID"),
        pytest.param("", 1, 400, {"description": "parse error", "reference": "session"},
                     id="empty session id and valid bus ID"),
        pytest.param("a2a2a2a2a2", 1, 400, {"description": "parse error", "reference": "session"},
                     id="bad data type session id and valid bus ID"),
        pytest.param("valid_session_id", "a", 400, {"description": "parse error", "reference": "bus"},
                     id="valid session id and bad data type bus ID"),
    ])
    def test_vdser_2059_2063_get_bus_configuration_invalid_data(self, session_id, bus_id, request_status,
                                                                expected_data, setup_class):
        if session_id == "valid_session_id":
            session_id = self.session.session_id

        logging.info(f"Step 1: Send get server status request.")
        get_bus_configuration_response = get_bus_configuration(session_id, bus_id, login_params)

        logging.info(f"Step 2: Verify that get bus configuration status is {request_status}")
        assert_that(get_bus_configuration_response.status_code,
                    f"Error: the get bus configuration response is "
                    f"{get_bus_configuration_response.status_code}").is_equal_to(request_status)

        logging.info(f"Step 3: Verify that responce body with expected data")
        response_body = json.loads(get_bus_configuration_response.text)
        assert_that(response_body, f"Error: the error get bus configuration response is "
                                   f"{get_bus_configuration_response.status_code}").is_equal_to(expected_data)

    def test_vdser_2064_get_bus_status_valid_data(self, setup_class):
        logging.info(f"Step 1: Send get server status request.")
        session_id = self.session.session_id
        get_bus_configuration_response = get_bus_status(session_id, 1, login_params)

        logging.info(f"Step 2: Verify that get bus configuration status is 200")
        assert_that(get_bus_configuration_response.status_code,
                    f"Error: the get bus configuration response is "
                    f"{get_bus_configuration_response.status_code}").is_equal_to(200)

        logging.info(f"Step 3: Verify that responce body with expected data")
        expected_result = {'reserve swap': {'swapped': 'false', 'automatic swap enabled': 'false'},
                           'scheduled backup': 'not in use',
                           'shared backup': {'assignment': 'not in use', 'chase': 'false'}}
        response_body = json.loads(get_bus_configuration_response.text)
        assert_that(response_body, f"Error: the get bus status response is "
                                   f"{get_bus_configuration_response.status_code}").is_equal_to(expected_result)

    @pytest.mark.parametrize("session_id, bus_id, request_status, expected_data", [
        pytest.param("2222222222", 1, 404, {"parameter": "session"}, id="wrong session id and valid bus ID"),
        pytest.param("valid_session_id", 1000, 404, {"parameter": "bus"},
                     id="valid session id and wrong bus ID"),
        pytest.param("", 1, 400, {"description": "parse error", "reference": "session"},
                     id="empty session id and valid bus ID"),
        pytest.param("a2a2a2a2a2", 1, 400, {"description": "parse error", "reference": "session"},
                     id="bad data type session id and valid bus ID"),
        pytest.param("valid_session_id", "a", 400, {"description": "parse error", "reference": "bus"},
                     id="valid session id and bad data type bus ID"),
    ])
    def test_vdser_2065_2069_get_bus_configuration_invalid_data(self, session_id, bus_id, request_status,
                                                                expected_data, setup_class):
        if session_id == "valid_session_id":
            session_id = self.session.session_id

        logging.info(f"Step 1: Send get server status request.")
        get_bus_configuration_response = get_bus_configuration(session_id, bus_id, login_params)

        logging.info(f"Step 2: Verify that get bus configuration status is {request_status}")
        assert_that(get_bus_configuration_response.status_code,
                    f"Error: the get bus configuration response is "
                    f"{get_bus_configuration_response.status_code}").is_equal_to(request_status)

        logging.info(f"Step 3: Verify that responce body with expected data")
        response_body = json.loads(get_bus_configuration_response.text)
        assert_that(response_body, f"Error: the error get bus configuration response is "
                                   f"{get_bus_configuration_response.status_code}").is_equal_to(expected_data)

    def test_vdser_2070_get_buses_valid_data(self, setup_class):
        logging.info(f"Step 1: Send get server status request.")
        session_id = self.session.session_id
        get_buses_response = get_buses(session_id, login_params)

        logging.info(f"Step 2: Verify that get bus configuration status is 200")
        assert_that(get_buses_response.status_code,
                    f"Error: the get buses response is {get_buses_response.status_code}").is_equal_to(200)

        logging.info(f"Step 3: Verify that responce body with expected data")
        expected_result = {'buses': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14',
                                     '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27',
                                     '28', '29', '30', '31', '32', '33', '34']}
        response_body = json.loads(get_buses_response.text)
        assert_that(response_body, f"Error: the get bus status response is "
                                   f"{get_buses_response.status_code}").is_equal_to(expected_result)

    @pytest.mark.parametrize("session_id, request_status, expected_data", [
        pytest.param("2222222222", 404, {"parameter": "session"}, id="wrong session id"),
        pytest.param("", 400, {"description": "parse error", "reference": "session"},
                     id="empty session id and valid bus ID"),
        pytest.param("a2a2a2a2a2", 400, {"description": "parse error", "reference": "session"},
                     id="bad data type session id and valid bus ID"),
    ])
    def test_vdser_2071_2073_get_bus_configuration_invalid_data(self, session_id, request_status,
                                                                expected_data, setup_class):
        logging.info(f"Step 1: Send get server status request.")
        get_buses_response = get_buses(session_id, login_params)

        logging.info(f"Step 2: Verify that get bus configuration status is {request_status}")
        assert_that(get_buses_response.status_code,
                    f"Error: the get bus configuration response is "
                    f"{get_buses_response.status_code}").is_equal_to(request_status)

        logging.info(f"Step 3: Verify that responce body with expected data")
        response_body = json.loads(get_buses_response.text)
        assert_that(response_body, f"Error: the error get bus configuration response is "
                                   f"{get_buses_response.status_code}").is_equal_to(expected_data)