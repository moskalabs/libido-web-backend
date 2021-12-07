import json, requests, re, bcrypt, jwt, uuid
import hashlib, hmac, base64, time
from random          import randint

from django.views    import View
from django.http     import JsonResponse
from django.conf     import settings

from .models         import User
import smtplib  
from email.mime.text import MIMEText

service_id   = settings.SERVICE_ID
access_key   = settings.ACCESS_KEY

uri          = f'/sms/v2/services/{service_id}/messages'
api_url      = f'https://sens.apigw.ntruss.com{uri}'

def make_signature(uri, access_key):
    timestamp         = str(int(time.time() * 1000))
    access_secret_key = bytes(settings.ACCESS_SECRET_KEY, 'UTF-8')
    message           = "POST" + " " + uri + "\n" + timestamp + "\n" + access_key
    message           = bytes(message, 'UTF-8')
    signin_key        = base64.b64encode(hmac.new(
        access_secret_key, message, digestmod=hashlib.sha256).digest())
    return signin_key, timestamp 

class SendSMSView(View):
    def post(self, request):
        try:
            data               = json.loads(request.body)
            auth_number        = randint(1000,10000)
            signkey, timestamp = make_signature(uri, access_key)
           
            messages           = { 'to' : data['phone_number']}
            headers            = {
                "Content-Type"             : "application/json; charset=utf-8",
                "x-ncp-apigw-timestamp"    : timestamp,
                "x-ncp-iam-access-key"     : access_key,
                "x-ncp-apigw-signature-v2" : signkey
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

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email        = data["email"]
            password     = data["password"]
            re_password  = data["re_password"]
            nickname     = data["nickname"]           
            phone_number = data["phone_number"]
            
            if password != re_password:
                return JsonResponse({"message" : "PASSWORD_MISMATCH_ERROR"}, status = 400)

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-_]+$', email):
                return JsonResponse({"message" : "EMAIL_OR_PASSWORD_VALIDATION_ERROR"}, status=400)

            if not re.match('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[~₩!@#$%^&*()\-_=+])[a-zA-Z0-9~!@#$%^&*()_\-+=]{8,17}$', password):
                return JsonResponse({"message" : "EMAIL_OR_PASSWORD_VALIDATION_ERROR"}, status=400)
            
            if not re.match('^[0-9]{10,11}$', phone_number):
                return JsonResponse({"message" : "PHONE_NUMBER_VALIDATION_ERROR"}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message" : "DUPLICATION_ERROR"}, status=400)

            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({"message" : "DUPLICATION_ERROR"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email        = email, 
                password     = hashed_password,
                nickname     = nickname,
                phone_number = phone_number,
                login_method = 'libido'
            )
            
            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=401) 

class SigninView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data["email"]
            password = data["password"]

            user = User.objects.get(email=email)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message" : "INVALID_USER_OR_INVALID_PASSWORD"}, status=401)

            access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            return JsonResponse({"message" : "SUCCESS", "ACCESS_TOKEN" : access_token}, status=200)
                
        except User.DoesNotExist:
            return JsonResponse({"message" : "USER_DOES_NOT_EXISTS"}, status=401) 

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=401)

class SendEmailView(View):
    def post(self, request):
        try:
            email = json.loads(request.body)['email']
        
            auth_number = uuid.uuid4().hex[:10]
            
            smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            smtp.starttls()
            smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            msg            = MIMEText(f'[인증번호] : {auth_number}')
            msg['Subject'] = 'Libido 비밀번호 재설정 안내'

            smtp.sendmail(settings.EMAIL_HOST_USER, email, msg.as_string())
            smtp.quit()

            user = User.objects.get(email=email)

            user.reset_token_number = auth_number
            user.save()
            
            return JsonResponse({'auth_number' : auth_number}, status=200)
        
        except KeyError:
            return JsonResponse({'message' : "KEY_ERROR"}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message' : "USER_DOES_NOT_EXISTS"}, status=401)

class ResetPasswordView(View):
    def post(self, request):
        try:
            data               = json.loads(request.body)
            email              = data["email"]
            password           = data["password"]
            re_password        = data["re_password"]
            reset_token_number = data['reset_token_number']
            
            if password != re_password:
                return JsonResponse({"message" : "PASSWORD_MISMATCH_ERROR"}, status = 400)

            if not re.match('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[~₩!@#$%^&*()\-_=+])[a-zA-Z0-9~!@#$%^&*()_\-+=]{8,17}$', password):
                return JsonResponse({"message" : "PASSWORD_VALIDATION_ERROR"}, status=400)

            user = User.objects.get(email=email)
            if user.reset_token_number != reset_token_number:
                return JsonResponse({"message" : "RESET_TOKEN_VALIDATION_ERROR"})

            user.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.save()
            
            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"message" : "USER_DOES_NOT_EXISTS"}, status=401)