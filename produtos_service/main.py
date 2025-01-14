from entry_points.app_flask import app

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.config['TRAILING_SLASH'] = False 
    app.run(host="0.0.0.0", port=5000, debug=True)