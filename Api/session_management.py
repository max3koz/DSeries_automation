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

class SessionManagement:
    @staticmethod
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

    @staticmethod
    def ping_session(session_id):
        logging.info("Pinging a D-Service session")
        url = f"{d_services_endpoint}sessions/{session_id}"
        logging.info(f"D-Services URL = {url}")
        session_params = f"{{'session': {session_id}}}"
        logging.info(f"Params = {session_params}")
        session_response = requests.get(url=url,
                                        params=urllib.parse.urlencode(login_params, quote_via=urllib.parse.quote),
                                        headers=headers)
        logging.info(f"Session Response Status Code = {session_response.status_code}")
        session_response_body = session_response.text
        logging.info(f"Session Response Body = {session_response_body}")
        return session_response.status_code

    @staticmethod
    def delete_session(session_id):
        logging.info(f"Deleting the D-Services session")
        url = f"{d_services_endpoint}sessions/{session_id}"
        logging.info(f"D-Services URL = {url}")
        session_response = requests.delete(url=url,
                                           headers=headers)
        logging.info(f"Session Response Status Code = {session_response.status_code}")
        if str(session_response.status_code) == "200":
            logging.info(f"Session with session ID {session_id} was deleted successfully")
        else:
            logging.info(f"Session Response Content {session_response.content}")
            session_response_body = session_response.text
            logging.info(f"Session Response Body = {session_response_body}")
        return session_response.status_code

    @staticmethod
    def unsubscribe_session(session_id, subscription_ID):
        logging.info(f"Deleting the D-Services session")
        url = f"{d_services_endpoint}sessions/{session_id}/subscriptions/{subscription_ID}"
        logging.info(f"Unsubscribe from the subscription {subscription_ID} for the session {session_id}")
        logging.info(f"by request: {url}")
        unsubscribe_response = requests.delete(url=url,
                                               headers=headers)
        logging.info(f"Unsubscribe response status code = {unsubscribe_response.status_code}")
        if str(unsubscribe_response.status_code) == "200":
            logging.info(f"Subscribe {subscription_ID} on session ID {session_id} was unsubscribed successfully")
        else:
            logging.info(f"Unsubscribe Response Content {unsubscribe_response.content}")
            unsubscribe_response_body = unsubscribe_response.text
            logging.info(f"Unsubscribe Response Body = {unsubscribe_response_body}")
        return unsubscribe_response.status_code