import logging
import requests
import urllib


from constants import d_services_endpoint, headers

def get_bus_configuration(session_id, bus_ID, login_params):
    logging.info(f"Deleting the D-Services session")
    url = f"{d_services_endpoint}buses/{bus_ID}/configuration?session={session_id}"
    logging.info(f"D-Services URL = {url}")
    get_bus_configuration_response = requests.get(url=url,
                                                  params=urllib.parse.urlencode(login_params, quote_via=urllib.parse.quote),
                                                  headers=headers)
    return get_bus_configuration_response

def get_bus_status(session_id, bus_ID, login_params):
    logging.info(f"Deleting the D-Services session")
    url = f"{d_services_endpoint}buses/{bus_ID}/state?session={session_id}"
    logging.info(f"D-Services URL = {url}")
    get_bus_status_response = requests.get(url=url,
                                          params=urllib.parse.urlencode(login_params, quote_via=urllib.parse.quote),
                                          headers=headers)
    return get_bus_status_response