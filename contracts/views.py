import datetime
import decimal
from dis import show_code
from venv import logger
from django.shortcuts import render, redirect, HttpResponse
from .models import Office_name, Contracts, FiscalYear, Contract_actions, Profile, Roles, Client, OtpToken
from django.contrib import messages
from .forms import RegisterForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.hashers import make_password, check_password
from notification.views import send_sms
from django.core.validators import FileExtensionValidator
from django.views import View
from django.http import JsonResponse
import csv
import logging
import aiohttp
import random

logger = logging.getLogger(__name__)



async def example(request):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://pokeapi.co/api/v2/pokemon/1") as res:
            data = await res.json()
            print(data)
    return HttpResponse(data)




def export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)

    # Write header row
    writer.writerow(['office_name','addresss'])  # Replace with your model fields

    # Fetch data from your model and write to the CSV file
    queryset = Office_name.objects.all()  # Replace 'YourModel' with your actual model name

    for item in queryset:
        writer.writerow([item.office_name, item.address])  # Replace with your model fields

    return response
    return render(request, 'home/reports.html')





def Json_Test(request):
    data = list(Office_name.objects.values())

    return JsonResponse(data, safe=False)


def index(request):
    return render(request, 'index.html')



def verify_otp(otp, otp_token):
    if otp == otp_token:
        print(otp,otp_token)
        return True
    else:
        return False




# @unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            if user.profile.otp:
                if request.method == 'GET':
                    # Generate and send OTP
                    otp = random.randint(10000, 999999)
                    OtpToken.objects.create(
                        user=user,
                        otp=otp,
                        purpose='login',
                    )
                    print(otp)


                    # Fetch the latest OTP for display
                    otp_token = OtpToken.objects.filter(
                        user=user,
                        purpose='login',
                        deleted_at__isnull=True
                    ).order_by('-created_date').first()

                    # Render the OTP input page
                    return render(request, "home/otp.html")

                elif request.method == 'POST':
                    otp_token = OtpToken.objects.filter(
                        user=user,
                        purpose='login',
                        deleted_at__isnull=True
                    ).order_by('-created_date').first()

                    otp = request.POST.get('otp')
                    if otp is not None:
                        try:
                            otp = int(otp)  # Ensure OTP is an integer
                            if otp_token and otp == otp_token.otp:
                                # OTP verification success
                                otp_token.deleted_at = datetime.now()  # Mark OTP as used
                                otp_token.save()
                                login(request, user)
                                messages.success(request, 'You are now logged in')
                                return redirect('dashboard')
                            else:
                                # OTP mismatch
                                messages.error(request, 'Invalid OTP. Please try again.')
                                return render(request, "home/otp.html")
                        except ValueError:
                            # Non-integer OTP entered
                            messages.error(request, 'OTP must be a valid number.')
                            return render(request, "home/otp.html")
                    else:
                        # OTP not provided
                        messages.error(request, 'Please enter the OTP.')
                        return render(request, "home/otp.html")
            else:
                # If OTP is not required, log the user in directly
                login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('dashboard')
        else:
            # Handle user not found case
            messages.error(request, 'User not found.')
            return redirect('login')
    else:
        return render(request, 'home/login.html')


def logout_view(request):
    send_sms('logout successful', '9844955757')
    logout(request)
    return redirect('login')


# @unauthenticated_user
def dashboard(request):
    offices = Office_name.objects.count()
    contracts = Contracts.objects.count()
    users = User.objects.count()
    client = Client.objects.count()
    activity = Contract_actions.objects.count()
    contract_list = Contracts.objects.all().order_by('created_date')[:6]
    # contract_list= None
    activities = Contract_actions.objects.all().order_by('-created_date')[:6]
    # activities = None
    context = {
        'offices': offices,
        'contracts': contracts,
        'users': users,
        'contract_list': contract_list,
        'activities': activities,
        'activity':activity,
        'clients': client,

    }

    return render(request, 'home/dashboard.html', context)


@login_required
# @allowed_users(allowed_roles=['admin','account'])
def company_list(request):
    offices = Office_name.objects.all().order_by('address')
    return render(request, 'home/company-list.html', {'Offices': offices})


