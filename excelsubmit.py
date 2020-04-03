from flask import Flask, render_template,jsonify,request

app = Flask(__name__)

@app.route("/demo", methods=["POST"])
def demo():
	nick_name = request.form.get("nick_name")
	print(nick_name)
	return "ok"


if __name__ == "__main__":
    app.run()
