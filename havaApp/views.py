#

from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import paramiko
from havaApp.models import SubmitInfo, LogInfo, HavaUserGroup
from havaApp.utils import ssh_connect
from havaApp.get_log import get_log_states
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(req):
    ip = req.GET.get('ip')
    page = req.GET.get('page')

    # 日志抽取
    if ip:
        get_log_states(ip)
        contact_list = LogInfo.objects.filter(ip=ip).order_by('-log_id')
    else:
        # 刷新主页，更新所有状态为run的日志
        get_log_states('0')
        contact_list = LogInfo.objects.all().order_by('-log_id')

    paginator = Paginator(contact_list, 15)  # Show 25 contacts per page

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    # 用户组
    user_group = HavaUserGroup.objects.all().values()
    hava_user_group = []
    for item in user_group:
        hava_user_group.append(item.get('user_group'))

    return render(req, 'index.html', {"contacts": contacts, 'hava_user_group': hava_user_group})


@csrf_exempt
def index_submit(req):


    data = req.POST
    print(data)

    # 判定账号密码是否正确
    try:
        conn = ssh_connect.SshConnect(data.get("ip"), 22, data.get("user"), data.get("password"))
    except Exception as e:
        return JsonResponse({"result": "fail", "context": "请输入正确的账号密码", 'e': e.__str__()})

    # 获取hostname
    host_name = conn.exec_command('hostname')
    # 判定hostname是否符合规则
    # if True:
    #     return JsonResponse({"result": "fail", "context": "请修改host为XXXX.huawei.com"})

    # 存储前端提交用户数据
    si_data = {k: v for k, v in data.items() if
               k in ['ip', 'user', 'password', 'hava_node', 'hava_user_group', 'hava_config']}
    si_data['host_name'] = host_name
    si_data['approve_states'] = 'wait'
    si = SubmitInfo(**si_data)
    si.save()

    log_info_data = {'host_name': host_name, 'ip': data.get("ip"), 'log_id': si.id, 'states': 'not_run', 'step': '0','approve_states':'wait' }
    LogInfo.objects.create(**log_info_data)

    #返回提交成功
    context = '''任务提交成功
    日志ID : {}
    ip: {} 
    host_name: {}'''.format(si.id, si_data.get('ip'), si_data.get('host_name'))

    return JsonResponse({"result": "success", "context": context})


@csrf_exempt
def approve(req):

    approve_method = req.POST.get('approve_method')
    approve_list = str(req.POST.get('approve_list')).split(',')

    print(approve_method,approve_list)

    if approve_method == None:

        page = req.GET.get('page')
        contact_list = SubmitInfo.objects.filter(approve_states='wait').order_by('-id')
        # contact_list = SubmitInfo.objects.all().order_by('-id')

        paginator = Paginator(contact_list, 15)  # Show 25 contacts per page

        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)

        # contacts = SubmitInfo.objects.all().order_by('-id')
        return render(req, 'approve.html', {"contacts": contacts})

    else:

        for id in approve_list:
            SubmitInfo.objects.filter(id=id).update(approve_states=approve_method)
            LogInfo.objects.filter(log_id=id).update(approve_states=approve_method)

            if approve_method == 'pass':
                data = SubmitInfo.objects.get(id=id)
                submit_job(data)

        context = '''下列日志ID状态更新成功 {} '''.format(approve_list)

        return JsonResponse({"result": "success", "context": context})


def submit_job(data):
    node_conf = {
        '10.121.143.1_本地1': '10.121.143.1_本地1.sh',
        '10.121.143.1_本地2': '10.121.143.1_本地2.sh',
        '10.121.143.1_云3': '',
        '10.121.143.1_云4': '',
        '10.121.105.75_云1': '',
        '10.121.105.75_云2': '',
        '10.121.105.75_云3': '',
        '10.121.105.75_云4': '',
    }

    conn = ssh_connect.SshConnect(data.ip, 22, data.user, data.password)

    # 拼接服务器字符串
    node_conf_key = '{}_{}'.format(data.hava_node, data.hava_config)
    node_conf_value = node_conf.get(node_conf_key)
    hava_submit_log_name = 'node_conf_{}_{}.log'.format(node_conf_key, data.id)
    localpath = os.path.join(os.path.join(os.path.dirname(__file__), 'script'), node_conf_value)
    remotepath = os.path.join('/tmp', node_conf_value)
    tmp_hava_submit_log = os.path.join('/tmp', hava_submit_log_name)
    cmd = 'nohup sh {} > {} 2>&1 & echo $! '.format(remotepath, tmp_hava_submit_log)
    print(cmd)

    # 上传脚本到服务器
    conn.put(localpath, remotepath)
    # 执行命令并获取命令pid
    hava_submit_log_pid = conn.exec_command(cmd)
    conn.close()

    # 更新LogInfo表
    log_info_data = {'hava_submit_log_name': hava_submit_log_name,
                     'hava_submit_log_pid': hava_submit_log_pid, 'states': 'run', 'step': '0'}

    LogInfo.objects.filter(log_id=data.id).update(**log_info_data)



# 展示日志
def show_log(req):
    log_name = (req.GET.get('log_name'))
    ip = req.GET.get('ip')
    get_log_states(ip)
    localpath = os.path.join(os.path.join(os.path.dirname(__file__), 'log_states'), log_name)
    with open(localpath, 'r') as f:
        lines = f.readlines()

    return render(req, 'show_log.html', {'lines': lines})
