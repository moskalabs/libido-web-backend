from .base import *


if "DATABASE_HOST" in os.environ:
    # Running the Docker image with configs
    DATABASES["default"]["ENGINE"] = os.getenv("DATABASE_ENGINE")
    DATABASES["default"]["HOST"] = os.getenv("DATABASE_HOST")
    DATABASES["default"]["PORT"] = os.getenv("DATABASE_PORT")
    DATABASES["default"]["NAME"] = os.getenv("DATABASE_NAME")
    DATABASES["default"]["USER"] = os.getenv("DATABASE_USER")
    DATABASES["default"]["PASSWORD"] = os.getenv("DATABASE_PASSWORD")
    DATABASES["default"]["OPTIONS"] = {
        "charset": "utf8mb4",  # prevent 1366, "Incorrect string value: '\\xEC\\x82\\xAC\\xEC\\x9A\\xA9...' for colum
    }

AWS_IAM_ACCESS_KEY = os.environ["AWS_IAM_ACCESS_KEY"]
AWS_IAM_SECRET_KEY = os.environ["AWS_IAM_SECRET_KEY"]
AWS_S3_REGION_NAME = os.environ["AWS_S3_REGION_NAME"]
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]

# EMAIL
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = os.environ["EMAIL_PORT"]
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]


SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
YOUTUBE_DATA_API_KEY = os.environ["YOUTUBE_DATA_API_KEY"]

EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# S3

AWS_S3_CUSTOM_DOMAIN = (
    f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
)
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_LOCATION = "static"

AWS_DEFAULT_ACL = "public-read"

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = "http://%s/static/" % AWS_S3_CUSTOM_DOMAIN
MEDIA_ROOT = os.path.join(AWS_S3_CUSTOM_DOMAIN, "libido")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}
