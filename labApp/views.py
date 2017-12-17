from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView
from .models import *
from .forms import *
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
import logging
from django.contrib import auth

logger = logging.getLogger('views')

# --------- списки ------------

def home(request):
    par = {
        'header': 'Home'
    }
    return render(request, 'home.html', context=par)

# список товаров
class ProdactsView(ListView):
    model = Prodact
    template_name = 'prodact_list.html'
    context_object_name = 'prodacts_list'

    paginate_by = 3

    # ####context['customer'] = models.Customer.objects.get(username=self.request.user)
    def get_context_data(self, **kwargs):
        context = super(ProdactsView, self).get_context_data(**kwargs)

        context['customer'] = auth.get_user(self.request).username
        return context

    def get_queryset(self):
        qs = super(ProdactsView, self).get_queryset()
        if qs is not None:
            for q in qs:
                if len(q.description)>50:
                    q.description = q.description[:50]+'...'
        return qs

    #@method_decorator(login_required(login_url='authorization'))
   # def dispatch(self, request, *args, **kwargs):
     #   return super(ProdactsView, self).dispatch(request, *args, **kwargs)

# список заказов
class OrderView(ListView):
    model = Order
    template_name = 'order_list.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        #context['customer'] = models.Customer.objects.get(user=self.request.user)
        context['customer'] = auth.get_user(self.request).username
        return context


    def get_queryset(self):
        try:
            #cust = models.Customer.objects.get(user=self.request.user)
            cust = models.Customer.objects.get(user=self.request.user)
            qs = models.Order.objects.filter(user=cust)
        except:
            qs = None
        if qs is not None:
            qs = qs.order_by('-order_date')
        return qs


   # @method_decorator(login_required(login_url='authorization'))
    #def dispatch(self, request, *args, **kwargs):
     #   return super(OrderView, self).dispatch(request, *args, **kwargs)


# страница товара
#@login_required(login_url='authorization')
def prodact_page(request, prodact):
    context = {}
    try:
        context['prodact'] = models.Prodact.objects.get(prodact_name=prodact)
        context['category'] = context['prodact'].category.all()
        context['order_form'] = OrderForm()
        if len(context['category']) == 0:
            context['category'] = None
    except:
        context['prodact'] = None
    context['cust'] = auth.get_user(request).username
    context['customer'] = models.Customer.objects.get(user=request.user)

    return render(request, 'prodact_page.html', context)


# заказ товара
@login_required(login_url='authorization')
def order(request, prodact):
    cust = models.Customer.objects.get(user=request.user)
    inits = {'customer': '{} {}'.format(cust.last_name, cust.first_name),
             'prodact': prodact}

    if request.method == "POST":
        form = OrderForm(request.POST, initial=inits)
        is_val = form.is_valid()
        if is_val:
            data = form.cleaned_data
            ord = models.Order()
            ord.user = cust
            ord.prodact = models.Prodact.objects.get(name=data['prodact'])
            ord.date = datetime.datetime.today()
            #ord.number = models.Prodact.objects.get(name=data['prodact'])
            ord.save()
            return HttpResponseRedirect('/')
    else:
        form = OrderForm(initial=inits)

    return render(request, 'order.html', {'form': form, 'customer': cust})



# --------- представления для веб-форм------------

