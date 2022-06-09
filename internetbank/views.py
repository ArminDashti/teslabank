from django.shortcuts import render, redirect
from .forms import login_form, create_account_form, transfer_form
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import logout as _logout
from django.contrib.auth import login as _login
from django.contrib.auth.models import User
from django.contrib.sessions.backends.base import SessionBase
from django.contrib.auth.decorators import login_required
from .models import transaction, customer_accounts
from .checking import check_account
from .transfer import run_transfer

def home(request):
    return render(request, 'internetbank/home.html', {})


def login(request):
    _logout(request)
    if request.method == 'GET':
        _login_form = login_form()
        return render(request, 'internetbank/login.html', {'login': _login_form})
    if request.method == 'POST':
        _login_form = login_form(request.POST)
        phone_number_from_from = _login_form['phone_number'].value()
        password_from_from = _login_form['password'].value()
        if _login_form.is_valid():
            authenticated_user = authenticate(username=phone_number_from_from, password=password_from_from)
            if authenticated_user is not None:
                _login(request, authenticated_user)
                request.session.set_expiry(900)
                request.session['firstname_in_session'] = authenticated_user.first_name
                request.session['lastname_in_session'] = authenticated_user.last_name
                request.session['id_in_session'] = int(authenticated_user.id)
                _check_account = check_account()
                get_info = _check_account.get_customer_information(authenticated_user.id)
                request.session['account_number_in_session'] = get_info['account_number']
                return redirect("/internetbank/dashboard/")
            else:
                return redirect("/internetbank/login/")


def createaccount(request):
    if request.method == 'GET':
        _create_account_form = create_account_form()
        return render(request, 'internetbank/createaccount.html', {'createaccount': _create_account_form})

    if request.method == 'POST':
        _create_account_form = create_account_form(request.POST)
        if _create_account_form.is_valid():
            phone_number_from_from = _create_account_form['phone_number'].value()
            checking_user = User.objects.filter(username=phone_number_from_from)
            if len(checking_user) == 0:
                password_from_from = _create_account_form['password'].value()
                first_name_from_from = _create_account_form['first_name'].value()
                last_name_from_from = _create_account_form['last_name'].value()
                User.objects.create_user(username=phone_number_from_from, password=password_from_from, first_name=first_name_from_from, last_name=last_name_from_from)
                messages.success(request, "Your account is created successfully.")
                authenticated_user = authenticate(username=phone_number_from_from, password=password_from_from)
                _login(request, authenticated_user)
                create_customer_account = customer_accounts(customer=authenticated_user)
                create_customer_account.save()
                return redirect("/internetbank/login/")
            else:
                messages.success(request, "The user already is created.")
                return render(request, 'internetbank/createaccount.html', {'createaccount': _create_account_form})


@login_required(login_url='/internetbank/login')
def dashboard(request):
    if request.method == 'GET':
        return render(request, 'internetbank/dash.html', {'first_name':request.session['firstname_in_session'], 'last_name':request.session['lastname_in_session'], 
        'account_number':request.session['account_number_in_session']})

@login_required(login_url='/internetbank/login')
def transfer(request):
    if request.method == 'GET':
        transfer_form_get = transfer_form()
        return render(request, 'internetbank/transfer.html', {'transfer_form':transfer_form_get})
    
    if request.method == 'POST':
        _check_account_ = check_account()
        transfer_form_get_post = transfer_form(request.POST)
        to_id = transfer_form_get_post['to_id'].value()
        passw = transfer_form_get_post['password'].value()
        amount = transfer_form_get_post['password'].value()
        _user_id = request.session['id_in_session']

        if _check_account_.check_customer_password(_user_id, passw) == False:
            messages.success(request, "Your Password is incorrect.")
            return redirect("/internetbank/transfer/")

        if _check_account_.check_customer_exist(to_id) == False:
            messages.success(request, "to_id is NOT correct.")
            return redirect("/internetbank/transfer/")

        customer_blalance = _check_account_.get_customer_information(auth_id=_user_id)
        amount = transfer_form_get_post['amount'].value()
        if int(amount) > int(customer_blalance['balance']):
            messages.success(request, "Amount is NOT enough.")
            return redirect("/internetbank/transfer/")
    
    transaction_id = run_transfer(request.session['account_number_in_session'], to_id, amount)
    customer_blalance = _check_account_.get_customer_information(auth_id=_user_id)
    new_balance = customer_blalance['balance']
    return render(request, 'internetbank/receipt.html', {'tc':transaction_id, 'new_balance':new_balance})


@login_required(login_url='/internetbank/login')
def transactionlist(request):
    _transactionlist = transaction.objects.filter(from_id=request.session['account_number_in_session'])
    return render(request, 'internetbank/transactionlist.html', {'transactionlist':_transactionlist})


@login_required(login_url='/internetbank/login')
def balance(request):
    _check_account = check_account()
    _id = int(request.session['id_in_session'])
    customer_blalance = _check_account.get_customer_information(auth_id=_id)
    return render(request, 'internetbank/balance.html', {'blc':customer_blalance['balance']})


def logout(request):
    _logout(request)
    return redirect("/internetbank/login/")

def confirm(request, test):
    HttpResponse(test)