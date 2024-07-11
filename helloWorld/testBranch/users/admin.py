from django.contrib import admin

from .models import *

admin.site.register(Users)
class ClubAdmin(admin.ModelAdmin):
    search_fields = [
        'users__email',              # To search by user email
    ]

    # Optional: To display users in the list view
    list_display = ('name', 'get_users')
    filter_horizontal = ('users', 'tagOrTags', 'leaders', 'advisors')  # Enables the horizontal filter for users

    def get_users(self, obj):
        return ", ".join([user.email for user in obj.users.all()])

    get_users.short_description = 'Users'


admin.site.register(Club, ClubAdmin)
admin.site.register(ClubTag)



# Register your models here.
