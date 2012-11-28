""" 
A small program that traverses a website's stylesheets to get the dominant colors used in it. It generates an HTML file containing the 
colors sorted by their frequency.
__author__ = "Prakhar Srivastav"
__date__ = "$Date: 2012/11/28"
"""

import re, collections, operator, urllib, sys
from lxml import html

color_dict = {
    "white"  :"ffffff",         
    "black"  :"000000", 
    "blue"   :"0000ff", 
    "fuchsia":"ff00ff", 
    "green"  :"008000", 
    "lime"   :"00ff00", 
    "maroon" :"800000", 
    "orange" :"ffA500", 
    "purple" :"800080"
}

def get_stylesheets(url):
    """ gets all the stylesheets from the url and generates color """
    url = "http://" + url
    html_content = urllib.urlopen(url).read()
    if not html_content:
        print "Couldn't connect to url"
    print "Getting colors for %s" % url
    parsed_page = html.fromstring(html_content)
    stylesheets = [l.get("href") for l in parsed_page.xpath("//link") 
                   if l.get("rel") == "stylesheet"]
    for s in stylesheets:
        try:
            code = urllib.urlopen(s).read()
        except:
            print "Couldn't read css files"
        html_content += code
    gen_color_from_css(html_content)

def gen_color_from_css(css):
    """ generates colors from css file passed"""
    generate_colors(get_colors(css))

def get_colors(code):
    """ takes a css stylesheet and returns a dict with colors 
    sorted on their frequency of appearance in the stylesheet"""
    colors = collections.defaultdict(int)
    regx = re.compile(r"#([0-9A-Fa-f]{3,6})|(black|white|blue|fuchsia|green|lime|maroon|orange|purple)|(rgba\(.*\))")
    all_colors = []
    for c in regx.findall(code):
        all_colors.append("".join([t for t in c]))
    for c in all_colors:
        colors[get_hex_color(c.lower())] += 1
    return sorted(colors.iteritems(), key=operator.itemgetter(1), reverse=True)

def get_hex_color(color):
    """ returns a hex-fied color for string passed in the form
    a9fa21, ccc, rgba(91, 41, 14, 0.2), olive """
    if color in color_dict:
        return color_dict[color]
    if len(color) == 3: 
        return color*2
    if re.match(r'^rgba', color):
        regx = re.compile(r"(\d+)\s*,")
        return "".join([hex(int(c))[2:] for c in regx.findall(color)])
    return color

def generate_colors(colors, filename="colors", generate_file=True):
    """ Generates a HTML file or print the colors """
    count = len(colors)
    if generate_file:
        header = "<html> <body> <h2>Sorted by number of occurences</h2> \
                 <h4>Total Colors used: %s</h4>" % count
        footer = "</body> </html>"
        template = "<div style='background: #%s; margin:10px;  \
                    float: left; width:80px; height:80px;'> %s </div>"
        with open(filename + ".html", "w") as f:
            print "--------- Generating %s file ------------- " % filename
            f.write(header + "\n".join([template % \
                    (c[0], c[0]) for c in colors]) + footer)
            print "--------- Done -------------"
    else:
        print "Color | Frequency"
        print "-----------------"
        if count > top_colors:
            for i in range(top_colors):
                print "%s | %s" % (colors[i][0], colors[i][1])
        else:
            for c in colors:
                print "%s | %s" % (c[0], c[1])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_stylesheets(sys.argv[1])
    else:
        print "Usage - python color-palette.py <url>"
        print "Getting colors for hacker news"
        get_stylesheets("news.ycombinator.com")
