# File Structure
This project includes 3 multi-threaded processes and a main to orchestrate running the processes.
  - Recording the screen and processing the image stream into a computer vision algorithm.
  - Displaying an overlay relaying relevant information captured from the OCR.
  - A speech detection model that relays voice commands into the players chat.

# Main Component
- Ensures that an instance of the game is running. Closes program when game is no longer open.
- Allows saving of intermediate images to debug CV component.
- Implements multi-threading to allow processes to hand of data between eachother.

# CV Component
The computer vision processing module includes cropping and resizing the image to capture the chat section of the screen, converting the image to gray, binizing the image using adaptive thresholding, running a tesseract model to extract and then filter relevant text.

# Overlay Component
The overlay module relies on an internet connection to get detected champion icons from Riot Game's "Data Dragon" database. Filters out duplicate flash timers for the same champion within 5 minutes. Displays the champion icon along with the expected time until their flash is on cooldown (plus 5 minutes from detection).

# Speech2Text Component
The speech detection module records sounds wave files from the users primary mic after designated hotkey is pressed (default is 'm') then processes sound file through Whisper model to predict the English words spoken. Simulating keyboard presses to seamlessly insert the spoken words into the chat.


![Example Image](https://github.com/unsupervised-machine/lol_flash_chat/blob/master/images_github/1_champion_flash_timer.JPG?raw=true)


# TODO 
## DEV INSTALL GUIDE
