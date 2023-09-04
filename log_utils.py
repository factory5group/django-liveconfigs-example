import json
import logging
from typing import Any

from logwood import global_config
from logwood.handlers.logging import StreamHandler

_OMIT = {'__dict__', '__class__', '__dir__', 'levelno', 'levelname',
         'exc_info', 'stack_info', 'request', 'msg', 'args', 'message'}


class StreamFormatterHandler(StreamHandler):

    def __init__(self, *args, **kwargs):
        hostname = kwargs.pop('hostname')
        self.format_message = self._format_message_json if hostname != 'localhost' else self._format_message_simple
        super().__init__(*args, **kwargs)

    @staticmethod
    def _apply_args(record: dict[str, Any]):
        if 'args' in record and record['args']:
            record['message'] %= record['args']
        del record['args']

    @classmethod
    def _format_message_json(cls, record: dict[str, Any]) -> str:
        cls._apply_args(record)
        return json.dumps(record)

    @classmethod
    def _format_message_simple(cls, record: dict[str, Any]) -> str:
        cls._apply_args(record)
        return global_config.default_format % record


class JsonFormatter(logging.Formatter):
    """ slightly more usable than json-log-formatter """

    def __init__(self):
        super().__init__()

    def format(self, record):
        """ copy & paste from standard logger """
        message = record.getMessage()
        data = {
            'message': message,
            'level': record.levelname,
            'severity': record.levelname,
            'timestamp': record.created,
            'timestamp_str': str(record.created)
        }
        if record.exc_info:
            record.exc_text = self.formatException(record.exc_info)
        if record.stack_info:
            data['stack_info'] = self.formatStack(record.stack_info)
        for attr, value in record.__dict__.items():
            if attr not in _OMIT:
                data[attr] = value

        return json.dumps(data, default=str)
