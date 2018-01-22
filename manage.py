from src import app, manager, admin
import os

port = os.getenv('VCAP_APP_PORT', '5000')

if __name__ == '__main__':
    app.config.from_object('src.config.DevelopmentConfig')
    # app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    app.run(host='0.0.0.0', port=int(port))
    #manager.run()
