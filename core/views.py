import jwt

from django.conf    import settings
from django.http    import JsonResponse

from users.models   import User

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            data = jwt.decode(access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            request.user = User.objects.get(id=data['id'])
                        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 401)            

        except User.DoesNotExist:
            return JsonResponse({'message' : 'UNKNOWN_USER'}, status = 401)

        return func(self, request, *args, **kwargs)

    return wrapper