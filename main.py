from blues_cues import display, video_processor, audio_processor
import queue
import threading

def run_vp(vp, queue):
    """
    vp: Video Processor
    """
    vp.run(queue)

def run_ap(ap, queue):
    """
    ap: Audio Processor
    """
    ap.run(queue)

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

    ap = audio_processor.AudioProcessor()
    ap_thread = threading.Thread(target=run_ap, args=(ap, q))
    ap_thread.start()
    app.run()

if __name__ == "__main__":
    main()
