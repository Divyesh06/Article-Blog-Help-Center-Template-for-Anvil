from ._anvil_designer import HeaderTemplate
from anvil import *

class Header(HeaderTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)