import logging

from controllers import Controller
from models import Options
from views import Root


def main():
    model = Options
    view = Root()
    controller = Controller(model, view)
    controller.start()


if __name__ == "__main__":
    logging.basicConfig(
        # stream=sys.stdout,
        level=logging.DEBUG,
        filename="log.log",
        filemode="w",
        format="%(asctime)s - %(" "name)s - %(" "levelname)s - %(" "message)s",
    )

    main()
