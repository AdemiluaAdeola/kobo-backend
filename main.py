# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List, Optional
# import uuid
# from datetime import datetime

# app = FastAPI(title="Task Management API")

# class Task(BaseModel):
#     id: str
#     title: str
#     description: Optional[str] = None
#     completed: bool = False
#     created_at: datetime
    
# tasks: List[Task] = []

# @app.post("/tasks", response_model=Task)
# def create_task(task: Task):
#     task.id = str(uuid.uuid4())
#     task.created_at = datetime.utcnow()
#     tasks.append(task)
#     return task

# @app.get("/tasks", response_model=List[Task])
# def get_tasks():
#     return tasks

# @app.get("/tasks/{task_id}", response_model=Task)
# def get_task(task_id: str):
#     for task in tasks:
#         if task.id == task_id:
#             return task
#     return {"error": "Task not found"}

# @app.put("/tasks/{task_id}", response_model=Task)
# def update_task(task_id: str, updated_task: Task):
#     for task in tasks:
#         if task.id == task_id:
#             task.title = updated_task.title
#             task.description = updated_task.description
#             task.completed = updated_task.completed
#             return task
#     return {"error": "Task not found"}

# @app.delete("/tasks/{task_id}")
# def delete_task(task_id: str):
#     for task in tasks:
#         if task.id == task_id:
#             tasks.remove(task)
#             return {"message": "Task deleted"}
#     return {"error": "Task not found"}

# from fastapi import FastAPI, HTTPException, Depends
# from pydantic import BaseModel
# from typing import List, Optional
# import uuid
# from datetime import datetime

# app = FastAPI(title="Simple Blog API")

# # ============ MODELS (like Django Models, but for validation) ============

# class PostBase(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class PostCreate(PostBase):
#     pass

# class Post(PostBase):
#     id: str
#     created_at: datetime
    
#     class Config:
#         from_attributes = True  # Allows ORM model conversion

# # ============ "DATABASE" (simulating with a dict for simplicity) ============

# fake_db = {}

# # ============ DEPENDENCIES (like Django's get_object_or_404) ============

# def get_post_or_404(post_id: str):
#     if post_id not in fake_db:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return fake_db[post_id]

# # ============ ROUTES (like Django's views.py + urls.py combined) ============

# @app.get("/")
# async def root():
#     return {"message": "Welcome to FastAPI Blog!"}

# @app.get("/posts", response_model=List[Post])
# async def list_posts():
#     """List all posts - like Django's ListView"""
#     return list(fake_db.values())

# @app.get("/posts/{post_id}", response_model=Post)
# async def get_post(post: Post = Depends(get_post_or_404)):
#     """Get single post - dependency injection handles 404"""
#     return post

# @app.post("/posts", response_model=Post, status_code=201)
# async def create_post(post: PostCreate):
#     """Create post - FastAPI validates input automatically"""
#     post_id = str(uuid.uuid4())
#     new_post = Post(
#         id=post_id,
#         created_at=datetime.now(),
#         **post.model_dump()
#     )
#     fake_db[post_id] = new_post
#     return new_post

# @app.put("/posts/{post_id}", response_model=Post)
# async def update_post(
#     post_update: PostCreate,
#     post: Post = Depends(get_post_or_404)
# ):
#     """Update post - partial updates handled via PATCH if needed"""
#     updated = Post(
#         id=post.id,
#         created_at=post.created_at,
#         **post_update.model_dump()
#     )
#     fake_db[post.id] = updated
#     return updated

# @app.delete("/posts/{post_id}", status_code=204)
# async def delete_post(post: Post = Depends(get_post_or_404)):
#     """Delete post - 204 No Content on success"""
#     del fake_db[post.id]
#     return None

from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timedelta
from enum import Enum
import uuid
import jwt
from passlib.context import CryptContext

app = FastAPI(title="Blog API with Auth")

