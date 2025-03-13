import logging

from PySide6.QtCore import QObject, Signal


class OutputLogging(logging.Handler):
    class Emitter(QObject):
        log = Signal(str)

    def __init__(self, widget_name):
        super().__init__()
        self.widget = widget_name
        self.emitter = OutputLogging.Emitter()
        self.emitter.log.connect(self.widget.append)

    def emit(self, record):
        log_message = self.format(record)
        if "********************" in log_message:
            text = f"""<p style='color:#ff00ff'>{log_message}</p>"""
        elif "INFO" in log_message:
            text = f"""<p style='color:#00ffff'>{log_message}</p>"""
        elif "WARNING" in log_message:
            text = f"""<p style='color:#ffff00'>{log_message}</p>"""
        elif "ERROR" in log_message or "CRITICAL" in log_message:
            text = f"""<pre style='color:#ff4500'>{log_message}</pre>"""
        else:
            text = log_message
        self.emitter.log.emit(text)
