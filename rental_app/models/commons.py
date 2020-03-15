"""
This file contains commons models
"""
from datetime import datetime

import sqlalchemy as sa
from rental_app import db
from rental_app.tools.commons import descripted_exception_logger


class BaseModel(db.Model):  # pragma: no cover
    """
    This class is the abstract model that inherited from other model
    """

    __abstract__ = True

    id = sa.Column(sa.Integer(), primary_key=True)
    created_at = sa.Column(
        sa.DateTime(),
        default=sa.func.now(),
        server_default=sa.func.now(),
        nullable=False,
    )
    updated_at = sa.Column(
        sa.DateTime(),
        default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )
    is_deleted = sa.Column(sa.Boolean(), default=False, server_default="false")
    deleted_at = sa.Column(sa.DateTime(), default=None)

    def __str__(self):
        if hasattr(self, "uuid"):
            return f"{self.__class__.__name__} <id: {self.id} {self.uuid}>"
        else:
            return "%s object (%s)" % (self.__class__.__name__, self.id)

    def save(self) -> "BaseModel":
        """
        This method used to add new record to table or update existing record

        Returns:
            [BaseModel] -- [The model object]
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self

        except Exception as e:
            db.session.rollback()
            descripted_exception_logger(e)
            raise

    def add_flush(self) -> "BaseModel":
        """
        This method similar with save, but use flush method of sqlalchemy instead of commit

        Returns:
            [BaseModel] -- [The model object]
        """
        try:
            db.session.add(self)
            db.session.flush()
            return self

        except Exception as e:
            db.session.rollback()
            descripted_exception_logger(e)
            raise

    def delete(self) -> "BaseModel":
        """
        This method used to mark the record to deleted

        Returns:
            [BaseModel] -- [The model object]
        """
        try:
            self.is_deleted = True
            self.deleted_at = datetime.now()

            db.session.add(self)
            db.session.commit()
            return self

        except Exception as e:
            db.session.rollback()
            descripted_exception_logger(e)
            raise
