import os

if os.getenv("DEBUG", "0") == "1":
    import debugpy

    debugpy.listen(("localhost", 5678))
    print("⏳⏳⏳⏳ Waiting for debugger attach...")
    debugpy.wait_for_client()
