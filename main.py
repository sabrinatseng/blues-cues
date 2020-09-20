from blues_cues import display, video_processor
import queue
import threading

def run_vp(vp, queue):
    """
    vp: Video Processor
    """
    vp.run(queue)

def main():
    """
    Runs Blue's Cues alongside a Zoom call.
    """
    q = queue.Queue()
    app = display.Application({"Meeting Demographics": ""}, q)
    vp = video_processor.VideoProcessor()
    vp_thread = threading.Thread(target=run_vp, args=(vp, q))
    vp_thread.start()
    app.run()
    # probably a loop here
    # get audio input
    # get video input
    # process audio input
    # process video input
    # update display

if __name__ == "__main__":
    main()
