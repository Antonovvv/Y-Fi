# -*- coding:utf-8 -*-
class Watcher:
    modified = False

    def watch_modify(func):   # 监听变化
        def wrapper(self, *args, **kwargs):
            if not self.modified:
                self.modified = True
                self.on_modified()
            return func(self, *args, **kwargs)
        return wrapper

    def on_modified(self):  # 变化后执行
        pass

    def on_saved(self):
        pass
