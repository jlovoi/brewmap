import json


class Beer:
    def __init__(self):
        # Creates an 'empty' beer with all characteristics defined as 0
        # Create the beer's characteristic dict
        self.review = {}

        # Add Characteristics to beer's review dict
        self.review['name'] = 'N/A'
        self.review['review_id'] = 0  # Unique ID for specific review
        self.review['weight'] = 0  # 1 (Light) to 10 (Heavy)
        self.review['color'] = 0  # 1 (Light) to 10 (Dark)
        self.review['profile'] = 0  # 1 (Malty/Sweet) to 10 (Hoppy/Bitter)
        self.review['fruit'] = 0  # 1 (Not Fruity At All) to 10 (Extremely Fruity)
        self.review['sour'] = 0  # 1 (Not Sour At All) to 10 (Extremely Sour)
        self.review['roast'] = 0  # 1 (Not Roasty At All) to 10 (Extremely Roasty)
        self.review['rating'] = 0  # 1 (HATE) to 10 (LOVE)

        # Fetch the review_count from brewmaps.json, set this review_id
        with open('review_count.json') as f:
            brewmaps_data = json.load(f)
        # Increment review_count, set this review_id
        brewmaps_data['review_count'] += 1
        self.review['review_id'] = brewmaps_data['review_count']
        with open('review_count.json', 'w') as f:
            json.dump(brewmaps_data, f)

    def new_review(self, userid, beer_name):
        # takes user input to characterize the beer, then writes to .json file
        # Check if the beer being reviewed is already in data
        # Use the name in database if similar name is used, and user confirms this is the beer they are reviewing
        with open('beer_reviews.json') as f:
            try:
                beer_data = json.load(f)
            except ValueError:  # In case the json file is empty
                beer_data = {userid: ''}

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
                    self.review['name'] = i
                    break
            elif response != 'y':
                self.review['name'] = beer_name

        self.review['weight'] = int(raw_input("How heavy is the beer? (1 for light, 10 for heavy)\n"))
        self.review['color'] = int(raw_input("Describe the color. (1 for light, 10 for dark)\n"))
        self.review['profile'] = int(raw_input("What is the profile? (1 for Malty/Sweet, 10 for Hoppy/Bitter)\n"))
        self.review['fruit'] = int(raw_input("Is the beer fruity? (1 for not at all, 10 for extremely fruity)\n"))
        self.review['sour'] = int(raw_input("How sour is the beer? (1 for not at all, 10 for extremely sour)\n"))
        self.review['roast'] = int(raw_input("Is the beer roasty? (1 for not at all, 10 for extremely roasty)\n"))
        self.review['rating'] = int(raw_input("Rate the beer from 1 to 10.\n"))

        return self.review

    def write_data(self, data):
        # Write info to .json file
        with open('beer_data.json') as f:
            beer_data = json.load(f)
            beer_data.update(data)
        with open('beer_data.json', 'w') as f:
            json.dump(beer_data, f)


class User:
    def __init__(self):
        # Creates a user profile, with a 'reviews' list, containing all of their respective 'beer' dictionaries
        self.userid = 0
        self.reviews = []
        self.username = ""

    def sign_in(self):
        # Check to see if user exists, use their id number if true, else call sign_up()
        with open('brewmap_users.json') as f:
            brewmap_users = json.load(f)
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
        with open('beer_reviews.json') as f:
            beer_reviews = json.load(f)
        for key, val in beer_reviews.items():
            if key == str(self.userid):
                self.reviews = val
                break

    def sign_up(self):
        # Create new user
        new_user = raw_input("That username is not found, please enter your first and fast name again: ").lower()
        with open('brewmap_users.json') as f:
            brewmap_users = json.load(f)
        self.userid = brewmap_users.len() + 2
        self.username = new_user
        print("Successfully created user: " + new_user.title())

        # add them to brewmap_users dictionary
        brewmap_users[self.username] = self.userid

        with open('brewmap_users.json', 'w') as f:
            json.dump(brewmap_users, f)
        print("Successfully added user to data...")

    def user_review(self):
        # User reviews a new beer, calling new_review()
        beer_name = raw_input("What is the name of the beer?\n").lower()

        beer = Beer()
        beer = beer.new_review(self.userid, beer_name)
        self.reviews.append(beer)

        self.add_review()

        # Update this beer's BrewMap with the review
        brewmap = BrewMap(beer['name'])
        brewmap.update(beer)

    def add_review(self):
        # Add the updated list of user reviews to beer_reviews.json
        with open('beer_reviews.json') as f:
            beer_reviews = json.load(f)
            beer_reviews[str(self.userid)] = self.reviews
        with open('beer_reviews.json', 'w') as f:
            json.dump(beer_reviews, f)

class BrewMap:
    def __init__(self, beer_name):
        # A BrewMap is the aggregated data for a specific beer
        self.name = beer_name
        self.data = {}

        # Pull data from brewmaps.json
        with open('brewmaps.json') as f:
            brewmaps = json.load(f)

        for key, val in brewmaps.items():
            if key == self.name:
                self.data['weight'] = val['weight']
                self.data['color'] = val['color']
                self.data['profile'] = val['profile']
                self.data['fruit'] = val['fruit']
                self.data['sour'] = val['sour']
                self.data['roast'] = val['roast']
                self.data['rating'] = val['rating']
                self.data['count'] = val['count']

    def update(self, beer_review):
        # Multiply data by count
        self.data['weight'] *= self.data['count']
        self.data['color'] *= self.data['count']
        self.data['profile'] *= self.data['count']
        self.data['fruit'] *= self.data['count']
        self.data['sour'] *= self.data['count']
        self.data['roast'] *= self.data['count']
        self.data['rating'] *= self.data['count']
        # Add review data
        self.data['weight'] += beer_review['weight']
        self.data['color'] += beer_review['color']
        self.data['profile'] += beer_review['profile']
        self.data['fruit'] += beer_review['fruit']
        self.data['sour'] += beer_review['sour']
        self.data['roast'] += beer_review['roast']
        self.data['rating'] += beer_review['rating']
        self.data['count'] += 1

        # Now average all the attributes now that every review has been accounted for
        self.data['weight'] /= self.data['count']
        self.data['color'] /= self.data['count']
        self.data['profile'] /= self.data['count']
        self.data['fruit'] /= self.data['count']
        self.data['sour'] /= self.data['count']
        self.data['roast'] /= self.data['count']
        self.data['rating'] /= self.data['count']

        # Update brewmaps.json
        with open('brewmaps.json') as f:
            brewmaps = json.load(f)
            brewmaps[self.name] = self.data
        with open('brewmaps.json', 'w') as f:
            json.dump(brewmaps, f)