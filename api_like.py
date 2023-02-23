from flask import Flask, request

from like_db import LikeDB

# Create an instance of Flask
app = Flask(__name__)

db = LikeDB('db.json')

@app.route('/api/add-like/', methods=['POST'])
def add_like():
    # get data from request
    data = request.get_json(force=True)

    # user_id, img_id
    user_id = data['user_id']
    img_id = data['image_id']

    # like img
    db.add_like(user_id, img_id)

    return {'status': 200}


@app.route('/api/add-dislike/', methods=['POST'])
def add_dislike():
    # get data from request
    data = request.get_json(force=True)

    # user_id, img_id
    user_id = data['user_id']
    img_id = data['image_id']

    # dislike img
    db.add_dislike(user_id, img_id)

    return {'status': 200}



@app.route('/api/<img_id>')
def get_data(img_id):
    data = db.get_likes_dislike(img_id)


    return {
        "like": data[0],
        "dislike": data[1]
    }
@app.route('/api/add_img/', methods=['POST'])
def add_image():
    # get data from request
    data = request.get_json(force=True)

    # user_id, img_id
    img_id = data['image_id']

    # like img
    db.add_immage(img_id)

    return {'status': 200}



# Run the app
if __name__ == "__main__":
    app.run(debug=True)