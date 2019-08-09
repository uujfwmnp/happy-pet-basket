import requests
import json

# Blizzard API Client Credentials
client_id     = 'YOUR-CLIENT-ID'
client_secret = 'YOUR-CLIENT-SECRET'
# Your Server & Character
myServer    = 'Server-Name'   # Spaces must convert to dashes
myCharacter = 'YourCharacter' # Caps don't matter
# Target Server & Character
targetServer    = 'Server-Name'
targetCharacter = 'YourCharacter'
# Server Region
region = 'us' # this can be us, eu, kr, tw

# Obtain Blizzard API Authorization Token
headers = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
}
auth = requests.post('https://'+region+'.battle.net/oauth/token', data=headers)
token = json.loads(auth.text)

# Function to request data from Blizzard, and then load the returned text string as JSON list
def dataRequest(region,server,character,token):
    get = requests.get('https://'+region+'.api.blizzard.com/wow/character/'+server+'/'+character+'?fields=pets&locale=en_US&access_token='+token['access_token'])
    if (get.status_code == 401): # Error handling: Invalid access token!
        exit('Error During Run: ' + get['reason'])
    else:
        dataRequest = json.loads(get.text)
    if ('status' in dataRequest.keys()): # The 'status' key only appears when the character or server is misspelled or missing.
        exit('Error Obtaining Data For ' + character + ' ' +server + ': ' + dataRequest['reason'])
    else:
        return dataRequest

# Setting up variables to call the dataRequest function for each character
myData = dataRequest(region,myServer,myCharacter,token)
targetData = dataRequest(region,targetServer,targetCharacter,token)

# Setup empty list, loop through the 'myRawPets' array variable, and append Creature Names to the empty list
myPets = []
myRawPets = myData['pets']['collected']
for i in range(0, len(myRawPets)):
    myPets.append(myRawPets[i]['creatureName'])

# Setup empty list, loop through the 'targetRawPets' array variable, and append Creature Names to the empty list
targetPets = []
targetRawPets = targetData['pets']['collected']
for i in range(0, len(targetRawPets)):
    targetPets.append(targetRawPets[i]['creatureName'])

# Result of comparing my pets vs target pets, set as variable, and sorted alphabetically
result = list(set(myPets) - set(targetPets))
result.sort(key=str.lower)

# Creating and writing to a text file, to list the missing pets
file = open(myCharacter+' vs '+targetCharacter+'.txt','w+')
file.write('These are the pets that "'+targetCharacter+'-'+targetServer+'" is missing. You have have at least one of each pet in this list:\n\n')

# A nice screen printing of the results, making sure to also write the results into the text file
for i in range(0, len(result)):
    print(result[i])
    file.write(result[i]+'\n')

# Closing the newly created file
file.close()
