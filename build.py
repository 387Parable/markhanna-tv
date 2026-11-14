import json, html
from pathlib import Path
def esc(v): return html.escape(v, quote=True)
books=json.loads(Path("books.json").read_text())
book=books[0]
def img(src,alt,cls=""): return f'<img class="{cls}" src="{esc(src)}" alt="{esc(alt)}">'
def button(url,label,cls="button"): return f'<a class="{cls}" href="{esc(url)}">{esc(label)}</a>'
def page(path,title,body):
 nav=''.join(f'<a href="{url}"'+(' aria-current="page"' if path==url else '')+f'>{label}</a>' for url,label in [('/','Home'),('/books','Books'),('/about','About'),('/shop-hidden','Shop'),('/contact','Contact')])
 dest=Path("index.html") if path=='/' else Path(path[1:]+'.html')
 dest.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)} | Mark Hanna</title><meta name="description" content="Books and biography of author Mark Hanna. Explore EBenezer: A Globalist’s Christmas Carol."><link rel="stylesheet" href="/style.css"><script src="/site.js" defer></script></head><body><a class="skip" href="#main">Skip to content</a><header><div class="bar"><a class="brand" href="/">MARK <span>HANNA</span></a><nav aria-label="Main navigation">{nav}</nav><form action="/search" role="search"><input name="q" aria-label="Search the site" placeholder="Search"><button aria-label="Search">↗</button></form></div></header><main id="main">{body}</main><footer><a class="brand" href="/">MARK HANNA</a><p>© 2026 Mark Hanna</p><a href="/contact">Contact</a></footer></body></html>''')
cover=img(book['cover'],book['title']+' book cover','cover')
intro='A futuristic supernatural thriller inspired by Dickens’s Christmas classic.'
page('/', 'Author & novelist',f'''<section class="hero"><div class="hero-text"><p class="eyebrow">A novel by Mark Hanna</p><h1>{book['title']}</h1><p class="subtitle">{book['subtitle']}</p><p class="lede">{intro} A billionaire technologist faces three visitors and a choice that could change the future.</p><div class="actions">{button('/the-book','Explore the book')}{button('/shop-hidden','Find a retailer','button outline')}</div></div><div class="art">{cover}</div></section><section class="quote"><blockquote>“More ambitious than the Dickens classic...Scrooge updated for the 21st century.”</blockquote><p>Michael Fedison · Author and editor</p></section><section class="author-strip"><div><p class="eyebrow">About the author</p><h2>Mark Hanna</h2><p>Author, entrepreneur, and former television professional.</p>{button('/about','Read the biography','text-link')}</div></section>''')
page('/books','Books','<section class="inner"><h1>Books</h1><div class="catalog">'+''.join(f'<article>{img(b["cover"],b["title"]+" cover","cover")}<div><h2>{esc(b["title"])}</h2><p>{esc(b["subtitle"])}</p>{button(b["path"],"About this book","text-link")}</div></article>' for b in books)+'</div></section>')
for b in books:
 page(b['path'],b['title'],f'''<section class="inner split"><div>{img(b['cover'],b['title']+' book cover','cover')}</div><div><p class="eyebrow">Fiction · Technothriller</p><h1>{esc(b['title'])}</h1><p class="subtitle">{esc(b['subtitle'])}</p>{''.join('<p>'+esc(p)+'</p>' for p in b['description'])}{button('/shop-hidden','Find a retailer')}</div></section>''')
about=json.loads(Path('about.json').read_text())
page('/about','About',f'''<section class="inner split"><div>{img(about['photo'],'Mark Hanna','portrait')}</div><div><p class="eyebrow">Biography</p><h1>Mark Hanna</h1>{''.join('<p>'+esc(p)+'</p>' for p in about['paragraphs'])}</div></section>''')
retailer_logos = {"Mises Store":"mises","ThriftBooks":"thriftbooks","eBay":"ebay","Kobo":"kobo","Barnes & Noble":"barnes-noble","Amazon":"amazon","Google Books":"google-books","Books-A-Million":"books-a-million","Walmart":"walmart","Bookshop.org":"bookshop"}

def retailer_link(label, url):
 logo = retailer_logos.get(label)
 if not logo:
  return button(url, label + ' ↗', 'retailer')
 return f'<a class="retailer retailer-logo" href="{esc(url)}"><img src="/assets/retailers/{logo}.webp" alt="{esc(label)}"></a>'

page('/shop-hidden','Shop',f'''<section class="inner"><p class="eyebrow">Book retailers</p><h1>Shop</h1><p class="subtitle">{book['title']}: {book['subtitle']}</p><p>Choose a retailer for editions, pricing, and availability.</p><div class="retailers">{''.join(retailer_link(label,url) for label,url in book['retailers'])}</div></section>''')
page('/contact','Contact','''<section class="inner narrow"><h1>Contact Mark</h1><form id="contact" action="/api/contact" method="post"><div class="fields"><label>First name<input name="firstName" required maxlength="100" autocomplete="given-name"></label><label>Last name<input name="lastName" required maxlength="100" autocomplete="family-name"></label></div><label>Email<input name="email" type="email" required maxlength="254" autocomplete="email"></label><label>Message<textarea name="message" rows="7" required maxlength="5000"></textarea></label><div hidden><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div><button class="button">Send message</button><p id="form-status" role="status"></p></form></section>''')
page('/search','Search','<section class="inner"><h1>Search</h1><div id="results" role="status"></div></section>')
Path('search-index.json').write_text(json.dumps([{'title':b['title'],'url':b['path'],'text':b['subtitle']+' '+' '.join(b['description'])} for b in books]+[{'title':'About Mark Hanna','url':'/about','text':' '.join(about['paragraphs'])},{'title':'Shop','url':'/shop-hidden','text':'Order buy retailers'},{'title':'Contact','url':'/contact','text':'Message email'}]))
