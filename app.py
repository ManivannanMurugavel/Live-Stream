from flask import Flask, render_template, Response, request, jsonify, make_response
import rethinkdb as r

conn = r.connect(host='localhost',
			 port=28015)


app = Flask(__name__)
@app.route('/live')
def index():
    return render_template('live.html')

@app.route('/save_data')
def save_data():
    data = request.args['data']
    r.db('whirldata').table("live_streaming").insert({'data':data}).run(conn)
    return 'success'

@app.route('/live-data')
def live_data():
	print('live stream')
	def live_stream():
		try:
			r.connect( "localhost", 28015).repl()
			cursor = r.db('whirldata').table("live_streaming").changes().run()
			for document in cursor:
				print(document)
				yield "data:" + str(document['new_val']['data']).replace("'",'"') + "\n\n"

		except:
			pass

	return Response(response = live_stream(),status=200, mimetype= 'text/event-stream')

if __name__ == "__main__":
	app.run(host="0.0.0.0",debug=True)
