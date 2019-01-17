from django.http import HttpResponse
import RPi.GPIO as GPIO
from django.utils import timezone
from doorctl.models import accessKey
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
import time


import logging

logger = logging.getLogger('django')


def check_key(use_key):
    response = dict()
    response['valid_key'] = False
    try:
        key = accessKey.objects.get(key=use_key)
        response['key_object'] = key
    except ObjectDoesNotExist:
        key_error = "Key: {} is Invalid".format(use_key)
        logger.error(key_error)
        response['message'] = key_error
        return response
    if key.use_limit != 0 and key.uses >= key.use_limit:
        key_error = "Key: {} is past it's use limit of {}!".format(use_key, key.use_limit)
        logger.error(key_error)
        response['message'] = key_error
        return response
    if key.expires:
        if timezone.now() > key.expires:
            key_error = "Key: {} has expired at {}!".format(use_key, key.expires)
            logger.error(key_error)
            response['message'] = key_error
            return response
    response['valid_key'] = True
    response['message'] = 'Valid Key'
    return response


def landing(request):
    use_key = request.GET.get('key', '')
    key_data = check_key(use_key)
    key_message = key_data['message']
    if key_data['valid_key']:
        unlock_time = key_data['key_object'].unlock_time
    else:
        unlock_time = 0
    return render(
        request,
        'door_landing.html',
        {
            "key_message": key_message,
            "valid_key": key_data['valid_key'],
            "key": use_key,
            "unlock_time": unlock_time
        }
    )


@require_http_methods(["POST"])
def ajax_door(request):
    use_key = request.POST['accessKey']
    key_data = check_key(use_key)
    if key_data['valid_key'] != True:
        return HttpResponse("Error", status=401)
    accessKey.objects.filter(key=use_key).update(uses=key_data['key_object'].uses + 1)
    logger.info("Door opened with key: {}".format(use_key))
    GPIO.output(5, 0)
    time.sleep(key_data['key_object'].unlock_time)
    GPIO.output(5, 1)
    return HttpResponse("Success", status=200)
