from django.http import HttpResponse
import RPi.GPIO as GPIO
from django.utils import timezone
from doorctl.models import accessKey, Door
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from pigateman.settings import EMAIL_HOST_USER
from django.http import HttpResponse
from django.template import loader
from ratelimit.decorators import ratelimit
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


@ratelimit(key='header:HTTP-X-FORWARDED-FOR', rate='10/m', block=True)
def landing(request):
    use_key = request.GET.get('key', '')
    keypad = False
    if use_key == '':
        key_data = dict()
        key_data['valid_key'] = False
        keypad = True
        key_message = None
    else:
        key_data = check_key(use_key)
        key_message = key_data['message']
    if key_data['valid_key']:
        unlock_time = key_data['key_object'].unlock_time
        if key_data['key_object'].instruction_message is not '':
            key_message = key_data['key_object'].instruction_message
    else:
        unlock_time = 0
    return render(
        request,
        'door_landing.html',
        {
            "key_message": key_message,
            "valid_key": key_data['valid_key'],
            "key": use_key,
            "unlock_time": unlock_time,
            "keypad": keypad
        }
    )


@ratelimit(key='header:HTTP-X-FORWARDED-FOR', rate='10/m', block=True)
@require_http_methods(["POST"])
def ajax_door(request):
    use_key = request.POST['accessKey']
    key_data = check_key(use_key)
    if not key_data['valid_key']:
        return HttpResponse(key_data['message'], status=401)
    if key_data['key_object'].notify:
        send_mail(
            'Gate Opened',
            'Notification of key use to open gate.',
            EMAIL_HOST_USER,
            [key_data['key_object'].notify_email]
        )
    key = accessKey.objects.filter(key=use_key)
    door = Door.objects.get(accesskey=key[0])
    key.update(uses=key_data['key_object'].uses + 1)
    logger.info("Door: {} opened with key: {}".format(door.name, use_key))
    GPIO.output(door.gpio_port, 0)
    time.sleep(key_data['key_object'].unlock_time)
    GPIO.output(door.gpio_port, 1)
    if key_data['key_object'].instruction_message is not '':
        response = key_data['key_object'].instruction_message
    else:
        response = 'Success'
    return HttpResponse(response, status=200)


class HttpResponseTooManyRequests(HttpResponse):
    status_code = 429


def ratelimited(request, exception):
    return HttpResponse('429 Rate Limit Exceeded',status=429)


def bad_csrf(request, **kwargs):
    return HttpResponse('Bad CSRF: {}'.format(kwargs), status=401)
