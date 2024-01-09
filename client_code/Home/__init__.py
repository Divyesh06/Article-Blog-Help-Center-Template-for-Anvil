from ._anvil_designer import HomeTemplate
from anvil import *
from ..Artice_Link import Artice_Link
from anvil.js import get_dom_node,window
from .. import data
from functools import partial
from anvil.tables import app_tables,query
from ..NewTicket import NewTicket
from ..Front_Articles import Front_Articles
from ..Article_Search_Results import Article_Search_Results
from anvil.js import window,import_from

class Home(HomeTemplate):
    
    def __init__(self, **properties):
        self.init_components(**properties)
        window.addEventListener("hashchange", self.navigate)
        self.front_articles=Front_Articles()
        self.results={}
        self.current_tab='F'
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
        hash=get_url_hash()
        self.main.clear()
        if 'article' in hash:
            data.load_article(hash['article'].split('-')[-1])
            
        elif hash=='!NewTicket':
            newticket=NewTicket()
            self.main.add_component(newticket)
            data.scroll_into_view(newticket.back,'start')
            data.change_meta('Need to get in touch with us for any support regarding Geeke? Fill this form and we will get back to you as soon as possible','Contact us - Geeke')
            
        else:
            self.main.add_component(self.front_articles)
            self.front_articles.load_articles()
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
            self.main.add_component(self.front_articles)

    def search_cancel_click(self, **event_args):
        self.search_bar.text=''
        self.search_bar_change()

    def back_click(self, **event_args):
        set_url_hash('')

    def ticket_click(self, **event_args):
        set_url_hash('#!NewTicket')

    def link_1_click(self, **event_args):
        set_url_hash('')