import sublime, sublime_plugin
import urllib  
import urllib2
import json

from urlparse import urlparse

class PastebinOpenCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.window().show_input_panel("Select URL to fetch", "", self.fetch, None, None)

  def fetch(self, url):
    parsed_url = urlparse(url)
    if not parsed_url.netloc == "pastebin.fi":
      return

    if not "raw" in url.split("/"):
      url = parsed_url.scheme + "://" + parsed_url.netloc + "/raw" + parsed_url.path

    try:
      response = urllib2.urlopen(url)  
      html = response.read()
      edit = self.view.begin_edit()
      view = self.view.window().new_file()
      view.set_name("testi.py")
      view.insert(edit, 0, html)

    except (urllib2.HTTPError) as (e):  
      return sublime.error_message('%s: HTTP error %s contacting API' % (__name__, str(e.code)))
    except (urllib2.URLError) as (e):  
      return sublime.error_message('%s: URL error %s contacting API' % (__name__, str(e.reason))) 