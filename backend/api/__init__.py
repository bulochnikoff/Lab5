from flask_restx import Api

api = Api(
    version='1.0',
    title='Research Dashboard API',
    description='API для интеграции научных данных',
    doc='/api/docs/'
)

# Импортируем и регистрируем namespace для сенсоров
from api.v1.sensors import ns as sensors_ns
api.add_namespace(sensors_ns, path='/api/v1/sensors')

# Импортируем и регистрируем namespace для ML-моделей
from api.v1.models import ns as models_ns
api.add_namespace(models_ns, path='/api/v1/models')