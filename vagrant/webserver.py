from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def renderRestaurants(self):
	output = ""
	output += "<html><body>"
	output += "<a href='/restaurants/new'>Make a New Restaurant Here:</a></br>"
	for restaurant in session.query(Restaurant).all():
		output += restaurant.name
		output += "</br>"
		output += "<a href='/restaurants/%s/edit'>Edit</a></br>" % str(restaurant.id)
		output += "<a href="'/restaurants/%s/delete'">Delete</a></br></br>" % str(restaurant.id)
	output += "</body></html>"
	self.wfile.write(output)
	print output
	return

def getId(path):
	segs = path.split("/")
	id = segs[-2]
	return id


class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith('/restaurants'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				renderRestaurants(self)
			elif self.path.endswith('/edit'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				id = getId(self.path)
				restaurant = session.query(Restaurant).filter_by(id=id).one()
				name = restaurant.name
				print name, id
				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype='multipart/form-data' action='restaurants/%s/edit'>" % str(id)
				output += "<h1>%s</h1>" % name
				output += "<input name='message' type='text' placeholder ='%s'>" % name
				output += "<input type='submit' value='Rename'> </form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
			elif self.path.endswith('delete'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				id = getId(self.path)
				restaurant = session.query(Restaurant).filter_by(id=id).one()
				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype='multipart/form-data' action='restaurants/%s/delete'>" % str(id)
				output += "<h1>Are you sure you want to delete %s?</h1>" % restaurant.name
				output += "<input type='submit' value='Delete'> </form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
			elif self.path.endswith('restaurants/new'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
				output += "<h1>Make A New Restaurant</h1>"
				output += "<input name='message' type='text' placeholder ='New Restaurant Name'>"
				output += "<input type='submit' value='Create'> </form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith('/restaurants/new'):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == "multipart/form-data":
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')[0]
				restaurant = Restaurant(name=messagecontent)
				session.add(restaurant)
				session.commit()
				self.send_response(301)
				self.send_header("Content-type", "text/html")
				self.send_header('Location', "/restaurants")
				self.end_headers()
				return
			elif self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == "multipart/form-data":
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')[0]
				newName = messagecontent
				id = getId(self.path)
				restaurant = session.query(Restaurant).filter_by(id=id).one()
				restaurant.name = newName
				session.add(restaurant)
				session.commit()
				self.send_response(301)
				self.send_header("Content-type", "text/html")
				self.send_header('Location', "/restaurants")
				self.end_headers()
				return
			elif self.path.endswith("/delete"):
				id = getId(self.path)
				restaurant = session.query(Restaurant).filter_by(id=id).one()
				session.delete(restaurant)
				session.commit()
				self.send_response(301)
				self.send_header("Content-type", "text/html")
				self.send_header('Location', "/restaurants")
				self.end_headers()
		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()
	except KeyboardInterrupt:
		print "^C centered, stopping web server..."
		server.socket.close()

if __name__=='__main__':
	main()
