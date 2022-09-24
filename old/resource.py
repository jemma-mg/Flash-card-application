from flask_restful import Api, Resource, abort, fields, marshal,reqparse
from flask_security import auth_required, current_user
from flask import request
from models import db, User as users_model
from models import Decks,Cards,Review
from datetime import datetime
api = Api(prefix="/api")

deck_parser = reqparse.RequestParser()
deck_parser.add_argument('Deckdescription')
deck_parser.add_argument('Deckname')
card_parser = reqparse.RequestParser()
card_parser.add_argument('Carddescription')
card_parser.add_argument('Cardname')
review_parser = reqparse.RequestParser()
review_parser.add_argument('Deckname')
review_parser.add_argument('Score')

deck_resource_fields={
    "r_id": fields.Integer,
    "r_user":fields.String,
    "r_deck":fields.String,
    "r_time":fields.String,
    "r_score":fields.Integer,
}

deck_resource_fields={
    "d_id": fields.Integer,
    "d_user":fields.String,
    "d_name":fields.String,
    "d_description":fields.String,
}
card_resource_fields={
    "c_id": fields.Integer,
    "c_deck": fields.Integer,
    "c_user":fields.Integer,
    "c_name":fields.String,
    "c_description":fields.String,
}



class Deck(Resource):
    @auth_required('token')
    def get(self):
            deck_exists=db.session.query(Decks).filter(Decks.d_user==current_user.id).all()
            if(deck_exists):
                return marshal(deck_exists, deck_resource_fields)
            else:
                abort(404, message='No Decks Yet')
    @auth_required('token')
    def delete(self,d_id):
        deck=db.session.query(Decks).filter(Decks.d_id==d_id).first()
        db.session.delete(deck)
        db.session.commit()
        return 200
    @auth_required('token')
    def post(self):
        args=deck_parser.parse_args()
        name=args.get('Deckname')
        desc=args.get('Deckdescription')
        deck_exists=db.session.query(Decks).filter(Decks.d_name==name,Decks.d_description==desc).first()
        if deck_exists:
            return {"error_code":'003',"error_message":"Deck_name exists"},409
        else:
            newdeck=Decks(d_user=current_user.id,d_name=name,d_description=desc)
            db.session.add(newdeck)
            db.session.commit()
            return {"message":"Operation_Completed"},201
    @auth_required('token')
    def patch(self,d_id):
        args=deck_parser.parse_args()
        name=args.get('Deckname')
        desc=args.get('Deckdescription')
        updateddeck=db.session.query(Decks).filter(Decks.d_id==d_id).update({Decks.d_name:name,Decks.d_description:desc});
        db.session.commit();
        return {"d_id":d_id , "d_name":name,"d_description":desc},200

        

class Card(Resource):
    @auth_required('token')
    def get(self,id):
            card_exists=db.session.query(Cards).filter(Cards.c_user==current_user.id,Cards.c_deck==id).all()
            if(card_exists):
                return marshal(card_exists, card_resource_fields)
            else:
                abort(404, message='No Cards Yet')
    @auth_required('token')
    def patch(self,id):
        args=card_parser.parse_args()
        name=args.get('Cardname')
        desc=args.get('Carddescription')
        updatedcard=db.session.query(Cards).filter(Cards.c_user==current_user.id,Cards.c_id==id).update({Cards.c_name:name,Cards.c_description:desc});
        db.session.commit();
        return {"c_id":id , "c_name":name,"c_description":desc},200
    @auth_required('token')
    def delete(self,id):
        card=db.session.query(Cards).filter(Cards.c_id==id).first()
        db.session.delete(card)
        db.session.commit()
        return 200
    @auth_required('token')
    def post(self,id):
        args=card_parser.parse_args()
        name=args.get('Cardname')
        desc=args.get('Carddescription')
        deck_exists=db.session.query(Cards).filter(Cards.c_user==current_user.id,Cards.c_deck==id,Cards.c_name==name,Cards.c_description==desc).first()
        if deck_exists:
            return {"error_code":'003',"error_message":"Card_name exists"},409
        else:
            newcard=Cards(c_deck=id,c_user=current_user.id,c_name=name,c_description=desc)
            db.session.add(newcard)
            db.session.commit()
            return {"message":"Operation_Completed"},201  

class Reviewt(Resource):
    def post(self):
        args=review_parser.parse_args()
        name=args.get('Deckname')
        score=args.get('Score')
        time=datetime.now()
        newdeck=Review(r_user=current_user.id,r_deck=name,r_time=time,r_score=score)
        db.session.add(newdeck)
        db.session.commit()
        return {"message":"Operation_Completed"},201

            

api.add_resource(Deck, '/deck','/deck/<string:d_id>','/deck/post')
api.add_resource(Card, '/card/<string:id>','/card/post/<string:id>' )
api.add_resource(Reviewt,'/review')

