from rental_app import db
from rental_app.enums import CarStatusStatus
from rental_app.models.commons import BaseModel


class Car(BaseModel):
    __tablename__ = "rental_app_cars"

    registration_number = db.Column(db.String(255), unique=True)
    color = db.Column(db.String(255), nullable=True)
    status = db.Column(
        db.Enum(CarStatusStatus, name="car_status"),
        nullable=False,
        default=CarStatusStatus.FREE,
    )
