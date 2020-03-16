from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from rental_app import db
from rental_app.enums import CarStatusStatus
from rental_app.models.commons import BaseModel


class Car(BaseModel):
    __tablename__ = "rental_app_cars"

    registration_number = db.Column(db.String(255), unique=True)
    color = db.Column(db.String(255), nullable=True)
    rents = relationship("Log")

    @hybrid_property
    def today_status(self):
        rents = self.rents
        today = datetime.now().today()
        filtered_rent = list(filter(lambda x: x.rent_date == today, rents))
        if len(filtered_rent) > 0:
            return CarStatusStatus.RENTED
        return CarStatusStatus.FREE

    @hybrid_method
    def status(self, date):
        rents = self.rents
        today = datetime.strptime(date, "%Y-%m-%d").date()
        filtered_rent = list(filter(lambda x: x.rent_date == today, rents))
        if len(filtered_rent) > 0:
            return CarStatusStatus.RENTED
        return CarStatusStatus.FREE

    @hybrid_method
    def get_customer(self, date):
        rents = self.rents
        today = datetime.strptime(date, "%Y-%m-%d").date()
        filtered_rent = list(filter(lambda x: x.rent_date == today, rents))
        if len(filtered_rent) == 1:
            filtered_rent = filtered_rent.pop()
            if hasattr(filtered_rent, "customer_name"):
                return filtered_rent.customer_name
        return None

