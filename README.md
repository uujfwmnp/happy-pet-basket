# happy-pet-basket
Interacts with Blizzard US WoW API to build a list of a friend's missing pets, that you own.

### Requirements
* Python 3.4 or better
* Requests module (`pip install requests`)
* Client access to the [Blizzard API](https://develop.battle.net/access)

### Usage
* Edit lines 5 and 6 to fill out the client ID and client secret for API authentication.
* Edit lines 8 and 9 to point to your server and character name.
* Edit lines 11 and 12 to point to your target server and character name.
* Edit line 14 if you need to change the region (default US, can be US, EU, KR, TW).
* When the script finishes running, it will output the results to both the screen and to a text file in the same directory as the script.
