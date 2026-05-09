from marshmallow import Schema, fields, validate

class SensorReadingSchema(Schema):
    sensor_id = fields.String(
        required=True,
        validate=validate.Length(min=36),
        description="UUID датчика (минимум 36 символов)"
    )
    value = fields.Float(
        required=True,
        description="Значение измерения"
    )
    timestamp = fields.DateTime(
        required=True,
        description="Время измерения в ISO формате (например, 2026-01-20T12:00:00Z)"
    )
    location = fields.Dict(
        keys=fields.Str(),
        values=fields.Float(),
        required=True,
        description="Геолокация: {'lat': широта, 'lon': долгота}"
    )