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
    stored_token = request.COOKIES.get('lover_token')
    if stored_token:
        return render(request, "proposal.html", {"success": True})

    db_code = AccessCode.objects.last()

    # If NO CODE IS SET → show "not meant for you"
    if not db_code:
        return render(request, "proposal.html", {"not_meant": True})

    # If form submitted
    if request.method == "POST":
        entered_code = request.POST.get("code")
        if entered_code == db_code.code:
            token = str(uuid.uuid4())
            response = render(request, "proposal.html", {"success": True})
            response.set_cookie("lover_token", token, max_age=60*60*24*30)
            db_code.delete()
            return response
        else:
            return render(request, "proposal.html", {"error": "Invalid or expired code 😔"})

    # Code exists but not entered yet → show the form
    return render(request, "proposal.html")