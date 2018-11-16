from havaApp.utils.ssh_connect import SshConnect
from havaApp.models import SubmitInfo, LogInfo
import os


def get_log_content(si_id, localpath, remotepath):
    si = SubmitInfo.objects.get(id=si_id)
    conn = SshConnect(si.ip, 22, si.user, si.password)
    conn.download(remotepath, localpath)
    conn.close()

def scan_log(localpath):
    states = 'success'
    step = '1'

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
        print(run_item)
        si_id = run_item.get('log_id')
        hava_submit_log_name = run_item.get('hava_submit_log_name')
        localpath =  os.path.join(os.path.join(BASE_DIR,'log_states'),hava_submit_log_name)
        remotepath = '/tmp/{}'.format(hava_submit_log_name)
        try:
            get_log_content(si_id , localpath, remotepath)
        except Exception as e:
            print(remotepath)
            print(e.__str__())
        states, step = scan_log(localpath)
        data = {'states': states, 'step': step}
        LogInfo.objects.filter(log_id=si_id).update(**data)