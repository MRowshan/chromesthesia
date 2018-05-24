from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.http import HttpResponse, JsonResponse, Http404
from .models import User, Colour, Sound, AttemptOne, AttemptTwo
import hashlib
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

# ============ Table of Contents ============
# 1 - admin                     - line 31
# 2 - if not logged in          - line 123
# 3 - if logged in              - line 141
# 3.1 - AttemptOne(A)           - line 164
# 3.2 - AttemptTwo(B)           - line 274
# 4 - login/signup/edit         - line 385
# 5 - sending colour/sound data - line 564
# 6 - results page              - line 678
# ===========================================


# Decorator function, mark user as logged in
def loggedin(f):
    def test(request):
        if 'email' in request.session:
            return f(request)
        else:
            return render(request, 'base.html')
    return test

# ====================================================================================================================
                                            # admin
@loggedin
def adminpage(request):
    e = request.session['email']
    if e == 'mustakimrowshan@icloud.com':
        getusers = User.objects.all().values_list('email', flat=True)
        for x in getusers:
            getAOne = AttemptOne.objects.all().values_list('colourOne', flat=True)
            getATwo = AttemptTwo.objects.all().values_list('colourTwo', flat=True)
        return render(request, 'admin/admin.html', {'loggedin': True, 'getusers': getusers, 'getAOne': getAOne, 'getATwo': getATwo})
    else:
        fname = request.session['firstname']
        e = request.session['email'] # Get email from session
        getuser = AttemptTwo.objects.filter(userTwo=e).count() # Count how many times an email appears in the AttemptTwo table
        checkAttemptOne = AttemptOne.objects.filter(userOne=e).count() # Count how many times an email appears in the AttemptOne table
        attemptcheck = "Incomplete" # Initialise variable to incomplete, results button should default to unavailable
        if checkAttemptOne == 18 and getuser == 18: # If attempt one and two are completed assign "Complete" to attemptcheck
            attemptcheck = "Complete"
        else:
            attemptcheck = "Incomplete"
        return render(request, 'home.html', {'attemptcheck': attemptcheck, 'firstname': fname, 'email': e, 'loggedin': True})

@loggedin
def getcolour(request):
    ue = request.POST.get('ue')
    request.session['uemail'] = ue
    # Get colourOne tuples(rows) from table where the column userOne = email
    aOne = AttemptOne.objects.filter(userOne=ue).values_list('colourOne', flat=True)
    # Get colourTwo tuples(rows) from table where the column userTwo = email
    aTwo = AttemptTwo.objects.filter(userTwo=ue).values_list('colourTwo', flat=True)
    percent = 0 # Initialise percent variable
    # For each entry in table one and two
    # zip() ends the for loop at the shortest table (when there are no more entries in a table)
    for colOne, colTwo in zip(aOne, aTwo):
        # If the two colour values match from both tables
        if colOne == colTwo:
            # Add value to the percent variable
            # This value is equal to (1/18)*100 to 11 decimal places
            percent += 5.55555555556
    # Round the final result to 3 decimal places using the round(value, decimal places) method
    percent = round(percent, 3)
    getresultsOne = AttemptOne.objects.filter(userOne=ue).values_list('colourOne', flat=True)
    getresultsTwo = AttemptTwo.objects.filter(userTwo=ue).values_list('colourTwo', flat=True)
    # Pass the value to the page
    return render(request, 'admin/adminResults.html', {'firstname': ue, 'percent': percent, 'getresultsOne': getresultsOne, 'getresultsTwo': getresultsTwo, 'loggedin': True})

# Main results page
@loggedin
def adminresults(request):
    ue = request.session['uemail'] # Get email from session
    # Get colourOne tuples(rows) from table where the column userOne = email
    aOne = AttemptOne.objects.filter(userOne=ue).values_list('colourOne', flat=True)
    # Get colourTwo tuples(rows) from table where the column userTwo = email
    aTwo = AttemptTwo.objects.filter(userTwo=ue).values_list('colourTwo', flat=True)
    percent = 0 # Initialise percent variable
    # For each entry in table one and two
    # zip() ends the for loop at the shortest table (when there are no more entries in a table)
    for colOne, colTwo in zip(aOne, aTwo):
        # If the two colour values match from both tables
        if colOne == colTwo:
            # Add value to the percent variable
            # This value is equal to (1/18)*100 to 11 decimal places
            percent += 5.55555555556
    # Round the final result to 3 decimal places using the round(value, decimal places) method
    percent = round(percent, 3)
    getresultsOne = AttemptOne.objects.filter(userOne=ue).values_list('colourOne', flat=True)
    getresultsTwo = AttemptTwo.objects.filter(userTwo=ue).values_list('colourTwo', flat=True)
    # Pass the value to the page
    return render(request, 'admin/adminResults.html', {'firstname': ue, 'percent': percent, 'getresultsOne': getresultsOne, 'getresultsTwo': getresultsTwo, 'loggedin': True})

