import os
import shutil

# Remove fake svgs in work/thumbs and work/thumbnail
if os.path.exists("work/thumbs"):
    shutil.rmtree("work/thumbs")
if os.path.exists("work/thumbnail") and os.path.isfile("work/thumbnail"):
    os.remove("work/thumbnail")

def setup_route(route_name, html_content):
    # route.html
    with open(route_name + ".html", "w", encoding="utf-8") as f:
        f.write(html_content)
    # route/index.html
    os.makedirs(route_name, exist_ok=True)
    with open(os.path.join(route_name, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

# about
if os.path.exists("about") and os.path.isfile("about"):
    with open("about", "r", encoding="utf-8") as f:
        about_html = f.read()
    os.remove("about")
    setup_route("about", about_html)

# contact
if os.path.exists("contact") and os.path.isfile("contact"):
    with open("contact", "r", encoding="utf-8") as f:
        contact_html = f.read()
    os.remove("contact")
    setup_route("contact", contact_html)

# work subroutes
for sub in ["hanzii", "mazii", "todaii", "niubii"]:
    sub_path = os.path.join("work", sub)
    if os.path.exists(sub_path) and os.path.isfile(sub_path):
        with open(sub_path, "r", encoding="utf-8") as f:
            sub_html = f.read()
        os.remove(sub_path)
        with open(sub_path + ".html", "w", encoding="utf-8") as f:
            f.write(sub_html)
        os.makedirs(sub_path, exist_ok=True)
        with open(os.path.join(sub_path, "index.html"), "w", encoding="utf-8") as f:
            f.write(sub_html)

# work/index.html redirects to work/hanzii
os.makedirs("work", exist_ok=True)
with open("work/index.html", "w", encoding="utf-8") as f:
    f.write('<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/work/hanzii"><script>window.location.replace("/work/hanzii");</script></head><body>Redirecting to <a href="/work/hanzii">/work/hanzii</a>...</body></html>')

print("Routes setup complete!")
