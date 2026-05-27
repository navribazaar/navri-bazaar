# navri_bazaar/views.py
import threading  
from django.shortcuts import render
from django.core.mail import send_mail 
from django.conf import settings
from .models import MarketFeedback

def send_async_email(subject, body, from_email, recipient_list):
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        print("🚀 BACKGROUND SMTP: Confirmation email dispatched successfully!")
    except Exception as email_error:
        print(f"❌ BACKGROUND SMTP ERROR: {email_error}")
        print("💡 FALLBACK LOG ENTRY: If SMTP fails, reading your email payload here:")
        print(f"TO: {recipient_list}\nSUBJECT: {subject}\nBODY:\n{body}\n---")

def landing_page(request):
    success = False
    error_msg = None

    if request.method == 'POST':
        user_guess = request.POST.get('user_guess', '').strip()
        industry_sector = request.POST.get('industry_sector', '').strip()
        other_sector = request.POST.get('other_sector', '').strip() 
        user_city = request.POST.get('user_city', '').strip()
        user_email = request.POST.get('user_email', '').strip()

        print(f"\n--- [INBOUND SUBMISSION ARRIVED] ---")
        print(f"EMAIL: '{user_email}' | CITY: '{user_city}'")

        if not user_guess or not industry_sector or not user_city or not user_email:
            error_msg = "All fields are mandatory. Drop your whole vision!"
            
        else:
            if MarketFeedback.objects.filter(user_email=user_email).exists():
                error_msg = "Your vision is already locked in for this email!"
            else:
                # 1. Commit structural records to database
                feedback = MarketFeedback.objects.create(
                    user_guess=user_guess,
                    industry_sector=industry_sector,
                    other_sector=other_sector if industry_sector == 'other' else None,
                    user_city=user_city,
                    user_email=user_email
                )
                
                # 2. Compile confirmation message strings
                sector_display = other_sector if industry_sector == 'other' else feedback.get_industry_sector_display()
                email_subject = "Vision Transmitted | NAVRIBAZAAR.IN"
                email_body = (
                    f"Hey Chief Conspiracy Theorist,\n\n"
                    f"Your vision for NAVRIBAZAAR.IN has been successfully logged into our genesis matrix.\n\n"
                    f"Here is what you locked in:\n"
                    f"- Industry: {sector_display}\n"
                    f"- Location: {user_city}\n"
                    f"- Your Concept: \"{user_guess}\"\n\n"
                    f"Stay sharp,\n"
                    f"Team Navri Bazaar"
                )
                
                # 3. Handle asynchronous processing
                # Fallback safeguard check if EMAIL_HOST_USER variable setup is missing in settings
                sender_mail = getattr(settings, 'EMAIL_HOST_USER', 'navribazaar.in@gmail.com')
                
                email_thread = threading.Thread(
                    target=send_async_email,
                    args=(email_subject, email_body, sender_mail, [user_email])
                )
                email_thread.start()

                success = True

    return render(request, 'navri_bazaar/landing.html', {'success': success, 'error_msg': error_msg})