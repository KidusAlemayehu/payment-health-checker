from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from urllib.parse import urlparse
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
        print(f'Checking health of {gateway["NAME"]}')
        
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)            
            if result.returncode != 0:
                failed_gateways.append(gateway)
                print(f'Failed to check health of {gateway["NAME"]}')
                # Print stderr for debugging
                print(f'Stderr output: {result.stderr}')
                continue
            print(f'Stdout Output: {result.stdout}')
            print(f'Stderr Output: {result.stderr}')
            
            if result.stdout != '200':
                failed_gateways.append(gateway)
                print(f'Gateway Failure {gateway["NAME"]}')
                continue
        
        except subprocess.TimeoutExpired:
            failed_gateways.append(gateway)
            print(f'Timeout occurred while checking health of {gateway["NAME"]}')
        
        except Exception as e:
            failed_gateways.append(gateway["NAME"])
            print(f'Error occurred while checking health of {gateway["NAME"]}: {e}')
        
        print(f'Completed checking health of {gateway["NAME"]}\n')
    print(f'Failed Gateways are: {failed_gateways}')
        
    if failed_gateways:
        send_mail(
            'Payment Gateway Health Check',
            f'The following payment gateways failed to respond: {", ".join([gateway["NAME"] for gateway in failed_gateways])}',
            settings.DEFAULT_FROM_EMAIL,
            ['kidusalemayehu44@gmail.com'],
        )
    else:
        send_mail(
            'Payment Gateway Health Check',
            'All payment gateways are working',
            settings.DEFAULT_FROM_EMAIL,
            ['kidusalemayehu44@gmail.com'],
        )