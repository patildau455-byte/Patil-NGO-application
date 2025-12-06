from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Banner(db.Model):
    __tablename__ = "banners"
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    display_order = db.Column(db.Integer, default=0)
    status = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "title": self.title,
            "description": self.description,
            "display_order": self.display_order,
            "status": self.status
        }

class VisionMission(db.Model):
    __tablename__ = "vision_mission"
    id = db.Column(db.Integer, primary_key=True)
    vision_title = db.Column(db.String(150))
    vision_description = db.Column(db.String(200))
    mission_title = db.Column(db.String(150))
    mission_description = db.Column(db.String(200))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "vision_title": self.vision_title,
            "vision_description": self.vision_description,
            "mission_title": self.mission_title,
            "mission_description": self.mission_description,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }

class Statistic(db.Model):
    __tablename__ = "statistic"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    value = db.Column(db.String(50))
    display_order = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default="active")

    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "value": self.value,
            "display_order": self.display_order,
            "status": self.status
        }

class Initiative(db.Model):
    __tablename__ = "initiatives"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    image_url = db.Column(db.String(150))
    display_order = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default="active")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,
            "display_order": self.display_order,
            "status": self.status
        }
