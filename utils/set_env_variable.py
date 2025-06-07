import os
import json

env_json = os.getenv('CryptoPaymentGateway-prod')
if os.getenv('PY_ENV') == 'PROD' and not env_json:
    raise Exception("Env variables are not present.")

if not env_json:
    # Dev/local fallback only!
    env = {
            "DATABASE_USER": "root",
            "DATABASE_PASSWORD": "r#$WedY$#nS@526",
            "engine": "mysql",
            "DATABASE_HOST": "mysql-april7-test-database.cfssa1sbzchp.eu-west-1.rds.amazonaws.com",
            "DATABASE_PORT": 3306,
            "DATABASE_NAME": "crypto_payment_gateway_v1",
            "FERNET_ENCRYPTION_KET":"cDVJejZXSUdpYTZpV1lBTE5JTWVndG16aFctSkZsaUwweEtkM21XeWdDOD0=" 
    }
else:
    env = json.loads(env_json)

ENV_VAR = env