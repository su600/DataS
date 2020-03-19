from flask import Flask, request, jsonify,render_template
import flask_excel as excel

app=Flask(__name__)
excel.init_excel(app)

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        aa=jsonify({"result": request.get_array(field_name='file')})
        bb = request.get_array(field_name='file')
        bb=zip(*bb)
        
        print(bb)
        return aa
    return render_template("ee.html")

@app.route("/export", methods=['GET'])
def export_records():
    return excel.make_response_from_array([[1,2], [3, 4]], "csv",
                                          file_name="export_data")

if __name__ == "__main__":
    app.run()