import json
import logging
import requests
import urllib

from constants import d_services_endpoint, headers, login_params

def create_session_request_body(schedule_window, as_run_log_window):
    request_body = (f"{{\"properties\": "
                    f""f"{{\"schedule window\": {schedule_window}, "
                    f"\"as-run log window\": {as_run_log_window}}}}}")
    return request_body

def create_session(schedule_window, as_run_log_window):
    logging.info("")
    logging.info("Initialising D-Service session")
    session_url = f"{d_services_endpoint}sessions"
    logging.info(f"Create session with the D-Services URL = [%s] {session_url}")
    logging.info(f"Params = {login_params}")
    params = urllib.parse.urlencode(login_params, quote_via=urllib.parse.quote)
    logging.info(f"Request body = {create_session_request_body(schedule_window, as_run_log_window)}")
    try:
        session_response = requests.post(url=session_url,
                                         params=params,
                                         headers=headers,
                                         data=create_session_request_body(schedule_window, as_run_log_window))
    except ConnectionRefusedError:
        logging.info(f"Connection refused [%s] {session_url}")
        exit()

    logging.info(f"Session Response Status Code = {session_response.status_code}")
    session_response_body = session_response.text
    logging.info(f"Session Response Body = {session_response_body}")
    session_id = json.loads(session_response_body)['session']
    return session_id

def ping_session(session_id):
    logging.info("Pinging a D-Service session")
    url = f"{d_services_endpoint}sessions/{session_id}"
    logging.info(f"D-Services URL = {url}")
    session_params = f"{{'session': {session_id}}}"
    logging.info(f"Params = {session_params}")
    params = urllib.parse.urlencode(login_params, quote_via=urllib.parse.quote)
    session_response = requests.get(url, params=params, headers=headers)
    logging.info(f"Session Response Status Code = {session_response.status_code}")
    session_response_body = session_response.text
    logging.info(f"Session Response Body = {session_response_body}")
    return session_response.status_code

def delete_session(session_id):
    logging.info(f"Deleting the D-Services session")
    url = f"{d_services_endpoint}sessions/{session_id}"
    logging.info(f"D-Services URL = {url}")
    session_response = requests.delete(url, headers=headers)
    logging.info(f"Session Response Status Code = {session_response.status_code}")
    if str(session_response.status_code) == "200":
        logging.info(f"Session with session ID {session_id} was deleted successfully")
    else:
        logging.info(f"Session Response Content {session_response.content}")
        session_response_body = session_response.text
        logging.info(f"Session Response Body = {session_response_body}")
    return session_response.status_code
