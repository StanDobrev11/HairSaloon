"""
URL configuration for HairSaloon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.core.mail import send_mail
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('HairSaloon.common.urls')),
    path('accounts/', include('HairSaloon.accounts.urls')),
    path('dashboard/', include('HairSaloon.bookings.urls')),
    path('services/', include('HairSaloon.services.urls')),
    path('personel/', include('HairSaloon.hairdressers.urls')),
    path('api/', include('HairSaloon.api.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
# send_mail(
#     subject='Test',
#     message='This is a test message without HTML',
#     from_email='dobrev81@gmail.com',
#     recipient_list=['gejiv57035@eryod.com', 'dobrev81@gmail.com'],
#     fail_silently=False
# )

#
# mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY), version='v3.1')
#
#
# def send_email_with_mailjet(subject, message, from_email, to_email):
#     data = {
#         'Messages': [
#             {
#                 "From": {
#                     "Email": from_email,
#                     "Name": "Your Name or Company Name"
#                 },
#                 "To": [
#                     {
#                         "Email": to_email,
#                         "Name": "Recipient Name"
#                     }
#                 ],
#                 "Subject": subject,
#                 "TextPart": message,
#                 "HTMLPart": f"<h3>{message}</h3>"
#             }
#         ]
#     }
#     result = mailjet.send.create(data=data)
#     return result.status_code, result.json()
#
#
# def send_test_email():
#     subject = "Hello from Mailjet"
#     message = "This is a test email sent from Django app using Mailjet."
#     from_email = "gejiv57035@eryod.com"  # Your verified sender email
#     to_email = 'dobrev81@gmail.com'  # Recipient's email
#
#     status_code, response = send_email_with_mailjet(subject, message, from_email, to_email)
#
#     if status_code == 200:
#         print(f"Email sent successfully!")
#     else:
#         print(f"Failed to send email: {response}")
#
#
# send_test_email()
