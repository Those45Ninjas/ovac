import markdown
import simplejson as json
import os

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

rootPath = os.path.dirname(app.root_path);

@app.route("/")
def index():
	"""Show the documentation"""
	# Open the readme file.
	with open(rootPath + "/readme.md", 'r') as markdown_file:
		# Parse the markdown and make some html tags.
		# TODO: Make a html template for the markdown to go inside.
		content = markdown_file.read()
		return markdown.markdown(content, extensions=['toc'])


class AccessoryList(Resource):
	def get(self):
		if os.path.isdir("/var/ova/controller/accessories"):
			data = []
			for file in os.listdir("/var/ova/controller/accessories"):
				if file.endswith(".json"):
					with open("/var/ova/controller/accessories/" + file, 'r') as fileContext:
						data.append(json.load(fileContext))
				
			return data, 200
		else:
			return '', 204 
		

api.add_resource(AccessoryList, '/accessories')

			