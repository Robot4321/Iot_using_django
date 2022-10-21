# Views Here
from django.http import HttpResponse
from django.shortcuts import render

import time
import RPi.GPIO as GPIO
from . import dht11
import requests
from datetime import datetime
import json
import os

def index(request):
    city_name,plant_name  = request.GET.get('city_name'),request.GET.get('plant_name')
    
    #print(len(city_name),len(plant_name))
    city_names = ['Bangalore', 'Delhi', 'Chennai']
    
    if city_name in city_names:

        GPIO.setmode(GPIO.BCM)
        instance = dht11.DHT11(pin=21)
        GPIO.setup(2, GPIO.IN)
        GPIO.setup(17, GPIO.OUT)
        servo1 = GPIO.PWM(17,50)
        servo1.start(0)
        duty = 2
        
        while True:
            if (GPIO.input(2)) == 0:
                print('Wet')
                servo1.ChangeDutyCycle(duty)
            
            elif (GPIO.input(2)) == 1:

                print('Dry')
                
                
                servo1.ChangeDutyCycle(12)    
                
                now = datetime.now()
                result = instance.read()
                print("Temp: %d C" % result.temperature +' '+"Humid: %d %%" % result.humidity)
                # send data to data_collector via api

                dict1 = {'id':city_name+str(now), 'date': now, 'temp':result.temperature, 'hum':result.humidity}

                pwd = os.path.dirname(__file__)
                filename = pwd+'/log_data.txt'
                
                # 1. Read file contents
                
                #print(data)
                f =  open(filename, "a")
                f.write('|'+str(dict1)+'|')



            time.sleep(10)
                
            
        else:
             GPIO.cleanup()
    else:
        #GPIO.output(12, False)
        GPIO.cleanup()
        print('a')
            



    return render (request,'index.html')
    
    #return HttpResponse('Hello')

def working(request):
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(7, GPIO.IN)
    try:
        while True:
            if (GPIO.input(7)) == 0:
                print('Wet')
                # turn off LED
            elif (GPIO.input(7)) == 1:
                print('Dry')
                # turn on LED
                # send data to data_collector via api

            time.sleep(10)
            render (request, 'working.html')
    finally:

        GPIO.cleanup()    


    