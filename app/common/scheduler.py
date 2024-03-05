from fastapi_scheduler import SchedulerAdmin

from app.repositories.token import JWTTokenRepository

scheduler = SchedulerAdmin.scheduler


@scheduler.scheduled_job("interval", minutes=15)
async def interval_task_test():
    await JWTTokenRepository.delete_expired_tokens()
