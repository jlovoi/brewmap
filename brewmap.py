from brewmap_classes import Beer, User

def main():
	run = 'y'
	while run == 'y':
		run = raw_input("Enter new beer? (y/n)\n")
		if run == 'y':
			user = User()
			user.sign_in()
			user.user_review()

main()
beer = Beer()
