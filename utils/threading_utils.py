import threading

def run_in_thread(target_func, *args, **kwargs):
    """Run a function in a separate daemon thread"""
    thread = threading.Thread(
        target=target_func,
        args=args,
        kwargs=kwargs,
        daemon=True
    )
    thread.start()
    return thread