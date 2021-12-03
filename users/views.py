import json, requests
import hashlib, hmac, base64, time

from django.views    import View
from django.http     import JsonResponse
from django.conf     import settings
from random          import randint

timestamp    = str(int(time.time() * 1000))

service_id   = settings.SERVICE_ID
access_key   = settings.ACCESS_KEY

uri          = f'/sms/v2/services/{service_id}/messages'
api_url      = f'https://sens.apigw.ntruss.com{uri}'

def make_signature(uri, access_key):
    access_secret_key = bytes(settings.ACCESS_SECRET_KEY, 'UTF-8')
    message           = "POST" + " " + uri + "\n" + timestamp + "\n" + access_key
    message           = bytes(message, 'UTF-8')
    signin_key        = base64.b64encode(hmac.new(
        access_secret_key, message, digestmod=hashlib.sha256).digest())
    return signin_key 

class SendSMSView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            auth_number = randint(1000,10000)

            messages    = { 'to' : data['phone_number']}
            
            headers     = {
                "Content-Type"             : "application/json; charset=utf-8",
                "x-ncp-apigw-timestamp"    : timestamp,
                "x-ncp-iam-access-key"     : access_key,
                "x-ncp-apigw-signature-v2" : make_signature(uri, access_key)
            }

            body = {
                "type"        : "SMS",
                "contentType" : "COMM",
                "from"        : settings.COMPANY_NUMBER,
                "content"     : "인증번호 [{}]를 입력해 주세요.".format(auth_number),
                "messages"    : [messages]
            }

            json_body = json.dumps(body)

            requests.post(api_url, headers = headers, data=json_body)

            return JsonResponse({'auth_number' : auth_number}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 401)