# Attempt One results page
@loggedin
def adminattemptoneResults(request):
    ue = request.session['uemail'] # Get email from session
    # Get colourOne tuples(rows) from table where the column userOne = email
    # 'flat=True' returns a list of values rather than a list of tuples
    getresults = AttemptOne.objects.filter(userOne=ue).values_list('colourOne', flat=True)
    # Send the list of colours to the page
    return render(request, 'admin/aOne.html', {'getresults': getresults, 'loggedin': True})

# Attempt Two results page
@loggedin
def adminattempttwoResults(request):
    ue = request.session['uemail'] # Get email from session
    # Get colourTwo tuples(rows) from table where the column userTwo = email
    # 'flat=True' returns a list of values rather than a list of tuples
    getresults = AttemptTwo.objects.filter(userTwo=ue).values_list('colourTwo', flat=True)
    # Send the list of colours to the page
    return render(request, 'admin/aTwo.html', {'getresults': getresults, 'loggedin': True})


# ====================================================================================================================
                                            # if not logged in
# Welcome page (first page when user visits site)
def welcome(request):
    # If user email exists in session (logged in), then keep them logged in
    if request.session.get('email'):
        return render(request, 'welcome.html', {'loggedin': True})
    else:
        return render(request, 'welcome.html')

# Home page / Purpose of application tab
def index(request):
    return render(request, 'home.html')

# Sound page 0 if not logged in
def sound0(request):
    return render(request, 'sound/sound0.html')

# ====================================================================================================================
                                            # if logged in
# Home page if logged in
@loggedin
def userhome(request):
    fname = request.session['firstname']
    e = request.session['email'] # Get email from session
    getuser = AttemptTwo.objects.filter(userTwo=e).count() # Count how many times an email appears in the AttemptTwo table
    checkAttemptOne = AttemptOne.objects.filter(userOne=e).count() # Count how many times an email appears in the AttemptOne table
    attemptcheck = "Incomplete" # Initialise variable to incomplete, results button should default to unavailable
    if checkAttemptOne == 18 and getuser == 18: # If attempt one and two are completed assign "Complete" to attemptcheck
        attemptcheck = "Complete"
    else:
        attemptcheck = "Incomplete"
    return render(request, 'home.html', {'attemptcheck': attemptcheck, 'firstname': fname, 'email': e, 'loggedin': True})

# Sound page 0 if logged in
@loggedin
def usersound0(request):
    sound = Sound.objects.get(pk=1)
    sid = sound.soundID
    return render(request, 'sound/sound0.html', {'sid': sid, 'loggedin': True}) 

                                            # AttemptOne(A)
# Sound pages 1-18 for Attempt A
@loggedin
def sound1A(request):
    sound = Sound.objects.get(pk=2) # Store database row where the pk=2 into variable sound
    sid = sound.soundID # Store soundID from database row into sid
    return render(request, 'sound/soundA/sound1A.html', {'sid': sid, 'loggedin': True}) # Load page and pass variables

@loggedin
def sound2A(request):
    sound = Sound.objects.get(pk=3)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound2A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound3A(request):
    sound = Sound.objects.get(pk=4)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound3A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound4A(request):
    sound = Sound.objects.get(pk=5)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound4A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound5A(request):
    sound = Sound.objects.get(pk=6)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound5A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound6A(request):
    sound = Sound.objects.get(pk=7)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound6A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound7A(request):
    sound = Sound.objects.get(pk=8)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound7A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound8A(request):
    sound = Sound.objects.get(pk=9)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound8A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound9A(request):
    sound = Sound.objects.get(pk=10)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound9A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound10A(request):
    sound = Sound.objects.get(pk=11)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound10A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound11A(request):
    sound = Sound.objects.get(pk=12)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound11A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound12A(request):
    sound = Sound.objects.get(pk=13)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound12A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound13A(request):
    sound = Sound.objects.get(pk=14)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound13A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound14A(request):
    sound = Sound.objects.get(pk=15)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound14A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound15A(request):
    sound = Sound.objects.get(pk=16)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound15A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound16A(request):
    sound = Sound.objects.get(pk=17)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound16A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound17A(request):
    sound = Sound.objects.get(pk=18)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound17A.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound18A(request):
    sound = Sound.objects.get(pk=19)
    sid = sound.soundID
    return render(request, 'sound/soundA/sound18A.html', {'sid': sid, 'loggedin': True})

                                            # AttemptTwo(B)
