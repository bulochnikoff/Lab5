from flask_restx import Namespace, Resource, fields
from flask import request

ns = Namespace('models', description='ML модели для прогнозирования')

# Модель входных данных для Swagger
input_model = ns.model('PredictInput', {
    'features': fields.List(fields.Float, required=True, description='Признаки для предсказания', example=[1.0, 2.5, 3.2])
})

# Модель выходных данных
output_model = ns.model('PredictOutput', {
    'prediction': fields.Float(description='Результат предсказания'),
    'status': fields.String(description='Статус')
})

@ns.route('/predict')
class Predict(Resource):
    @ns.expect(input_model)
    @ns.response(200, 'Успешно', output_model)
    @ns.response(400, 'Ошибка в данных')
    def post(self):
        """
        Получить предсказание на основе признаков
        (сейчас заглушка — сумма признаков)
        """
        data = request.get_json()
        if not data or 'features' not in data:
            return {"error": "Поле 'features' обязательно"}, 400
        features = data['features']
        if not isinstance(features, list):
            return {"error": "features должен быть списком чисел"}, 400
        
        # Заглушка
        prediction = sum(features)
        
        return {
            "prediction": prediction,
            "status": "success"
        }, 200