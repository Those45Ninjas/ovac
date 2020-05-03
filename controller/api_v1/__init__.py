import markdown
import simplejson as json
import os

from flask import Flask, render_template
from flask_restful import Resource, Api

app = Flask(__name__, template_folder='../templates')
api = Api(app)

rootPath = os.path.dirname(app.root_path);

@app.route("/")
def index():
	"""Show the documentation"""
	# Open the readme file.
	with open(rootPath + "/readme.md", 'r') as markdown_file:
		# Parse the markdown file.
		markdown_parsed = markdown.markdown(markdown_file.read(), extensions=['toc', 'extra', 'codehilite'])

		# Run the markdown through the template file.
		return render_template("doc-page.html", title="readme.md", markdown = markdown_parsed)


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

			