from flask import Flask,abort,request
from flask_restful import Api, Resource, reqparse
# mongo is for users collection
import mongo
# admin is for courses collection
import admin

app = Flask(__name__)
api = Api(app)

# validation 
newCourseArgs = reqparse.RequestParser()
newCourseArgs.add_argument("courseCode",type=str, help="String name is required", required=True)

newTaskArgs = reqparse.RequestParser()
newTaskArgs.add_argument("courseCode",type=str, help="String name is required", required=True)
newTaskArgs.add_argument("description",type=str, help="String description is required", required=True)
newTaskArgs.add_argument("dueDate",type=str, help="String dueDate is required", required=True)

removeTaskArgs = reqparse.RequestParser()
removeTaskArgs.add_argument("courseCode",type=str, help="String name is required", required=True)
removeTaskArgs.add_argument("description",type=str, help="String description is required", required=True)

newSubArgs = reqparse.RequestParser()
newSubArgs.add_argument("username",type=str, help="String username is required", required=True)
newSubArgs.add_argument("courseCode",type=str, help="String courseCode is required", required=True)


# convert mongodb cursors to dicts
def remove_id(data):
    del data['_id']

def cursorToList(data):
    output = []
    for d in data:
        remove_id(d)
        output.append(d)
    return output

def commonGet(key):
    course = request.args.get('courseCode')
    if course == None:
        return {"error":"please provide a course param"}, 400
    data = admin.getCourse(course)
    arr = cursorToList(data)
    if len(arr) > 0:
        # there should be only one course in arr
        output= arr[0]
        return output[key]
    return {"error":"courseCode is invalid"}, 400


class ManageUUsers(Resource):
    def get(self):
        user = request.args.get('username')
        if user == None:
            return {"error":"please provide a username param"}, 400
        data = mongo.getUser(user)
        if data != None:
            remove_id(data)
            print(data)
            return data
        return {"error":"username is invalid"}, 400

class ManageUCourses(Resource):
    def get(self):
        #URL?courseCode=cscb36
        #use & for additonal parameters
        courseCode = request.args.get('courseCode')
        if courseCode == None:
            return {"error":"please provide a courseCode param"}, 400
        # convert Mongodb cursor to array
        data = admin.getCourse(courseCode)
        arr = cursorToList(data)
        if len(arr)>0:
            print(arr)
            return arr, 200
        return {"error":"courseCode is invalid"}, 400

    def post(self):
        # validate args
        args = newCourseArgs.parse_args()
        try:
            admin.createCourse(args['courseCode'])
            return {"message":args['courseCode']+" succesfully created"}, 200
        except:
            return {"error":"failed to create "+args['courseCode']}, 500

    def delete(self):
        args = newCourseArgs.parse_args()
        try:
            admin.removeCourse(args['courseCode'])
            return {"message":args['courseCode']+" succesfully removed"}, 200
        except:
            return {"error":"failed to remove "+args['courseCode']}, 500

class ManageUCourseTasks(Resource):
    def get(self):
        return commonGet('tasks')

    def post(self):
        # validate args
        args = newTaskArgs.parse_args()
        try:
            admin.addTask(args['courseCode'],args['description'], args['dueDate'])
            return {"message":args['description']+" succesfully added to "+args['courseCode']}, 200
        except:
            return {"error":"failed to add task "+args['description']+" to "+args['courseCode']}, 500

    def delete(self):
        args = removeTaskArgs.parse_args()
        try:
            admin.removeTask(args['courseCode'],args['description'])
            return {"message":args['description']+" succesfully removed from "+args['courseCode']}, 200
        except:
            return {"error":"failed to remove "+args['description']+" from "+args['courseCode']}, 500

    def put(self):
        args = newTaskArgs.parse_args()
        try:
            # this only changes the dueDate
            admin.editTask(args['courseCode'],args['description'], args['dueDate'])
            return {"message":"successfully changed due date for "+args['description']+" "+args['courseCode']}, 200
        except:
            return {"error":"failed to change due date for "+args['description']+" "+args['courseCode']}, 500

class ManageUCourseSubs(Resource):
    def get(self):
        return commonGet('subscribers')

    # FIX ID problem for Subscribe

    def post(self):
         # validate args
        args = newSubArgs.parse_args()
        try:
            admin.subscribe(args['username'],args['courseCode'])
            return {"message":args['username']+" succesfully subscribed to "+args['courseCode']}, 200
        except:
            return {"error":"failed to subscribe "+args['username']+" to "+args['courseCode']}, 500

    # FIX ID problem for UnSubscribe

    def delete(self):
        args = newSubArgs.parse_args()
        try:
            admin.unsubscribe(args['username'],args['courseCode'])
            return {"message":args['username']+" succesfully unsubscribed from "+args['courseCode']}, 200
        except:
            return {"error":"failed to unsubscribe "+args['username']+" from "+args['courseCode']}, 500



# End points
api.add_resource(ManageUUsers,"/api/manageu/users")
api.add_resource(ManageUCourses,"/api/manageu/courses")
api.add_resource(ManageUCourseTasks,"/api/manageu/courses/tasks")
api.add_resource(ManageUCourseSubs,"/api/manageu/courses/subscribers")

if __name__ =="__main__":
    app.run(debug=True)
