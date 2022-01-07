from fastapi import  APIRouter, status, HTTPException


def construct_router():

    admin = APIRouter(
        tags=["Admin"]
    )

    @admin.post('/notify/student')
    async def notify_by_batch():
        pass

    @admin.post('/add/student/subscription')
    async def add_student_subscription():
        pass

    @admin.post('/remove/student/subscription')
    async def remove_student_subscription():
        pass

    @admin.post('/verify/student')
    async def verify_student():
        pass

    return admin
