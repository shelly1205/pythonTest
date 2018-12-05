from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# 首页(登录）
def index(request):
    return render(request, "index.html")


# 登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user', username, 3600)
            request.session['user'] = username

            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})
    # 防止直接通过浏览器访问/login_action/的情况
    return render(request, 'index.html')


# 退出登录
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response


# 发布会管理（登录之后默认页面）
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    # username = request.COOKIES.get('user', '')
    username = request.session.get('user', '')
    return render(request, 'event_manage.html', {'user': username, "events": event_list})


# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    s_name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=s_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})


# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    # 创建每页3条数据的分页器
    paginator = Paginator(guest_list, 3)
    # 获取当前要显示第几页
    page = request.GET.get('page', '')
    try:
        # 获取第page页的数据
        contacts = paginator.page(page)
        # 如果页数参数错误，显示第一页
    except PageNotAnInteger:
        contacts = paginator.page(1)
        # 如果页数超出范围，显示最后一页
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {"user": username, "guests": contacts})


# 嘉宾手机号的查询
@login_required
def search_phone(request):
    username = request.session.get('user', '')
    s_phone = request.GET.get('phone', '')
    guest_list = Guest.objects.filter(phone__contains=s_phone)
    paginator = Paginator(guest_list, 3)
    page = request.GET.get("page", '')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {"user": username, "guests": contacts})


# 签到页面
@login_required
def sign_index(request, eid):
    username = request.session.get('user', '')
    # 默认调用get方法，如果查询不到对象，则会抛出404异常
    event = get_object_or_404(Event, id=eid)
    guest_amount = Guest.objects.filter(event_id=eid)
    guests_sign_in = Guest.objects.filter(event_id=eid, sign=True)
    return render(request, 'sign_index.html', {"user": username, 'event': event, 'guest_amount': guest_amount,
                                               'guests_sign_in': guests_sign_in})


# 签到动作
@login_required
def sign_index_action(request, eid):
    username = request.session.get('user', '')
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    guest_amount = Guest.objects.filter(event_id=eid)
    guests_sign_in = Guest.objects.filter(event_id=eid, sign=True)
    # print(phone)

    result = Guest.objects.filter(phone=phone)
    # 找不到匹配的手机号
    if not result:
        return render(request, 'sign_index.html', {'user': username, 'event': event, 'guest_amount': guest_amount,
                                                   'guests_sign_in': guests_sign_in, 'hint': 'phone error!'})

    # 使用get()方法时，当找不到匹配的内容时，就会报DoesNotExist exception.
    # 所以先用filter()筛选后，如果有数据，再执行下一步get（）
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'user': username, 'event': event, 'guest_amount': guest_amount,
                                                   'guests_sign_in': guests_sign_in,
                                                   'hint': 'phone or event id error!'})
    # 使用get()方法获得查询结果
    result = Guest.objects.get(phone=phone, event_id=eid)
    # print(result)
    if result.sign:
        return render(request, 'sign_index.html', {'user': username, 'event': event, 'guest_amount': guest_amount,
                                                   'guests_sign_in': guests_sign_in, 'hint': 'user has sign in.'})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        guests_sign_in = Guest.objects.filter(event_id=eid, sign=True)
        return render(request, 'sign_index.html', {'user': username, 'event': event, 'guest_amount': guest_amount,
                                                   'guests_sign_in': guests_sign_in,
                                                   'hint': 'sign in success!', 'guest': result})

