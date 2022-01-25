import json, re, bcrypt, jwt, uuid, requests, unicodedata, smtplib, boto3
from json.decoder import JSONDecodeError
from email.mime.text import MIMEText

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from django.views import View
from django.http import JsonResponse
from django.conf import settings

from users.models import User, Follow
from rooms.models import UserRoomHistory
from core.views import login_required

from users.serializers import UserSerializer, FollowSerializer


class BaseViewSet(
    # mixins.CreateModelMixin,
    # mixins.RetrieveModelMixin, # retrive open -> user_id retrive
    # mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class EmailDuplicateCheckView(View):
    def post(self, request):
        try:
            email = json.loads(request.body)["email"]

            if not email:
                return JsonResponse({"message": "VALUE_ERROR"}, status=401)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "DUPLICATION_ERROR"}, status=401)

            return JsonResponse({"message": "AVAILABLE_EMAIL"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=401)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)


class NicknameDuplicateCheckView(View):
    def post(self, request):
        try:
            nickname = json.loads(request.body)["nickname"]

            if not nickname:
                return JsonResponse({"message": "VALUE_ERROR"}, status=401)

            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({"message": "DUPLICATION_ERROR"}, status=401)

            return JsonResponse({"message": "AVAILABLE_NICKNAME"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=401)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)


class SignupSendEmailView(View):
    def post(self, request):
        try:
            email = json.loads(request.body)["email"]

            if not email:
                return JsonResponse({"message": "VALUE_ERROR"}, status=401)

            auth_number = uuid.uuid4().hex[:10]

            smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            smtp.starttls()
            smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            msg = MIMEText(f"[인증번호] : {auth_number}")
            msg["Subject"] = "Libido 회원가입 인증번호 안내"

            smtp.sendmail(settings.EMAIL_HOST_USER, email, msg.as_string())
            smtp.quit()

            return JsonResponse({"auth_number": auth_number}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=401)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)


class ResetPasswordSendEmailView(View):
    def post(self, request):
        try:
            email = json.loads(request.body)["email"]

            if not email:
                return JsonResponse({"message": "VALUE_ERROR"}, status=401)

            if not User.objects.filter(email=email).exists():
                return JsonResponse({"message": "USER_DOES_NOT_EXISTS"}, status=401)

            auth_number = uuid.uuid4().hex[:10]

            smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            smtp.starttls()
            smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            msg = MIMEText(f"[인증번호] : {auth_number}")
            msg["Subject"] = "Libido 비밀번호 재설정 인증번호 안내"

            smtp.sendmail(settings.EMAIL_HOST_USER, email, msg.as_string())
            smtp.quit()

            user = User.objects.get(email=email)
            user.reset_token_number = auth_number
            user.save()

            return JsonResponse({"auth_number": auth_number}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=401)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)


class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data["email"]
            password = data["password"]
            re_password = data["re_password"]
            nickname = data["nickname"]
            receive_email = data["is_receive_email"]
            nation = data["nation"]

            if (
                not email
                or not password
                or not re_password
                or not nickname
                or not nation
            ):
                return JsonResponse({"message": "VALUE_ERROR"}, status=401)

            if password != re_password:
                return JsonResponse({"message": "PASSWORD_MISMATCH_ERROR"}, status=400)

            if not re.match("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-_]+$", email):
                return JsonResponse(
                    {"message": "EMAIL_OR_PASSWORD_VALIDATION_ERROR"}, status=400
                )

            if not re.match(
                "^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[~₩!@#$%^&*()\-_=+])[a-zA-Z0-9~!@#$%^&*()_\-+=]{8,17}$",
                password,
            ):
                return JsonResponse(
                    {"message": "EMAIL_OR_PASSWORD_VALIDATION_ERROR"}, status=400
                )

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "DUPLICATION_ERROR"}, status=400)

            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({"message": "DUPLICATION_ERROR"}, status=400)

            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

            User.objects.create(
                email=email,
                password=hashed_password,
                nickname=nickname,
                nation=nation,
                is_receive_email=receive_email,
                login_method="libido",
            )

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=401)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)