# Sound pages 1-18 for Attempt B
@loggedin
def sound1B(request):
    sound = Sound.objects.get(pk=2) # Store database row where the pk=2 into variable sound
    sid = sound.soundID # Store soundID from database row into sid
    return render(request, 'sound/soundB/sound1B.html', {'sid': sid, 'loggedin': True}) # Load page and pass variables

@loggedin
def sound2B(request):
    sound = Sound.objects.get(pk=3)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound2B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound3B(request):
    sound = Sound.objects.get(pk=4)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound3B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound4B(request):
    sound = Sound.objects.get(pk=5)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound4B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound5B(request):
    sound = Sound.objects.get(pk=6)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound5B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound6B(request):
    sound = Sound.objects.get(pk=7)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound6B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound7B(request):
    sound = Sound.objects.get(pk=8)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound7B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound8B(request):
    sound = Sound.objects.get(pk=9)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound8B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound9B(request):
    sound = Sound.objects.get(pk=10)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound9B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound10B(request):
    sound = Sound.objects.get(pk=11)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound10B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound11B(request):
    sound = Sound.objects.get(pk=12)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound11B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound12B(request):
    sound = Sound.objects.get(pk=13)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound12B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound13B(request):
    sound = Sound.objects.get(pk=14)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound13B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound14B(request):
    sound = Sound.objects.get(pk=15)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound14B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound15B(request):
    sound = Sound.objects.get(pk=16)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound15B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound16B(request):
    sound = Sound.objects.get(pk=17)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound16B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound17B(request):
    sound = Sound.objects.get(pk=18)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound17B.html', {'sid': sid, 'loggedin': True})

@loggedin
def sound18B(request):
    sound = Sound.objects.get(pk=19)
    sid = sound.soundID
    return render(request, 'sound/soundB/sound18B.html', {'sid': sid, 'loggedin': True})

# ====================================================================================================================
                                            # login/signup/edit

# Hash password from input
def hash_password(password):
    # Salting the password to make it harder to decode
    s1 = 'hqb%$t'
    s2 = 'cg*l'
    # Using sha256 to encrypt the password with added salt
    return hashlib.sha256(s1.encode() + password.encode()).hexdigest() + ':' + s2

def verify(request):
    return render(request, 'verify.html')

# Signup page
def signup(request):
    if 'email' not in request.POST: # If no email is found, go to signup page
        return render(request, 'signup.html')
    else:
        e = request.POST['email'] # Get email from session
        try:
            e = User.objects.get(pk=e) # Store row into variable e if the email exists into the table
            error = "An account with this email already exists" # Error message
            return render(request, 'signup.html', {'error': error}) # If email exists, load the page with error message
        except User.DoesNotExist: # If user does not exist in try statement, create user
            # .strip() method to remove blank spaces on the left and right
            # .title() method to capitalise first letter of the name
            p  = request.POST['password'].strip() # Get password from page
            p  = hash_password(p) # Hash password
            e  = request.POST['email'].strip() # Get email from page
            fn = request.POST['firstname'].strip().title() # Get firstname from page
            sn = request.POST['surname'].strip().title() # Get surname from page
            a  = request.POST['age'].strip() # Get age from page
            g  = request.POST['gender'].strip() # Get gender from page
            dh = request.POST['dominanthand'].strip() # Get dominanthand from page
            # Update user table with new information
            u  = User(email=e, firstname=fn, age=a, gender=g, dominanthand=dh, surname=sn, password=p) 
            u.save()
            # Add email and firstname to session
            request.session['email'] = e;
            request.session['firstname'] = fn;
            getuser = AttemptTwo.objects.filter(userTwo=e).count() # Count how many times an email appears in the AttemptTwo table
            checkAttemptOne = AttemptOne.objects.filter(userOne=e).count() # Count how many times an email appears in the AttemptOne table
            attemptcheck = "Incomplete" # Initialise variable to incomplete, results button should default to unavailable
            if checkAttemptOne == 18 and getuser == 18: # If attempt one and two are completed assign "Complete" to attemptcheck
                attemptcheck = "Complete"
            else:
                attemptcheck = "Incomplete"
            return render(request, 'home.html', {'attemptcheck': attemptcheck, 'firstname': fn, 'email': e, 'loggedin': True})

