import sublime, sublime_plugin, time, os.path

activity_json_template = "{time_gmt_ms:%s,event:'%s',id:%s,buffer_id:%s,is_loading:%s,is_dirty:%s,is_read_only:%s,file_ext:'%s',size:%s}"  
class SublimeListenrCommand(sublime_plugin.EventListener):  
  def get_activity_json(self, view, evt):
    time_gmt_ms = str(int( time.time() * 1000 ))
    file_ext = os.path.splitext( view.file_name() )[1]
    file_size = str( view.size() )    
    return activity_json_template % (time_gmt_ms, evt, view.id(), view.buffer_id(), view.is_loading(), view.is_dirty(), view.is_read_only(), file_ext, file_size)
  def handle_activity(self, activity_json):
    # TODO send this bad boy to the server
    print activity_json
  def on_new(self, view):
    self.handle_activity( self.get_activity_json(view, "on_new") )
  def on_clone(self, view):
    self.handle_activity( self.get_activity_json(view, "on_clone") )
  def on_load(self, view):
    self.handle_activity( self.get_activity_json(view, "on_load") )
  def on_close(self, view):
    self.handle_activity( self.get_activity_json(view, "on_close") )
  def on_pre_save(self, view):
    self.handle_activity( self.get_activity_json(view, "on_pre_save") )
  def on_post_save(self, view): 
    self.handle_activity( self.get_activity_json(view, "on_post_save") )
  def on_modified(self, view):
    self.handle_activity( self.get_activity_json(view, "on_modified") )
  def on_selection_modified(self, view):
    self.handle_activity( self.get_activity_json(view, "on_selection_modified") )
  def on_activated(self, view):
    self.handle_activity( self.get_activity_json(view, "on_activated") )
  def on_deactivated(self, view):
    self.handle_activity( self.get_activity_json(view, "on_deactivated") )