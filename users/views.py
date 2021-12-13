import json, re, bcrypt, jwt, uuid
from json.decoder import JSONDecodeError

from django.views    import View
from django.http     import JsonResponse
from django.conf     import settings

from .models         import User
import smtplib  
from email.mime.text import MIMEText

class EmailDuplicateCheckView(View):
    def post(self, request):
        try:
            email = json.loads(request.body)["email"]
            
            if not email:
                return JsonResponse({"message" : "VALUE_ERROR"}, status=401)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message" : "DUPLICATION_ERROR"}, status=401)
            
            return JsonResponse({"message" : "AVAILABLE_EMAIL"}, status=201)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=401)

        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status=400)

class NicknameDuplicateCheckView(View):
    def post(self, request):
        try:
            nickname = json.loads(request.body)["nickname"]

            if not nickname:
                return JsonResponse({"message" : "VALUE_ERROR"}, status=401)
            
            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({"message" : "DUPLICATION_ERROR"}, status=401)

            return JsonResponse({"message" : "AVAILABLE_NICKNAME"}, status=201)    
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=401)

        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status=400)    

class SignupSendEmailView(View):
    def post(self, request):
        try:
            email = json.loads(request.body)['email']

            if not email:
                return JsonResponse({"message" : "VALUE_ERROR"}, status=401)

            auth_number = uuid.uuid4().hex[:10]
            
            smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            smtp.starttls()
            smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            msg            = MIMEText(f'[인증번호] : {auth_number}')
            msg['Subject'] = 'Libido 회원가입 인증번호 안내'

            smtp.sendmail(settings.EMAIL_HOST_USER, email, msg.as_string())
            smtp.quit()

            return JsonResponse({'auth_number' : auth_number}, status=200)
        
        except KeyError:
            return JsonResponse({'message' : "KEY_ERROR"}, status=401)   

        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status=400)   

class ResetPasswordSendEmailView(View):
    def post(self, request):
        try:
            email = json.loads(request.body)['email']

            if not email:
                return JsonResponse({"message" : "VALUE_ERROR"}, status=401)

            if not User.objects.filter(email=email).exists():
                return JsonResponse({"message" : "USER_DOES_NOT_EXISTS"}, status=401)

            auth_number = uuid.uuid4().hex[:10]

            smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            smtp.starttls()
            smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            msg            = MIMEText(f'[인증번호] : {auth_number}')
            msg['Subject'] = 'Libido 비밀번호 재설정 인증번호 안내'

            smtp.sendmail(settings.EMAIL_HOST_USER, email, msg.as_string())
            smtp.quit()

            user = User.objects.get(email=email)
            user.reset_token_number = auth_number
            user.save()

            return JsonResponse({'auth_number' : auth_number}, status=200)    

        except KeyError:
            return JsonResponse({'message' : "KEY_ERROR"}, status=401)   

        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status=400)  

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email       = data["email"]
            password    = data["password"]
            re_password = data["re_password"]
            nickname    = data["nickname"]           
            nation      = data["nation"]

            if not email or not password or not re_password or not nickname or not nation:
                return JsonResponse({"message" : "VALUE_ERROR"}, status=401)

            if password != re_password:
                return JsonResponse({"message" : "PASSWORD_MISMATCH_ERROR"}, status=400)

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-_]+$', email):
                return JsonResponse({"message" : "EMAIL_OR_PASSWORD_VALIDATION_ERROR"}, status=400)

            if not re.match('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[~₩!@#$%^&*()\-_=+])[a-zA-Z0-9~!@#$%^&*()_\-+=]{8,17}$', password):
                return JsonResponse({"message" : "EMAIL_OR_PASSWORD_VALIDATION_ERROR"}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message" : "DUPLICATION_ERROR"}, status=400)

            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({"message" : "DUPLICATION_ERROR"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email        = email, 
                password     = hashed_password,
                nickname     = nickname,
                nation       = nation,
                login_method = 'libido'
            )
            
            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=401)

        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status=400)

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
        
        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status=400)

class ResetPasswordView(View):
    def post(self, request):
        try:
            data               = json.loads(request.body)
            email              = data["email"]
            password           = data["password"]
            re_password        = data["re_password"]
            reset_token_number = data["reset_token_number"]
            
            user = User.objects.get(email=email)

            if password != re_password:
                return JsonResponse({"message" : "PASSWORD_MISMATCH_ERROR"}, status = 400)

            if not re.match('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[~₩!@#$%^&*()\-_=+])[a-zA-Z0-9~!@#$%^&*()_\-+=]{8,17}$', password):
                return JsonResponse({"message" : "PASSWORD_VALIDATION_ERROR"}, status=400)

            if user.reset_token_number != reset_token_number:
                return JsonResponse({"message" : "RESET_TOKEN_VALIDATION_ERROR"})

            user.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.save()
            
            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"message" : "USER_DOES_NOT_EXISTS"}, status=401)

        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status=400)