import glob
import shutil
from doit.task import clean_targets

DOIT_CONFIG = {
    "cleandep": True,
    "cleanforget": True,
    "default_tasks": ["html"],
}

def task_pot():
    "extract server's messages for translation"
    return {
        "actions": ["pybabel extract . -o templates.pot"],
        "file_dep": ["."],
        "targets": ["templates.pot"],
        "clean": [clean_targets],
    }

def task_po():
    "update server translation file"
    return {
        "actions": ["pybabel update -D LocalesMOOD -d mood/server/po -i templates.pot"],
        "targets": ["mood/server/po/ru_RU.UTF-8/LC_MESSAGES/LocalesMOOD.po"],
    }

def task_mo():
    "compile server translation file"
    return {
        "actions": ["pybabel compile -D LocalesMOOD -d mood/server/po -l ru_RU.UTF-8"],
        "targets": ["mood/server/po/ru_RU.UTF-8/LC_MESSAGES/LocalesMOOD.mo"],
        "clean": [clean_targets],
    }

def task_i18n():
    "do full server translation cycle"
    return {
        "actions": None,
        "task_dep": ["pot", "po", "mo"],
    }

def task_html():
    "generate HTML documentation"
    return {
        "actions": ['sphinx-build -M html docs docs/_build'],
        "file_dep": [*glob.iglob("*.rst"), *glob.iglob("mood/*/*.py")],
        "clean": [(shutil.rmtree, ["_build"])],
    }

def task_test():
    "run server response tests"
    return {
        "actions": ["python3 -m unittest check/mood_test.py"],
    }

def task_sdist():
    return {
        "actions": ["python3 -m build --sdist"]
    }

def task_wheel():
    return {
        "actions": ["python3 -m build --wheel"]
    }
