import winrm

def create_server_connect_session():
    connect_session = winrm.Session('http://10.12.70.226:5985/wsman', auth=('Administrator', 'Tecom1'))
    return connect_session

def run_dservices_service(connect_session):
    # command = 'cmd /c start "D-Services" /d "C:\\"Program Files"\\D-Services" "D-services host"'
    command = 'cmd /c "cd C:\Program Files\D-Services && \"D-Services host.exe\""'
    result = connect_session.run_cmd(command)
    return result

def stop_server_session(connect_session):
    command = 'taskkill /F /IM "d-services host.exe"'
    result = connect_session.run_cmd(command)
    return result

# Вывод результата
# print(result.std_out.decode())
# print(result.std_err.decode())