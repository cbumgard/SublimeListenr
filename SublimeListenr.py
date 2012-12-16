import sublime
import sublime_plugin
import time
import os.path
import urllib
import httplib
import threading

# t = time_gmt_ms
# e = event
# i = id
# b = buffer_id
# l = is_loading
# d = is_dirty
# r = is_read_only
# f = file_ext
# s = size
activity_json_template = '{"t":%s,"e":%s,"i":%s,"b":%s,"l":%s,"d":%s,"r":%s,"f":"%s","s":%s}'

events = {
  "on_new": 1, 
  "on_clone": 2, 
  "on_load": 3, 
  "on_close": 4, 
  "on_pre_save": 5, 
  "on_post_save": 6, 
  "on_modified": 7, 
  "on_selection_modified": 8, 
  "on_activated": 9, 
  "on_deactivated": 10}

api_url_base = "listenr-5152.onmodulus.net:80"
api_endpoint = "/listenr"

class SublimeListenrCommand(sublime_plugin.EventListener):  
  def __init__(self):
    self.activity = []    
    self.threads = []
  def get_activity_json(self, view, evt):
    time_gmt_ms = str(int( time.time() * 1000 ))
    file_ext = os.path.splitext( view.file_name() )[1]
    file_size = str( view.size() )    
    return activity_json_template % (
      time_gmt_ms, 
      evt,
      view.id(), 
      view.buffer_id(), 
      1 if view.is_loading() else 0, 
      1 if view.is_dirty() else 0, 
      1 if view.is_read_only() else 0,
      file_ext, 
      file_size)
  def post_activity_to_server(self):
    if len(self.activity) == 0:
      return
    thread = SublimeListenrApiPost(self.activity, 5)
    self.threads.append(thread)
    thread.start()
    self.activity = [] # clear array to free space; the thread made a local copy on init
    self.handle_threads(self.threads)
  def handle_activity(self, activity_json):
    self.activity.append(activity_json)
  def on_new(self, view):
    self.handle_activity( self.get_activity_json(view, events["on_new"]) )
  def on_clone(self, view):
    self.handle_activity( self.get_activity_json(view, events["on_clone"]) )
  def on_load(self, view):
    self.handle_activity( self.get_activity_json(view, events["on_load"]) )
  def on_close(self, view):
    self.handle_activity( self.get_activity_json(view, events["on_close"]) )
    self.post_activity_to_server()    
  def on_pre_save(self, view):
    self.handle_activity( self.get_activity_json(view, events["on_pre_save"]) )
  def on_post_save(self, view): 
    self.handle_activity( self.get_activity_json(view, events["on_post_save"]) )
    self.post_activity_to_server()
  def on_modified(self, view):
    self.handle_activity( self.get_activity_json(view, events["on_modified"]) )
  def on_selection_modified(self, view):
    self.handle_activity( self.get_activity_json(view, events["on_selection_modified"]) )
  def on_activated(self, view):
    self.handle_activity( self.get_activity_json(view, events["on_activated"]) )
  def on_deactivated(self, view):
    self.handle_activity( self.get_activity_json(view, events["on_deactivated"]) )
  def handle_threads(self, threads, offset=0, i=0, dir=1):
      next_threads = []
      for thread in self.threads:
          if thread.is_alive():
              next_threads.append(thread)
              continue
          if thread.result == False:
              continue
      self.threads = next_threads
      sublime.status_message('Listenr successfully posted activity')

class SublimeListenrApiPost(threading.Thread):
  def __init__(self, activity_json, timeout):
    self.activity_json = activity_json
    self.timeout = timeout
    self.result = None  
    threading.Thread.__init__(self)
  def run(self):
    try:
      print "[%s Plugin] Posting %s activity events to %s" % \
        (__name__, len(self.activity_json), api_url_base)
      data = urllib.urlencode({"activity": self.activity_json}, True)
      headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
      conn = httplib.HTTPConnection(api_url_base)
      conn.request("POST", api_endpoint, data, headers)
      conn.close()      
      return
    except (Exception) as (e):
      err = '[%s Plugin] URL error %s contacting API' % (__name__, str(e))  
    print err
    # sublime.error_message(err)
    self.result = False      
