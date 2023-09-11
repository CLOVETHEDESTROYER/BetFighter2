from flask import Flask, jsonify




app=Flask(__name__)


#members API route
@app.route('/')
def winner():
    data = {'Winner': ["Member1", "Member2", "Member3", "CacaBallZ", "nalga", "cacamane"]}
    print(data)
    return jsonify(data)

if __name__ == "__main__":
    app.run(port= 8000, debug=True)
