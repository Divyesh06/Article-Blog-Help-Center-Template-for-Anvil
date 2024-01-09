from ._anvil_designer import Artice_LinkTemplate
from anvil import *
from .. import data
from anvil.js import get_dom_node

class Artice_Link(Artice_LinkTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.item=properties['item']
        self.title.text=self.item['title']
        self.subtitle.text=self.item['subtitle']
        self.image_1.source=self.item['bg'].replace('upload/','upload/c_fill,h_500,w_800/')
        self.link_1.url='#'+data.hash_setter(self.item)
        get_dom_node(self.link_1).onclick=self.open_article
        data.articles_cache[data.id_numbers(self.item.get_id())]=self.item
        
    def open_article(self,e): 
        get_open_form().search_bar.text=''
        set_url_hash(data.hash_setter(self.item))
        e.preventDefault()