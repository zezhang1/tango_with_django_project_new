from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponse
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse
def index(request):
    # return HttpResponse("Rango says hey there partner!<a href='/rango/about/'>About</a>")
    # context_dict={'boldmessage' : "Crunchy, creamy, cookie, candy, cupcake!"}
    # return render(request, 'rango/index.html', context=context_dict)
    # 客户对主页的要求之一是显示最受欢迎的 5 个分类
    # 查询数据库，获取目前存储的所有分类
    # 按点赞次数倒序排列分类
    # 获取前 5 个分类（如果分类数少于 5 个，那就获取全部）
    # 把分类列表放入 context_dict 字典
    # 稍后传给模板引擎
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list


    return render(request, 'rango/index.html', context=context_dict)
# 这里的 Category.objects.order_by('-likes')[:5] 从 Category 模型中查询最受欢迎的前 5 个分
# 类。order_by() 方法的作用是排序，这里我们根据 likes 字段的值倒序排列。-likes 中的 - 号表
# 示倒序（如果没有 - 号，返回的结果是升序排列的）。因为我们想获得一个分类对象列表，所以
# 使用 Python 的列表运算符从列表中获取前 5 个对象（[:5]），返回一个 Category 对象子集。
# 查询结束后，把列表的引用（category_list 变量）传给 context_dict 字典。最后把这个字典作
# 为模板上下文传给 render() 函数。

def about(request):
    # return HttpResponse("Rango says here is the about page.<a href='/rango/'>Index</a>")
    # context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context=context_dict)


def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
