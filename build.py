import json, html
from pathlib import Path
def esc(v): return html.escape(v, quote=True)
books=json.loads(Path("books.json").read_text())
book=books[0]
def img(src,alt,cls=""): return f'<img class="{cls}" src="{esc(src)}" alt="{esc(alt)}">'
def button(url,label,cls="button"): return f'<a class="{cls}" href="{esc(url)}">{esc(label)}</a>'
about_photo = json.loads(Path("about.json").read_text())["photo"]
site_url = "https://www.markhanna.tv"
site_pages = []
page_descriptions = {
    "/": "Official website of Mark Hanna, author of EBenezer: A Globalist’s Christmas Carol, a futuristic Christmas technothriller inspired by Charles Dickens.",
    "/about": "Meet Mark Hanna, author of EBenezer, and explore his background in writing, technology, entrepreneurship, and television.",
    "/books": "Explore books by Mark Hanna, including EBenezer: A Globalist’s Christmas Carol, a futuristic retelling of Dickens’s classic.",
    "/reviews": "Read three reader reviews of Mark Hanna’s EBenezer: A Globalist’s Christmas Carol.",
    "/shop-hidden": "Find EBenezer: A Globalist’s Christmas Carol by Mark Hanna at booksellers and compare available editions.",
    "/contact": "Contact Mark Hanna through the official author website.",
    "/search": "Search the Mark Hanna author website.",
}

def page_metadata(path, title):
    canonical = site_url + path
    current_book = next((item for item in books if item["path"] == path), None)
    if current_book:
        title = f'{current_book["title"]}: {current_book["subtitle"]}'
        description = f'{title} by Mark Hanna reimagines Dickens’s A Christmas Carol as a futuristic supernatural thriller about a Big Tech titan facing three visitors.'
    else:
        description = page_descriptions[path]
    title = f"{title} | Mark Hanna"
    author = {"@type": "Person", "@id": site_url + "/about#author", "name": "Mark Hanna", "url": site_url + "/about"}
    website = {"@type": "WebSite", "@id": site_url + "/#website", "name": "Mark Hanna", "url": site_url + "/", "publisher": {"@id": author["@id"]}}
    graph = [author, website]
    if current_book or path == "/":
        featured = current_book or book
        url = site_url + featured["path"]
        graph.append({"@type": "Book", "@id": url + "#book", "url": url, "name": featured["title"] + ": " + featured["subtitle"], "author": {"@id": author["@id"]}, "image": site_url + featured["cover"], "inLanguage": "en", "description": " ".join(featured["description"])})
    if path != "/search":
        site_pages.append(canonical)
    image = site_url + (about_photo if path == "/about" else (current_book or book)["cover"])
    graph_json = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("<", "\\u003c")
    robots = '<meta name="robots" content="noindex,follow">' if path == "/search" else ""
    return f'<title>{esc(title)}</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{esc(canonical)}">{robots}<meta property="og:type" content="{"book" if current_book else "website"}"><meta property="og:site_name" content="Mark Hanna"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{esc(canonical)}"><meta property="og:image" content="{esc(image)}"><meta name="twitter:card" content="summary_large_image"><script type="application/ld+json">{graph_json}</script>'

def page(path,title,body):
 nav=''.join(f'<a href="{url}"'+(' aria-current="page"' if path==url else '')+f'>{label}</a>' for url,label in [('/','Home'),('/books','Books'),('/about','About'),('/shop-hidden','Shop'),('/reviews','Reviews'),('/contact','Contact')])
 dest=Path("index.html") if path=='/' else Path(path[1:]+'.html')
 dest.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{page_metadata(path,title)}<link rel="stylesheet" href="/style.css"><script src="/site.js" defer></script><link rel="icon" type="image/png" href="/favicon.png"></head><body><a class="skip" href="#main">Skip to content</a><header><div class="bar"><a class="brand" href="/">MARK <span>HANNA</span></a><nav aria-label="Main navigation">{nav}</nav><form action="/search" role="search"><input name="q" aria-label="Search the site" placeholder="Search"><button aria-label="Search">↗</button></form></div></header><main id="main">{body}</main><footer><a class="brand" href="/">MARK HANNA</a><p>© 2026 Mark Hanna</p><a href="/contact">Contact</a></footer></body></html>''')
cover=img(book['cover'],book['title']+' book cover','cover')
intro='A futuristic supernatural thriller inspired by Dickens’ Christmas classic.'
page('/', 'Author of EBenezer: A Globalist’s Christmas Carol',f'''<section class="hero"><div class="hero-text"><p class="eyebrow">A novel by Mark Hanna</p><h1>{book['title']}</h1><p class="subtitle">{book['subtitle']}</p><p class="lede">{intro} The planet’s foremost billionaire and Big Tech titan faces three visitors and a choice that could change not only his life...but the future of the planet.</p><div class="actions">{button('/the-book','Explore the book')}{button('/shop-hidden','Find a retailer','button outline')}</div></div><div class="art">{cover}</div></section><section class="quote"><blockquote>“More ambitious than the Dickens classic...Scrooge updated for the 21st century.”</blockquote><p>Michael Fedison · Author and editor</p></section><section class="author-strip"><div><p class="eyebrow">About the author</p><h2>Mark Hanna</h2><p>Writer, technologist, entrepreneur, and former television professional.</p>{button('/about','Read the biography','text-link')}</div></section>''')
page('/books','Books','<section class="inner"><h1>Books</h1><div class="catalog">'+''.join(f'<article>{img(b["cover"],b["title"]+" cover","cover")}<div><h2>{esc(b["title"])}</h2><p>{esc(b["subtitle"])}</p>{button(b["path"],"About this book","text-link")}</div></article>' for b in books)+'</div></section>')
for b in books:
 quote = f'<blockquote class="book-cover-quote">{esc(b["cover_quote"])}</blockquote>' if b.get("cover_quote") else ""
 page(b['path'],b['title'],f'''<section class="inner split"><div>{img(b['cover'],b['title']+' book cover','cover')}{quote}</div><div><p class="eyebrow">Fiction · Technothriller</p><h1>{esc(b['title'])}</h1><p class="subtitle">{esc(b['subtitle'])}</p>{''.join('<p>'+esc(p)+'</p>' for p in b['description'])}{button('/shop-hidden','Find a retailer')}</div></section>''')
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

reviews = json.loads(Path("reviews.json").read_text())

def render_review(review):
    name = esc(review["name"])
    heading = esc(review["title"])
    author = f'<p class="review-author"><strong>{name}</strong></p>'
    affiliations = [esc(label) for label in review.get("affiliations", [])]
    credentials = ", ".join([*affiliations, esc(review["credential"])])
    paragraphs = "".join(f"<p>{esc(paragraph)}</p>" for paragraph in review["paragraphs"])
    return f'<article class="review"><div class="review-heading"><h2>{heading}</h2><span class="review-stars" role="img" aria-label="5 out of 5 stars">★★★★★</span></div>{paragraphs}<div class="review-credit">{author}<p>{credentials}</p></div></article>'

page("/reviews", "Reviews", '<section class="inner reviews"><h1>Reviews</h1><p class="subtitle">EBenezer: A Globalist’s Christmas Carol</p><div class="review-list">' + "".join(map(render_review, reviews)) + "</div></section>")

Path("sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{esc(url)}</loc></url>\n" for url in site_pages) + "</urlset>\n", encoding="utf-8")
Path("robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {site_url}/sitemap.xml\n", encoding="utf-8")
