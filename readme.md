For local test:
- clone repository
- fill project settings for smtp auth to make email notification work
- run 'docker-compose up' in root directory
- superuser: admin:admin

For production:
- clone repository
- fill project settings for smtp auth to make email notification work
- fill project settings SITE_NAME and SITE_PORT
- run 'docker-compose up -d' in root directory
- configure nginx