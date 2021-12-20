def tweeps():
    
    # Create a list of users to track from the .tweeps file
    tweep = []
    tweepfile = '.tweeps'
    with open(tweepfile, 'r') as t:
        users = t.readlines()
        for user in users:
            user = user.rstrip('\n')
            tweep.append(user)
        t.close()
        print(tweep)
        return tweep
