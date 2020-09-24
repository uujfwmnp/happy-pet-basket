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
    get = requests.get('https://'+region+'.api.blizzard.com/profile/wow/character/'+server+'/'+character+'/collections/pets?namespace=profile-'+region+'&locale=en_US&access_token='+token['access_token'])
    if (get.status_code == 401):   # Error handling: Invalid access token!
        exit('Error During Run: Invalid Access Token')
    elif (get.status_code == 404): # Error handling: Invalid character or server!
        exit('Error Obtaining Data For ' + character + ' ' +server + ': ' + get.json()['detail']+'\n Check the spelling and try again.')
    else:
        data_request = json.loads(get.text)
        return data_request

# Setup empty list, loop through the target array variable, and append Creature Names to the empty list
def pet_list(target):
    pets = []
    for i in range(0, len(target)):
        pets.append(target[i]['species']['name'])
    return pets

# Setting up variables to call the data_request function for each character
myData = data_request(region,myServer,myCharacter,token)
targetData = data_request(region,targetServer,targetCharacter,token)

# Calling the pet_list() function to get the collected data for each character
myPets = pet_list(myData['pets'])
targetPets = pet_list(targetData['pets'])

# Result of comparing my pets vs target pets, set as variable, duplicates removed, and sorted alphabetically
result = list(set(myPets) - set(targetPets))
result.sort(key=str.lower)

# Creating an output array giving the name of the pet, and the number of each owned (if you have more than 1)
output = {}
for pet_name in result:
    if (myPets.count(pet_name) >= 2):
        output[pet_name] = str(myPets.count(pet_name))

# Creating and writing to a text file, to list the missing pets
file = open(myCharacter+' vs '+targetCharacter+'.txt','w+')
file.write('These are the pets that "'+targetCharacter+'-'+targetServer+'" is missing:\n\n')

# A nice screen printing of the results, making sure to also write the results into the text file
file.write('# Pets Owned'+'\t'+'Pet Name'+'\n')
for name,number in output.items():
    print(number +'\t\t'+ name)
    file.write(number +'\t\t'+ name+'\n')

# Closing the newly created file
file.close()
