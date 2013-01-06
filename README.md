# SublimeListenr

Listens for any code editing events in Sublime Text 2. Logs them to a server for fun & profit. Or more specifically for a fun experiment in capturing and visualizing code activity. And ideally turning it into something cool, like generative ambient sounds. No personal/confidential information is captured, although to make this more fun & useful you can set your github username in the settings file in order to do stats on your activity. This plugin is intended for fun, creative endeavors :)

## Example

### On Client

Here's a sample activity message (captured as JSON) when typing a character into a Python file:

```json
{"t":1357441371196,"e":6,"i":28,"b":26,"l":0,"d":0,"r":0,"f":"py","s":4564,"h":"6a75228602aaaa8d473afff7a4163d2a","g":"cbumgard"}
```

### On Server

Which is transformed to the following on the server and persisted in MongoDB to look like:

```json
{
  "time_gmt_ms" : ISODate("2013-01-06T03:00:56.203Z"),
  "event" : "on_selection_modified",
  "id" : 28,
  "buffer_id" : 26,
  "is_loading" : false,
  "is_dirty" : false,
  "is_read_only" : false,
  "file_ext" : ".py",
  "size" : 4564,
  "file_name_hash" : "6a75228602aaaa8d473afff7a4163d2a",
  "github_username" : "cbumgard",
  "client_ip" : "127.0.0.1",
  "created" : ISODate("2013-01-06T03:00:56.508Z"),
  "__v" : 0,
  "_id" : ObjectId("50e8e8e87f0bba0000000014")
}
```

## Settings

Add your github username to monitor, aggregate, or play with your data by changing the setting "github_username" in the [settings file](https://github.com/cbumgard/SublimeListenr/blob/master/SublimeListenr.sublime-settings).

## Captured Activity

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

Taken from [Sublime Text Plugin Docs](http://www.sublimetext.com/docs/2/api_reference.html#sublime_plugin.EventListener)

## License

This module is MIT licensed [here](https://github.com/cbumgard/SublimeListenr/blob/master/LICENSE).