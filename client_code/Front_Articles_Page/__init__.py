from ._anvil_designer import Front_Articles_PageTemplate
from anvil import *
from functools import partial
from anvil.js import get_dom_node
from .. import data
from ..Artice_Link import Artice_Link
import anvil.server
from ..Artice_Link_Skeleton import Artice_Link_Skeleton

class Front_Articles_Page(Front_Articles_PageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.cached_results={}
        self.categories=[
        {
            "name":"Articles",
            "desc":"Access all announcements, content and tutorials"
        },
        {
            "name":"Guidelines",
            "desc":"See our policies and guidelines"
        },                        
        ] 
        
        #Change this according to the categories you require

        for cateogry in self.categories:
            tab=Button(text=cateogry['name'],font_size=20,tag=cateogry)
            tab.set_event_handler('click',self.switch_tab)
            self.tabs.add_component(tab)

        
        for i in range(20):
            self.skeletals.add_component(Artice_Link_Skeleton())
    
    def switch_tab(self,**event_args):
        sender=event_args['sender']
        tab_data=sender.tag
        self.current_tab=tab_data['name']
        for i in self.tabs.get_components():
            i.foreground='theme:primary'
            i.background=''
            i.role=['unselected','tab']
        sender.background='theme:primary'
        sender.foreground='theme:white'
        sender.role='tab'
        self.desc.text=tab_data['desc']
        self.load_articles()
        
    def load_articles(self):
        with anvil.server.no_loading_indicator:
            self.articles.clear()
            self.skeletals.visible=True
            self.cached_results
            results=self.cached_results.get(self.current_tab)
            if not results:
                from anvil.tables import app_tables,order_by,query
                results=app_tables.articles.search(order_by('priority',ascending=False),data.fetch_parameters,category=self.current_tab)
                self.cached_results[self.current_tab]=results
            for article in results:
                self.articles.add_component(Artice_Link(item=article))
            self.skeletals.visible=False

    def tabs_show(self, **event_args):
        self.tabs.get_components()[0].raise_event('click')