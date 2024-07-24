# IoT-Workshop

# venv setup
sudo apt install python3.11-venv
python3 -m venv myiot
source myiot/bin/activate

# libraries to be added
pip3 install RPi.GPIO
pip3 install adafruit-circuitpython-dht
sudo apt-get install libgpiod2
pip3 install paho-mqtt

# LED code
#led on off

import RRi.GPIO as GPIO

#LEDPINs

PIN_LED_BLUE = 23
PIN_LED_RED = 24
PIN_LED_GREEN = 25

#LED pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_LED_BLUE, GPIO.OUT)
GPIO.setup(PIN_LED_RED, GPIO.OUT)
GPIO.setup(PIN_LED_GREEN, GPIO.OUT)

#led function definition
def blue_on():
    print("Blue LED on")
    GPIO.output(PIN_LED_BLUE, GPIO.HIGH)

def blue_off():
    print("Blue LED off")
    GPIO.output(PIN_LED_BLUE, GPIO.LOW)
    
#Blue led on
blue_on()

#blue led off
blue_off()

GPIO.cleanup()

#DHT11 sensor read
import adafruit_dht
import board
import time

dht_device = adafruit_dht.DHT11(board.D4)

def read_dht_sensor():
	temperature = dht_device.temperature
	humidity = dht_device.humidity
  return temperature,humidity
  
while True:
    try:
        # Read sensor data
        temperature, humidity = read_dht_sensor()

        if temperature is not None and humidity is not None:
        print(f"temperature : {temperature} , Humidity : {humidity}")  
        else:
            print("Failed to retrieve sensor data. Check wiring!")   
    except KeyboardInterrupt:
        print("\nProgram terminated!")
        break  
    except Exception as e:
        print(f"Error: {e}")
    # Wait for 10 seconds before next reading
    time.sleep(10)

import paho.mqtt.client as mqtt
import json

# MQTT Broker Connection Details
# Replace with your MQTT broker address
BROKER_ADDRESS = "a2h0zp3xnw63ym-ats.iot.ap-southeast-2.amazonaws.com" 
# Default MQTT port 
PORT = 8883
# MQTT topic to subscribe
TopicSub = "iot/workshop/adarsh-ap/command" 
# MQTT topic to publish tempeature data
TopicPubTemp = "iot/workshop/adarsh-ap/telemetry/temp"  
# MQTT topic to publish humidity data
TopicPubHum = "iot/workshop/adarsh-ap/telemetry/humidity"

# Paths to your SSL/TLS certificates
CA_CERTS = "CA.pem"
# Optional, if client authentication is required
CLIENT_CERT = "cert.crt"
# Optional, if client authentication is required
CLIENT_KEY = "private.key"


def on_message(client, userdata, message):
    #code for handling command message like ON OFF led 

client = mqtt.Client()
client.on_message = on_message

# Configure SSL/TLS
client.tls_set(ca_certs=CA_CERTS,
               certfile=CLIENT_CERT,
               keyfile=CLIENT_KEY,
               tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)


# Connect to the MQTT broker
client.connect(BROKER_ADDRESS, PORT, keepalive=60)
client.loop_start()
client.subscribe(TopicSub)

#dht read data publishing
client.publish(TopicPubTemp, temperature)

client.disconnect()
