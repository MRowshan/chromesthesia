from django.contrib import admin

from .models import User, Colour, Sound, AttemptOne, AttemptTwo

# Display objects as tables in admin page
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'firstname', 'surname', 'age', 'gender', 'dominanthand', 'password')

class ColourAdmin(admin.ModelAdmin):
    list_display = ('colourID', 'hexcode')

class SoundAdmin(admin.ModelAdmin):
    list_display = ('soundID', 'instrument', 'pitch')

class AttemptOneAdmin(admin.ModelAdmin):
    list_display = ('userOne', 'colourOne', 'soundOne')

class AttemptTwoAdmin(admin.ModelAdmin):
    list_display = ('userTwo', 'colourTwo', 'soundTwo')

# Register models to admin page
admin.site.register(User, UserAdmin)
admin.site.register(Colour, ColourAdmin)
admin.site.register(Sound, SoundAdmin)
admin.site.register(AttemptOne, AttemptOneAdmin)
admin.site.register(AttemptTwo, AttemptTwoAdmin)