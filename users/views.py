import json, re, bcrypt

from django.views    import View
from django.http     import JsonResponse

from .models         import User

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email       = data["email"]
            password    = data["password"]
            re_password = data["re_password"]
            nickname    = data["nickname"]           
            nation      = data["nation"]

            if password != re_password:
                return JsonResponse({"message" : "PASSWORD_MISMATCH_ERROR"}, status=400)
            
            if nickname == "":
                return JsonResponse({"message" : "KEY_ERROR"}, status=401)

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