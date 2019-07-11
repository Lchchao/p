
import os
import sys
import traceback
import logging
import logging.config



logger = logging.getLogger("debug")

#logger = logging.getLogger("daily")
#logger_d = logging.getLogger("daily")
#logger_e = logging.getLogger("error")

def init_log(log_path, log_name, log_level = "DEBUG"):
    ''''''
    log_level = log_level.upper()

    LOG_PATH_DEBUG = "%s/%s_debug.log" % (log_path,log_name)
    LOG_PATH_DAILY = "%s/%s_daily.log" % (log_path,log_name)
    LOG_PATH_ERROR = "%s/%s_error.log" % (log_path,log_name)
    #日志文件大小
    LOG_FILE_MAX_BYTES = 1 * 512 * 1024 * 1024
    #备份文件个数
    LOG_FILE_BACKUP_COUNT = 365

    log_conf = {
        "version" : 1,
        "formatters" : {
            "format1" : {
                "format" : '%(asctime)-15s [%(thread)d] - [%(filename)s %(lineno)d] %(levelname)s %(message)s',
            },
        },

        "handlers" : {
            "handler1": {
                "class" : "logging.handlers.TimedRotatingFileHandler",
                "level" : log_level,
                "formatter" : "format1",
                "when" : 'midnight',
                "backupCount" : LOG_FILE_BACKUP_COUNT,
                "filename" : LOG_PATH_DAILY
            },
            "handler2": {
                "class" : "logging.handlers.RotatingFileHandler",
                "level" : log_level,
                "formatter" : "format1",
                "maxBytes" :  LOG_FILE_MAX_BYTES,
                "backupCount" : LOG_FILE_BACKUP_COUNT,
                "filename" : LOG_PATH_DEBUG
            },
            "handler3": {
                "class" : "logging.handlers.RotatingFileHandler",
                "level" : "ERROR",
                "formatter" : "format1",
                "maxBytes" :  LOG_FILE_MAX_BYTES,
                "backupCount" : LOG_FILE_BACKUP_COUNT,
                "filename" : LOG_PATH_ERROR
            },
        },

        "loggers" : {
            "daily" : {
                "handlers" : ["handler1"],
                "level" : log_level,
            },
            "debug": {
                "handlers" : ["handler2"],
                "level" : log_level
            },
            "error": {
                "handlers" : ["handler3"],
                "level" : "ERROR"
            },
        }
    }
    logging.config.dictConfig(log_conf)