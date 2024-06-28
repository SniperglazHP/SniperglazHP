This code is made in micropython and was designed to work through a 16X2 I2C LCD screen connected to an ESP32 microcontroller to display a game on its screen, this will ideally be connected to a breadboard and this in turn will add a button to make everything this works.

The game is a catch-it-type game, in which there are 5 attempts and the player must press a button at the correct time to catch the target, displaying the message "you won", otherwise the message "you lost" will be displayed.

Another thing to note is that this game has the possibility of sending game data to a free database called "firebase" from Google (it must be down right now because it was a free trial), apart from that everything should work fine.
