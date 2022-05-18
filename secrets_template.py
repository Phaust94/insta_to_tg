ACCOUNT_USERNAME = "my.account@gmail.com"   # Email for an instagram account used to spy on people
ACCOUNT_PASSWORD = 'qwertyuiop'     # Password for the instagram account
TARGETS = {
    232192182: "therock"
}
# Dictionary of user ID to username in Instagram.
# Username is just instagram handle in the URL, and user ID you may find as follows:
# 1. Open target page in Instagram desktop
# The page has to be accessible when opened from ACCOUNT_USERNAME account
# 2. Refresh the page
# 3. Right-click, then cLick "Inspect" in Chrome  anywhere
# 4. Search for "window._sharedData = {....}" and copy that big piece of code inside curly brackets
# 5. In that code, search for "owner". You will find a piece that looks like this:
# "owner":{"id":"232192182","username":"therock"}. That number in "id": "<ACTUAL_ID>" is the ID you are looking for.
API_KEY = '000000BJHDSFJHDSFJDNFJIDNSFIJDS'
# Telegram bot API key. You get it when you register a new bot with @BotFather in Telegram.
TG_TARGET = 7773443111
# The ID of the chat used to send data to. Usually it's your TG ID.
# You can find id by forwarding any message from that person to @username_to_id_bot bot in TG.
