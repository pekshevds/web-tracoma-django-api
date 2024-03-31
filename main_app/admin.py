from django.contrib import admin
import config


admin.site.site_header = config.SITE_HEADER
admin.site.site_title = config.SITE_TITLE
admin.site.index_title = config.INDEX_TITLE
