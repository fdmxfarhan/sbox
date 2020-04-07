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
  if(client.available()){
    rec = client.read();
    Serial.println(rec);
    if(rec == 'T')      led = true;
    else if(rec == 'F') led = false;
    else if(rec == 'N'){
      client.print(Name);
    }
  }
  if(led){
    digitalWrite(13, 1);
    digitalWrite(16, 1);
  }else{
    digitalWrite(13, 0);
    digitalWrite(16, 0);
  }
  
  delay(100);
}
