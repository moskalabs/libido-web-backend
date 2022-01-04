```

개발 환경으로 도커 실행

docker-compose --env-file .env.dev config

docker-compose --env-file .env.dev up -d --build

운영환경으로 도커 실행

docker-compose --env-file .env.prd up -d --build

```
