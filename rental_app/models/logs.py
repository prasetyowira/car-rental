import sqlalchemy as sa

from rental_app import db
from rental_app.models.commons import BaseModel


class Log(BaseModel):
    __tablename__ = "rental_app_logs"

    car_id = db.Column(db.Integer, sa.ForeignKey('rental_app_cars.id'), nullable=False)
    customer_name = db.Column(db.String(255), nullable=False)
    rent_date = db.Column(db.Date)
    inquiry_at = db.Column(
        sa.DateTime(),
        default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )
    has_settled = sa.Column(sa.Boolean(), default=False, server_default="false")
