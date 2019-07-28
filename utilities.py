# Validate the sign-in form data
def is_valid_data(fullname,username,email,phone,password):
    # check if the values are empty
    if not (fullname.strip() and username.strip() and email.strip() and phone.strip() and password.strip()):
        return "Please fill out the form completely"
    # check if user already exists with that username
    elif User.query.filter_by(username=username).all() :
        return "A user already exists with the given username"
    # check if user already exists with the same email number
    elif User.query.filter_by(email=email).all() :
        return "A user already exists with the given email"
        # check if user already exists with that phone
    elif User.query.filter_by(phone=phone).all() :
        return "A user already exists with the given phone"
    # Passed all test cases
    else:
        return 1
