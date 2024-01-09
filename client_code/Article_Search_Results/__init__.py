from ._anvil_designer import Article_Search_ResultsTemplate
from anvil import *
from .. import data
from ..Artice_Link import Artice_Link
from anvil.tables import app_tables,query
from ..Artice_Link_Skeleton import Artice_Link_Skeleton
import anvil.server

class Article_Search_Results(Article_Search_ResultsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.query=properties['query']
        self.search_title.text=f'Results for "{self.query}"'
        self.added_results=[]
        for i in range(20):
            self.articles_skeleton.add_component(Artice_Link_Skeleton())
        # Any code you write here will run before the form opens.

    def form_show(self, **event_args):
      with anvil.server.no_loading_indicator:
        for i in range(3):
            if self.query==get_open_form().search_bar.text:
                if i==0:
                    phase_results=app_tables.articles.search(data.fetch_parameters,title=query.ilike('%'+self.query+'%'))
                elif i==1:
                    phase_results=app_tables.articles.search(data.fetch_parameters,subtitle=query.ilike('%'+self.query+'%'))
                elif i==2:
                    phase_results=app_tables.articles.search(data.fetch_parameters,cont=query.ilike('%'+self.query+'%'))
                for result in phase_results:
                    if result not in self.added_results:
                        self.articles.add_component(Artice_Link(item=result))
                self.added_results.extend(phase_results)
                
            else:
                self.remove_from_parent()
        self.articles_skeleton.remove_from_parent()
        if not self.added_results:
            self.noresults.visible=True