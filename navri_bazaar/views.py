# navri_bazaar/views.py
from django.shortcuts import render
from django.core.mail import send_mail 
from django.conf import settings
from .models import MarketFeedback

def landing_page(request):
    success = False
    error_msg = None

    if request.method == 'POST':
        # 1. Pull and clean values securely from form submission
        user_guess = request.POST.get('user_guess', '').strip()
        industry_sector = request.POST.get('industry_sector', '').strip()
        other_sector = request.POST.get('other_sector', '').strip() 
        user_city = request.POST.get('user_city', '').strip()
        user_email = request.POST.get('user_email', '').strip()

        # 🔥 LIVE LOG DIAGNOSTICS: View these inside your Render Live Logs console
        print(f"\n--- [NEW INBOUND SUBMISSION] ---")
        print(f"EMAIL: '{user_email}'\nGUESS: '{user_guess}'\nSECTOR: '{industry_sector}'\nCITY: '{user_city}'\n")

        # 2. Strict Validation: Prevent blank spaces from passing through
        if not user_guess or not industry_sector or not user_city or not user_email:
            error_msg = "All fields are mandatory. Drop your whole vision!"
            
        else:
            # 3. Duplicate Check: Prevent duplicate entries (ignores blank string lookups)
            if MarketFeedback.objects.filter(user_email=user_email).exists():
                error_msg = "Your vision is already locked in for this email!"
            else:
                # 4. Save clean data record to your database
                feedback = MarketFeedback.objects.create(
                    user_guess=user_guess,
                    industry_sector=industry_sector,
                    other_sector=other_sector if industry_sector == 'other' else None,
                    user_city=user_city,
                    user_email=user_email
                )
                
                # 5. Format the custom confirmation email template body
                sector_display = other_sector if industry_sector == 'other' else feedback.get_industry_sector_display()
                
                email_subject = "Vision Transmitted | NAVRIBAZAAR.IN"
                email_body = (
                    f"Hey Chief Conspiracy Theorist,\n\n"
                    f"Your vision for NAVRIBAZAAR.IN has been successfully logged into our genesis matrix.\n\n"
                    f"Here is what you locked in:\n"
                    f"- Industry: {sector_display}\n"
                    f"- Location: {user_city}\n"
                    f"- Your Concept: \"{user_guess}\"\n\n"
                    f"If your sector wins the community baseline evaluation, you'll be the first to receive alpha access and early-bird platform perks.\n\n"
                    f"Stay sharp,\n"
                    f"Team Navri Bazaar"
                )
                
                # 6. Execute secure SMTP connection dispatch
                try:
                    send_mail(
                        subject=email_subject,
                        message=email_body,
                        from_email=settings.EMAIL_HOST_USER,  # Uses your verified Gmail connection from settings
                        recipient_list=[user_email],             
                        fail_silently=False,
                    )
                    print("🚀 SMTP VERIFICATION: EMAIL OUTBOUND DISPATCHED SUCCESSFULLY!")
                except Exception as email_error:
                    print(f"❌ SMTP DISPATCH CRASH: Details: {email_error}")

                success = True

    return render(request, 'navri_bazaar/landing.html', {'success': success, 'error_msg': error_msg})