@login_required
def add_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        pan_no = request.POST.get('pan_no')
        document = request.FILES.get('document')
        extra = request.POST.get('pan_no')

        office = Office_name(
            office_name=name,
            address=address,
            pan_no=pan_no,
            extra=extra
        )

        if document:
            office.document = document

        office.save()
        messages.success(request, "Saved Successfully")
        return redirect('company_list')
    else:
        return render(request, 'home/add-company.html')


@login_required
def edit_company(request, pk):
    office = get_object_or_404(Office_name, pk=pk)
    if request.method == 'POST':
        office_name = request.POST.get('name')
        address = request.POST.get('address')
        pan_no = request.POST.get('pan_no')
        # Update the office object
        office.office_name = office_name
        office.address = address
        office.pan_no = pan_no
        office.save()
        return redirect('company_list')
    else:
        return render(request, 'home/edit_office.html', {'office': office})




@login_required
def delete_company(request, pk):
    office = get_object_or_404(Office_name, pk=pk)
    office.delete()
    messages.success(request, 'deleted Successfully')
    return redirect('company_list')


@login_required
def delete_contract(request, pk):
    contract = get_object_or_404(Contracts, pk=pk)
    contract.delete()
    messages.info(request, 'Contract deleted Successfully.')
    return redirect('contract-list')


@login_required
def contract(request):
    contracts = Contracts.objects.all()
    return render(request, 'home/contract-list.html', {'contracts': contracts})


@transaction.atomic
def user_create(request):
    roles = Roles.objects.all()
    users = User.objects.all()
    context = {
        'roles': roles,
        'users': users
    }
    if request.method == 'POST':
        role = request.POST.get('role')
        try:
            roles = get_object_or_404(roles, id=role)
        except Roles.DoesNotExist:
            messages.error(request, "Can't get roles")
            return redirect('create-user')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        bio = request.POST.get('bio')
        image_new = request.FILES.get('image')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
        else:
            new_user = User.objects.create(
                first_name=fname,
                last_name=lname,
                email=email,
                username=username,
                password=make_password(password1),
                is_staff=False,
                is_active=True,
            )
            new_user.save()
            profile = Profile.objects.create(
                roles_id=role,
                bio=bio,
                user=new_user,
                # image=image_new,
            )
            if image_new:
                profile.image.save(image_new.name, image_new)

            profile.save()

            messages.success(request, 'User Created Successfully')
            return redirect('users')
    else:
        return render(request, 'home/create-user.html', context)

    return render(request, 'home/create-user.html', context)


