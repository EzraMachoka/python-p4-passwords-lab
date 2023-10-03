#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username'],
            password_hash=json['password']
        )
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201
    def post(self):
        json = request.get_json()
        username = json.get('username')
        password = json.get('password')
        
        if not username or not password:
            return {'message': 'Both username and password are required'}, 400

        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'message': 'Username already exists'}, 400

        
        user = User(username=username)
        user.password_hash = password  
        db.session.add(user)
        db.session.commit()

        
        session['user_id'] = user.id

        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
        return {}, 204  

class Login(Resource):
    def post(self):
        json_data = request.get_json()
        print(f'json_data: {json_data}')  
        username = json_data.get('username')
        print(f'username: {username}')    
        password = json_data.get('password')

        


class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {'message': '204: No Content'}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
