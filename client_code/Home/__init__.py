'''
This template is free to use for all kinds of usage (personal and commercial)

If this template helps you save some time and effort, you can consider supporting me at https://www.buymeacoffee.com/geeke.app 
However, this is not compulsory at all.
'''

from ._anvil_designer import HomeTemplate
from anvil import *
from anvil.js import get_dom_node,window
from .. import data
from anvil.tables import app_tables,query
from ..NewTicket import NewTicket
from ..Front_Articles_Page import Front_Articles_Page
from ..Article_Search_Results import Article_Search_Results

class Home(HomeTemplate):
    
    def __init__(self, **properties):
        self.init_components(**properties)
        window.addEventListener("hashchange", self.navigate)
        self.front_articles_page=Front_Articles_Page()
        self.results={}
        get_dom_node(self.main).style.minHeight='75vh' #Ensure that the footer remains at bottom'
        data.current_form=self
        self.search_bar=self.header.search_bar
        self.search_cancel=self.header.search_cancel
        self.button_1=self.header.button_1
        self.ticket=self.header.ticket
        self.link_1=self.header.link_1
        self.ticket.set_event_handler('click',self.ticket_click)
        self.search_bar.set_event_handler('change',self.search_bar_change)
        self.search_bar.set_event_handler('pressed_enter',self.search_bar_change)
        self.search_cancel.set_event_handler('click',self.search_cancel_click)
        self.button_1.set_event_handler('click',self.search_bar_change)
        self.link_1.set_event_handler('click',self.link_1_click)
        
    def navigate(self,*args):
        hash=get_url_hash().replace('!','')
        self.main.clear()
        if 'article' in hash:
            data.load_article_from_hash(hash)
            
        elif hash=='NewTicket':
            newticket=NewTicket()
            self.main.add_component(newticket)
            data.scroll_into_view(newticket,'start')
            data.change_meta('Need to get in touch with us for any support regarding Geeke? Fill this form and we will get back to you as soon as possible','Contact us - Geeke')

        #If you add some other forms, make sure to add them here too for navigation
        
        else:
            self.main.add_component(self.front_articles_page)
            self.front_articles_page.load_articles()
            data.change_meta('Need help on Geeke? Access all our articles or directly get in touch with us for any issue.','Geeke Support')
            
    def form_show(self, **event_args):
        self.navigate()

    def search_bar_change(self, **event_args):
        search_query=self.search_bar.text.strip()
        if search_query:
            self.search_cancel.visible=True
            self.main.clear()
            self.main.add_component(Article_Search_Results(query=search_query))
        else:
            self.search_cancel.visible=False
            self.main.clear()
            self.main.add_component(self.front_articles_page)

    def search_cancel_click(self, **event_args):
        self.search_bar.text=''
        self.search_bar_change()

    def ticket_click(self, **event_args):
        set_url_hash('#!NewTicket')

    def link_1_click(self, **event_args):
        set_url_hash('')