# Login page
def login(request):
    if 'email' not in request.POST: # If no email is found, go to login page
        return render(request, 'login.html')
    else: # If user has entered an email, log them in
        e = request.POST['email'] # Get email from page
        p = request.POST['password'] #Get password from page
        try: # Check if email exists in database
            u = User.objects.get(pk=e)
            p = hash_password(p) # Encrypt password from input
            # Check if password from input and database match 
            if p == u.password: 
                # Add email and name to session
                request.session['email'] = e;
                request.session['firstname'] = u.firstname;
                fname = request.session['firstname']
                e = request.session['email'] # Get email from session
                getuser = AttemptTwo.objects.filter(userTwo=e).count() # Count how many times an email appears in the AttemptTwo table
                checkAttemptOne = AttemptOne.objects.filter(userOne=e).count() # Count how many times an email appears in the AttemptOne table
                attemptcheck = "Incomplete" # Initialise variable to incomplete, results button should default to unavailable
                if checkAttemptOne == 18 and getuser == 18: # If attempt one and two are completed assign "Complete" to attemptcheck
                    attemptcheck = "Complete"
                else:
                    attemptcheck = "Incomplete"
                return render(request, 'home.html', {'attemptcheck': attemptcheck, 'firstname': fname, 'email': e, 'loggedin': True})
            # If password doesn't match
            else:
                error = "Incorrect Username or Password" # Error message to be passed to login page
                return render(request, 'login.html', {'error': error})
        except User.DoesNotExist: # If email doesn't exist in database 
                error = "Incorrect Username or Password" # Error message to be passed to login page
                return render(request, 'login.html', {'error': error})

# Logout page
def logout(request):
    if 'email' in request.session: # If email found in session
        e = request.session['email']
        request.session.flush() # Flush session of all information
        return render(request, 'login.html') # Load login page
    else: # If no email is found in session
        return render(request, 'home.html') # Redirect user to home page

# Edit profile page
def editProfile(request):
    e = request.session['email'] # Get email from session
    u = User.objects.get(pk=e) # Get other information for that email
    # Store information about user into variables
    fn = u.firstname
    sn = u.surname
    age = u.age
    dh = u.dominanthand
    g = u.gender
    # Pass variables to the page
    return render(request, 'editProfile.html', {'email': e, 'firstname': fn, 'surname': sn, 'age': age, 'dominanthand': dh, 'gender': g})

# Update Firstname
def saveFN(request):
    e = request.session['email'] # Get email from session
    fn = request.POST.get('fn') # Get firstname from page input
    request.session['firstname'] = fn # Update session with new firstname variable
    # Find row in database where the pk=email, and update the row named 'firstname' with fn
    User.objects.filter(pk=e).update(firstname=fn)
    # Pass the new firstname to the page
    data = { 'firstname': fn }
    return JsonResponse(data, safe=False)

#Update Surname
def saveSN(request):
    e = request.session['email'] # Get email from session
    sn = request.POST.get('sn') # Get surname from page input
    request.session['surname'] = sn # Update session with new firstname variable
    # Find row in database where the pk=email, and update the row named 'surname' with sn
    User.objects.filter(pk=e).update(surname=sn)
    # Pass the new surname to the page
    data = { 'surname': sn }
    return JsonResponse(data, safe=False)

#Update Age
def saveAge(request):
    e = request.session['email']
    age = request.POST.get('age')
    request.session['age'] = age
    User.objects.filter(pk=e).update(age=age)
    data = { 'age': age }
    return JsonResponse(data, safe=False)

#Update Gender
def saveG(request):
    e = request.session['email']
    gender = request.POST.get('g')
    request.session['gender'] = gender
    User.objects.filter(pk=e).update(gender=gender)
    data = { 'gender': gender }
    return JsonResponse(data, safe=False)

