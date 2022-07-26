from flask_jwt_extended import jwt_required
from models.store import StoreModel
from flask_restful import Resource

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message' : 'Store not found'}

    def post(self,name):
        if StoreModel.find_by_name(name) :
            return {'message' : "A store with name '{}' already exists" .format(name)}

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message' : "post error"}

        return store.json()

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store :
            store.delete_from_db()
            return {'message' : "Store deleted"}
        return {'message' : "Store not found"}


class StoreList(Resource):
    def get(self):
        return {'stores' : [x.json() for x in StoreModel.query.all()]}  