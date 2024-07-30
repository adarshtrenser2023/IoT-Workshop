import time
import adafruit_dht
import board
import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO

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
 

# LED Pins

PIN_LED_RED = 25
PIN_LED_GREEN = 24
PIN_LED_BLUE = 23

def setup_LED_PINS():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_LED_BLUE, GPIO.OUT)
    GPIO.setup(PIN_LED_RED, GPIO.OUT)
    GPIO.setup(PIN_LED_GREEN, GPIO.OUT)

def blue_on():
    print("Blue LED on")
    GPIO.output(PIN_LED_BLUE, GPIO.HIGH)

def blue_off():
    print("Blue LED off")
    GPIO.output(PIN_LED_BLUE, GPIO.LOW)

def red_on():
    print("Red LED on")
    GPIO.output(PIN_LED_RED, GPIO.HIGH)

def red_off():
    print("Red LED off")
    GPIO.output(PIN_LED_RED, GPIO.LOW)

def green_on():
    print("Green LED on")
    GPIO.output(PIN_LED_GREEN, GPIO.HIGH)

def green_off():
    print("Green LED off")
    GPIO.output(PIN_LED_GREEN, GPIO.LOW)

#initializing dht11 PIN
dht_device = adafruit_dht.DHT11(board.D4)

def read_dht_sensor():
	temperature = dht_device.temperature
	humidity = dht_device.humidity   
	return temperature,humidity

def on_message(client, userdata, message):
    jsonObject = json.loads(message.payload.decode("utf-8"))
    color = jsonObject['color']
    action = jsonObject['action']

    if color == "blue" and action == "on":
        blue_on()    
    elif color == "blue" and action == "off":
        blue_off()
    elif color == "red" and action == "on":
        red_on()
    elif color == "red" and action == "off":
        red_off()
    elif color == "green" and action == "on":
        green_on()   
    elif color == "green" and action == "off":
        green_off()
    else:
        print("Unknown LED color")


setup_LED_PINS()

# MQTT Client Setup
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

# Main loop to read sensor data and publish
while True:
    try:
        # Read sensor data
        temperature, humidity = read_dht_sensor()
        if temperature is not None and humidity is not None:
            # Publish sensor data to MQTT broker
            client.publish(TopicPubTemp, temperature)
            client.publish(TopicPubHum, humidity)
            
        else:
            print("Failed to retrieve sensor data. Check wiring!")
            
        # Wait for 10 seconds before next reading
        time.sleep(10)  
    except KeyboardInterrupt:
        print("\nProgram terminated!")
        break  
    except Exception as e:
        print(f"Error: {e}")

# Disconnect MQTT client and cleanup
client.disconnect()
GPIO.cleanup()