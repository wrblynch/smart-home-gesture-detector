const int BUTTON_PIN = 14; // map BUTTON_PIN to the GPIO pin we're using
bool sending;

void setup()
{
     //initialize button_pin as an input
     pinMode(BUTTON_PIN, INPUT_PULLUP);
     setupCommunication();
     sending = true;
}


void loop()
{
     // if the button is pushed down, turn on the LED
     if (digitalRead(BUTTON_PIN) == LOW) {
          sending = true;    
     }
     // if the button isn't pushed down, turn the LED off
     else {
          sending = false;
     }
     if(sending) {
      Serial.println("sending");
      String response = "pressed";
      sendMessage(response);
     }
}
