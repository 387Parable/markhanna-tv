# MarkHanna.tv

Run `python3 build.py` after editing books.json or about.json. Serve the generated HTML and assets with Vercel clean URLs. Existing Wix paths /about, /the-book, /shop-hidden, and /contact are retained.

For contact delivery, set RESEND_API_KEY, CONTACT_FROM (verified Resend sender), and CONTACT_TO (approved inbox) in the MarkHanna.tv Vercel project. Test delivery before routing the domain. No database is needed for the current implementation.
