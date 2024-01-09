from ._anvil_designer import Artice_LinkTemplate
from anvil import *
from .. import data
from anvil.js import get_dom_node

class Artice_Link(Artice_LinkTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.item=properties['item']
        self.title.text=self.item['title']
        self.subtitle.text=self.item['subtitle']
        self.image_1.source=self.item['bg']
        unique_hash=data.hash_getter(self.item)
        self.link_1.url='#'+unique_hash #Doing this so that to help wit + Users will be able to open link in new tab if they want
        get_dom_node(self.link_1).onclick=self.open_article
        data.articles_cache[unique_hash]=self.item
        
    def open_article(self,e): 
        get_open_form().search_bar.text=''
        set_url_hash(data.hash_getter(self.item))
        e.preventDefault() #We do not actually want to open link if the user has simply clicked the article