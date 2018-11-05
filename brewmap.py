from brewmap_classes import BeerReview, User

def main():
	run = 'y'
	while run == 'y':
		run = raw_input("Review a beer? (y/n)\n")
		if run == 'y':
			user = User()
			user.sign_in()
			user.user_review()


main()
