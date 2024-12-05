import uvicorn
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def main():
    uvicorn.run(
        "src.app.app:app",
        host="0.0.0.0",
        port=8004,
        reload=True,
        reload_dirs=".",
        log_level="info",
        reload_excludes="volumes",
    )


if __name__ == "__main__":
    main()
