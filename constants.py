import pathlib

path_to_project = pathlib.Path(f"{pathlib.Path.home()}/PycharmProjects/PythonProject/DSeries_automation")

# D-Services params
cred1 = "Administrator"
cred2 = "Tecom1"
d_services_endpoint_ip = "10.12.70.226"
d_services_endpoint = f"http://{d_services_endpoint_ip}:60000/test/"

# DMAS params
dmas_active_ip = "10.12.70.12"

# D-Services request params
headers = {'Content-Type': 'application/json'}
login_params = {'user name': '', 'password': ''}
schedule_window = 16
as_run_log_window = 16

# system.cfg file params
system_cfg_dict = \
{
    'GENERAL': {
        'DMAS_IP': dmas_active_ip,
        'SESSION_TIMEOUT': '1200',
        'LOG_LEVEL': '8',
        'MAX_NOTIFICATION_QUEUE_SIZE': '5000',
        'GET_NOTIFICATION_TIMEOUT': '10',
        'ASRUN_EXPIRATION': '3',
        'URL': 'http://*:60000/test',
        'BRK_TYPE': 'C,X'
    },
    'LOG': {'GENERAL': '8', 'PRESTO': '8', 'SQI': '8', 'SCHSVR': '8'},
    'SCHSRV': {'USER': '', 'PASSWORD': '', 'PORT': '20022'},
    'SQI': {'PORT': '22227', 'CPU': '1', 'SYSTEM_ID': 'SITE1', 'CPU_TYPE': 'Automation'},
    'CORS': {'ACCESS_LIST': '*'}
}
