import os, fnmatch
import sys
import pyinotify


class EventProcessor(pyinotify.ProcessEvent):
    _methods = ["IN_CREATE",
                "IN_DELETE",
                "IN_DELETE_SELF",
                "IN_MODIFY",
                "IN_MOVED_TO"]

def process_generator(cls, method):
    def _method_name(self, event):

        file1 = open("/usr/local/src/output.txt","w")
        for entry in os.scandir('/usr/local/src/monitor/'):
            if entry.is_file():
                print("(\"Updated File is: "+entry.name+")",file = file1)
        file1.close()

    _method_name.__name__ = "process_{}".format(method)
    setattr(cls, _method_name.__name__, _method_name)

for method in EventProcessor._methods:
    process_generator(EventProcessor, method)

watch_manager = pyinotify.WatchManager()
event_notifier = pyinotify.Notifier(watch_manager, EventProcessor())

watch_this = os.path.abspath("/usr/local/src/monitor/")
watch_manager.add_watch(watch_this, pyinotify.ALL_EVENTS)
event_notifier.loop()
