"""gunicorn WSGI server configuration."""

from multiprocessing import cpu_count
from os import environ
from os import path

def max_workers():
    return cpu_count()


def env_variables():
    dir_path = path.dirname(path.realpath(__file__))
    environ["DIALOGFLOW_PROJECT_ID"] = "projo-qruhoy"
    environ["GOOGLE_APPLICATION_CREDENTIALS"] = path.join(dir_path, "Projo-5b58254183f8.json")
    return


env_variables()
