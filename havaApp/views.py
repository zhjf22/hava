#

from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import paramiko
from havaApp.models import SubmitInfo, LogInfo
from havaApp.utils import ssh_connect
from havaApp.get_log import get_log_states
import os

def index(req):
    context = {
        "result": "success",
        "hava_node": ["10.121.143.1", "10.121.105.73"],
        "hava_user_group": ["测试", "研发", "PM"],
        "hava_config": ["云1", "云1","云3","云4"]
    }

    return render(req, 'index.html', context=context)


@csrf_exempt
def index_submit(req):
    node_conf = {
        '10.121.143.1_云1': '10.121.143.1_云1.sh',
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

    if data.get("user") == '' or data.get("password") == '' or data.get("ip") == '':
        return JsonResponse({"result": "fail", "context": "IP或用户名或密码为空"})

    #判定账号密码是否正确
    try:
        conn = ssh_connect.SshConnect(data.get("ip"), 22, data.get("user"), data.get("password"))
    except Exception as e :
        return JsonResponse({"result": "fail", "context": "请输入正确的账号密码", 'e':e.__str__()})

    si_data = {k: v for k, v in data.items() if
               k in ['ip', 'user', 'password', 'hava_node', 'hava_user_group', 'hava_config']}

    si = SubmitInfo(**si_data)
    si.save()

    node_conf_key = '{}_{}'.format(data.get('hava_node'), data.get('hava_config'))
    node_conf_value = node_conf.get(node_conf_key)
    hava_submit_log_name = 'node_conf_{}_{}.log'.format(node_conf_key, si.id)

    #上传脚本到服务器
    conn = ssh_connect.SshConnect(si.ip, 22, si.user, si.password)
    localpath = os.path.join(os.path.join(os.path.dirname(__file__),'script') ,node_conf_value)
    remotepath = os.path.join('/tmp',node_conf_value)

    cmd = 'nohup sh {} > /tmp/{} 2>&1 & echo $! '.format(remotepath, hava_submit_log_name)
    print(cmd)
    #上传脚本
    conn.put(localpath,remotepath)
    #执行命令并获取命令pid
    hava_submit_log_pid = conn.exec_command(cmd)
    conn.close()

    si_data['id'] = si.id

    log_info_data = {'log_id': si.id, 'hava_submit_log_name': hava_submit_log_name,
                     'hava_submit_log_pid': hava_submit_log_pid ,'states':'run','step':'0'}

    LogInfo.objects.create(**log_info_data)

    return render(req, 'submit.html', context=si_data)


def select_log(req):
    log_id = req.GET.get('log_id')

    if log_id:
        get_log_states(log_id)
        context = LogInfo.objects.filter(log_id=log_id)
    else:
        context = LogInfo.objects.all().order_by('-id')

    return render(req, 'select_log.html', {"loginfo": context})


def show_log(req):
    log_id = req.GET.get('log_id')
    log_name = (req.GET.get('log_name'))
    get_log_states(log_id)
    localpath = os.path.join(os.path.join(os.path.dirname(__file__), 'log_states'), log_name)
    with open(localpath,'r') as f:
        lines = f.readlines()

    return render(req,'show_log.html',{'lines':lines})