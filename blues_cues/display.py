import tkinter as tk
import threading
import queue
import time
from collections import OrderedDict

UPDATE_RATE_MS = 3000   # update every 3s

class Application():
    def __init__(self, data, queue):
        """
        data: an OrderedDict {str : str}, mapping the title for the data
                to the data itself
        """
        self.queue = queue
        self.data = data

    def run(self):
        self.root = tk.Tk()

        self.root.title("Blue's Cues")
        self.root.geometry("200x{}".format(self.root.winfo_screenheight()))
        self.create_labels()

        self.root.after(0, self.process_queue_msg)

        self.root.mainloop()

    def create_labels(self):
        self.labels = OrderedDict()
        for title, data in self.data.items():
            # create 2 labels, one for title, one for data
            self.labels[title] = [
                tk.Label(self.root, text=title),
                tk.Label(self.root, text=data)
            ]
            self.labels[title][0].pack()
            self.labels[title][1].pack()
    
    def process_queue_msg(self):
        while self.queue.qsize():
            (title, data_item) = self.queue.get(0)
            self.data[title] = data_item
            self.labels[title][1].configure(text=data_item)

        self.root.after(UPDATE_RATE_MS, self.process_queue_msg)

    def on_close(self):
        # TODO: some stuff to output the stats possibly
        self.root.destroy()

### TEST FUNCTION FOR MULTITHREADING
def blocking_code(out_queue):
    print("Start blocking function")
    time.sleep(3)
    out_queue.put(("data1", "5"))
    time.sleep(3)
    print("End blocking function")

if __name__ == "__main__":
    # test multithreading with blocking_code function
    q = queue.Queue()
    app = Application({"data1": "1", "data2": "2"}, q)
    x = threading.Thread(target=blocking_code, args=(q,))
    x.start()
    app.run()