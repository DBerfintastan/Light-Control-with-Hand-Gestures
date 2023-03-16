#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>

// Set these to run example.
#define WIFI_SSID "mmeliht"
#define WIFI_PASSWORD "5054790057"

// FireBase 
#define FIREBASE_AUTH "yqNfP6FGPHysjoUC2LGl7Ky3PFiejr0k5gpZxEc7"
#define FIREBASE_HOST "database-b0c01-default-rtdb.firebaseio.com"

#define led D1


void setup() {
  pinMode(led,OUTPUT);
  Serial.begin(9600);

  delay(10);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
  
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

}

void loop(){

  // handle error

  
  int data = atoi(Firebase.getString("data").c_str());
  if (Firebase.failed()) {
      Serial.print("setting /message failed:");
      Serial.println(Firebase.error());  
      return;
  }
  Serial.print(data);
  Firebase.setInt("Melih", 123);

  if(data ==1){
      digitalWrite(led,HIGH);
  }
  else{
      digitalWrite(led,LOW);
  }


  

}
