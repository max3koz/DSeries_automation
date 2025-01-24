import pathlib

path_to_project = pathlib.Path(f"{pathlib.Path.home()}/Projects/AQA_course/")

d_services_endpoint_ip = "10.12.70.226"
d_services_endpoint = f"http://{d_services_endpoint_ip}:60000/test/"

headers = {'Content-Type': 'application/json'}
login_params = {'user name': '', 'password': ''}

schedule_window = 16
as_run_log_window = 16
