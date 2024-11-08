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
            if not Municipality.query.filter_by(name=name).first():
                municipality = Municipality(name=name)
                db.session.add(municipality)
        db.session.commit()
        print("Successfully seeded municipalities")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding municipalities: {str(e)}")
        raise

def seed_sample_organizations():
    samples = [
        {
            "name": "Rädda Barnen Stockholm",
            "description": "Arbetar för barns rättigheter genom utbildning, hälsovård och katastrofhjälp.",
            "municipality_id": 1,  # Stockholm
            "website": "https://example.com/radda-barnen",
            "email": "stockholm@example.org",
            "phone": "08-123 45 67",
            "address": "Landsvägen 39, 172 63 Sundbyberg",
            "approved": True
        },
        {
            "name": "Naturskyddsföreningen Göteborg",
            "description": "Sveriges största miljöorganisation som arbetar med klimat, hav, skog, miljögifter och jordbruk.",
            "municipality_id": 2,  # Göteborg
            "website": "https://example.com/naturskydd-gbg",
            "email": "goteborg@example.org",
            "phone": "031-711 22 33",
            "address": "Första Långgatan 28B, 413 27 Göteborg",
            "approved": True
        },
        {
            "name": "Stadsmissionen Malmö",
            "description": "Stödjer människor i utsatthet och arbetar för ett mänskligare samhälle för alla.",
            "municipality_id": 3,  # Malmö
            "website": "https://example.com/stadsmissionen-malmo",
            "email": "malmo@example.org",
            "phone": "040-664 22 40",
            "address": "Västergatan 2A, 211 21 Malmö",
            "approved": True
        },
        {
            "name": "Uppsala Kvinnojour",
            "description": "Erbjuder stöd och skydd till kvinnor och barn som utsätts för våld i nära relationer.",
            "municipality_id": 4,  # Uppsala
            "website": "https://example.com/uppsala-kvinnojour",
            "email": "uppsala@example.org",
            "phone": "018-10 10 49",
            "address": "Box 1852, 751 48 Uppsala",
            "approved": True
        },
        {
            "name": "Friluftsfrämjandet Västerås",
            "description": "Främjar ett aktivt friluftsliv och verkar för bevarande av naturområden.",
            "municipality_id": 5,  # Västerås
            "website": "https://example.com/friluft-vasteras",
            "email": "vasteras@example.org",
            "phone": "021-13 14 15",
            "address": "Vasagatan 12, 722 15 Västerås",
            "approved": True
        },
        {
            "name": "Djurens Rätt Örebro",
            "description": "Sveriges största djurrätts- och djurskyddsorganisation som arbetar för ett samhälle fritt från djurförtryck.",
            "municipality_id": 6,  # Örebro
            "website": "https://example.com/djurens-ratt-orebro",
            "email": "orebro@example.org",
            "phone": "019-611 29 33",
            "address": "Kungsgatan 23, 702 11 Örebro",
            "approved": True
        },
        {
            "name": "RFSL Linköping",
            "description": "Arbetar för att homosexuella, bisexuella, transpersoner och queera ska ha samma rättigheter och möjligheter som alla andra.",
            "municipality_id": 7,  # Linköping
            "website": "https://example.com/rfsl-linkoping",
            "email": "linkoping@example.org",
            "phone": "013-13 22 50",
            "address": "Ågatan 55, 582 22 Linköping",
            "approved": True
        },
        {
            "name": "BRIS Helsingborg",
            "description": "Barnens rätt i samhället - stödjer barn och unga genom chatt, telefon och mail.",
            "municipality_id": 8,  # Helsingborg
            "website": "https://example.com/bris-helsingborg",
            "email": "helsingborg@example.org",
            "phone": "042-10 20 30",
            "address": "Drottninggatan 7, 252 21 Helsingborg",
            "approved": True
        }
    ]
    
    try:
        for org_data in samples:
            if not Organization.query.filter_by(name=org_data["name"]).first():
                org = Organization(**org_data)
                db.session.add(org)
        db.session.commit()
        print("Successfully seeded sample organizations")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding sample organizations: {str(e)}")
        raise

@app.route('/')
def index():
    municipalities = Municipality.query.order_by(Municipality.name).all()
    selected_municipality = request.args.get('municipality', type=int)
    search_term = request.args.get('search', '').strip()
    
    organizations = Organization.search(
        search_term=search_term,
        municipality_id=selected_municipality
    )
    
    return render_template('index.html', 
                         organizations=organizations,
                         municipalities=municipalities,
                         selected_municipality=selected_municipality,
                         search_term=search_term)

@app.route('/organization/<int:org_id>')
def organization_details(org_id):
    org = Organization.query.get_or_404(org_id)
    if not org.approved:
        return redirect(url_for('index'))
    return render_template('organization.html', org=org)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = OrganizationForm()
    form.municipality_id.choices = [(m.id, m.name) for m in Municipality.query.order_by(Municipality.name).all()]
    
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
    search_term = request.args.get('search', '').strip()
    pending_organizations = Organization.search(
        search_term=search_term,
        approved=False
    )
    return render_template('admin.html', organizations=pending_organizations, search_term=search_term)

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
    seed_sample_organizations()