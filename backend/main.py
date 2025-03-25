import argparse
from flask import Flask
from api.routes import configure_routes

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Blur Face - Video Face Blurring Application")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--port", type=int, default=5000, help="Port for the web server")
    return parser.parse_args()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    configure_routes(app)
    return app

if __name__ == "__main__":
    args = parse_arguments()
    app = create_app()
    app.run(debug=args.debug, port=args.port)
    print(f"Blur Face server running on port {args.port}")