#Update Dominant Hand
def saveDH(request):
    e = request.session['email']
    dh = request.POST.get('dh')
    request.session['dominanthand'] = dh
    User.objects.filter(pk=e).update(dominanthand=dh)
    data = { 'dominanthand': dh }
    return JsonResponse(data, safe=False)

#Update Password
def saveP(request):
    e = request.session['email']
    p = request.POST.get('p')
    p = hash_password(p) # Encrypt password before updating database
    User.objects.filter(pk=e).update(password=p)
    data = { 'password': p }
    return JsonResponse(data, safe=False)

#Check Current Password
def checkP(request):
    e = request.session['email'] 
    u = User.objects.get(pk=e)
    p = request.POST.get('p')
    p = hash_password(p)
    # Check if password enters matches the database password entry
    if p == u.password:
        # If it matches pass the string "correct"
        check = "Correct"
        data = { 'check': check }
    else:
        # Else pass the string "incorrect password"
        check = "Incorrect Password"
        data = { 'check': check }  
    return JsonResponse(data, safe=False)

# ====================================================================================================================
                                            # sending colour/sound data
# Choose attempt page
@loggedin
def chooseAttempt(request):
    fname = request.session['firstname']; # Get firstname from session
    return render(request, 'chooseAttempt.html', {'firstname': fname}) # Pass firstname to page

# Method to check if user has completed attemptone(A)
def checkAttemptA(request):
    e = request.session['email'] # Get email from session
    getuser = AttemptOne.objects.filter(userOne=e).count() # Count how many times an email appears in the AttemptOne table
    if getuser != 18: # If the user doesn't appear 18 times in the table (18 sounds=18 entries per attempt)
        # Load the first sound page
        text = "Continue"
        data = { 'text': text }
        return JsonResponse(data, safe=False)
    else: # Else if the user appears 18 times in the table
        # Send firstname and completed message to the page
        text = "You have completed this attempt, please move on to the next one"
        data = { 'text': text }
        return JsonResponse(data, safe=False)

# Method to check if user has completed attempttwo(B)
def checkAttemptB(request):
    e = request.session['email'] # Get email from session
    getuser = AttemptTwo.objects.filter(userTwo=e).count() # Count how many times an email appears in the AttemptTwo table
    checkAttemptOne = AttemptOne.objects.filter(userOne=e).count() # Count how many times an email appears in the AttemptOne table
    if checkAttemptOne == 18: # If user has completed attemptone (18 entries in AttemptOne table)
        if getuser != 18: # And user has not completed attempttwo (less than 18 entries in AttemptTwo table)
                text = "Continue"
                data = { 'text': text }
                return JsonResponse(data, safe=False)
            # else:
            #     # Load the first sound page
            #     text = "Locked"
            #     data = { 'text': text }
            #     return JsonResponse(data, safe=False)
        else: # Else if the user appears 18 times in the table
            # Send firstname and completed message to the page
            text = "You have completed this attempt. Thank you for participating!"
            data = { 'text': text }
            return JsonResponse(data, safe=False)
    else: # Else if the user hasn't completed attemptone
        # Send name and message to the page
        text = "Please complete Attempt One first"
        data = { 'text': text }
        return JsonResponse(data, safe=False)

# Add colour to AttemptOne table
@loggedin
def sendColourA(request):
    e = request.session['email'] # Get email from session
    sid = request.POST.get('sid') # Get soundID from page
    cid = request.POST.get('cid') # Get colourID from page
    blank = "" # Create a blank variable
    if cid == blank: # If a colour is not selected, default to #ffffff(white)
        cid = "#ffffff" # Set colourID to #ffffff(white)
    try: # Check if user has submitted a result for the sound already
        getdata = AttemptOne.objects.get(userOne=e, soundOne= sid) # Get row where column 'userTwo'=email and 'soundTwo'=soundID   
        if sid == getdata.soundOne: # If soundID from page matches database
            # Replace old colour selection with new one
            attemptupdate = AttemptOne(id=getdata.id, userOne=e, soundOne=sid, colourOne=cid)
            attemptupdate.save()
        else: # Else if the soundID doesn't match
            # Create new entry with user selection
            attemptupdate = AttemptOne(userOne=e, soundOne=sid, colourOne=cid)
            attemptupdate.save()
    except AttemptOne.DoesNotExist: # If user has not submitted a result for the sound already
        # Create new entry with user selection
        attemptupdate = AttemptOne(userOne=e, soundOne=sid, colourOne=cid)
        attemptupdate.save()
    # Send data from table to page
    data = {
        'email': attemptupdate.userOne,
        'sid': attemptupdate.soundOne,
        'cid': attemptupdate.colourOne,
    }
    return JsonResponse(data, safe=False)

