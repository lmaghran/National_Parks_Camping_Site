from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# app= Flask(__name__)

db = SQLAlchemy()

class Campsite(db.Model):
    """Data model for a human."""

    __tablename__ = "campsite_info_tbl"

    facility_id= db.Column(db.Integer, primary_key=True)
    parent_rec_area_id= db.Column(db.Integer, db.ForeignKey('rec_area_tbl.rec_area_id'))
    campsite_name= db.Column(db.String(40))
    campsite_lat= db.Column(db.Float(15))
    campsite_long= db.Column(db.Float(15))
    campsite_json_latlong = db.Column(db.String(100))
    is_reservable = db.Column(db.Boolean())
    campsite_type = db.Column(db.String(100))
    campsite_description= db.Column(db.Text())


    def __repr__(self):
        return f"""<Id={self.facility_id}, FName={self.campsite_name}>"""

class Recreation_area(db.Model):

    __tablename__ = "rec_area_tbl"

    rec_area_id = db.Column(db.Integer, primary_key=True)
    rec_id_name = db.Column(db.String(5))
    rec_name= db.Column(db.String(40))
    rec_area_des= db.Column(db.Text())
    campsites=db.relationship("Campsite", 
              backref=db.backref("rec_area", order_by='Campsite.campsite_name'))


    def __repr__(self):
        return f"""<Rec_id={self.rec_area_id},Id_name={self.rec_id_name}>"""

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///npcamping'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


# db.create_all()

if __name__ == "__main__":

    from server import app
    connect_to_db(app)