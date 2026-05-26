# navri_bazaar/views.py
from django.shortcuts import render
from django.core.mail import send_mail 
from .models import MarketFeedback

def landing_page(request):
    success = False
    error_msg = None

    if request.method == 'POST':
        user_guess = request.POST.get('user_guess', '').strip()
        industry_sector = request.POST.get('industry_sector', '').strip()
        other_sector = request.POST.get('other_sector', '').strip() 
        user_city = request.POST.get('user_city', '').strip()
        user_email = request.POST.get('user_email', '').strip()

        if user_guess and industry_sector and user_city and user_email:
            # Prevent duplicate submissions from the same email
            if MarketFeedback.objects.filter(user_email=user_email).exists():
                error_msg = "Your vision is already locked in for this email!"
            else:
                # Save data to database, handling the conditional 'other' field logic
                feedback = MarketFeedback.objects.create(
                    user_guess=user_guess,
                    industry_sector=industry_sector,
                    other_sector=other_sector if industry_sector == 'other' else None,
                    user_city=user_city,
                    user_email=user_email
                )
                
                # --- Send Confirmation Email Loop ---
                # Determine what sector label to display in the email body
                sector_display = other_sector if industry_sector == 'other' else feedback.get_industry_sector_display()
                
                email_subject = "Vision Transmitted | NAVRIBAZAAR.IN"
                email_body = f"""Hey Chief Conspiracy Theorist,\n\nYour vision for NAVRIBAZAAR.IN has been successfully logged into our genesis matrix.\n\nHere is what you locked in:\n- Industry: {sector_display}\n- Location: {user_city}\n- Your Concept: "{user_guess}"\n\nIf your sector wins the community baseline evaluation, you'll be the first to receive alpha access and early-bird platform perks.\n\nStay sharp,\nTeam Navri Bazaar"""
                
                try:
                    send_mail(
                        email_subject,
                        email_body,
                        'noreply@navribazaar.in',  # Sender address mask
                        [user_email],             # Recipient target list
                        fail_silently=False,
                    )
                except Exception:
                    pass  # Prevents frontend execution crash if local machine has no email router active

                success = True
        else:
            error_msg = "All fields are mandatory. Drop your whole vision!"

    return render(request, 'navri_bazaar/landing.html', {'success': success, 'error_msg': error_msg})