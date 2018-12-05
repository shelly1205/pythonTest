from django.contrib import auth as django_auth
import base64
from django.http import JsonResponse
from sign.models import Event, Guest
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import time
import hashlib
from Crypto.Cipher import AES
import json


# ======================添加用户认证============================
# 用户认证
def user_auth(request):
    get_http_auth = request.META.get('HTTP_AUTHORIZATION', b'')
    auth = get_http_auth.split()
    try:
        auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(':')
    except IndexError:
        return 'null'
    username, password = auth_parts[0], auth_parts[2]
    user = django_auth.authenticate(username=username, password=password)
    if user is not None:
        django_auth.login(request, user)
        return 'success'
    else:
        return 'fail'


# 查询发布会接口--增加用户认证
def sec_get_event_list(request):

    auth_result = user_auth(request)
    if auth_result == 'null':
        return JsonResponse({'status': 10011, 'message': 'user auth null'})
    if auth_result == 'fail':
        return JsonResponse({'status': 10012, 'message': 'user auth fail'})

    eid = request.GET.get('eid', '')
    name = request.GET.get('name', '')

    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': 'success', 'data': event})

    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for result in results:
                event = {}
                event['name'] = result.name
                event['limit'] = result.limit
                event['status'] = result.status
                event['address'] = result.address
                event['start_time'] = result.start_time
                datas.append(event)
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})


# ======================添加签名+时间戳============================
# 用户签名+时间戳
def user_sign(request):

    if request.method == 'POST':
        client_time = request.POST.get('time', '')
        client_sign = request.POST.get('sign', '')
    else:
        return 'error'

    if client_time == '' or client_sign == '':
        return 'sign null'

    # 服务器时间
    now_time = time.time()  # 例如：1466426831
    server_time = str(now_time).split('.')[0]

    # 获取时间差
    time_difference = int(server_time) - int(client_time)
    if time_difference >= 60:
        return 'timeout'

    # 签名检查
    md5 = hashlib.md5()
    sign_str = client_time + '&Guest-Manager'
    sign_bytes_utf8 = sign_str.encode(encoding='utf-8')
    md5.update(sign_bytes_utf8)
    server_sign = md5.hexdigest()

    if server_sign != client_sign:
        return 'sign fail'
    else:
        return 'sign success'


# 添加发布会接口-- 增加签名+时间戳
def sec_add_event(request):
    sign_result = user_sign(request)
    if sign_result == 'error':
        return JsonResponse({'status': 10011, 'message': 'request error'})
    elif sign_result == 'sign null':
        return JsonResponse({'status': 10012, 'message': 'user sign null'})
    elif sign_result == 'timeout':
        return JsonResponse({'status': 10013, 'message': 'user sign timeout'})
    if sign_result == 'sign fail':
        return JsonResponse({'status': 10014, 'message': 'user sign fail'})
    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    limit = request.POST.get('limit', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')
    start_time = request.POST.get('start_time', '')

    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event id is already exists'})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name is already exists'})

    if status == '':
        status = 1

    try:
        Event.objects.create(id=eid, name=name, limit=limit, status=status, address=address, start_time=start_time)
    except ValidationError:
        error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status': 10024, 'message': error})
    return JsonResponse({'status': 200, 'message': 'add event success!'})


# ==========================AES加密算法============================
BS = 16
# 还原字符串长度
unpad = lambda s: s[0: - ord(s[-1])]


def decryptBase64(src):
    return base64.urlsafe_b64decode(src)


# 解析AES密文
def decryptAES(src, key):

    src = decryptBase64(src)

    vi = b'r6Tg7u8Iuj80I6G9'
    cryptor = AES.new(key, AES.MODE_CBC, vi)

    text = cryptor.decrypt(src).decode()
    return unpad(text)


def aes_decryption(request):
    app_key = 'W7v4IWH8hdjk0t9U'

    if request.method == 'POST':
        data = request.POST.get('data', '')
    else:
        return 'error'

    # 解密
    decode = decryptAES(data, app_key)
    # 转化为字典
    dict_data = json.loads(decode)
    return dict_data


# 嘉宾查询接口-- AES算法
def sec_get_guest_list(request):
    dict_data = aes_decryption(request)

    if dict_data == 'error':
        return JsonResponse({'status': 10011, 'message': 'request error'})

    # 取出对应的发布会id和嘉宾手机号
    eid = dict_data['eid']
    phone = dict_data['phone']

    if eid == '':
        return JsonResponse({'status': 10021, 'message': 'eid cannot be empty'})

    if eid != '' and phone == '':
        datas = []
        results = Guest.objects.filter(event_id=eid)
        if results:
            for result in results:
                guest = {}
                guest['real_name'] = result.real_name
                guest['phone'] = result.phone
                guest['email'] = result.email
                guest['sign'] = result.sign
                datas.append(guest)
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
    if eid != '' and phone != '':
        guest = {}
        try:
            result = Guest.objects.get(event_id=eid, phone=phone)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            guest['real_name'] = result.real_name
            guest['phone'] = result.phone
            guest['email'] = result.email
            guest['sign'] = result.sign
            return JsonResponse({'status': 200, 'message': 'success', 'data': guest})
