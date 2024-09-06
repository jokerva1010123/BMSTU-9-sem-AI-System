import sys

from dialog import Dialog


def main() -> None:
    dialog = Dialog()
    return dialog.run()


if __name__ == '__main__':
    sys.exit(main())
