#!/usr/bin/python
""" Test the effect of delay on CSS and JS """

__version__ = "1.6"

import BaseHTTPServer
from SocketServer import ThreadingMixIn
import time

html_content = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <script>
        (function(){
            var counter = 0;
            var gotCSS = false;
            var gotJS = false;
            var str;
            setInterval(function(){
                counter++;
                if(counter < 12){
                    var result = document.getElementById("result");
                    if(!gotCSS && getComputedStyle(result)["color"] != "rgb(0, 0, 0)"){
                        console.log("Got CSS parsed at " + counter + " seconds");
                        gotCSS = true;
                        str = "CSS parsing was ";
                        if(counter > 2){
                            str += "delayed :(";
                        }
                        else{
                            str += "immediate! Woot!"
                        result.innerHTML += str;
                    }
                    if(!gotJS && window.testing123){
                        str = "<br/>JS parsing was ";
                        console.log("Got JS parsed at " + counter + " seconds");
                        gotJS = true;
                        if(counter > 6){
                            str += "delayed :`(";
                        }
                        else{
                            str += "immediate! woot!!!"
                        }
                        result.innerHTML += str;
                    }
                }
            }, 1000);
            })();
        </script>
        <link href="test.css" rel="stylesheet">
    </head>
    <body>
        <p id="result"></p>
        <script src="test.js" type="text/javascript"></script>
    </body>
</html>
"""

css_content = """
#result{color: blue}
/* This is just a content to blzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
 * zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
 * zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz */

""" 

js_content = """
window.testing123 = true;
console.log("This is 1st");
console.timeStamp("bla");
/* This comment is here to take some space. GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGg
 * sd50iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiifsdgsdgsdgfdfgdfg*/
console.log("This is 2nd");
console.timeStamp("bla");
"""

""" *********************************************************************** """
class DelayRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """ Extensible proxy request handler. Extend by inheritance """

    def __init__(self, *args, **kwargs):
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self, post_data=None, is_head=False):
        """Serve a GET request."""
        css = "css" in self.path
        js = "js" in self.path
        delay = 0
        if css:
            content = css_content
            delay = 5
        elif js:
            content = js_content
            delay = 10
        else:
            content = html_content

        if delay:
            pre_content = content[:50]
            post_content = content[50:]
            self.send_response(200)
            self.wfile.write(pre_content)
            self.wfile.flush()
            time.sleep(delay)
            self.wfile.write(post_content)
            self.wfile.flush()
        else:
            self.send_response(200)
            self.wfile.write(content)
            self.wfile.flush()


class ThreadingServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    def __init__(self, address, handler):
        BaseHTTPServer.HTTPServer.__init__(self, address, handler)

def run(HandlerClass=DelayRequestHandler,
             port=8002):
    srv = ThreadingServer(("", port), HandlerClass)
    print "serving requests on port", port
    srv.serve_forever()

if __name__ == '__main__':
    run()
