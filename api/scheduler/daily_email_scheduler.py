from uuid import uuid4

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from api.services.email.send_daily_emails import SendDailyQuoteEmails


class EmailScheduler:
    def __init__(
        self, scheduler: AsyncIOScheduler, sender: SendDailyQuoteEmails
    ) -> None:
        self.scheduler = scheduler
        self.sender = sender

    async def start(self) -> None:
        self.scheduler.add_job(
            self.sender.execute,
            trigger="cron",
            id=str(uuid4()),
            name="Enviar email diários",
            hour=8,
            minute=0,
            coalesce=True,
            misfire_grace_time=300,
            replace_existing=True,
            max_instances=1,
        )

        self.scheduler.start()

    async def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