# ============ CONFIGURATION ============
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ============ PASSWORD HASHING ============
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# ============ MODELS ============

class UserRole(str, Enum):
    READER = "reader"      # Can read only
    AUTHOR = "author"      # Can CRUD own posts
    EDITOR = "editor"      # Can edit any post, publish/unpublish
    ADMIN = "admin"        # Full access

class UserBase(BaseModel):
    username: str
    email: str
    role: UserRole = UserRole.READER

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class User(UserBase):
    id: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime

class UserPublic(BaseModel):
    """Public user info (no password)"""
    id: str
    username: str
    role: UserRole

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=10)
    published: bool = False

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=10)
    published: Optional[bool] = None

class Post(PostBase):
    id: str
    author_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class PostWithAuthor(Post):
    author: UserPublic

class Token(BaseModel):
    access_token: str
    token_type: str

# ============ MOCK DATABASE ============
users_db = {}
posts_db = {}

# ============ AUTH & PERMISSIONS SYSTEM ============

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class PermissionDenied(HTTPException):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

# --- Authentication Dependencies ---

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Like Django's request.user - validates JWT and returns user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = users_db.get(user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Like Django's @login_required"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# --- Permission Checkers (like Django's permission decorators) ---

def require_role(*allowed_roles: UserRole):
    """Decorator-like dependency for role-based access"""
    def checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in allowed_roles:
            raise PermissionDenied(
                f"Required role: {', '.join(allowed_roles)}"
            )
        return current_user
    return checker

# Specific permission shortcuts
require_author = require_role(UserRole.AUTHOR, UserRole.EDITOR, UserRole.ADMIN)
require_editor = require_role(UserRole.EDITOR, UserRole.ADMIN)
require_admin = require_role(UserRole.ADMIN)

# --- Object-Level Permissions (like Django's ObjectPermission) ---

def check_post_ownership(post: Post, user: User) -> bool:
    """Like Django's .has_object_permission()"""
    return post.author_id == user.id

def can_edit_post(post: Post, user: User) -> bool:
    """Complex permission logic"""
    if user.role == UserRole.ADMIN:
        return True
    if user.role == UserRole.EDITOR:
        return True  # Editors can edit any post
    if user.role == UserRole.AUTHOR and post.author_id == user.id:
        return True  # Authors can only edit own posts
    return False

def can_delete_post(post: Post, user: User) -> bool:
    """Only admins and authors (own posts) can delete"""
    if user.role == UserRole.ADMIN:
        return True
    if user.role == UserRole.AUTHOR and post.author_id == user.id:
        return True
    return False

def can_publish_post(user: User) -> bool:
    """Only editors and admins can publish"""
    return user.role in [UserRole.EDITOR, UserRole.ADMIN]

# ============ AUTH ROUTES ============

@app.post("/auth/register", response_model=UserPublic, status_code=201)
async def register(user_data: UserCreate):
    """User registration - like Django's UserCreationForm"""
    # Check unique username/email
    for existing in users_db.values():
        if existing.username == user_data.username:
            raise HTTPException(status_code=400, detail="Username already registered")
        if existing.email == user_data.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = str(uuid.uuid4())
    hashed_pw = get_password_hash(user_data.password)
    
    user = User(
        id=user_id,
        username=user_data.username,
        email=user_data.email,
        role=user_data.role,
        hashed_password=hashed_pw,
        created_at=datetime.now()
    )
    users_db[user_id] = user
    return UserPublic(id=user.id, username=user.username, role=user.role)

@app.post("/auth/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 token endpoint - like Django's login view"""
    # Find user by username
    user = next(
        (u for u in users_db.values() if u.username == form_data.username),
        None
    )
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "role": user.role.value},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.get("/auth/me", response_model=UserPublic)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user - like Django's request.user"""
    return UserPublic(id=current_user.id, username=current_user.username, role=current_user.role)

# ============ POST CRUD WITH PERMISSIONS ============

