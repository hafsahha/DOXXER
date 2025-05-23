from app import create_app

app = create_app()

if __name__ == '__main__':
    # Jalankan Flask development server dengan debug mode sesuai konfigurasi
    app.run(debug=app.config.get('DEBUG', False))
