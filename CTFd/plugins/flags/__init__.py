from CTFd.plugins import register_plugin_assets_directory

import re
import string
import hmac


class BaseFlag(object):
    name = None
    templates = {}

    @staticmethod
    def compare(self, saved, provided):
        return True


class CTFdStaticFlag(BaseFlag):
    name = "static"
    templates = {  # Nunjucks templates used for key editing & viewing
        'create': '/plugins/flags/assets/static/create.html',
        'update': '/plugins/flags/assets/static/edit.html',
    }

    @staticmethod
    def compare(chal_key_obj, provided):
        saved = chal_key_obj.content
        data = chal_key_obj.data

        if len(saved) != len(provided):
            return False,False
        result = 0

        if data == "case_insensitive":
            for x, y in zip(saved.lower(), provided.lower()):
                result |= ord(x) ^ ord(y)
        else:
            for x, y in zip(saved, provided):
                result |= ord(x) ^ ord(y)
        return result == 0, False


class CTFdRegexFlag(BaseFlag):
    name = "regex"
    templates = {  # Nunjucks templates used for key editing & viewing
        'create': '/plugins/flags/assets/regex/create.html',
        'update': '/plugins/flags/assets/regex/edit.html',
    }

    @staticmethod
    def compare(chal_key_obj, provided):
        saved = chal_key_obj.content
        data = chal_key_obj.data

        if data == "case_insensitive":
            res = re.match(saved, provided, re.IGNORECASE)
        else:
            res = re.match(saved, provided)

        return res and res.group() == provided, False

class DynamicFlag(BaseFlag):
    name = "dynamic"
    templates = {
        'create': '/plugins/flags/assets/dynamic/create.html',
        'update': '/plugins/flags/assets/dynamic/edit.html',
    }

    @staticmethod
    def compare(chal_key_obj, provided):
        saved = chal_key_obj.content
        data = chal_key_obj.data

        from fyp import generateFlag,checkShareFlag
        from CTFd.utils.user import get_current_team
        saved = generateFlag(saved,get_current_team())
        if len(saved) != len(provided):
            return False,False
        result = 0
        share = False
        if data == "case_insensitive":
            saved = saved.lower()
            provided = provided.lower()

        for x, y in zip(saved, provided):
            result |= ord(x) ^ ord(y)

        if result != 0:
            share = checkShareFlag(saved,provided)

        if share:
            from CTFd.utils.events import socketio
            socketio.emit('notification', {"title": "Share Flag Detected", "content": "Suspect team name: " + get_current_team().name}, broadcast=True)
        return result == 0,share


FLAG_CLASSES = {
    'static': CTFdStaticFlag,
    'regex': CTFdRegexFlag,
    'dynamic': DynamicFlag
}


def get_flag_class(class_id):
    cls = FLAG_CLASSES.get(class_id)
    if cls is None:
        raise KeyError
    return cls


def load(app):
    register_plugin_assets_directory(app, base_path='/plugins/flags/assets/')
