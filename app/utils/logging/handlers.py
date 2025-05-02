import os
import calendar
import logging
from datetime import datetime

from . import formatters


def _get_monthly_log_directory():
    # get the current month's name in lowercase
    month = calendar.month_name[datetime.now().month].lower()
    # construct the directory path
    log_dir = os.path.join(".dream_logs", month)
    # create the directory if it does not exist
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def _get_latest_log_file():
    # get the log directory for the current month
    log_dir = _get_monthly_log_directory()
    # fetch existing log files and sort them numerically by index
    log_files = [
        f for f in os.listdir(log_dir) if f.startswith("logs_") and f.endswith(".log")
    ]
    if log_files:
        log_files.sort(
            key=lambda x: int(x.split("_")[1].split(".")[0])
        )  # sort by index
        return os.path.join(log_dir, log_files[-1])  # return the latest file
    # if no log files exist, return the first log file path
    return os.path.join(log_dir, "logs_0.log")


def _get_next_log_file():
    # get the log directory for the current month
    log_dir = _get_monthly_log_directory()
    # fetch existing log files and sort them numerically by index
    log_files = [
        f for f in os.listdir(log_dir) if f.startswith("logs_") and f.endswith(".log")
    ]
    if log_files:
        log_files.sort(
            key=lambda x: int(x.split("_")[1].split(".")[0])
        )  # sort by index
        # calculate the next file index
        next_index = int(log_files[-1].split("_")[1].split(".")[0]) + 1
        return os.path.join(log_dir, f"logs_{next_index}.log")
    # if no log files exist, return the first log file path
    return os.path.join(log_dir, "logs_0.log")


class MonthlyRotatingFileHandler(logging.Handler):
    def __init__(self, max_bytes=1024 * 1024):  # 1024 * 1024 = 1MB
        super().__init__()
        self.max_bytes = max_bytes
        self.current_file = _get_latest_log_file()

    def emit(self, record):
        # check if the current log file exceeds the size limit
        if (
            os.path.exists(self.current_file)
            and os.path.getsize(self.current_file) >= self.max_bytes
        ):
            self.current_file = _get_next_log_file()  # rotate to the next log file
        # write the log record to the current file
        with open(self.current_file, "a") as log_file:
            log_file.write(self.format(record) + "\n")


def monthly_rotating_file_handler(max_bytes=1024 * 1024):  # 1024 * 1024 = 1MB
    # create a custom monthly rotating file handler
    handler = MonthlyRotatingFileHandler(max_bytes=max_bytes)
    handler.setFormatter(formatters.Default())
    return handler
