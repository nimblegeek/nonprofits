from app import db
from datetime import datetime
from sqlalchemy import or_

class Municipality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    organizations = db.relationship('Organization', backref='municipality', lazy=True)

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    website = db.Column(db.String(200))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    municipality_id = db.Column(db.Integer, db.ForeignKey('municipality.id'), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def search(cls, search_term=None, municipality_id=None, approved=True):
        query = cls.query
        
        if search_term:
            search_filter = or_(
                cls.name.ilike(f'%{search_term}%'),
                cls.description.ilike(f'%{search_term}%'),
                cls.email.ilike(f'%{search_term}%'),
                cls.address.ilike(f'%{search_term}%')
            )
            query = query.filter(search_filter)
        
        if municipality_id:
            query = query.filter_by(municipality_id=municipality_id)
            
        query = query.filter_by(approved=approved)
        
        return query.order_by(cls.name)
