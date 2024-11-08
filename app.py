import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

from models import Municipality, Organization
from forms import OrganizationForm

def seed_municipalities():
    municipalities = [
        "Stockholm", "Göteborg", "Malmö", "Uppsala", "Västerås", "Örebro", 
        "Linköping", "Helsingborg", "Jönköping", "Norrköping", "Lund", "Umeå",
        "Gävle", "Borås", "Södertälje", "Eskilstuna", "Halmstad", "Växjö",
        "Karlstad", "Sundsvall", "Östersund", "Trollhättan", "Luleå", "Kalmar",
        "Falun", "Skellefteå", "Karlskrona", "Kristianstad", "Skövde", "Uddevalla",
        "Botkyrka", "Nacka", "Örnsköldsvik", "Varberg", "Motala", "Enköping",
        "Nyköping", "Sandviken", "Trelleborg", "Landskrona", "Ängelholm", "Lidköping",
        "Piteå", "Gotland", "Norrtälje", "Falkenberg", "Karlskoga", "Ystad",
        "Kiruna", "Katrineholm"
    ]
    try:
        for name in municipalities:
            # Check if municipality already exists
            if not Municipality.query.filter_by(name=name).first():
                municipality = Municipality(name=name)
                db.session.add(municipality)
        db.session.commit()
        print("Successfully seeded municipalities")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding municipalities: {str(e)}")
        raise

@app.route('/')
def index():
    municipalities = Municipality.query.all()
    selected_municipality = request.args.get('municipality', type=int)
    query = Organization.query.filter_by(approved=True)
    
    if selected_municipality:
        query = query.filter_by(municipality_id=selected_municipality)
    
    organizations = query.all()
    return render_template('index.html', 
                         organizations=organizations,
                         municipalities=municipalities,
                         selected_municipality=selected_municipality)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = OrganizationForm()
    form.municipality_id.choices = [(m.id, m.name) for m in Municipality.query.all()]
    
    if form.validate_on_submit():
        org = Organization(
            name=form.name.data,
            description=form.description.data,
            website=form.website.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            municipality_id=form.municipality_id.data
        )
        db.session.add(org)
        db.session.commit()
        flash('Tack för din ansökan! Den kommer att granskas av en administratör.', 'success')
        return redirect(url_for('index'))
    
    return render_template('submit.html', form=form)

@app.route('/admin')
def admin():
    pending_organizations = Organization.query.filter_by(approved=False).all()
    return render_template('admin.html', organizations=pending_organizations)

@app.route('/approve/<int:org_id>', methods=['POST'])
def approve_organization(org_id):
    org = Organization.query.get_or_404(org_id)
    org.approved = True
    db.session.commit()
    flash('Organisation godkänd!', 'success')
    return redirect(url_for('admin'))

with app.app_context():
    db.create_all()
    seed_municipalities()
