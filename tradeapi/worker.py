from celery import shared_task

from .backend import trade
from .models import Offer
from .enum import TransactionTypeEnum


@shared_task
def get_trade():
    pass