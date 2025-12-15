from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

def send_verification_email(request, user, token):
    current_site = get_current_site(request)
    uid = user.pk
    verify_url = f"http://{current_site.domain}{reverse('accounts:verify-email')}?token={token}&uid={uid}"
    message = f"Hi {user.email},\n\nPlease verify your email by visiting:\n{verify_url}\n\nThanks!"
    send_mail("Verify your email", message, None, [user.email])

def send_order_confirmation(order):
    
    lines = [f"Order #{order.pk} - Total: {order.total_amount}", ""]
    for item in order.items.all():
        lines.append(f"{item.product.title} x{item.quantity} @ {item.price}")
    body = "\n".join(lines)
    send_mail(
        subject=f"Order Confirmation - #{order.pk}",
        message=body,
        from_email=None,
        recipient_list=[order.user.email],
    )