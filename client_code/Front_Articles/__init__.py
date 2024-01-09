from ._anvil_designer import Front_ArticlesTemplate
from anvil import *
from functools import partial
from anvil.js import get_dom_node
from .. import data
from ..Artice_Link import Artice_Link
import anvil.server
from ..Artice_Link_Skeleton import Artice_Link_Skeleton

class Front_Articles(Front_ArticlesTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.cached_results={}
        self.current_tab='F'
        self.f.tag='F'
        get_dom_node(self.desc).style.paddingLeft='5px'
        self.g.tag='G'
        for i in range(20):
            self.skeletals.add_component(Artice_Link_Skeleton())
    
    def switch_tab(self,**event_args):
        sender=event_args['sender']
        self.current_tab=sender.tag
        for i in self.tabs.get_components():
            i.foreground='theme:primary'
            i.background=''
            i.role=['unselected','tab']
        sender.background='theme:primary'
        sender.foreground='theme:white'
        sender.role='tab'
        if self.current_tab=='F':
            self.desc.text='Access all announcements, content and tutorials related to Geeke'
        else:
            self.desc.text='See our policies and guidelines for keeping Geeke safe'
        self.load_articles()
        
    def load_articles(self):
        with anvil.server.no_loading_indicator:
            self.articles.clear()
            self.skeletals.visible=True
            results=self.cached_results.get(self.current_tab)
            if not results:
                from anvil.tables import app_tables,order_by,query
                results=app_tables.articles.search(order_by('priority',ascending=False),data.fetch_parameters,category=self.current_tab)
                self.cached_results[self.current_tab]=results
            for article in results:
                self.articles.add_component(Artice_Link(item=article))
            self.skeletals.visible=False