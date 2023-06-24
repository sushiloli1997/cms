from django.shortcuts import render, redirect, HttpResponse
from .models import Office_name, Contracts, Contract_actions,Profile, Roles, Client
from django.contrib import messages
from .forms import RegisterForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .decorators import unauthenticated_user,allowed_users
from django.contrib.auth.hashers import make_password





def index(request):
    return render(request, 'index.html')


@unauthenticated_user

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            m=messages.success(request, 'You are now logged in')
            print("Logged in")
            return redirect('dashboard')
        else:
            print("username and password is incorrect")
            messages.error(request, "username and password is incorrect")
            return redirect('login')
    else:
        return render(request, 'home/login.html')
    



def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def dashboard(request):

    offices = Office_name.objects.count()
    contracts = Contracts.objects.count()
    users = User.objects.count()
    client = Client.objects.count()
    activity= Contract_actions.objects.count()
    contract_list = Contracts.objects.all().order_by('created_date')[:6]
    activities = Contract_actions.objects.all().order_by('-created_date')[:6]

    context ={
        'offices':offices,
        'contracts': contracts,
        'users':users,
        'contract_list':contract_list,
        'activities':activities,
        'clients':client,

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
        office = Office_name(office_name=name, address=address)
        office.save()
        messages.success(request, "Saved  Successfully")
        return redirect('company_list')
    else:
        # messages.success(request, 'error while adding company')
        return render(request, 'home/add-company.html')




@login_required
def delete_company(request, pk):
    office = get_object_or_404(Office_name, pk=pk)
    office.delete()
    messages.success(request, 'deleted Successfully')
    return redirect('company_list')




@login_required
def delete_contract(request, pk):
    contract =get_object_or_404(Contracts, pk=pk)
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
            messages.error(request,"Can't get roles")
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
                password= make_password(password1),
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

    if request.method == 'POST':
        office_id = request.POST.get('office_name')
        try:
            office = get_object_or_404(Office_name, id=office_id)
        except Office_name.DoesNotExist:
            messages.error(request, 'Invalid office ID')
            return render(request, 'home/add-contract.html', {'offices': offices,'clients':clients})

        client_id= request.POST.get('client')
        try:
            clients=get_object_or_404(Client, id= client_id)
        except Client.DoesNotExist:
            messages.error(request, 'Invalid Client')
            return render(request, 'home/add-contract.html', {'offices': offices,'clients':clients})

        User = get_user_model()
        user = get_object_or_404(User, id =request.user.id)

        title_of_contract = request.POST.get('title_of_contract')
        contract_with = request.POST.get('contract_with')
        address = request.POST.get('address')
        amount = request.POST.get('amount')
        contract_date = request.POST.get('contract_date')
        billing_date = request.POST.get('billing_date')
        contract_file = request.FILES.get('contract_file')
        
        
        contracts = Contracts(
            office=office,
            title_of_contract=title_of_contract,
            client_id=client_id,
            address=address,
            amount = amount,
            contract_date=contract_date,
            billing_date=billing_date,
            # contract_file=contract_file,
            user = user
        )
        contracts.save()
        if contract_file:
            contracts.contract_file.save(contract_file.name, contract_file)

        actions = Contract_actions(
            contract = contracts,
            status = 1,
            amount= amount,
            user =user,
            extra = {
                'contract_id': contracts.id,
                'title_of_contract':title_of_contract,
                'clients':client_id,
                'address':address,
                'contract_date':contract_date,
                'billing_date': billing_date,
                'user': user.id
            },
        )
        actions.save()
        messages.success(request, 'Added successfully')
    
        

    return render(request, 'home/add-contract.html', {'offices': offices,'clients':all_clients})




@login_required
def contract_view(request, pk):
    datas = Contracts.objects.get(pk=pk)
    actions = Contract_actions.objects.filter(contract_id=pk).order_by('-created_date')
    try:
       # print(actions)
        return render(request, 'home/view-contract-detail.html', {
            'datas':datas,
            'actions':actions
            })  
       
    except MultipleObjectsReturned:
        return render(request, 'home/view-contract-detail.html', {
            'datas':datas,
            'actions':actions
            
            })
    
    except ObjectDoesNotExist:
                return render(request,'home/page-404.html')


@login_required
@allowed_users(allowed_roles=[2])
def approve_contract(request, contract_id):
    User = get_user_model()
    user = get_object_or_404(User, id =request.user.id)
    contract = Contracts.objects.get(id=contract_id)
    if request.method == 'POST':
        remarks = request.POST.get('approve')
    actions = Contract_actions(
        contract= contract,
        status = 2,
        amount=0,
        remarks = remarks,
        user =user,
        extra = {}) 
                
    print(user)
    actions.save()
    return redirect('view-contract', pk=contract_id)


@allowed_users(allowed_roles=[1])
def reject_contract(request, contract_id):
    User =get_user_model()
    user =get_object_or_404(User, id=request.user.id)
    contract = Contracts.objects.get(id=contract_id)
    if request.method == 'POST':
        remarks = request.POST.get('reject')
    actions = Contract_actions(
        contract= contract,
        status = 3,
        amount=0,
        remarks = remarks,
        user=user,
        extra = {})
                
    print(contract)
    actions.save()
    return redirect('view-contract', pk=contract_id)



def add_comment(request, contract_id):
    User = get_user_model()
    user = get_object_or_404(User, id =request.user.id)
    contract = Contracts.objects.get(id=contract_id)
    if request.method == 'POST':
        remarks = request.POST.get('comment')
    actions = Contract_actions(
               contract= contract,
                status = 5,
                amount=0,
                user =user,
                remarks = remarks,
                extra = {}) 
                
    print(user)
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
    User =get_user_model()
    user =get_object_or_404(User, id=request.user.id)
    contract = get_object_or_404(Contracts, id=contract_id)
    contract.payment_status = True
    contract.save()
    if request.method == 'POST':
        remarks = request.POST.get('comment')
    actions = Contract_actions(
               contract= contract,
                status = 4,
                amount=0,
                remarks = remarks,
                user=user,
                extra = { } )
    actions.save()
    return redirect('view-contract', pk=contract_id)
   






def register(request):
    pass


def web_index(request):
    return render(request, 'home/index.html')



@login_required
def profile(request,id):
    profile = Profile.objects.filter(id=id)
    context = {
        'profile':profile,

    }
    return render(request, 'home/profile.html', context)







@login_required

def add_clients(request):
    if request.method =='POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact_person= request.POST.get('contact_person')
        mobile = request.POST.get('mobile')
        client= Client.objects.create(name=name, address=address, contact_person=contact_person, mobile=mobile)
        client.save()
        messages.success(request,'Client added successfully!')
        return redirect('add-clients')
    else:
        clients = Client.objects.all()
        return render(request, 'home/add-clients.html',{'clients':clients})





def client_profile(request, pk):
    client = Client.objects.get(pk=pk)
    contracts = Contracts.objects.filter(client=pk)

    context = {
        'client':client,
        "contracts":contracts
    }
    return render(request, 'home/client-profile.html',context)





def error_404(request):
    
    return render(request, 'home/page-404.html')



