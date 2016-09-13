import argparse

from .bot import ThespomatBot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--clear', '-c', action='store_true', help='clear timeline')
    args = parser.parse_args()

    b = ThespomatBot()
    try:
        b.auth()
        if args.clear:
            b.clear()
        else:
            b.loop()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
