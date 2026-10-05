import logging
from apscheduler.schedulers.background import BackgroundScheduler
from .scraper import ScraperService
from ..database import SessionLocal

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler(timezone="Asia/Kolkata")


def run_scraper_job() -> int:
    with SessionLocal() as session:
        count = ScraperService(session).run_once()
        logger.info("Scraper job persisted %s updates", count)
        return count


def start_scheduler() -> None:
    if scheduler.running:
        return
    scheduler.add_job(run_scraper_job, "interval", minutes=15, id="delay-scraper", replace_existing=True, max_instances=1)
    scheduler.start()


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
