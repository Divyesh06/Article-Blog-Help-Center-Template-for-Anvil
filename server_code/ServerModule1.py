import anvil.server
from anvil.tables import app_tables
import anvil.tables.query as q

@anvil.server.callable
def submit_ticket(**data):
    app_tables.tickets.add_row(**data)

def hash_getter(row):
    title=row['title']
    row_id=row.get_id()
    row_id=row_id.replace('[','').replace(']','').replace(',','_')
    hash_url=f"!?article={title.replace(' ','-')}-{row_id}"
    return hash_url

@anvil.server.http_endpoint('/sitemap.xml')
def return_sitempap():
    url=anvil.server.get_app_origin()
    sitemap=f'''
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">s
<url>
<loc>{url}</loc>
</url>
    '''
    for article in app_tables.articles.search():
        sitemap+=f'''
<url>
<loc>{url}{hash_getter(article)}</loc>
</url>
'''
    sitemap+='</urlset>'
    blob=anvil.BlobMedia('text/xml',bytes(sitemap.encode()),name='sitemap.xml')
    return blob