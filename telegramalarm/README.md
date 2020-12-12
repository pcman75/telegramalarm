# About
This is Homeassistant add-on providing Telegram integration. The add-on is using [Telethon library](https://github.com/LonamiWebs/Telethon) to interact with Telegram's API as a user, which alows a much deeper integration then the Bot API.

### Example of use case:
In my country there is a earthquaqe alert system implemented through Telegram. A bot alert you on dedicated alarm channels about the upcoming earthquaqe in the next tens of seconds in your area.
I thought it would be useful to implement a Homeassistant integration with binary sensors triggering when alert messages are posted on these channels.
This opens the possibility to implement further automation such as siren triggering or phone notifications when there are posts on these channels

# Configuration

## Step 1 
You need to get your own API ID and hash from telegram
1. [Login to your Telegram account](https://my.telegram.org/) with the phone number of the developer account to use.
2. Click under API Development tools.
3. A *Create new application* window will appear. Fill in your application details. There is no need to enter any URL, and only the first two fields (App title and Short name) can currently be changed later.
4. Click on Create application at the end. Remember that your API hash is secret and Telegram won’t let you revoke it. Don’t post it anywhere!

## Step 2
Edit the configuration and replace the placholders for TG_API_ID and TG_API_HASH with your own API ID and Hash you got from previous step

## Step 3
Click *OPEN WEB UI* in the Info page

## Step 4
Enter your phone number and then the recieved code. You should get the session string.

## Step 5
Edit the configuration and replace the placholder for TG_SESSION with your session string you got from the previous step

# Usage
Edit the configuration and add as many Telegram channels as you like. The "channels" could be telegram bot channels you are subscribed to or even conversations with your Telegram friends. 

The addon will create a binary.sensor for each channel and every time a new message is posted, the sensor will be turned on for 5 seconds
