def update_config_dict(config_dict, update_data):
    for section, values in update_data.items():
        if section in config_dict:
            config_dict[section].update(values)
        else:
            config_dict[section] = values

def create_file_from_dict(connect_session, file_path, config_dict):
    with open(file_path, 'w') as f:
        for section, values in config_dict.items():
            f.write(f'[{section}]\n')
            for key, value in values.items():
                f.write(f'{key}={value}\n')
    with open(file_path, 'r') as f:
        content = f.read()
    commands = [(f'cmd /c "cd C:\Program Files\D-Services && echo {line.strip()} >> '
                 f'{file_path}"') for line in content.split('\n') if line.strip()]
    for command in commands:
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
    process = get_cmd_output(server_connect_session,
                                    f"tasklist /FI \"IMAGENAME eq {process_name}.exe\"")
    return process_name in process
