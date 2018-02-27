from django.contrib import admin
from .models import Author, Book, BookInstance, Genre, Language

# Register your models here.

#admin.site.register(Book)
#admin.site.register(Author)
#admin.site.register(BookInstance)
admin.site.register(Language)
admin.site.register(Genre)

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'id', 'status', 'due_back', 'borrower')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availablity', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
