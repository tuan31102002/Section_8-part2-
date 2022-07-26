import sqlite3
from flask import jsonify, request
from flask_restful import Resource,reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.item import ItemModel


class Item(Resource):
    # @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'messages' : 'Item not found'}

          # item = next(filter(lambda x : x['name'] == name , items), None)
        # for item in items:
        #     if item['name'] == name :
        #         return {'item' : item}
        #     else:
        #         None 

    
    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message' : "An item with name '{}' already exists" .format(name)}

        data = request.get_json()
        # item = {
        #     'name' : name,
        #     'price': data['price']
        # }
        item = ItemModel(name, data['price'] ,data['store_id'])
        try:
            # ItemModel.insert(item)
            item.save_to_db()
        except:
            return {'message' : 'An error occurerd inserting the item'}

        return item.json()

        # if next(filter(lambda x : x['name'] == name,items) , None):
        #     return {'message' : "An item with name '{}' aleady exis " . format(name)}
        
        # for x in items :
        #     if x['name'] == name:
        #         return {'message' : "An item with name '{}' aleady exis" .format(name)}
        #     else :
        #         data = request.get_json()
        #         item = {
        #             'name' : name , 
        #             'price' : data['price']
        #         }
        #         items.append(item)
        #         return item

    # @jwt_required
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item :
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404
        # connection = sqlite3.connect('data.sqlite')
        # cursor = connection.cursor()

        # query = "DELETE FROM items WHERE name=:name"
        # cursor.execute(query,{"name":name})

        # connection.commit()
        # connection.close()
        
        # return {'message' : ' Item deleted'}

        # <----------------------------------->
        # global item
        # items = list(filter(lambda x : x['name'] != name , items) )
        # return {'message' : ' Item deleted'}

    # @jwt_required
    def put(self,name):
        # parser = reqparse.RequestParser()
        # parser.add_argument('price',type = float , required = True , help = "the price is not null")
        # data = parser.parse_args()
        data = request.get_json() #nhap du lieu
        item = ItemModel.find_by_name(name)
        # update_item = {
        #     'name' : name,
        #     'price' : data['price']
        # }
        if item is None :
            item = ItemModel(name , data['price'] ,data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()



        # <--------------------------------------->
        # update_item = ItemModel(name , data['price'])
        # if item is None :
        #     try:
        #         update_item.insert()
        #     except:
        #         return {"message" : "insert errors"}
        # else :
        #     try:
        #         update_item.update()
        #     except:
        #         return {"message" : "update errors"}
        # return update_item.json()

class ItemList(Resource):
    @jwt_required()
    def get(self):
                
        
        return {'items' : [x.json() for x in ItemModel.query.all()]}




        # connection = sqlite3.connect('data.sqlite')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items =[]
        # for row in result:
        #     items.append({'id' : row[0],'name' : row[1], 'price' : row[2]})

        # connection.close()

        # return {'items' : items}

        # if row:
        #     return {'items' : {'item' : {'name' : row[0],'price' : row[1]}}}
        # return {'messages' : 'Item not found'}


