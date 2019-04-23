# -*- coding: utf-8 -*-
from spike_system.view.apis import queue
def modify_mysql_inventory():
    while 1:
        result = queue.get_nowait()
        if not result:
            break
        print "output.py: data {} out of queue {}".format(result, time.strftime("%c"))
        time.sleep(2)