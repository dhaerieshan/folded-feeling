import uuid
from django.shortcuts import render
from .models import AccessCode

def admin_page(request):
    latest_code = AccessCode.objects.last()
    message = ""
    if request.method == "POST":
        new_code = request.POST.get("new_code")
        # Remove old codes and tokens
        AccessCode.objects.all().delete()
        AccessCode.objects.create(code=new_code)
        message = "New code set successfully!"
        latest_code = AccessCode.objects.last()
    return render(request, "adminpage.html", {"message": message, "latest_code": latest_code})


def proposal_page(request):
    # Check if user already has valid cookie
    stored_token = request.COOKIES.get('lover_token')
    if stored_token:
        # User is already authorized via cookie
        return render(request, "proposal.html", {"success": True})

    db_code = AccessCode.objects.last()

    if request.method == "POST":
        entered_code = request.POST.get("code")
        if db_code and entered_code == db_code.code:
            # Generate a unique token for this device
            token = str(uuid.uuid4())
            response = render(request, "proposal.html", {"success": True})
            response.set_cookie("lover_token", token, max_age=60*60*24*30)
            # Delete code so it can't be reused
            db_code.delete()
            return response
        else:
            return render(request, "proposal.html", {"error": "Invalid or expired code 😔"})

    # No valid cookie and no code entered yet
    return render(request, "proposal.html", {"not_meant": True})