class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data["email"]
            password = data["password"]

            user = User.objects.get(email=email)

            result = {
                "nickname": user.nickname,
                "profile_image_url": user.profile_image_url,
            }

            if not bcrypt.checkpw(
                password.encode("utf-8"), user.password.encode("utf-8")
            ):
                return JsonResponse(
                    {"message": "INVALID_USER_OR_INVALID_PASSWORD"}, status=401
                )

            access_token = jwt.encode(
                {"id": user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM
            )
            return JsonResponse(
                {"result": result, "ACCESS_TOKEN": access_token}, status=200
            )

        except User.DoesNotExist:
            return JsonResponse({"message": "USER_DOES_NOT_EXISTS"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=401)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)


class ResetPasswordView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data["email"]
            password = data["password"]
            re_password = data["re_password"]
            reset_token_number = data["reset_token_number"]

            user = User.objects.get(email=email)

            if password != re_password:
                return JsonResponse({"message": "PASSWORD_MISMATCH_ERROR"}, status=400)

            if not re.match(
                "^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[~₩!@#$%^&*()\-_=+])[a-zA-Z0-9~!@#$%^&*()_\-+=]{8,17}$",
                password,
            ):
                return JsonResponse(
                    {"message": "PASSWORD_VALIDATION_ERROR"}, status=400
                )

            if user.reset_token_number != reset_token_number:
                return JsonResponse({"message": "RESET_TOKEN_VALIDATION_ERROR"})

            user.password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            user.save()

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"message": "USER_DOES_NOT_EXISTS"}, status=401)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)


class GoogleSignInView(View):
    def get(self, request):
        try:
            access_token = request.headers["Authorization"]

            if access_token == "":
                return JsonResponse({"message": "VALUES_ERROR"}, status=401)

            user_info_response = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            user_info = user_info_response.json()

            sub = user_info.get("sub")
            email = user_info.get("email")
            name = user_info.get("name")
            login_method = "google"

            if sub == None or email == None or name == None:
                return JsonResponse({"message": "VALUES_ERROR"}, status=401)

            obj, created = User.objects.get_or_create(
                email=email, nickname=name, platform_id=sub, login_method=login_method
            )

            status_code = 201 if created else 200

            results = {
                "platform_id": obj.platform_id,
                "email": obj.email,
                "nickname": obj.nickname,
            }

            jwt_payload = {"id": obj.platform_id}
            access_token = jwt.encode(
                jwt_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
            )

            return JsonResponse(
                {"results": results, "access_token": access_token}, status=status_code
            )

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class NaverSignInView(View):
    def get(self, request):
        try:
            access_token = request.headers["Authorization"]

            if access_token == "":
                return JsonResponse({"message": "VALUES_ERROR"}, status=401)

            user_info_response = requests.get(
                "https://openapi.naver.com/v1/nid/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            user_info = user_info_response.json()

            if (
                user_info["response"]["id"] == ""
                or user_info["response"]["email"] == ""
                or user_info["response"]["name"] == ""
            ):
                return JsonResponse({"message": "VALUES_ERROR"}, status=401)

            id = user_info["response"]["id"]
            email = user_info["response"]["email"]
            name = user_info["response"]["name"]
            login_method = "naver"

            obj, created = User.objects.get_or_create(
                email=email, nickname=name, platform_id=id, login_method=login_method
            )

            status_code = 201 if created else 200

            results = {
                "platform_id": obj.platform_id,
                "email": obj.email,
                "nickname": obj.nickname,
            }

            jwt_payload = {"id": obj.platform_id}
            access_token = jwt.encode(
                jwt_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
            )

            return JsonResponse(
                {"results": results, "access_token": access_token}, status=status_code
            )

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, safe=False, status=400)


class UserFollowView(View):
    @login_required
    def get(self, request):
        user = request.user
        OFFSET = int(request.GET.get("offset", 0))
        LIMIT = int(request.GET.get("display", 8))

        follows = Follow.objects.filter(users_id=user.id).select_related(
            "users", "followed"
        )
        friends = [follow.followed for follow in follows][OFFSET : OFFSET + LIMIT]

        result = [
            {
                "id": friend.id,
                "nickname": friend.nickname,
                "image_url": friend.profile_image_url,
                "follows": friend.follow_by_users.all().count(),
            }
            for friend in friends
        ]

        return JsonResponse({"message": result}, status=200)

    @login_required
    def post(self, request):
        friend_id = json.loads(request.body)["friend_id"]

        follow_obj, created = Follow.objects.get_or_create(
            users_id=request.user.id, followed_id=friend_id
        )

        if not created:
            follow_obj.delete()
            return JsonResponse({"message": "FOLLOW_LIST_DELETE_SUCCESS"}, status=200)

        return JsonResponse({"message": "FOLLOW_LIST_CREATE_SUCCESS"}, status=201)


