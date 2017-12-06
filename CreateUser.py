from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask.ext.mysql import MySQL

mySql =MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Your_Database_Password'
app.config['MYSQL_DATABASE_DB'] = 'Your_Database_Name'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mySql.init_app(app)
api = Api(app)

class CreateUser(Resource):
	#@app.route('/CreateUser', methods=['POST'])
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('FIRST_NAME', type=str, help = 'Enter First Name')
			parser.add_argument('MIDDLE_NAME', type=str, help = 'Enter Middle Name')
			parser.add_argument('LAST_NAME', type=str, help = 'Enter Last Name')
			parser.add_argument('USERNAME', type=str, help = 'Enter Username')
			args = parser.parse_args()

			_userFirstName = args['FIRST_NAME']
			_userMiddleName = args['MIDDLE_NAME']
			_userLastName = args['LAST_NAME']
			_userUsername = args['USERNAME']

			conn = mySql.connect()
			cursor = conn.cursor()
			cursor.callproc('User_Details_Actions_Post_Info',(_userFirstName, _userMiddleName, _userLastName, _userUsername))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				return {'Status_Code' : '200', 'Message' : 'User Created'}
			else:
				return {'Status_Code' : '1000', 'Message' : str(data[0])}

			return {'Email' : args['email'], 'Password' : args['password']}
		except Exception as e:
			return {'error' : str(e)}


class GetItemsByID(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('ID',type=str)
			args = parser.parse_args()

			_userID = args['ID']
			conn = mySql.connect()
			cursor = conn.cursor()
			cursor.callproc('User_Details_Report_RetrieveList',(_userID))
			data = cursor.fetchall()

			items_list = []
			for item in data:
				i = {'ID' : item[0], 'First Name' : item[1], 'Middle Name' : item[2], 'Last Name' : item[3], 'Username': item[4] }
				items_list.append(i)

			return {'status code' : '200', 'UserDetailsByID' : items_list}


		except Exception as e:
			return {'error': str(e)}


class GetAllItems(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('ID',type=str)
			args = parser.parse_args()

			_userID = args['ID']
			conn = mySql.connect()
			cursor = conn.cursor()
			cursor.callproc('User_Details_Report_RetrieveDetails',(_userID))
			data = cursor.fetchall()

			items_list = []
			for item in data:
				i = {'ID' : item[0], 'First Name' : item[1], 'Middle Name' : item[2], 'Last Name' : item[3], 'Username': item[4] }
				items_list.append(i)

			return {'status code' : '200', 'UserList' : items_list}


		except Exception as e:
			return {'error': str(e)}


api.add_resource(CreateUser, '/CreateUser')
api.add_resource(GetItemsByID, '/GetItemsByID')
api.add_resource(GetAllItems, '/GetAllItems')

if __name__ == '__main__':
	cu=CreateUser()
	cu.post()
	app.run(debug = True)
