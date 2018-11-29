from havaApp.utils.ssh_connect import SshConnect
from havaApp.models import SubmitInfo, LogInfo, Device
import os
import re

def get_log_content(si_id, localpath, remotepath):
    si = SubmitInfo.objects.get(id=si_id)
    conn = SshConnect(si.ip, 22, si.user, si.password)
    conn.download(remotepath, localpath)
    conn.close()

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


def get_log_states(si_id='0'):

    if si_id == '0':
        run = LogInfo.objects.filter(states='run').values()
    else:
        run = LogInfo.objects.filter(log_id=si_id).values()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    if not run:
        return

    for run_item in run:
        if run_item.get('states') == 'success':
            pass
        else:
            si_id = run_item.get('log_id')
            hava_submit_log_name = run_item.get('hava_submit_log_name')
            localpath =  os.path.join(os.path.join(BASE_DIR,'log_states'),hava_submit_log_name)
            remotepath = '/tmp/{}'.format(hava_submit_log_name)
            try:
                get_log_content(si_id , localpath, remotepath)
            except Exception as e:
                print(e.__str__())
            states, step = scan_log(localpath)
            if states == 'success':
                #更新逻辑
                host_name = "huawei_1234"
                hava_user_group = SubmitInfo.objects.get(id = si_id).hava_user_group
                device_data = {"states":states,"hava_user_group":hava_user_group}
                Device.objects.update_or_create(host_name=host_name ,defaults=device_data)
                # Device.objects.filter(host_name=host_name).update(states=states)

            data = {'states': states, 'step': step}
            LogInfo.objects.filter(log_id=si_id).update(**data)

