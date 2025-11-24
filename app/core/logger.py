"""
Error logging system for Overlay Annotator
Logs all errors to file for debugging
"""
import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logging(log_dir: Path = None):
    """Setup logging to both file and console"""
    
    # Create logs directory
    if log_dir is None:
        log_dir = Path.home() / "overlay_annotator_logs"
    log_dir.mkdir(exist_ok=True)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"overlay_annotator_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # File handler - saves everything
            logging.FileHandler(log_file, encoding='utf-8'),
            # Console handler - shows important messages
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger('OverlayAnnotator')
    logger.info("=" * 60)
    logger.info("Overlay Annotator Started")
    logger.info(f"Log file: {log_file}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {sys.platform}")
    logger.info("=" * 60)
    
    return logger, log_file


def log_exception(logger, exc_info=None):
    """Log an exception with full traceback"""
    if exc_info is None:
        exc_info = sys.exc_info()
    
    logger.error("Exception occurred:", exc_info=exc_info)
    
    # Also print to console for visibility
    import traceback
    print("\n" + "=" * 60)
    print("ERROR OCCURRED:")
    print("=" * 60)
    traceback.print_exception(*exc_info)
    print("=" * 60)
    print("Check log file for full details")
    print("=" * 60 + "\n")


# Global exception handler
def exception_hook(exc_type, exc_value, exc_traceback):
    """Global exception handler"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger = logging.getLogger('OverlayAnnotator')
    logger.critical("Unhandled exception:", exc_info=(exc_type, exc_value, exc_traceback))
    
    # Show user-friendly error
    print("\n" + "!" * 60)
    print("CRITICAL ERROR - Application crashed!")
    print("!" * 60)
    print(f"Error: {exc_value}")
    print("\nPlease check the log file for details.")
    print("Log location: ~/overlay_annotator_logs/")
    print("!" * 60 + "\n")
