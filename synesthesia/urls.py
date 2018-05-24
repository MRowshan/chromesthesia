from django.conf.urls import url, include
from . import views
import uuid

app_name = 'synesthesia'
urlpatterns = [

# ====================================================================================================================
                                            # admin

    url(r'^adminpage/$', views.adminpage, name='adminpage'), #admin page
    url(r'^getcolour/$', views.getcolour, name='getcolour'), #getcolour page
    url(r'^adminresults/$', views.adminresults, name='adminresults'), #admin results page
    url(r'^adminattemptoneResults/$', views.adminattemptoneResults, name='adminattemptoneResults'), #admin attempt one page
    url(r'^adminattempttwoResults/$', views.adminattempttwoResults, name='adminattempttwoResults'), #admin attempt two page
# ====================================================================================================================
                                            # if not logged in

    url(r'^$', views.welcome, name='welcome'), #welcome page
    url(r'^home/$', views.index, name='index'), #home page/tab on home page
    url(r'^sound0/$', views.sound0, name='sound0'), #tuba-c3 (EXAMPLE)

# ====================================================================================================================
                                            # if logged in

    url(r'^userhome/$', views.userhome, name='userhome'), #home page if logged in
    url(r'^usersound0/$', views.usersound0, name='usersound0'), #tuba-c3 (EXAMPLE)

                                            #AttemptOne(A)
    url(r'^sound1A/$',  views.sound1A,  name='sound1A'), #classic-clean-c5
    url(r'^sound2A/$',  views.sound2A,  name='sound2A'), #classic-clean-c2
    url(r'^sound3A/$',  views.sound3A,  name='sound3A'), #classic-clean-c0

    url(r'^sound4A/$',  views.sound4A,  name='sound4A'), #classic-electric-piano-c6
    url(r'^sound5A/$',  views.sound5A,  name='sound5A'), #classic-electric-piano-c3
    url(r'^sound6A/$',  views.sound6A,  name='sound6A'), #classic-electric-piano-c0

    url(r'^sound7A/$',  views.sound7A,  name='sound7A'), #full-brass-c6
    url(r'^sound8A/$',  views.sound8A,  name='sound8A'), #full-brass-c3
    url(r'^sound9A/$',  views.sound9A,  name='sound9A'), #full-brass-c0

    url(r'^sound10A/$', views.sound10A, name='sound10A'), #grand-organ-c6
    url(r'^sound11A/$', views.sound11A, name='sound11A'), #grand-organ-c3
    url(r'^sound12A/$', views.sound12A, name='sound12A'), #grand-organ-c1

    url(r'^sound13A/$', views.sound13A, name='sound13A'), #subby-bass-c8
    url(r'^sound14A/$', views.sound14A, name='sound14A'), #subby-bass-c6
    url(r'^sound15A/$', views.sound15A, name='sound15A'), #subby-bass-c3

    url(r'^sound16A/$', views.sound16A, name='sound16A'), #wedding-organ-c6
    url(r'^sound17A/$', views.sound17A, name='sound17A'), #wedding-organ-c3
    url(r'^sound18A/$', views.sound18A, name='sound18A'), #wedding-organ-c0

                                            #AttemptTwo(B)
    url(r'^sound1B/$',  views.sound1B,  name='sound1B'), #classic-clean-c5
    url(r'^sound2B/$',  views.sound2B,  name='sound2B'), #classic-clean-c2
    url(r'^sound3B/$',  views.sound3B,  name='sound3B'), #classic-clean-c0

    url(r'^sound4B/$',  views.sound4B,  name='sound4B'), #classic-electric-piano-c6
    url(r'^sound5B/$',  views.sound5B,  name='sound5B'), #classic-electric-piano-c3
    url(r'^sound6B/$',  views.sound6B,  name='sound6B'), #classic-electric-piano-c0

    url(r'^sound7B/$',  views.sound7B,  name='sound7B'), #full-brass-c6
    url(r'^sound8B/$',  views.sound8B,  name='sound8B'), #full-brass-c3
    url(r'^sound9B/$',  views.sound9B,  name='sound9B'), #full-brass-c0

    url(r'^sound10B/$', views.sound10B, name='sound10B'), #grand-organ-c6
    url(r'^sound11B/$', views.sound11B, name='sound11B'), #grand-organ-c3
    url(r'^sound12B/$', views.sound12B, name='sound12B'), #grand-organ-c1

    url(r'^sound13B/$', views.sound13B, name='sound13B'), #subby-bass-c8
    url(r'^sound14B/$', views.sound14B, name='sound14B'), #subby-bass-c6
    url(r'^sound15B/$', views.sound15B, name='sound15B'), #subby-bass-c3

    url(r'^sound16B/$', views.sound16B, name='sound16B'), #wedding-organ-c6
    url(r'^sound17B/$', views.sound17B, name='sound17B'), #wedding-organ-c3
    url(r'^sound18B/$', views.sound18B, name='sound18B'), #wedding-organ-c0

# ====================================================================================================================
                                            # login/signup/edit

    url(r'^login/$', views.login, name='login'), #login page
    url(r'^signup/$', views.signup, name='signup'), #signup page
    url(r'^logout/$', views.logout, name='logout'), #logout page
    url(r'^editProfile/$', views.editProfile, name='editProfile'), #editProfile page
    url(r'^saveFN/$', views.saveFN, name='saveFN'), #update firstname
    url(r'^saveSN/$', views.saveSN, name='saveSN'), #update surname
    url(r'^saveAge/$', views.saveAge, name='saveAge'), #update age
    url(r'^saveG/$', views.saveG, name='saveG'), #update gender
    url(r'^saveDH/$', views.saveDH, name='saveDH'), #update dominant hand
    url(r'^saveP/$', views.saveP, name='saveP'), #update password
    url(r'^checkP/$', views.checkP, name='checkP'), #check current password

# ====================================================================================================================
                                            # sending colour/sound data

    url(r'^chooseAttempt/$', views.chooseAttempt, name='chooseAttempt'), #chooseAttempt page
    url(r'^checkAttemptA/$', views.checkAttemptA, name='checkAttemptA'), #run checkAttemptA
    url(r'^checkAttemptB/$', views.checkAttemptB, name='checkAttemptB'), #run checkAttemptB
    url(r'^sendColourA/$', views.sendColourA, name='sendColourA'), #run sendColourA
    url(r'^sendColourB/$', views.sendColourB, name='sendColourB'), #run sendColourB

# ====================================================================================================================
                                            # results page

    url(r'^results/$', views.results, name='results'), #results page if logged in
    url(r'^results/attemptone$', views.attemptoneResults, name='attemptoneResults'), #attemptoneResults page
    url(r'^results/attempttwo$', views.attempttwoResults, name='attempttwoResults'), #attemptoneResults page

]

