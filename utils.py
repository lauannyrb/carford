from flask import abort, make_response


def abort_request(message, status_code):
    respose = make_response({'message': message}, status_code)
    abort(respose)
