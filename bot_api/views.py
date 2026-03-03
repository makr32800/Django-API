from django.http import JsonResponse
import json
import os

def search_account(request):
    # Kinukuha ang accountNumber parameter mula sa URL
    target_acc = request.GET.get('accountNumber')
    
    # Path ng data.txt sa loob ng bot_api folder
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'data.txt')
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # Paghahanap sa record
        for customer in data['customers']:
            for acc in customer['accounts']:
                if acc['accountNumber'] == target_acc:
                    # Kapag match, ibalik ang dx`ata na kailangan ng Genesys
                    return JsonResponse({
                        "found": True,
                        "firstName": customer['name']['first'],
                        "accountType": acc['accountTypeDescription'],
                        "sCifId": customer['sCifId']
                    })
                    
        return JsonResponse({"found": False, "msg": "No match found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)