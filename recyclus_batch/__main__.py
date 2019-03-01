import os
from recyclus_sim import create_app

app = create_app(os.getenv('FLASK_ENV') or 'development')
app.run(host='0.0.0.0', port=5000, debug=True)