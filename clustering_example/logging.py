"""
"""
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_path = os.path.join(settings.BASE_DIR, 'tmp/logs/clustering_example.log')

handler = logging.FileHandler(log_path)

def log_info(request, data):
    user_agent = request.META.get('HTTP_USER_AGENT')
    formatter = logging.Formatter('[%(asctime)s] - %(message)s\n')
    handler.setFormatter(formatter)

    handler.setLevel(logging.INFO)

    logger.addHandler(handler)
    log_msg = "{api} - {user_agent}\nMsg: {data}".format(
        api=request.path,
        user_agent=user_agent,
        data=data)
    logger.info(log_msg)

def log_info_without_request(data):
    formatter = logging.Formatter('[%(asctime)s] - %(message)s\n')
    handler.setFormatter(formatter)

    handler.setLevel(logging.INFO)

    logger.addHandler(handler)
    log_msg = "Msg: {data}".format(
        data=data)
    logger.info(log_msg)
