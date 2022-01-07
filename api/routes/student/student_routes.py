
from fastapi import APIRouter, HTTPException, status


def construct_router():

    student = APIRouter(
        tags=["Student"]
    )


    @student.get("/{roll_no}", status_code=status.HTTP_200_OK)
    async def get_student_by_roll(roll_no: str):
        return roll_no

    @student.get("/", status_code=status.HTTP_200_OK)
    async def get_student():
        pass

    @student.post("/add", status_code=status.HTTP_201_CREATED)
    async def add_student():
        pass

    @student.post("/ban", status_code=status.HTTP_200_OK)
    async def ban_student():
        pass


    @student.delete("/delete", status_code=status.HTTP_200_OK)
    async def delete_student():
        pass


    return student
