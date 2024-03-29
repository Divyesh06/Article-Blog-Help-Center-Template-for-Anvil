from anvil import set_url_hash
from anvil.tables import app_tables,query
from .Article_Viewer import Article_Viewer
from anvil.js import get_dom_node
from anvil.js.window import jQuery,document
from anvil import *

fetch_parameters=query.fetch_only('title','subtitle','category','bg')
articles_cache={}
current_form=None

def scroll_into_view(comp,pos='start'):
    get_dom_node(comp).scrollIntoView({"behavior":"smooth","block":pos})
    
def hash_getter(row):
    title=row['title']
    row_id=row.get_id()
    row_id=row_id.replace('[','').replace(']','').replace(',','_')
    hash_url=f"!?article={title.replace(' ','-')}-{row_id}"
    return hash_url
    
def load_article_from_hash(hash):
    row_id=f"[{hash['article'].split('-')[-1].replace('_',',')}]"
    article=articles_cache.get(row_id)
    if not article:
        article=app_tables.articles.get_by_id(row_id,fetch_parameters)
        articles_cache[row_id]=article
    form=current_form
    form.main.clear()
    viewer=Article_Viewer(item=article)
    form.main.add_component(viewer)
    scroll_into_view(viewer.back)
    change_meta(article['subtitle'],article['title']+' - Geeke',article['bg'])

def remove_meta(selector):
    jQuery(selector).remove()

def create_meta(name,content):
    meta=document.createElement('meta');
    meta.name=name
    meta.content=content
    jQuery('head').append(meta);
    
def change_meta(description,title,image=None):
        jQuery('title').remove();
        remove_meta('meta[name="description"]')
        remove_meta('meta[name="og:description"]')
        remove_meta('meta[name="og:title"]')
        new_title = document.createElement('title')
        new_title.text = title
        jQuery('head').append(new_title)
        create_meta('description',description)
        create_meta('og:description',description)
        create_meta('og:title',title)
        create_meta('title',title)
        if image:
            create_meta('og:image',image)