from django.http import HttpResponse
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)


def door(request):
    GPIO.output(5, 0)
    time.sleep(6)
    GPIO.output(5, 1)
    return HttpResponse("Door Opened")
