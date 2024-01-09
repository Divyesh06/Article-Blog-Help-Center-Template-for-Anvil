from ._anvil_designer import Artice_Link_SkeletonTemplate
from anvil import *
from .. import data
from anvil.js import get_dom_node

class Artice_Link_Skeleton(Artice_Link_SkeletonTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)   