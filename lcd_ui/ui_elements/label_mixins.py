import time

class DynamicLabel(object):
    def run(self,event_queue,interval=1):
        while self._parent.is_displayed:
            self.update_content(event_queue)
            time.sleep(interval)

    def update_content(self, event_queue):
        pass

class ScrollingLabel(DynamicLabel):
    def run(self,event_queue,interval=.6):
        line_len=16
        self.avail_chars = line_len-len(self.init_content)-1
        
        if self.dynamic_content:
            if isinstance(self.dynamic_content,str):
                if self.avail_chars >= len(self.dynamic_content):
                    self.init_content = self.init_content + self.dynamic_content
                    self.dynamic_content = ""

        self.current_start = 0
        super().run(event_queue,interval=interval)

    def update_content(self, event_queue):
        current_content = self.content
        if isinstance(self.dynamic_content,str):
            dynamic_content = self.dynamic_content
        else:
            dynamic_content = self.dynamic_content.value


        extra_chars = len(dynamic_content)-self.avail_chars
        self.content = self.init_content + dynamic_content[self.current_start:self.current_start+self.avail_chars]
        self.current_start = (self.current_start + 1)%(extra_chars+1)
        
        if current_content != self.content:
            event_queue.put({'type':'display_update'})