# Add colour to AttemptTwo table
@loggedin
def sendColourB(request):
    e = request.session['email'] # Get email from session
    sid = request.POST.get('sid') # Get soundID from page
    cid = request.POST.get('cid') # Get colourID from page
    blank = "" # Create a blank variable
    if cid == blank: # If a colour is not selected, default to #ffffff(white)
        cid = "#ffffff" # Set colourID to #ffffff(white)
    try: # Check if user has submitted a result for the sound already
        getdata = AttemptTwo.objects.get(userTwo=e, soundTwo=sid) # Get row where column 'userTwo'=email and 'soundTwo'=soundID      
        if sid == getdata.soundTwo: # If soundID from page matches database
            # Replace old colour selection with new one
            attemptupdate = AttemptTwo(id=getdata.id, userTwo=e, soundTwo=sid, colourTwo=cid)
            attemptupdate.save()
        else: # Else if the soundID doesn't match
            # Create new entry with user selection
            attemptupdate = AttemptTwo(userTwo=e, soundTwo=sid, colourTwo=cid)
            attemptupdate.save()
    except AttemptTwo.DoesNotExist: # If user has not submitted a result for the sound already
        # Create new entry with user selection
        attemptupdate = AttemptTwo(userTwo=e, soundTwo=sid, colourTwo=cid)
        attemptupdate.save()
    # Send data from table to page
    data = {
        'email': attemptupdate.userTwo,
        'sid': attemptupdate.soundTwo,
        'cid': attemptupdate.colourTwo,
    }
    return JsonResponse(data, safe=False)

# ====================================================================================================================
                                            # results page
# Main results page
@loggedin
def results(request):
    e = request.session['email'] # Get email from session
    fn = request.session['firstname'] # Get email from session
    # Get colourOne tuples(rows) from table where the column userOne = email
    aOne = AttemptOne.objects.filter(userOne=e).values_list('colourOne', flat=True)
    # Get colourTwo tuples(rows) from table where the column userTwo = email
    aTwo = AttemptTwo.objects.filter(userTwo=e).values_list('colourTwo', flat=True)
    percent = 0 # Initialise percent variable
    # For each entry in table one and two
    # zip() ends the for loop at the shortest table (when there are no more entries in a table)
    for colOne, colTwo in zip(aOne, aTwo):
        # If the two colour values match from both tables
        if colOne == colTwo:
            # Add value to the percent variable
            # This value is equal to (1/18)*100 to 11 decimal places
            percent += 5.55555555556
    # Round the final result to 3 decimal places using the round(value, decimal places) method
    percent = round(percent, 3)
    getresultsOne = AttemptOne.objects.filter(userOne=e).values_list('colourOne', flat=True)
    getresultsTwo = AttemptTwo.objects.filter(userTwo=e).values_list('colourTwo', flat=True)
    # Pass the value to the page
    return render(request, 'results/result.html', {'firstname': fn, 'getresultsOne': getresultsOne, 'getresultsTwo': getresultsTwo, 'percent': percent, 'loggedin': True})

# Attempt One results page
@loggedin
def attemptoneResults(request):
    e = request.session['email'] # Get email from session
    # Get colourOne tuples(rows) from table where the column userOne = email
    # 'flat=True' returns a list of values rather than a list of tuples
    getresults = AttemptOne.objects.filter(userOne=e).values_list('colourOne', flat=True)
    # Send the list of colours to the page
    return render(request, 'results/attemptone.html', {'getresults': getresults, 'loggedin': True})

# Attempt Two results page
@loggedin
def attempttwoResults(request):
    e = request.session['email'] # Get email from session
    # Get colourTwo tuples(rows) from table where the column userTwo = email
    # 'flat=True' returns a list of values rather than a list of tuples
    getresults = AttemptTwo.objects.filter(userTwo=e).values_list('colourTwo', flat=True)
    # Send the list of colours to the page
    return render(request, 'results/attempttwo.html', {'getresults': getresults, 'loggedin': True})