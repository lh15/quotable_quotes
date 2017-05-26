from django.conf.urls import url
from views import *           # So we can call functions from our routes!
urlpatterns = [
	url(r'^$', index, name = "index"),
    url(r'^process_registration$', process_registration, name = 'process_registration'),
    url(r'^process_login$', process_login, name = 'process_login'),
    url(r'^login$', login, name = 'login'),
    url(r'^log_out$', log_out, name = 'log_out'),
	url(r'^display_quotes$', display_quotes, name = "display_quotes"),          
	url(r'^process_quote$', process_quote, name = "process_quote"),          
	url(r'^add_fav/(?P<id>[^\n]+)/$', add_fav, name = "add_fav"),            
	url(r'^remove_fav/(?P<id>[^\n]+)/$', remove_fav, name = "remove_fav"),            
	url(r'^delete_quote/(?P<id>[^\n]+)/$', delete_quote, name = "delete_quote"),            
	url(r'^users/(?P<id>[^\n]+)/$', display_user, name = "display_user"),       
]