class UserHistoryView(View):
    @login_required
    def get(self, request):
        histories = (
            UserRoomHistory.objects.filter(users=request.user)
            .select_related("rooms", "rooms__room_categories")
            .prefetch_related("rooms__rooms_contents")
        )

        if not histories:
            return JsonResponse({"message": "USER_HISTORY_DOES_NOT_EXISTS"}, status=404)

        result = [
            {
                "id": history.rooms.id,
                "title": history.rooms.title,
                "thumbnails_url": history.rooms.rooms_contents.all()[0].thumbnails_url,
                "description": history.rooms.description,
                "is_public": history.rooms.is_public,
                "room_categories": history.rooms.room_categories.name,
            }
            for history in histories
        ]

        return JsonResponse({"message": result}, status=200)

    @login_required
    def post(self, request):
        room_id = json.loads(request.body)["room_id"]
        obj, created = UserRoomHistory.objects.update_or_create(
            rooms_id=room_id, users_id=request.user.id
        )

        if created:
            return JsonResponse({"message": "HISTORY_CREATE_SUCCESS"}, status=200)

        return JsonResponse({"message": "HISTORY_UPDATE_SUCCESS"}, status=200)


class UserProfileView(View):
    @login_required
    def get(self, request):
        user = User.objects.get(id=request.user.id)

        result = {
            "profile_image_url": user.profile_image_url,
            "nickname": user.nickname,
            "email": user.email,
            "description": user.description,
            "is_receive_email": user.is_receive_email,
            "nation": user.nation,
        }

        return JsonResponse({"result": result}, status=201)

    @login_required
    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)

            image = request.FILES.get("filename")
            nickname = request.POST.get("nickname")
            nation = request.POST.get("nation")
            receive_email = request.POST.get("is_receive_email")
            description = request.POST.get("description")

            if nickname != None:
                if User.objects.filter(nickname=nickname).exists():
                    return JsonResponse({"message": "DUPLICATION_NICKNAME"}, status=400)
                user.nickname = nickname
                user.save()

            if nickname == "":
                return JsonResponse({"message": "VALUES_ERROR"}, status=400)

            if nation != None:
                user.nation = nation
                user.save()

            if receive_email != None:
                user.nation = receive_email
                user.save()

            if description != None:
                user.description = description
                user.save()

            if image != None:
                upload_key = str(uuid.uuid4().hex[:10]) + image.name

                s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=settings.AWS_IAM_ACCESS_KEY,
                    aws_secret_access_key=settings.AWS_IAM_SECRET_KEY,
                )

                file = user.profile_image_url[56:]
                s3_client.delete_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file
                )

                upload_key = unicodedata.normalize("NFC", upload_key)

                s3_client.upload_fileobj(
                    image,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    upload_key,
                    ExtraArgs={"ContentType": image.content_type},
                )

                profile_image_url = (
                    "https://libido-test-dev.s3.ap-northeast-2.amazonaws.com/"
                    + upload_key
                )

                user.profile_image_url = profile_image_url
                user.save()

            result = {
                "nickname": user.nickname,
                "email": user.email,
                "nation": user.nation,
                "description": user.description,
                "profile_image_url": user.profile_image_url,
                "is_receive_email": user.is_receive_email,
            }

            return JsonResponse({"message": "SUCCESS", "result": result}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=401)


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    permission_classes = []
    renderer_classes = []
    serializer_action_classes = {
        "list": UserSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except KeyError:
            return UserSerializer

    @swagger_auto_schema(method="GET", responses={status.HTTP_200_OK: FollowSerializer})
    @action(methods=["GET"], detail=False, url_path="followers", permission_classes=[])
    def followers(self, request):
        user = request.user
        serializers = FollowSerializer(
            instance=user.followers, allow_null=True, many=True
        )
        return Response(serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_STRING, description="팔로우 할 유저 PK"
                ),
            },
        ),
        responses={status.HTTP_200_OK: FollowSerializer},
    )
    @action(methods=["POST"], detail=False, url_path="follow", permission_classes=[])
    def follow(self, request):
        followed_id = request.data["followed_id"]
        user_id = request.user.id
        follow = User.follow(user_id=user_id, followed_user_id=followed_id)
        serializers = FollowSerializer(instance=follow, allow_null=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_STRING, description="언팔로우 할 유저 PK"
                ),
            },
        ),
        responses={status.HTTP_200_OK: FollowSerializer},
    )
    @action(methods=["POST"], detail=False, url_path="unfollow", permission_classes=[])
    def unfollow(self, request):
        followed_id = request.data["followed_id"]
        user_id = request.user.id
        User.unfollow(user_id=user_id, followed_user_id=followed_id)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
