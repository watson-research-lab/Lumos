#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFiNINA.h>
#include <Adafruit_AS7341.h>

//citations: https://github.com/adafruit/Adafruit_AS7341 
//citations https://github.com/knolleary/pubsubclient

Adafruit_AS7341 as7341;

void setup_wifi();
void reconnect();
static char payload[256];
StaticJsonDocument<256> doc;
#define TOKEN "" /* Spectrometer Token */
#define DEVICEID "" /* Spectrometer Device ID */
const char* ssid = ""; /* add WiFi name in quotes */
const char* password = ""; /* add WiFi password in quotes */
const char mqtt_server[] = ""; /* add MQTT server */
const char publishTopic[] = ""; /* add MQTT Topic */
WiFiSSLClient wifiClient;
PubSubClient mqtt(wifiClient);

unsigned long timer;
static unsigned long last_us = 0;

/*Input variables*/
#define RUNNING_MIN 3   /* The opearting time for each frequency, i.e. each sampling test period = 3 mins  */
float Hz = 0.5; /* inital frequency*/
float Frequency_Interval = 0.5;/* frequency interval */

unsigned int period = 1000000/Hz; /* Python data process uses this*/
unsigned long start_time;


void setup_wifi(){
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while( WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
void reconnect(){
  while(!mqtt.connected()){
    Serial.print("Disconnect,");
    Serial.print("failed, rc=");
    Serial.print(mqtt.state());
    
    mqtt.disconnect();
    if (mqtt.connect(DEVICEID, TOKEN, NULL)) {
      Serial.println("Connected to MQTT Broker");
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(mqtt.state());
      Serial.println("try again in 5 second");
      digitalWrite(LED_BUILTIN, LOW);
      delay(5000);
    }
  }
}
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  if (!as7341.begin()){
    Serial.println("Could not find AS7341");
    while (1) { delay(10); }
  }
  as7341.setATIME(100);
  as7341.setASTEP(999);
  as7341.setGain(AS7341_GAIN_256X);
  setup_wifi();
  mqtt.setServer(mqtt_server, 8883);
}
void loop() {
  uint16_t readings[12];
  uint16_t counts[12];
  if (!mqtt.connected())
  {
    reconnect();
  }
  mqtt.loop();
  timer = micros() ;
  if(timer -last_us>period)
  {
    if(timer-start_time>RUNNING_MIN*60000000){ /* frequency: 1 min = 6e7us */

      Hz+=Frequency_Interval;  /* after every RUNNING_MIN, increase sampling frequency by Frequency_Interval(0.5), such that Test Frequency = 0.5, 1, 1.5, 2... */
      if(Hz>10){    
        start_time=timer;   
        Serial.print("Frequency = "); /* python identifier */
        Serial.print(Hz);
        Serial.print(", period = ");
        Serial.println(period);
        Serial.println("\n");
        exit(0);
      }
      period = 1000000/(Hz);

      Serial.print("Frequency = "); /*used for data process in Python. These texts are used*/
      Serial.print(Hz);                     /* to locate the head for sampling data */ 
      Serial.print(", period = ");          /* under each Frequency  */
      Serial.println(period);
      Serial.println("\n");
      delay(2000);                  
      /* data looks like: */
      /*  21:07:12.706 -> Frequency = 4.50, period = 222222
          21:07:12.706 -> 
          21:07:12.706 ->                                     
          21:07:14.695 -> test
          ....                                              */
      start_time=micros();
      timer=start_time;
    }
    last_us=timer;
     sample();
  }
}

void sample() {
  uint16_t readings[12];
  uint16_t counts[12];

  for(uint8_t i = 0; i < 12; i++) {
      if(i == 4 || i == 5) continue;
      // we skip the first set of duplicate clear/NIR readings
      // (indices 4 and 5)
      counts[i] = readings[i];
  }
    doc["F1_415nm"] = counts[0];
    doc["F2_445nm"] = counts[1];
    doc["F3_480nm"] = counts[2];
    doc["F4_515nm"] = counts[3];
    doc["F5_555nm"] = counts[6];
    doc["F6_590nm"] = counts[7];
    doc["F7_630nm"] = counts[8];
    doc["F8_680nm"] = counts[9];
    doc["Clear"]    = counts[10];
    doc["NIR"]      = counts[11];
    serializeJsonPretty(doc, payload); 
    mqtt.publish(publishTopic, payload);
    Serial.println(payload);

}
