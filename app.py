from configure import detect_configuration
from core import create_app

configuration = detect_configuration()

app = create_app(configuration)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