def delete_user(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect('users')


from .models import Roles


class Role(View):
    def get(self, request):
        roles = Roles.objects.all() 
        logger.exception(print)
        return render(request, 'home/roles.html',{'roles':roles})
        



@login_required
def userlist(request):
    try:
        users = User.objects.all()
    except User.DoesNotExist:
        users = None

    form = RegisterForm()
    context = {
        'users': users,
        'form': form
    }

    return render(request, 'home/users.html', context)



@login_required
def icons_view(request):
    return render(request, 'home/icons.html')




@transaction.atomic
def add_contract(request):
    offices = Office_name.objects.all()
    all_clients = Client.objects.all()
    all_fiscalyear = FiscalYear.objects.all()

    ext_validation = FileExtensionValidator(['pdf','PDF'])

    if request.method == 'POST':
        office_id = request.POST.get('office_name')
        try:
            office = get_object_or_404(Office_name, id=office_id)
        except Office_name.DoesNotExist:
            messages.error(request, 'Invalid office ID')
            return render(request, 'home/add-contract.html', {'offices': offices, 'clients': all_clients})

        client_id = request.POST.get('client')
        try:
            clients = get_object_or_404(Client, id=client_id)
        except Client.DoesNotExist:
            messages.error(request, 'Invalid Client')
            return render(request, 'home/add-contract.html', {'offices': offices, 'clients': clients})

        fiscal_year_id = request.POST.get('year')

        try:
            fiscalyear = get_object_or_404(FiscalYear, id=fiscal_year_id)
            
        except FiscalYear.DoesNotExist:
            messages.error(request, "unable to find fiscal year")
            return render(request, 'home/add-contract.html', {
                'offices': offices, 'clients': clients
                })

        User = get_user_model()
        user = get_object_or_404(User, id=request.user.id)

        title_of_contract = request.POST.get('title_of_contract')
        fiscal_year = request.POST.get('fiscalyear')
        amount = request.POST.get('amount')
        contract_date = request.POST.get('contract_date')
        billing_date = request.POST.get('billing_date')
        contract_file = request.FILES.get('contract_file')

        contracts = Contracts(
            office=office,
            title_of_contract=title_of_contract,
            client_id=client_id,
            fiscalyear=fiscalyear,
            amount=amount,
            contract_date=contract_date,
            billing_date=billing_date,
            # contract_file=contract_file,
            user=user
        )

        contracts.save()
        if contract_file:
            contracts.contract_file.save(contract_file.name, contract_file)

        actions = Contract_actions(
            contract=contracts,
            status=1,
            amount=amount,
            user=user,
            extra={
                'contract_id': contracts.id,
                'title_of_contract': title_of_contract,
                'clients': client_id,
                'fiscal_year': fiscal_year,
                'contract_date': contract_date,
                'billing_date': billing_date,
                'user': user.id
            },
        )
        actions.save()
        messages.success(request, 'Added successfully')

    return render(request, 'home/add-contract.html',
                  {
                      'offices': offices,
                      'clients': all_clients,
                      'all_fiscalyear': all_fiscalyear,
                  })







# def comission():
#     return str(datas.comission)

@login_required
def contract_view(request, pk):
    datas = Contracts.objects.get(pk=pk)
    actions = Contract_actions.objects.filter(contract_id=pk).order_by('-created_date')
    if datas.comission == "":
        receivable= datas.amount
    else:
        receivable = float(datas.amount) - float(datas.comission)
        # dd(receivable)

    try:
        
        return render(request, 'home/view-contract-detail.html', {
            'datas': datas,
            'actions': actions,
            'receivable':receivable,
            
        })

    except MultipleObjectsReturned:
        return render(request, 'home/view-contract-detail.html', {
            'datas': datas,
            'actions': actions,

        })

    except ObjectDoesNotExist:
        return render(request, 'home/page-404.html')



def error_404(request, exception):
    # return render(request, '404.html', status=404)
    return HttpResponse("Thisis 404 page")



@login_required
@allowed_users(allowed_roles=[1, 2, 3])
def approve_contract(request, contract_id):
    User = get_user_model()
    user = get_object_or_404(User, id=request.user.id)
    contract = Contracts.objects.get(id=contract_id)
    if request.method == 'POST':
        remarks = request.POST.get('approve')
    actions = Contract_actions(
        contract=contract,
        status=2,
        amount=0,
        remarks=remarks,
        user=user,
        extra={})

    actions.save()
    return redirect('view-contract', pk=contract_id)






@allowed_users(allowed_roles=[1])
def reject_contract(request, contract_id):
    User = get_user_model()
    user = get_object_or_404(User, id=request.user.id)
    contract = Contracts.objects.get(id=contract_id)
    if request.method == 'POST':
        remarks = request.POST.get('reject')
    actions = Contract_actions(
        contract=contract,
        status=3,
        amount=0,
        remarks=remarks,
        user=user,
        extra={})

    actions.save()
    return redirect('view-contract', pk=contract_id)



@login_required
def add_comission(request, contract_id):
    User = get_user_model()
    
    user = get_object_or_404(User, id=request.user.id)
    
    contract = Contracts.objects.get(id=contract_id)

    if request.method == 'POST':
        comission_amount = request.POST.get('comission_amount')
        remarks = request.POST.get('comment')
        contract.comission = comission_amount
        contract.save()

        actions = Contract_actions(
        contract=contract,
        status=20,
        amount=comission_amount,
        user=user,
        remarks=remarks,
        
        extra={
            "remarks": remarks,
            "comission": comission_amount,
            
        })
        actions.save()
        

    return redirect('view-contract', pk=contract_id)

    



@login_required
def add_comment(request, contract_id):
    User = get_user_model()
    user = get_object_or_404(User, id=request.user.id)
    contract = Contracts.objects.get(id=contract_id)
    if request.method == 'POST':
        remarks = request.POST.get('comment')
    actions = Contract_actions(
        contract=contract,
        status=5,
        amount=0,
        user=user,
        remarks=remarks,
        extra={})

    actions.save()
    return redirect('view-contract', pk=contract_id)




# def approve_contract(request, pk):

#     if request.method == 'POST':
#         contract =get_object_or_404(Contracts, id=pk)
#         User = get_user_model()
#         user = get_object_or_404(User, id=request.user.id)
#         print(user)
#         add_action = Contract_actions(contract=contract, status =2, amount=0, extra={} )
#         add_action.save()
#         return redirect('contract-list')


#     contract= get_object_or_404(Contracts, contract_id=contract_id)
#     actions = get_object_or_404(Contract_actions)
#     User = get_user_model()
#     user = get_object_or_404(User, id =request.user.id)
#     Add_Actions = Contract_actions(
#         contract = contract,
#         status= 2,
#         amount = 'null',
#         extra = {
#             'contract_id': contract,
#             'user': user.id,
#             'amount':0,

#         },
#     )
#     Add_Actions.save()

# return render(request, 'home/view-contract-detail.html',{'contract'})


def update_payment_status(request, contract_id):
    contract = get_object_or_404(Contracts, id=contract_id)
    User = get_user_model()
    user = get_object_or_404(User, id=request.user.id)

    if request.method == 'POST':
        remarks = request.POST.get('comment')

        payment_type = request.POST.get('payment_type')
        amount = request.POST.get('amount') or 0
        print(payment_type)
        if payment_type == 'full':
            contract.payment_status = True
            contract.save()

        actions = Contract_actions(
            contract=contract,
            status=4,
            amount=amount,
            remarks=remarks,
            user=user,
            extra={
                "Payment Type": payment_type,
                "amount": amount,
                "remarks": remarks,
                "user": request.user.id,
            }
        )
        actions.save()

        
    return redirect('view-contract', pk=contract_id)



@login_required
def profile(request):
    user = request.user

    profile = Profile.objects.get(user=user)
    context = {
        'profile': profile,

    }
    return render(request, 'home/profile.html', context)




@login_required
def add_clients(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact_person = request.POST.get('contact_person')
        mobile = request.POST.get('mobile')
        client = Client.objects.create(name=name, address=address, contact_person=contact_person, mobile=mobile)
        client.save()
        messages.success(request, 'Client added successfully!')
        return redirect('add-clients')
    else:
        clients = Client.objects.all()
        return render(request, 'home/add-clients.html', {'clients': clients})





def client_profile(request, pk):
    client = Client.objects.get(pk=pk)
    contracts = Contracts.objects.filter(client=pk)

    context = {
        'client': client,
        "contracts": contracts
    }
    return render(request, 'home/client-profile.html', context)






def compare_amount(request, contract_id):
    contract = Contracts.objects.get(id=contract_id)
    action_amounts = Contract_actions.objects.filter(contract=contract)
    matching_actions = action_amounts.filter(amount=contract.amount)
    matching_actions_data = list(matching_actions.values())
    return JsonResponse(matching_actions_data, safe=False)




# check if valid or None
def valid_query(param):
    return param !='' and param is not None


def search(request):
    pass




def report(request):
    all_contracts = Contracts.objects.all()
    offices = Office_name.objects.all
    title= request.GET.get('title')
    amount = request.GET.get('amount')
    office_id = request.GET.get('office')




    if title is not None:
        if valid_query(title):
            all_contracts = all_contracts.filter(title_of_contract__icontains=title)
    
    if amount is not None:
        if valid_query(amount):
            all_contracts = all_contracts.filter(amount__icontains=amount)
    
    if office_id is not None:
        if valid_query(office_id):
            all_contracts = all_contracts.filter(office=office_id)
            print(office_id)


    context = {
        'all_contracts': all_contracts,
        'offices':offices
    }
    
    return render(request, 'home/reports.html', context)



@login_required
def change_password(request):
    username=request.user.username
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        test= request.user.password
        check = check_password(old_password, test)
        if check == True:
            #check password
            if new_password1==new_password2:
                update_user = User.objects.get(username=username)
                update_user.set_password(new_password1)
                update_user.save()
                logout(request)
                messages.success(request,'Password Changed Successfully. Please Login')
                return redirect('/profile/')
            else:
                messages.error(request,"Password didn't match!")
                return redirect('/profile/')
        else:
            messages.error(request, 'Password is incorect')
            return redirect('/profile/')

    else:
        return render(request, 'home/profile.html')