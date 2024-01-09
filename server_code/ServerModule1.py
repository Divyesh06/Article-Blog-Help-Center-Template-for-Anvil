import anvil.server
from anvil.tables import app_tables
import anvil.tables.query as q

@anvil.server.callable
def submit_ticket(**data):
    app_tables.tickets.add_row(**data)
    
def id_numbers(row_id):
    return row_id.replace('[','').replace(']','').replace(',','_')
    
def hash_setter(row):
    title=row['title']
    row_id=row.get_id()
    hash_url=f"{title.replace(' ','-')}-{id_numbers(row_id)}"
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
<loc>{url}#!?article={hash_setter(article)}</loc>
</url>
'''
    sitemap+='</urlset>'
    blob=anvil.BlobMedia('text/xml',bytes(sitemap.encode()),name='sitemap.xml')
    return blob


@anvil.server.http_endpoint('/articles/:row_id')
def get_research(row_id):
    article=app_tables.articles.get_by_id(f"[{row_id.split('-')[-1].replace('_',',')}]",q.fetch_only('title','subtitle','bg'))
    title=article['title']
    description=article['subtitle']
    image=article['bg']
    hash_url = f"https://support.geeke.app/#!?article={row_id}"
    html=f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="icon" type="image/png" href="https://support.geeke.app/_/theme/Geeke%20Favicon.png">
    <meta property="og:image" content="{image}" />
    <script>
    window.location.href="{hash_url}"
    
    </script>
    """
    return anvil.BlobMedia('text/html',bytes(html.encode()))