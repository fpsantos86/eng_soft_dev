
from entry_points.app_flask import app

if __name__ == "__main__":
    # Configuração adicional, se necessário
    app.run(host="0.0.0.0", port=5000, debug=True)