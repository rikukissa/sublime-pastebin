import sublime, sublime_plugin
import urllib  
import urllib2
import json

class PastebinPasteCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    selections = [] 
    for selection in self.view.sel():
      selections.append(self.view.substr(selection))

    sublime.set_timeout(lambda:
      self.post_selections(selections)
    , 1)

  def copy_to_clipboard(self, hashes, index):
    if index is -1: return
    sublime.set_clipboard(hashes[index][0])

  def show_urls(self, hashes):
    if len(hashes) == 1:
      return self.copy_to_clipboard(hashes, 0)
      
    self.view.window().show_quick_panel(hashes, lambda index:
      self.copy_to_clipboard(hashes, index)
    )

  def post_selections(self, selections):
    hashes = []
    for selection in selections:
      try:
        request = urllib2.Request('http://pastebin.fi/documents', selection) 
        response = urllib2.urlopen(request)  
        html = response.read()
        data = json.loads(html)
        url = "http://pastebin.fi/" + data[u'key']

        # Check for extension
        file_path = self.view.file_name()
        if not (file_path is None):
          url += "." + file_path.split(".")[-1]

        hashes.append([url, "Copy to clipboard"])

      except (urllib2.HTTPError) as (e):  
        sublime.error_message('%s: HTTP error %s contacting API' % (__name__, str(e.code)))
      except (urllib2.URLError) as (e):  
        sublime.error_message('%s: URL error %s contacting API' % (__name__, str(e.reason))) 
    
    self.show_urls(hashes)

