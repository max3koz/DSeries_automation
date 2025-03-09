def update_config_dict(config_dict, update_data):
    for section, values in update_data.items():
        if section in config_dict:
            config_dict[section].update(values)
        else:
            config_dict[section] = values

def dict_to_string(config_dict):
    result = []
    for section, values in config_dict.items():
        result.append(f'[{section}]')
        for key, value in values.items():
            result.append(f'{key}={value}')
    return '\r\n'.join(result)

def build_command_string(file_path, content):
    command_lines = content.split('\n')
    commands = ' && '.join([f'echo {line} >> {file_path}' for line in command_lines if line])
    command = f'cmd /c "cd C:\\Program Files\\D-Services && {commands}"'
    return command

def create_file_on_dservices_server(connect_session, file_path, config_dict):
    content = dict_to_string(config_dict)
    command = build_command_string(file_path, content)
    connect_session.run_cmd(command)

def copy_file_on_server(connect_session, sample_file, result_file):
    # 'copy system_default.cfg system.cfg'
    command = f'cmd /c "cd C:\Program Files\D-Services && copy {sample_file} {result_file}"'
    result = connect_session.run_cmd(command)
    return result

def delete_file_on_server(connect_session, file):
    # 'del system.cfg'
    command = f'cmd /c "cd C:\Program Files\D-Services && del {file}"'
    result = connect_session.run_cmd(command)
    return result

def get_cmd_output(connect_session, command):
    result = connect_session.run_cmd(command)
    return result.std_out.decode("utf-8")

def verify_service_run(server_connect_session, process_name):
    process = get_cmd_output(server_connect_session,f"tasklist /FI \"IMAGENAME eq {process_name}.exe\"")
    return process_name in process
