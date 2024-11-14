from fastapi import HTTPException
from starlette import status


class UserExc:
    user_id: int

    @classmethod
    def http204(cls, user_id):
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"User with id {user_id} deleted",
        )

    @classmethod
    def http404(cls, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} doesnt exist",
        )

    @staticmethod
    def http400():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with same email exists",
        )


class PostExc:
    post_id: int

    @classmethod
    def http404(cls, post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} not exists",
        )

    @classmethod
    def http403(cls):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="NO PERMISSION FOR THIS POST!!!",
        )


class VoteExc:
    user_id: int
    post_id: int

    @classmethod
    def http404(cls):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vote does not exists",
        )

    @classmethod
    def http409(cls, user_id, post_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user_id} has already voted on post {post_id}",
        )
