import json


class Beer:
    def __init__(self):
        # Creates an 'empty' beer with all characteristics defined as 0
        # Create the beer's characteristic dict
        self.char = {}

        # Add Characteristics to beer's char dict
        self.char['name'] = 'N/A'
        self.char['user'] = 0  # User ID number
        self.char['weight'] = 0  # 1 (Light) to 10 (Heavy)
        self.char['color'] = 0  # 1 (Light) to 10 (Dark)
        self.char['profile'] = 0  # 1 (Malty/Sweet) to 10 (Hoppy/Bitter)
        self.char['fruit'] = 0  # 1 (Not Fruity At All) to 10 (Extremely Fruity)
        self.char['sour'] = 0  # 1 (Not Sour At All) to 10 (Extremely Sour)
        self.char['roast'] = 0  # 1 (Not Roasty At All) to 10 (Extremely Roasty)
        self.char['rating'] = 0  # 1 (HATE) to 10 (LOVE)

    def new_beer(self, userid, beer_name):
        # takes user input to characterize the beer, then writes to .json file
        self.char['user'] = userid

        # Check if the beer being reviewed is already in data
        # Use the name already in database if similar name is used, and user confirms this is the beer they are reviewing
        with open('beer_reviews.json') as file:
            try:
                beer_data = json.load(file)
            except ValueError:  # In case the json file is empty
                beer_data = {0: ''}

        # gather keys of beer names, store in list 'beer_names'
        beer_names = []
        for key, val in beer_data.items():
            for i in val:
                if not i['name'] in beer_names:
                    beer_names.append(i['name'])
        response = 'n'

        # check if this beer has already been reviewed. if so, use same name to avoid duplicates
        for i in beer_names:
            if beer_name in i or i in beer_name:
                response = raw_input(i.title() + ' is already in our data. Is this the same beer? (y/n)\n').lower()
                if response != 'y':
                    continue
                else:
                    self.char['name'] = i
                    break
            elif response != 'y':
                self.char['name'] = beer_name

        self.char['weight'] = int(raw_input("How heavy is the beer? (1 for light, 10 for heavy)\n"))
        self.char['color'] = int(raw_input("Describe the color. (1 for light, 10 for dark)\n"))
        self.char['profile'] = int(raw_input("What is the profile? (1 for Malty/Sweet, 10 for Hoppy/Bitter)\n"))
        self.char['fruit'] = int(raw_input("Is the beer fruity? (1 for not at all, 10 for extremely fruity)\n"))
        self.char['sour'] = int(raw_input("How sour is the beer? (1 for not at all, 10 for extremely sour)\n"))
        self.char['roast'] = int(raw_input("Is the beer roasty? (1 for not at all, 10 for extremely roasty)\n"))
        self.char['rating'] = int(raw_input("Rate the beer from 1 to 10.\n"))

        return self.char

    def write_data(self, data):
        # Write info to .json file
        with open('beer_data.json') as file:
            beer_data = json.load(file)
            beer_data.update(data)
        with open('beer_data.json', 'w') as file:
            json.dump(beer_data, file)


class User:
    def __init__(self):
        # Creates a user profile, with a 'reviews' list, containing all of their respective 'beer' dictionaries
        self.userid = 0
        self.reviews = []
        self.username = ""

    def sign_in(self):
        # Check to see if user exists, use their id number if true, else call sign_up()
        with open('brewmap_users.json') as file:
            brewmap_users = json.load(file)
        username = raw_input("Enter first and last name: ").lower()
        for key, val in brewmap_users.items():
            if username == key:
                self.userid = val
                print("Successfully logged in as " + key.title())
                break

        # If user is not found, make a new one
        if self.userid == 0:
            self.sign_up()

        # Update beer_reviews.json with new beer review
        with open('beer_reviews.json') as file:
            beer_reviews = json.load(file)
        for key, val in beer_reviews.items():
            if key == str(self.userid):
                self.reviews = val
                break

    def sign_up(self):
        # Create new user
        new_user = raw_input("That username is not found, please enter your first and fast name again: ").lower()
        self.userid = brewmap_users.len() + 2
        self.username = new_user
        print("Successfully created user: " + new_user.title())

        # add them to brewmap_users dictionary
        with open('brewmap_users.json') as file:
            brewmap_users = json.load(file)
            brewmap_users[self.username] = self.userid
        with open('brewmap_users.json', 'w') as file:
            json.dump(brewmap_users, file)
        print("Successfully added user to data...")

    def user_review(self):
        # User reviews a new beer, calling new_beer()
        beer_name = raw_input("What is the name of the beer?\n").lower()

        beer = Beer()
        beer = beer.new_beer(self.userid, beer_name)
        self.reviews.append(beer)

        self.add_review()
        self.add_brewmap(beer['name'])

    def add_review(self):
        # Add the updated list of user reviews to beer_reviews.json
        with open('beer_reviews.json') as file:
            beer_reviews = json.load(file)
            beer_reviews[str(self.userid)] = self.reviews
        with open('beer_reviews.json', 'w') as file:
            json.dump(beer_reviews, file)

    def add_brewmap(self, beer_name):
        brewmap = BrewMap(beer_name)
        # Add this object to brewmaps.json
        with open('brewmaps.json') as file:
            try:
                brewmaps = json.load(file)
                if beer_name in brewmaps:
                    brewmaps.remove(beer_name)
                    brewmaps.append(brewmap)
                with open('brewmaps.json', 'w') as file:
                    json.dump(brewmaps, file)
            except ValueError:
                with open('brewmaps.json', 'w') as file:
                    json.dump(brewmap, file)


class BrewMap:  # Need to find a way to store these objects - not serializable in json
    def __init__(self, beer_name):
        # A BrewMap is the aggregated data for a specific beer
        self.name = beer_name
        self.weight = 0
        self.color = 0
        self.profile = 0
        self.fruit = 0
        self.sour = 0
        self.roast = 0
        self.rating = 0
        self.count = 0

    def update(self):
        # Find all beer reviews for this specific beer, pull all data
        with open('beer_reviews.json') as file:
            beer_reviews = json.load(file)
        for key, val in brewmaps.items():
            for i in val.len():
                if i['name'] == self.name:
                    self.weight += i['weight']
                    self.color += i['color']
                    self.profile += i['profile']
                    self.fruit += i['fruit']
                    self.sour += i['sour']
                    self.roast += i['roast']
                    self.rating += i['rating']
                    self.count += 1

        # Now average all the attributes now that every review has been accounted for
        self.weight = self.weight / self.count
        self.color = self.color / self.count
        self.profile = self.profile / self.count
        self.fruit = self.fruit / self.count
        self.sour = self.sour / self.count
        self.roast = self.roast / self.count
        self.rating = self.rating / self.count
