from django.http import JsonResponse
import json
import os

def search_account(request):
    # Kunin ang account number mula sa Genesys
    target_acc = request.GET.get('accountNumber')
    
    # Lokasyon ng data.txt
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'data.txt')
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # Hanapin ang matching account sa lahat ng customers
        for customer in data['customers']:
            for acc in customer['accounts']:
                if acc['accountNumber'] == target_acc:
                    # Ibalik ang kumpletong details para sa Phase 1 at Phase 2
                    return JsonResponse({
                        "found": True,
                        "firstName": customer['name']['first'],
                        "lastName": customer['name']['last'],
                        "accountType": acc['accountTypeDescription'],
                        "sCifId": customer['sCifId'],
                        "mobileNumber": customer.get('mobileNumber', "No Mobile") # Dito natin kukunin ang bagong field
                    })
                    
        return JsonResponse({"found": False, "msg": "Account not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)