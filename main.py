from flask import Flask,abort
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# validation 
userPutArgs = reqparse.RequestParser()
userPutArgs.add_argument("name",type=str, help="String name is required")
userPutArgs.add_argument("gender",type=str, help="String gender is required")
userPutArgs.add_argument("age",type=int, help="int age is required")

names = {"colin":{"age":19, "gender":"male"},
         "bill":{"age":70, "gender":"male"}}

#inherits from resource
def aborty():
    abort(404,description="Could not find user")
class Users(Resource):
    #overwrite get ()
    def get(self,name):
        if name not in names:
            aborty()
        return names[name]
    def put(self,name):
        if name != '':
            args = userPutArgs.parse_args()
            names[args['name']] = {"gender":args["gender"],"age":args['age']}
            return args, 201
        return {"error":"broke"}
    def delete(self,name):
        del names[name]
        return '',204

# add resource to api with endpoint /api/users
api.add_resource(Users,"/api/users/<string:name>")

if __name__ =="__main__":
    app.run(debug=True)
