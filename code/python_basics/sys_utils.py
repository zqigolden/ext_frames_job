import subprocess
import os
# import log

# logger = log.Logger()


def run_system_commands(cmd_lines, cwd=''):
    for cmd_line in cmd_lines:
        run_system_command(cmd_line, cwd)


def run_system_command(cmd_line, cwd=''):
    # logger.info('%s %s', cwd, cmd_line)
    # print('%s %s', cwd, cmd_line)
    cur_cwd = os.getcwd()
    if cwd != '':
        os.chdir(cwd)
    ps = subprocess.Popen(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)

    stdout, stderr = ps.communicate()
    status = ps.wait()
    if len(stdout) > 0:
        print(stdout)
        # logger.info(stdout)

    if cwd != '':
        os.chdir(cur_cwd)

    if status != 0:
        raise Exception('Exception running command: \n%s\n%s\n%s' % (cmd_line, stdout, stderr))


if __name__ == "__main__":
    run_system_command('ls')
