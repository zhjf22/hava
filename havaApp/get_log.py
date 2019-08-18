from havaApp.utils.ssh_connect import SshConnect
from havaApp.models import SubmitInfo, LogInfo, Device
import os
import re
from datetime import datetime


def download_content(conn, localpath, remotepath):
    conn.download(remotepath, localpath)


def get_log_pid_states(conn,pid):
    pid = pid.strip()
    cmd = "ps -p {} | awk '{}' ".format(pid.strip(),'{print $1}')
    pid_res = conn.exec_command(cmd)
    pid_num = re.findall('\d+', pid_res)

    states = 'run'
    if not pid_num:
        states = 'finish'

    return states


def scan_log(localpath):

    compile_name = re.compile('.*?____step(\d+)____.*')
    step = '00'
    states = 'run'

    with open(localpath,'r') as f:
        text_list = f.readlines()

    for line in text_list:
        group =  re.match(compile_name,line)
        if group:
            step = group[1]

    if step == '10':
        states = 'success'
        step = '100%'
    else:
        step = '{:.2f}%'.format(int(step)*100.0/7)

    print(states,step)
    return states, step


def get_log_states(ip=0):

    if ip != 0:
        run = LogInfo.objects.filter(ip=ip, states='run').values()
    else:
        run = LogInfo.objects.filter(states='run').values()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    if not run:
        return

    for run_item in run:
        if run_item.get('states') == 'success' or run_item.get('states') == 'fail':
            pass
        else:
            print(datetime.now())
            si_id = run_item.get('log_id')
            hava_submit_log_name = run_item.get('hava_submit_log_name')
            localpath =  os.path.join(os.path.join(BASE_DIR,'log_states'),hava_submit_log_name)
            remotepath =  os.path.join('/tmp',hava_submit_log_name)
            print(remotepath)
            si = SubmitInfo.objects.get(id=si_id)
            lg = LogInfo.objects.get(log_id=si_id)
            conn = SshConnect(si.ip, 22, si.user, si.password)
            pid_states = ''
            try:
                #下载日志明细
                download_content(conn , localpath, remotepath)
                pid_states =  get_log_pid_states(conn,lg.hava_submit_log_pid)
            except Exception as e:
                print(e.__str__())
            finally:
                conn.close()

            states, step = scan_log(localpath)

            if pid_states == 'finish' and states != 'success':
                states = 'fail'

            #如果成功，更新数据库
            if states == 'success':
                host_name = SubmitInfo.objects.get(id=si_id).host_name
                hava_user_group = SubmitInfo.objects.get(id = si_id).hava_user_group
                device_data = {"states":states,"hava_user_group":hava_user_group}
                Device.objects.update_or_create(host_name=host_name ,defaults=device_data)

            data = {'states': states, 'step': step}

            LogInfo.objects.filter(log_id=si_id).update(**data)

