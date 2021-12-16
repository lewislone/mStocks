#include <ESP8266WiFi.h>

const char* ssid = "lll2.4G_tp";
const char* password = "easyinstall";

IPAddress staticIP(192,168,0,222);
IPAddress gateway(192,168,0,1);
IPAddress subnet(255,255,255,0);

void setup()
{
  Serial.begin(115200);
  Serial.println();

  Serial.print("Connecting");
  WiFi.config(staticIP, gateway, subnet);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
    Serial.printf("wifi status: %d\n", WiFi.isConnected());
    Serial.printf("Connected, IP address: ");
    Serial.println(WiFi.localIP());
    Serial.printf("Connected, mac address: %s\n", WiFi.macAddress().c_str());
    Serial.printf("Gataway IP: %s\n", WiFi.gatewayIP().toString().c_str());
    Serial.printf("SSID: %s\n", WiFi.SSID().c_str());
    Serial.printf("RSSI: %d dBm\n", WiFi.RSSI());
  ESP.wdtEnable(5000); //5s watchdog
}

void loop() 
{
  Serial.printf("wifi mode: %d\n", WiFi.getMode());
  //WiFi.disconnect(true);
  delay(500);
  if(WiFi.isConnected() == false) {
    Serial.print("reconnecting");
    WiFi.reconnect();
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
  }
  Serial.printf("wifi status: %d\n", WiFi.isConnected());

  delay(1000);
}
