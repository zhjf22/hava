from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import paramiko
from havaApp.models import SubmitInfo, LogInfo
from havaApp.utils import ssh_connect
from havaApp.get_log import get_log_states


def index(req):
    context = {
        "result": "success",
        "hava_node": ["10.121.143.1", "10.121.105.75"],
        "hava_user_group": ["测试", "研发", "PM"],
        "hava_config": ["云", "本地"]
    }

    return render(req, 'index.html', context=context)


@csrf_exempt
def index_submit(req):
    node_conf = {
        '10.121.143.1_云1': 'cat /etc/hosts',
        '10.121.143.1_云2': '',
        '10.121.143.1_云3': '',
        '10.121.143.1_云4': '',
        '10.121.105.75_云1': '',
        '10.121.105.75_云2': '',
        '10.121.105.75_云3': '',
        '10.121.105.75_云4': '',
    }

    data = req.POST
    print(data)

    if data.get("user") == '' or data.get("password") == '' or data.get("remote_ip") == '':
        return JsonResponse({"result": "fail", "context": "IP或用户名或密码为空"})

    si_data = {k: v for k, v in data.items() if
               k in ['ip', 'user', 'password', 'hava_node', 'hava_user_group', 'hava_config']}

    si = SubmitInfo(**si_data)
    si.save()
    node_conf_key = '{}_{}'.format(data.get('hava_node'), data.get('hava_config'))
    hava_submit_log_name = 'node_conf_{}_{}.log'.format(node_conf_key, si.id)

    # 输入执行命令
    cmd = 'nohup {} > /tmp/{} 2>&1 & echo $! '.format(node_conf.get(node_conf_key), hava_submit_log_name)

    print(cmd)
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=data.get('ip'), port=22, username=data.get('user'), password=data.get('password'))

    stdin, stdout, stderr = ssh.exec_command(cmd)
    hava_submit_log_pid = stdout.read()

    ssh.close()

    si_data['id'] = si.id
    print(si.id)

    log_info_data = {'log_id': si.id, 'hava_submit_log_name': hava_submit_log_name,
                     'hava_submit_log_pid': hava_submit_log_pid ,'states':'run','step':'0'}

    lg = LogInfo(**log_info_data)
    lg.save()

    return render(req, 'submit.html', context=si_data)


def select_log(req):
    log_id = req.GET.get('log_id')

    if log_id:
        get_log_states(log_id)
        context = LogInfo.objects.filter(log_id=log_id)
    else:
        context = LogInfo.objects.all()

    return render(req, 'select_log.html', {"loginfo": context})


