from datetime import datetime, timedelta, timezone

from .database import Base, SessionLocal, engine
from .models import DelayIncident


INCIDENTS = [
    ("Western", "UP", "Dadar", "Dadar - Bandra", 18, "Major", "Signal fault near Dadar is holding UP services."),
    ("Western", "DN", "Andheri", "Andheri - Borivali", 12, "Major", "Overhead wire fluctuation is slowing DN trains."),
    ("Western", "UP", "Borivali", "Borivali - Andheri", 7, "Minor", "Platform congestion is causing short holds."),
    ("Western", "DN", "Mumbai Central", "Dadar - Mumbai Central", 24, "Severe", "Points failure reported near Mumbai Central."),
    ("Western", "UP", "Nalasopara", "Virar - Nalasopara", 5, "Minor", "Track inspection is causing a brief service delay."),
    ("Western", "DN", "Bandra", "Bandra - Andheri", 31, "Severe", "Technical snag has disrupted DN fast services."),
    ("Central", "DN", "Kurla", "Dadar - Kurla", 27, "Severe", "A technical snag at Kurla is delaying DN services."),
    ("Central", "UP", "Ghatkopar", "Ghatkopar - Vikhroli", 6, "Minor", "Track congestion is causing a small UP delay."),
    ("Central", "DN", "Thane", "Kurla - Thane", 14, "Major", "Signal checks near Thane are slowing trains."),
    ("Central", "UP", "Byculla", "Byculla - Dadar", 9, "Minor", "Crowding at Byculla is delaying departures."),
    ("Central", "DN", "Vikhroli", "Ghatkopar - Vikhroli", 19, "Major", "Overhead equipment inspection is in progress."),
    ("Central", "UP", "Dadar", "Dadar - Kurla", 22, "Severe", "A points failure at Dadar is affecting UP locals."),
    ("Harbour", "UP", "Wadala Road", "Wadala Road - Kurla", 9, "Minor", "Points failure near Wadala Road is causing delays."),
    ("Harbour", "DN", "Vashi", "Panvel - Vashi", 22, "Severe", "Heavy rainfall has slowed DN services."),
    ("Harbour", "UP", "Govandi", "Govandi - Mankhurd", 11, "Major", "Signal issue near Govandi is affecting UP trains."),
    ("Harbour", "DN", "Chembur", "Chembur - Tilak Nagar", 4, "Minor", "A short platform hold is being cleared."),
    ("Harbour", "UP", "Kurla", "Wadala Road - Kurla", 16, "Major", "Track congestion near Kurla is delaying UP locals."),
    ("Harbour", "DN", "Mankhurd", "Govandi - Mankhurd", 8, "Minor", "A late rake arrival is causing a short delay."),
]


def seed() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        now = datetime.now(timezone.utc)
        db.add_all(
            [
                DelayIncident(
                    line=line,
                    direction=direction,
                    station=station,
                    affected_stretch=stretch,
                    delay_minutes=delay,
                    priority=priority,
                    announcement_text=announcement,
                    created_at=now - timedelta(minutes=index * 7),
                )
                for index, (line, direction, station, stretch, delay, priority, announcement) in enumerate(INCIDENTS)
            ]
        )
        db.commit()
    print(f"Seeded {len(INCIDENTS)} delay incidents.")


if __name__ == "__main__":
    seed()
