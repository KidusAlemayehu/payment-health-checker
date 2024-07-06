from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from urllib.parse import urlparse
from checker.models import PaymentService
import sys
import subprocess

GATEWAYS = [
    # {
    #     "NAME":"TELEBIRR",
    #     "IDENTIFIER":"TELE_BIRR",
    #     "URL": '8.8.8.8'
    # },
    {
        "NAME":"YENE_PAY",
        "IDENTIFIER":"YENE_PAY",
        "URL": "https://endpoints.yenepay.com/api/"
    },
    {
        "NAME":"CHAPA",
        "IDENTIFIER":"CHAPA",
        "URL": "https://api.chapa.co/v1/"
    }
]
@shared_task
def send_periodic_emails():
    send_mail(
        'Periodic Email Task To check Payment Gateway Health',
        'This is a periodic email sent from payment gateway health checker service.',
        settings.DEFAULT_FROM_EMAIL,
        ['kidusalemayehu44@gmail.com'],
    )
    
@shared_task
def periodic_gateway_ping():
    failed_gateways = []
    for gateway in GATEWAYS:
        command = 'curl -s -o /dev/null -w "%%{http_code}" %s'%(gateway["URL"])
        service = PaymentService.objects.filter(identifier=gateway['IDENTIFIER']).first()
                
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)            
            if result.returncode != 0:
                failed_gateways.append(gateway)
                sys.stderr.write(f'Failed to check health of {gateway["NAME"]}')
                # Print stderr for debugging
                sys.stderr.write(f'Stderr output: {result.stderr}')
                continue
            
            if result.stdout != '200' and service.is_active != False:
                failed_gateways.append(gateway)
                sys.stderr.write(f'Payment Gateway Failure Occured at -> {gateway["NAME"]}')
                service.is_active = False
                service.save()
                
                continue
            
            if result.stdout == '200' and service.is_active == False:
                sys.stderr.write(f'Payment Gateway Connection Reestablished -> {gateway["NAME"]}')
                service.is_active = True
                service.save()
                send_mail(
            'Payment Gateway Health Check',
            f'The following payment gateway starts to work:  {(gateway["NAME"])}',
            settings.DEFAULT_FROM_EMAIL,
            ['kidusalemayehu44@gmail.com'],
        )
                
        
        except subprocess.TimeoutExpired:
            failed_gateways.append(gateway)
            sys.stderr.write(f'Timeout occurred while checking health of {gateway["NAME"]}')
        
    if failed_gateways:
        send_mail(
            'Payment Gateway Health Check',
            f'The following payment gateways failed to respond: {", ".join([gateway["NAME"] for gateway in failed_gateways])}',
            settings.DEFAULT_FROM_EMAIL,
            ['kidusalemayehu44@gmail.com'],
        )