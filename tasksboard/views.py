from django.shortcuts import get_object_or_404, render, HttpResponse
from django.template.context import Context
from django.http import JsonResponse, response
import time
import cups
import json
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt
from gc import get_objects


# Create your views here.

def board(request):
    from .models import Board
    boards = Board.objects.all()
    context ={
        'boards':boards,
    }
    # print(boards)
    return render(request, 'tasks/boards.html', context)
    # return render(request, 'home/tasks.html')


# def view_board(request, id):
#     from .models import Board, List, Card, Comment

#     board = get_object_or_404(Board, id=id)
#     lists = List.objects.filter(board=board)
#     cards = Card.objects.raw("select * from  card where lists=lists")
#     context = {
#         'board': board,
#         'lists': lists,
#         'cards':cards
#     }
#     return render(request, 'tasks/tasks.html', context)

def view_board(request, id):
    from .models import Board, List, Card, Comment
    board = get_object_or_404(Board, id=id)
    lists = List.objects.filter(board=board)

    lists_with_cards = []
    for list in lists:
        cards = Card.objects.filter(list_id=list.id)
        # print(cards)
        lists_with_cards.append({
                    'lists': list,
                    'cards': cards
                })

    context = {
        'board': board,
        'lists': lists,
        'lists_with_cards':lists_with_cards,

    }
    return render(request, 'tasks/tasks.html', context)



def move_card(request, id):
    list = get_object_or_404(List, id=id)
    print(list)
    return list



def add_comment(request, id):
    pass


# @csrf_exempt
# def move_card(request):
#     if request.method == 'POST':
#         try:
#             # Get data from the request
#             data = json.loads(request.body)
#             card_id = data.get('card_id')
#             new_list_name = data.get('new_list_name')

#             # Find the card and the new list by name
#             card = Card.objects.get(id=card_id)
#             new_list = List.objects.get(name=new_list_name)

#             # Update the card's list
#             card.list = new_list
#             card.save()

#             return JsonResponse({'success': True})

#         except Card.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'Card not found'}, status=404)
#         except List.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'List not found'}, status=404)
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)}, status=400)
#     else:
#         return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)



def get_printers_and_status(request):
    """
    Discover available printers and return their status.
    """
    try:
        # Connect to the CUPS server
        conn = cups.Connection()

        # Fetch available printers
        printers = conn.getPrinters()

        # Structure the printer information for JSON response
        printer_details = {
            name: {
                "Printer Info": details.get("printer-info", "Unknown"),
                "Printer State": {
                    3: "Idle",
                    4: "Printing",
                    5: "Processing",
                }.get(details.get("printer-state", 0), "Unknown"),
                "State Reasons": details.get("printer-state-reasons", []),
                "Location": details.get("printer-location", "Unknown"),
                "Make and Model": details.get("printer-make-and-model", "Unknown"),
            }
            for name, details in printers.items()
        }

        # Return the printer details as JSON
        return JsonResponse({"printers": printer_details}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




# response

# {
#   "printers": {
#     "Canon_MF3010": {
#       "Printer Info": "Canon MF3010",
#       "Printer State": "Idle",
#       "State Reasons": ["none"],
#       "Location": "Sushil’s MacBook Air",
#       "Make and Model": "Canon MF3010"
#     }
#   }
# }

@csrf_exempt
def print_file(request):
    """
    Submit a file for printing and monitor its status.
    """
    try:
        if request.method == 'POST':
            # Handle file upload
            uploaded_file = request.FILES.get('file')
            printer_name = request.POST.get('printer_name', "Canon_MF3010")

            if not uploaded_file:
                return JsonResponse({"error": "No file uploaded"}, status=400)

            # Save the uploaded file to the server
            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Connect to the CUPS server
            conn = cups.Connection()

            # Check if the printer is available
            printers = conn.getPrinters()
            if printer_name not in printers:
                return JsonResponse({"error": f"Printer '{printer_name}' not found"}, status=404)

            # Submit the print job
            job_id = conn.printFile(printer_name, file_path, "Django Print Job", {})
            print(f"Job submitted successfully. Job ID: {job_id}")

            # Monitor job status
            while True:
                jobs = conn.getJobs()
                if job_id not in jobs:
                    return JsonResponse({"message": f"Job {job_id} completed or removed from the queue."}, status=200)

                job = jobs[job_id]
                job_state = job.get("job-state", None)
                job_state_reasons = job.get("job-state-reasons", "Unknown")

                # Check for completion, cancellation, or errors
                if job_state in [7, 8, 9]:  # Canceled, Aborted, or Completed
                    break

                # Wait before checking again
                time.sleep(2)

            return JsonResponse({
                "message": "Job completed.",
                "Job ID": job_id,
                "Job State": {
                    7: "Canceled",
                    8: "Aborted",
                    9: "Completed",
                }.get(job_state, "Unknown"),
                "State Reasons": job_state_reasons,
            })
        else:
            return render(request, 'print-file.html')
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



# def print_file(request):
#     """
#     Submit a file for printing and monitor its status.
#     """
#     try:
#         # Get parameters from the request
#         file_path = request.GET.get("file_path")
#         printer_name = request.GET.get("printer_name", "Canon_MF3010")

#         if not file_path:
#             return JsonResponse({"error": "Missing 'file_path' parameter"}, status=400)

#         # Connect to the CUPS server
#         conn = cups.Connection()

#         # Check if the printer is available
#         printers = conn.getPrinters()
#         if printer_name not in printers:
#             return JsonResponse({"error": f"Printer '{printer_name}' not found"}, status=404)

#         # Submit the print job
#         job_id = conn.printFile(printer_name, file_path, "Django Print Job", {})
#         print(f"Job submitted successfully. Job ID: {job_id}")

#         # Monitor job status
#         while True:
#             jobs = conn.getJobs()
#             if job_id not in jobs:
#                 return JsonResponse({"message": f"Job {job_id} completed or removed from the queue."}, status=200)

#             job = jobs[job_id]
#             job_state = job.get("job-state", None)
#             job_state_reasons = job.get("job-state-reasons", "Unknown")

#             # Check for completion, cancellation, or errors
#             if job_state in [7, 8, 9]:  # Canceled, Aborted, or Completed
#                 break

#             # Wait before checking again
#             time.sleep(2)

#         return JsonResponse({
#             "message": "Job completed.",
#             "Job ID": job_id,
#             "Job State": {
#                 7: "Canceled",
#                 8: "Aborted",
#                 9: "Completed",
#             }.get(job_state, "Unknown"),
#             "State Reasons": job_state_reasons,
#         })
#     return render(request,'print-file.html')

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)


# {
#   "message": "Job completed.",
#   "Job ID": 1793,
#   "Job State": "Completed",
#   "State Reasons": ["none"]
# }




@csrf_exempt
def upload_for_print(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return render(request, 'print-file.html', {"error": "No file uploaded."})

        # Save the uploaded file temporarily
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Pass the file URL to the template for downloading or printing locally
        file_url = f"{settings.MEDIA_URL}{uploaded_file.name}"

        return render(request, 'print-file.html', {"file_url": file_url})
    return render(request, 'print-file.html')
