from .. import models,schemas
from sqlalchemy.orm import Session
from fastapi import status, HTTPException,Depends, APIRouter,Response
from ..database import get_db
from typing import List
from .. import oauth2


router=APIRouter(
    prefix= "/posts",
    tags=["Posts"]
)

#get all posts
@router.get('/',response_model=List[schemas.Post])
async def get_posts(db: Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts")
    # posts=cursor.fetchall()
    posts= db.query(models.Post).all()
    return posts


#get latest post
@router.get('/latest',response_model=List[schemas.Post])
async def latest_post(db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    new_posts=db.query(models.Post).order_by(models.Post.created_at.desc()).all()
    return new_posts


#get specific post
@router.get('/{id}',response_model=schemas.Post)
async def get_post(id:int,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):  
    try:
        # cursor.execute("SELECT * FROM posts WHERE id=%s",(str(id),))
        # post=cursor.fetchone()
        post=db.query(models.Post).filter(models.Post.id==id).first()
        return post
    except: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
  
#create a post
@router.post('/', status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_posts(post:schemas.PostCreate,db: Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    
    print(user_id)
    try:
        # cursor.execute("INSERT INTO posts(title,content,published) VALUES(%s,%s,%s)RETURNING *",(post.title,post.content,post.published))
        # new_post=cursor.fetchone()
        # conn.commit()

        new_post=models.Post(**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"couldn't create: {str(e)}")




#delete a post
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):

    # cursor.execute("DELETE FROM posts where id=%s RETURNING *",(str(id),))
    # deleted_post= cursor.fetchone()
    # conn.commit()
    post=db.query(models.Post).filter(models.Post.id==id)

    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.patch('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.Post)
async def update_post(id:int,updated_post:schemas.PostCreate,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *",(p.title,p.content,p.published,str(id)))
    # updated_post=cursor.fetchone()

    # conn.commit()
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post= post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    db.refresh(post)

    return post




