from app import create_app, db
from app.models import Campaign, Order, Prize

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Campaign': Campaign,
        'Order': Order,
        'Prize': Prize
    }

if __name__ == '__main__':
    app.run(debug=True)
