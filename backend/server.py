from flask_cors import CORS
import connexion

# Create the application instance
app = connexion.App(__name__, specification_dir=".")
CORS(app.app)
app.add_api('manvsvirus.yml')

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=False, port=8080)