@app.post("/posts", response_model=Post, status_code=201)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(require_author)  # Must be author+
):
    """Create post - Authors can create, but editors must publish"""
    # Auto-publish for editors/admins, draft for authors
    published = post_data.published if can_publish_post(current_user) else False
    
    post_id = str(uuid.uuid4())
    now = datetime.now()
    
    post = Post(
        id=post_id,
        title=post_data.title,
        content=post_data.content,
        published=published,
        author_id=current_user.id,
        created_at=now,
        updated_at=now
    )
    posts_db[post_id] = post
    return post

@app.get("/posts", response_model=List[PostWithAuthor])
async def list_posts(
    published_only: bool = Query(True, description="Filter to published posts only"),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    List posts - Complex permission-based filtering
    - Anonymous: published only
    - Readers: published only  
    - Authors: published + their own drafts
    - Editors/Admins: all posts
    """
    posts = list(posts_db.values())
    filtered_posts = []
    
    for post in posts:
        # Determine if user can see this post
        can_see = False
        
        if post.published:
            can_see = True
        elif current_user:
            if current_user.role in [UserRole.EDITOR, UserRole.ADMIN]:
                can_see = True
            elif post.author_id == current_user.id:
                can_see = True
        
        if can_see:
            author = users_db.get(post.author_id)
            post_with_author = PostWithAuthor(
                **post.model_dump(),
                author=UserPublic(id=author.id, username=author.username, role=author.role)
            )
            filtered_posts.append(post_with_author)
    
    return filtered_posts

@app.get("/posts/{post_id}", response_model=PostWithAuthor)
async def get_post(
    post_id: str,
    current_user: Optional[User] = Depends(get_current_user)
):
    """Get single post with visibility check"""
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Visibility check
    if not post.published:
        if not current_user:
            raise HTTPException(status_code=403, detail="Authentication required")
        if current_user.role not in [UserRole.EDITOR, UserRole.ADMIN]:
            if post.author_id != current_user.id:
                raise PermissionDenied("Cannot view unpublished post")
    
    author = users_db.get(post.author_id)
    return PostWithAuthor(
        **post.model_dump(),
        author=UserPublic(id=author.id, username=author.username, role=author.role)
    )

@app.put("/posts/{post_id}", response_model=Post)
async def update_post(
    post_id: str,
    update_data: PostUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update post with object-level permissions"""
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check permissions
    if not can_edit_post(post, current_user):
        raise PermissionDenied("Cannot edit this post")
    
    # Special handling for publish/unpublish
    if update_data.published is not None:
        if not can_publish_post(current_user):
            raise PermissionDenied("Cannot publish/unpublish posts")
    
    # Apply updates
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(post, field, value)
    
    post.updated_at = datetime.now()
    posts_db[post_id] = post
    return post

@app.delete("/posts/{post_id}", status_code=204)
async def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete with ownership check"""
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if not can_delete_post(post, current_user):
        raise PermissionDenied("Cannot delete this post")
    
    del posts_db[post_id]
    return None

# ============ ADMIN ROUTES ============

@app.get("/admin/users", response_model=List[UserPublic])
async def list_all_users(
    current_user: User = Depends(require_admin)  # Admin only
):
    """Admin-only endpoint - like Django admin"""
    return [
        UserPublic(id=u.id, username=u.username, role=u.role)
        for u in users_db.values()
    ]

@app.patch("/admin/users/{user_id}/role")
async def change_user_role(
    user_id: str,
    new_role: UserRole,
    current_user: User = Depends(require_admin)
):
    """Promote/demote users"""
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = new_role
    return {"message": f"User {user.username} is now {new_role.value}"}

@app.post("/admin/posts/{post_id}/publish")
async def admin_publish_post(
    post_id: str,
    current_user: User = Depends(require_editor)  # Editor+
):
    """Editor/Admin can publish any post"""
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.published = True
    post.updated_at = datetime.now()
    return post

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)