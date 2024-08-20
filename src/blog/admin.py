from django.contrib import admin

# Register your models here.


from blog.models import Tag, Article, Category, PhotoGroup, Photo


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_time'
    list_display = ('title', 'category', 'author', 'date_time', 'view')
    list_filter = ('category', 'author')
    filter_horizontal = ('tag',)
    exclude = ('picture',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


# @admin.register(Photo)
# class PhotoAdmin(admin.TabularInline):
#     model = Photo
#     fields = ('group', 'photo', 'desc', 'view_img')
#     readonly_fields = ('view_img',)
#     exclude = ('view_img',)
#
#
# @admin.register(PhotoGroup)
# class PhotoGroupAdmin(admin.ModelAdmin):
#     list_display = ('name', 'desc', 'create_time', 'update_time', 'active')
#     list_filter = ('active', 'create_time', 'update_time')
#     fields = ('name', 'cover', 'desc', 'active',)
#     inlines = [PhotoAdmin, ]


class PhotoAdmin(admin.TabularInline):
    model = Photo
    fields = ('group', 'photo', 'desc', 'view_img')
    readonly_fields = ('view_img',)
    exclude = ('view_img',)


class PhotoGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'create_time', 'update_time', 'active')
    list_filter = ('active', 'create_time', 'update_time')
    fields = ('name', 'cover', 'desc', 'active',)
    inlines = [PhotoAdmin, ]


admin.site.register(PhotoGroup, PhotoGroupAdmin)
