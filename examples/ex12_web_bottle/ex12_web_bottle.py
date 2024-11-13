import webbrowser

import bottle


@bottle.route("/")
def main_route():
    return "Hello world"


def main():
    webbrowser.open("http://localhost:8000/")
    bottle.run(port=8000)


if __name__ == "__main__":
    main()
