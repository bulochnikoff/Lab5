from flask_restx import Namespace, Resource, fields
from flask import request
from api.v1.schemas import SensorReadingSchema
from api import api

ns = Namespace('sensors', description='Операции с датчиками')

reading_model = ns.model('Reading', {
    'sensor_id': fields.String(required=True, min_length=36, description='UUID датчика'),
    'value': fields.Float(required=True, description='Значение измерения'),
    'timestamp': fields.DateTime(required=True, description='Время измерения (ISO)'),
    'location': fields.Nested(ns.model('Location', {
        'lat': fields.Float(required=True),
        'lon': fields.Float(required=True)
    }), required=True, description='Геолокация')
})

@ns.route('/readings')
class Readings(Resource):
    @ns.expect(reading_model)
    @ns.response(201, 'Успешно добавлено')
    @ns.response(400, 'Ошибка валидации')
    def post(self):
        from database import db, SensorReading
        import datetime
        data = request.json
        schema = SensorReadingSchema()
        errors = schema.validate(data)
        if errors:
            return {"errors": errors}, 400
        
        reading = SensorReading(
            sensor_id=data['sensor_id'],
            value=data['value'],
            timestamp=datetime.datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00')),
            lat=data['location']['lat'],
            lon=data['location']['lon']
        )
        db.session.add(reading)
        db.session.commit()
        return {"status": "success", "data": data}, 201

    def get(self):
        from database import SensorReading
        readings = SensorReading.query.all()
        return [r.to_dict() for r in readings], 200

@ns.route('/test')
class Test(Resource):
    def get(self):
        return {"message": "sensors blueprint works"}