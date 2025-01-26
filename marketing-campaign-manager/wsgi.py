from app import create_app, db
from app.models import Campaign, Order, Prize

app = create_app()

if __name__ == '__main__':
    app.run()