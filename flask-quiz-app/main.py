from app import app
from waitress import serve


if __name__ == "__main__":
    #app.run(debug=True) 
    serve(app, host="0.0.0.0", port=8080)
   
