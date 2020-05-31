from flask import Flask, jsonify, request
import json

app = Flask(__name__)


@app.route('/status')
def hello():
    return jsonify({"status": "OK"} )

@app.route('/users')
def all_users():
    with open('users.json') as f:
        return jsonify(json.load(f))

@app.route('/users/<string:id>')
def user(id):
    with open('users.json') as f:
        users = json.load(f)
        for user in users:
            if user.get('id') == id:
                return jsonify(user)

@app.route('/users/', methods=['POST'])
def post_user():
    if not request.get_json():
        abort(400, description="Not a valid JSON")
    if 'id' not in request.get_json():
        abort(400, description="missing ID")
    data = request.get_json()
    with open('users.json') as f:
        users = json.load(f)
        users.append(data)
    with open('users.json','w') as f:
        json.dump(users, f)
        return ("success\n")

@app.route('/users/<string:id>', methods=['PUT'])
def update_user(id): 
    fields = ['name', 'balance', 'type']
    data = request.get_json()
    with open('users.json') as f:
        users = json.load(f)
        for user in users:
            if user.get('id') == id:
                for key, value in data.items():
                    if key in fields:
                        user[key] = value
    with open('users.json', 'w') as f:
        json.dump(users, f)
        return ("success\n")                          

if __name__ == '__main__':
    app.run()
