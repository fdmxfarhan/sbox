/*
    This sketch sends a string to a TCP server, and prints a one-line response.
    You must run a TCP server in your local network.
    For example, on Linux you can use this command: nc -v -l 3000
*/

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#ifndef STASSID
#define STASSID "fdmxfarhan"
#define STAPSK  "fdmxfarhan"
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "192.168.43.210";
const uint16_t port = 3000;

ESP8266WiFiMulti WiFiMulti;

WiFiClient client;
char line;
bool led = false;;
void setup() {
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(14, OUTPUT);
  pinMode(16, OUTPUT);
  pinMode(2, OUTPUT);
  digitalWrite(2, 1);
  Serial.begin(115200);

  // We start by connecting to a WiFi network
  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP(ssid, password);

  Serial.println();
  Serial.println();
  Serial.print("Wait for WiFi... ");

  while (WiFiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  digitalWrite(2, 0);
  delay(500);
  while (!client.connect(host, port)) {
    Serial.println("connection...");
    delay(100);
  }
}


void loop() {
  client.println("hello from ESP8266");

  if(client.available()){
    line = client.read();
    Serial.println(line);
    if(line == 'T')  led = true;
    else             led = false;
  }
  if(led){
    digitalWrite(12, 1);
    digitalWrite(14, 1);
  }else{
    digitalWrite(12, 0);
    digitalWrite(14, 0);
  }
  
  
  delay(100);
}
