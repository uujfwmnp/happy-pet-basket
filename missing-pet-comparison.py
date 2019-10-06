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
def data_request(region,server,character,token):
    get = requests.get('https://'+region+'.api.blizzard.com/wow/character/'+server+'/'+character+'?fields=pets&access_token='+token['access_token'])
    if (get.status_code == 401): # Error handling: Invalid access token!
        exit('Error During Run: ' + get['reason'])
    else:
        data_request = json.loads(get.text)
    if ('status' in data_request.keys()): # The 'status' key only appears when the character or server is misspelled or missing.
        exit('Error Obtaining Data For ' + character + ' ' +server + ': ' + data_request['reason'])
    else:
        return data_request

# Setup empty list, loop through the target array variable, and append Creature Names to the empty list
def pet_list(target):
    pets = []
    for i in range(0, len(target)):
        pets.append(target[i]['creatureName'])
    return pets

# Setting up variables to call the data_request function for each character
myData = data_request(region,myServer,myCharacter,token)
targetData = data_request(region,targetServer,targetCharacter,token)

# Calling the pet_list() function to get the collected data for each character
myPets = pet_list(myData['pets']['collected'])
targetPets = pet_list(targetData['pets']['collected'])

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
