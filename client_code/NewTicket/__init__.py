from ._anvil_designer import NewTicketTemplate
from anvil import *
from anvil.js import get_dom_node
import anvil.server
from datetime import date

class NewTicket(NewTicketTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        options=['Report an Issue','Ask a Question','Request a Feature','Other Reason',]
        for option in options:
            option_link=Link(text=option,font_size=16,foreground='theme:black')
            option_link.set_event_handler('click',self.select_option)
            self.options.add_component(option_link)
        self.options_shown=True
        
    def hide_options(self):
        get_dom_node(self.options).style.marginTop=f'-{get_dom_node(self.options).offsetHeight}px'
        self.options_shown=False
        
    def select_option(self,**event_args):
        sender=event_args['sender']
        self.selected_option.text=sender.text
        sender.icon='fa:check-lg'
        sender.foreground='theme:primary'
        for option in self.options.get_components():
            if option!=sender:
                option.foreground='theme:black'
                option.icon=''
        self.hide_options()
        
    def show_options(self):
        get_dom_node(self.options).style.marginTop='0'
        self.options_shown=True
        
    def selected_option_click(self, **event_args):
        if not self.options_shown:
            self.show_options()
        else:
            self.hide_options()

    def submit_click(self, **event_args):
        self.submit.enabled=False
        anvil.server.call('submit_ticket',**{'category':self.selected_option.text,'email':self.email.text,'description':self.description.text,'date':date.today()})
        Notification('We shall get back to you as soon as possible',title='Your request has been submitted',timeout=3,style='success').show()
        get_open_form().back_click()

    def back_click(self, **event_args):
        set_url_hash('')