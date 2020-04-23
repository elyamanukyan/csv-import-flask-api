import os
import csv
import operator
from flask import Flask, request, jsonify, abort, Response

app = Flask(__name__)


def sort_order(csv_file):
    # Function for sorting rows from CSV files (by the ascending order based on date of birth)
    with open(csv_file, 'r') as content_file:
        read_csv = csv.reader(content_file, delimiter=',')

        people = []

        for row in read_csv:
            if read_csv.line_num == 1:  # skip header row containing column names
                continue
            if row:
                people.append(row)

        # sorting people by using operator module
        people_sorted = sorted(
            people, key=operator.itemgetter(2), reverse=True  # index 2 means sort by dobs which is third column (0,1,2)
        )

    return people_sorted


def parse_files(flask_request):
    # Function for parsing files and returning content as List
    contents = []
    try:
        temp_file = './tst.tmp'  # Temporary file for saving all files
        files = flask_request.files
        for file in files:
            # create temp file for each posted / uploaded files
            files[file].save(temp_file)

            if os.path.isfile(temp_file):
                # sort csv file per iteration and add it to the contents LIST
                contents.append(sort_order(temp_file))

                # delete temp file after sorting is done and we appended data to contents
                os.unlink(temp_file)
    except Exception as ex:
        abort(Response(str(ex)))

    return contents


@app.route("/dobs", methods=['GET', 'POST'])
def dobs():
    # The first function we call: handling the coming request
    msg = 'Not Supported Method'

    if request.method == "GET":
        msg = sort_order('dobs.csv')

    elif request.method == "POST":
        # if a JSON content was provided in the body ( json format )
        if request.get_json():
            _json = request.get_json()
            msg = _json

        # if there are files uploaded in the form-data
        elif request.files:
            msg = parse_files(flask_request=request)

    return jsonify(msg), 200


if __name__ == '__main__':
    app.run(debug=True, port=9090)
