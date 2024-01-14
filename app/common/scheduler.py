from fastapi_scheduler import SchedulerAdmin
from app.repositories.auth import AuthRepository


scheduler = SchedulerAdmin.scheduler


@scheduler.scheduled_job('interval', minutes=15)
async def interval_task_test():
    await AuthRepository.delete_expired_tokens()
