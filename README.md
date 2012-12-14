SublimeListenr
=

Listens for any code editing events in Sublime Text 2. Logs them to a server for fun & profit. Or more specifically for a fun experiment in capturing and visualizing code activity. And ideally turning it into something cool, like generative ambient sounds. **No personal/confidential information is captured.**

Here's a sample activity message (captured as JSON) when typing a character into a Python file:

> {time_gmt_ms:1355477878934,event:'on_modified',id:72,buffer_id:68,is_loading:False,is_dirty:True,is_read_only:False,file_ext:'.md',size:1444}

The following events are captured:

* on_new(view)    None  Called when a new buffer is created.
* on_clone(view)  None  Called when a view is cloned from an existing one.
* on_load(view) None  Called when the file is finished loading.
* on_close(view)  None  Called when a view is closed (note, there may still be other views into the same buffer).
* on_pre_save(view) None  Called just before a view is saved.
* on_post_save(view)  None  Called after a view has been saved.
* on_modified(view) None  Called after changes have been made to a view.
* on_selection_modified(view) None  Called after the selection has been modified in a view.
* on_activated(view)  None  Called when a view gains input focus.
* on_deactivated(view)  None  Called when a view loses input focus.

(Taken from http://www.sublimetext.com/docs/2/api_reference.html#sublime_plugin.EventListener)
