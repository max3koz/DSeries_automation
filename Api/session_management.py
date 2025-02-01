import json
import logging
import requests
import urllib

from constants import d_services_endpoint, headers

def create_session_request_body(schedule_window, as_run_log_window):
    request_body = (f"{{\"properties\": "
                    f""f"{{\"schedule window\": {schedule_window}, "
                    f"\"as-run log window\": {as_run_log_window}}}}}")
    return request_body

class Session:
    def __init__(self, login_params, schedule_window, as_run_log_window):
        session_url = f"{d_services_endpoint}sessions"
        logging.info(f"Create session with the D-Services URL = [%s] {session_url}")
        params = urllib.parse.urlencode(login_params, quote_via=urllib.parse.quote)
        try:
            session_response = requests.post(url=session_url,
                                             params=params,
                                             headers=headers,
                                             data=create_session_request_body(schedule_window, as_run_log_window))
        except ConnectionRefusedError:
            logging.info(f"Connection refused [%s] {session_url}")
            exit()
        session_response_body = session_response.text
        logging.info(f"Session Response Body = {session_response_body}")
        if session_response.status_code == 200:
            self.session_id = json.loads(session_response_body)['session']
        self.session_response = session_response
        self.session_response_body = session_response_body

    def ping_session(self, login_params):
        logging.info("Pinging a D-Service session")
        url = f"{d_services_endpoint}sessions/{self}"
        logging.info(f"D-Services URL = {url}")
        session_params = f"{{'session': {self}}}"
        logging.info(f"Params = {session_params}")
        session_response = requests.get(url=url,
                                        params=urllib.parse.urlencode(login_params, quote_via=urllib.parse.quote),
                                        headers=headers)
        # logging.info(f"Session Response Status Code = {session_response.status_code}")
        # session_response_body = session_response.text
        # logging.info(f"Session Response Body = {session_response_body}")
        return session_response

    def delete_session(self):
        logging.info(f"Deleting the D-Services session")
        url = f"{d_services_endpoint}sessions/{self}"
        logging.info(f"D-Services URL = {url}")
        session_response = requests.delete(url=url, headers=headers)
        # logging.info(f"Session Response Status Code = {session_response.status_code}")
        # if str(session_response.status_code) == "200":
        #     logging.info(f"Session with session ID {self} was deleted successfully")
        # else:
        #     logging.info(f"Session Response Content {session_response.content}")
        return session_response

    def unsubscribe_session(self, subscription_id):
        logging.info(f"Deleting the D-Services session")
        url = f"{d_services_endpoint}sessions/{self}/subscriptions/{subscription_id}"
        logging.info(f"Unsubscribe from the subscription {subscription_id} for the session {self} by request:")
        logging.info(f"{url}")
        unsubscribe_response = requests.delete(url=url,
                                               headers=headers)
        # logging.info(f"Unsubscribe response status code = {unsubscribe_response.status_code}")
        # if str(unsubscribe_response.status_code) == "200":
        #     logging.info(f"Subscribe {subscription_id} on session ID {self} was unsubscribed successfully")
        # else:
        #     logging.info(f"Unsubscribe Response Content {unsubscribe_response.content}")
        return unsubscribe_response.status_code
