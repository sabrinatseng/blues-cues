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
    app = display.Application({
        "Meeting Demographics": "",
        "Meeting Sentiment": "",
        "Audience Engagement": "",
        }, q)
    vp = video_processor.VideoProcessor()
    vp_thread = threading.Thread(target=run_vp, args=(vp, q))
    vp_thread.start()
    app.run()

if __name__ == "__main__":
    main()
