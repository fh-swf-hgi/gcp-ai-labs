import os
import tempfile
import filetype
from werkzeug.utils import secure_filename
from flask import Flask, send_file, request
from google.cloud import vision


def get_file_path(filename):
    file_name = secure_filename(filename)
    return os.path.join(tempfile.gettempdir(), file_name)

app = Flask(__name__)

#source: https://cloud.google.com/translate/docs/basic/translating-text?hl=de
def translate_text(target, text):
    return text


@app.route("/", methods=['GET', 'POST'])
def tag_labels():
    if request.method == 'POST':
        file = request.files['file']
        filename=secure_filename(file.filename)
        client = vision.ImageAnnotatorClient()
        content = file.read()
        image = vision.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        res = ""
        for label in labels:
            res += (label.description + "\n")
        return translate_text('de', res)

    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File (v0.2)</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
