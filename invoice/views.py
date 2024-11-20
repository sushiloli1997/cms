from django.contrib import messages
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from contracts.models import Contracts, Client
from .models import PaymentStatus
from django.views.decorators.http import require_http_methods
from .models import Invoices, InvoiceTracks
from django.urls import reverse
from django.contrib.auth.models import User

from faker import Faker
from django.db import IntegrityError
fake= Faker()



def new_index(request):
    for i in range(0,10):
        print(i)
        try:
            user=User.objects.create_user(username=fake.user_name(), first_name=fake.name(), last_name=fake.last_name(), email=fake.email(), password=fake.password())
            user.save()
        except IntegrityError as e:
            print(f"Error creating user {user}")
            continue
        except Exception as e:
            print(f"Error creating user {user}")
            continue
        print(f"created Successfully{user}")

    print("all created successfully")

    return render(request, 'invoice/test.html')


# Create your views here.
@require_http_methods(['GET'])
def error_404_page(request, exception):
    return HttpResponse(exception)


def invoice(request):
    payment_type = PaymentStatus.choices
    contracts = Contracts.objects.all()
    clients = Client.objects.all()
    invoices = Invoices.objects.all()

    if request.method == "POST":
        payment_status = request.POST.get('payment')
        contract_id = request.POST.get('contract')
        number_of_invoice = request.POST.get('number_of_invoice')
        invoice_date = request.POST.get('invoice_date')
        client_id = request.POST.get('client')
        try:
            clients = get_object_or_404(Client, id=client_id)
            # client = get_object_or_404(Client, id=client_id)
        except Client.DoesNotExist:
            return messages.error(request, "Client ID is missing")

        try:
            contract = get_object_or_404(Contracts, id=contract_id)
        except Contracts.DoesNotExist:
            return messages.error(request, "Unable to get Contract")
        try:
            invoice = Invoices.objects.create(
                status=payment_status,
                contract=contract,
                number_of_invoice=number_of_invoice,
                date_of_issue=invoice_date,
                client_id=client_id,
            )
            invoice.save()
            messages.info(request, 'Saved Successfully.')
            return redirect('invoice')
        except IntegrityError as e:
            return HttpResponse("Error creating invoice: " + str(e))
    context = {
        'clients': clients,
        'payment_type': payment_type,
        'contracts': contracts,
        'invoices': invoices
    }
    return render(request, "invoice/invoice.html", context)


def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoices, pk=pk)
    try:
        invoice.soft_delete()
        messages.success(request, 'Deleted Successfully')
    except ObjectDoesNotExist:
        messages.success(request, "Object not Found")
    return redirect('invoice')


def view_invoice(request, pk):
    invoice = get_object_or_404(Invoices, pk=pk)
    invoicetracks = InvoiceTracks.objects.filter(invoice_id=pk)
    total_amount = 0

    for track in invoicetracks:
        if track.rate is not None and track.quantity is not None:
            amount = track.rate * track.quantity
            total_amount =amount

    context = {
        'invoice': invoice,
        'invoicetracks': invoicetracks,
        'total_amount': total_amount,
    }
    return render(request, 'invoice/invoice-detail.html', context)


def add_invoicetracks(request, pk):
    invoice = get_object_or_404(Invoices, pk=pk)
    if request.method == 'POST':
        invoice = request.POST.get('invoice')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        rate = request.POST.get('rate')
        try:
            invoice = get_object_or_404(Invoices, pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse("Invocie details not found")
        InvoiceTracks.objects.create(
            invoice=invoice,
            description=description,
            amount=amount,
            rate=rate,
            action=2,
            status=1
        )
        return redirect(reverse('view-invoice', kwargs={'pk': pk}))
    else:
        return redirect('invoice')