# регистрация вручную
def registration_form(request):
    errors = {}
    request.encoding = 'utf-8'
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username:
            errors['uname']='Введите логин'
        elif len(username) < 5:
            errors['uname']='Длина логина должна быть не меньше 5 символов'

        if User.objects.filter(username=username).exists():
            errors['uname']='Такой логин уже занят'

        password = request.POST.get('password')
        if not password:
            errors['psw']='Введите пароль'
        elif len(password) < 8:
            errors['psw']='Длина пароля должна быть не меньше 8 символов'

        password2 = request.POST.get('password2')
        if password != password2:
            errors['psw2']='Пароли должны совпадать'

        email = request.POST.get('email')
        if not email:
            errors['email']='Введите email'

        last_name = request.POST.get('last_name')
        if not last_name:
            errors['lname']='Введите фамилию'

        first_name = request.POST.get('first_name')
        if not first_name:
            errors['fname']='Введите имя'

        birthday = request.POST.get('birthday')
        if not birthday:
            errors['bday'] = 'Введите дату рождения'

        sex = request.POST.get('sex')
        if not sex:
            errors['sex'] = 'Введите пол'

        if not errors:

            user = User.objects.create_user(username, email, password)
            cust = Customer()
            cust.user = user
            #cust.customer_name = username
            #cust.email = email
            cust.last_name = last_name
            cust.first_name = first_name
            cust.birthday = birthday
            cust.sex = sex
            cust.save()
            return HttpResponseRedirect('/authorization_form')
        else:
            context = {'errors': errors, 'username': username, 'email': email, 'last_name': last_name,
                   'first_name': first_name, 'birthday': birthday, 'sex': sex}
            return render(request, 'registration_form.html', context)

    return render(request, 'registration_form.html', {'errors': errors })


# форма регистрации
class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=5,label='Логин')
    password = forms.CharField(min_length=8,widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Повторите ввод')
    email = forms.EmailField(label='Email')
    last_name = forms.CharField(label='Фамилия')
    first_name = forms.CharField(label='Имя')
    birthday = forms.DateField(label='День рождения')
    #sex = forms.CharField(label='Пол')
    choices = (('м', 'мужской'), ('ж', 'женский'))
    sex = forms.ChoiceField(label='Пол', widget=forms.RadioSelect, choices=choices)
    img = forms.FileField(label='Фото', widget=forms.ClearableFileInput(attrs={'class': 'ask-signup-avatar-input'}),
                            required=False)


class AuthorizationForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


# регистрация
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        is_val = form.is_valid()
        data = form.cleaned_data
        if data['password']!=data['password2']:
            is_val = False
            form.add_error('password2', ['Пароли должны совпадать'])
        if User.objects.filter(username=data['username']).exists():
            form.add_error('username', ['Такой логин уже занят'])
            is_val = False

        if is_val:
            data = form.cleaned_data
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            cust = Customer()
            cust.user = user
            cust.first_name = data['first_name']
            cust.last_name = data['last_name']
            cust.birthday = data ['birthday']
            cust.sex = data ['sex']
            cust.save()
            return HttpResponseRedirect('/authorization')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


# авторизация вручную
def authorization_form(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username:
            errors['uname']='Введите логин'

        password = request.POST.get('password')
        if not password:
            errors['psw']='Введите пароль'

        user = authenticate(request, username=username, password=password)
        if user is None and 'uname' not in errors.keys() and 'psw' not in errors.keys():
            errors['login'] = 'Логин или пароль введены неверно'

        if not errors:
            login(request, user)
            return HttpResponseRedirect('/success_authorization_form')
        else:
            context = {'errors': errors}
            return render(request, 'authorization_form.html', context)

    return render(request, 'authorization_form.html', {'errors':errors})


# авторизация django
def authorization(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        print(form)
        data = form.cleaned_data

        if form.is_valid():
            user = authenticate(request, username=data['username'], password=data['password'])
            # user = authenticate(request, username='petrov',password='12345678')
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/success_authorization')
            else:
                form.add_error('username', ['Неверный логин или пароль'])
            #raise forms.ValidationError('Имя пользователя и пароль не подходят')

    else:
        form = AuthorizationForm()

    return render(request, 'authorization.html', {'form': form})


# успешная авторизация вручную
def success_authorization_form(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/authorization')


# успешная авторизация django
@login_required(login_url='/authorization')
def success_authorization(request):
    return HttpResponseRedirect('/')

# выход
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def ajax_order(request):
    if request.method == "POST":
        prodact = models.Prodact.objects.get(name=request.POST['prodact_name'])
        customer = models.Customeler.objects.get(user=models.User.objects.get(email=request.POST['customer_email']))
        date = datetime.date(int(request.POST['date']))
        number = int(request.POST['number'])

        ord = models.Order()
        ord.user = customer
        ord.prodact = prodact
        ord.number = number
        ord.date = date
        ord.save()
        return HttpResponse('success')