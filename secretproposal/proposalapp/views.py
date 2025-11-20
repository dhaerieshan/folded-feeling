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
    db_code = AccessCode.objects.last()
    stored_token = request.COOKIES.get("lover_token")

    # ---------- Case 1: No active code exists ----------
    if not db_code:
        return render(request, "proposal.html", {"not_meant_for_you": True})

    # ---------- Case 2: User already has correct token ----------
    if stored_token and db_code.token == stored_token:
        return render(request, "proposal.html", {"success": True})

    # ---------- Case 3: User is submitting code ----------
    if request.method == "POST":
        entered_code = request.POST.get("code")

        if entered_code == db_code.code:
            # Generate one-time device token
            token = str(uuid.uuid4())
            db_code.token = token
            db_code.save()

            response = render(request, "proposal.html", {"success": True})
            response.set_cookie("lover_token", token, max_age=60*60*24*30)

            # Delete code after use
            db_code.delete()

            return response

        return render(request, "proposal.html", {"error": "Invalid or expired code 😔"})

    # ---------- Case 4: Code exists but not submitted yet ----------
    return render(request, "proposal.html", {"enter_code": True})