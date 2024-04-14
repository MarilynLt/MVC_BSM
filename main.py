from controllers import Controller
from models import Options
from views import Root


def main():
    model = Options
    view = Root()
    controller = Controller(model, view)
    controller.start()


if __name__ == "__main__":
    main()
