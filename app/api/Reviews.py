from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Review
from app.schemas.ReviewSchema import ReviewCreate, ReviewUpdate, ReviewResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    new_review = Review(
        ClientID=review.ClientID,
        ServiceID=review.ServiceID,
        Rating=review.Rating,
        Comment=review.Comment,
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@router.get("/", response_model=list[ReviewResponse])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.ReviewID == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")
    return review


@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, review: ReviewUpdate, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.ReviewID == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")

    if review.Rating is not None:
        db_review.Rating = review.Rating
    if review.Comment is not None:
        db_review.Comment = review.Comment

    db.commit()
    db.refresh(db_review)
    return db_review


@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.ReviewID == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")

    db.delete(db_review)
    db.commit()
    return {"message": f"Valoración {review_id} eliminada"}
