import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from backend.services.scraper import ScraperService

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        ScraperService.run,
        trigger=IntervalTrigger(minutes=15),
        id='scraper_15min',
        name='Scraper Task',
        misfire_grace_time=60,
        max_instances=1
    )
    scheduler.start()
    logger.info("Background scheduler initialized and started.")
