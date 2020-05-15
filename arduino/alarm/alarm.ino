#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#ifndef STASSID
#define STASSID "fdmxfarhan"
#define STAPSK  "fdmxfarhan"
#endif

#define Name "alarm"

const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "192.168.43.210";
const uint16_t port = 3000;

ESP8266WiFiMulti WiFiMulti;

WiFiClient client;
char rec;
bool led = false;;
void setup() {
  pinMode(12, OUTPUT); //led1
  pinMode(13, OUTPUT); //buzzer
  pinMode(14, OUTPUT); //led2
  pinMode(16, OUTPUT); //vibrate
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
  while (!client.connected()){
    digitalWrite(2,1);
    delay(100);
    client.connect(host, port);
  }
  digitalWrite(2,0);
  if(client.available()){
    rec = client.read();
    Serial.println(rec);
    if(rec == 'L'){
      digitalWrite(12, 1);
      digitalWrite(14, 1);
    }
    else if(rec == 'l') {
      digitalWrite(12, 0);
      digitalWrite(14, 0);
    }
    else if(rec == 'B') {
      digitalWrite(13, 1);
    }
    else if(rec == 'b') {
      digitalWrite(13, 0);
    }
    else if(rec == 'V') {
      digitalWrite(16, 1);
    }
    else if(rec == 'v') {
      digitalWrite(16, 0);
    }
    else if(rec == 'N'){
      client.print(Name);
    }
  }
  delay(100);
}
