# Django Blog - Comments Feature

## Features
- Users can add comments to blog posts.
- Only authenticated users can post, edit, and delete their own comments.
- Comments are displayed under each blog post.
- Secure access using Django authentication.

## URLs
| URL | View | Access |
|------|------|--------|
| `/post/<id>/` | View post & comments | Everyone |
| `/post/<id>/comment/new/` | Add comment | Authenticated users |
| `/comment/<id>/update/` | Edit comment | Only the comment author |
| `/comment/<id>/delete/` | Delete comment | Only the comment author |

## Setup Instructions
1. Run migrations:
   python manage.py makemigrations
   python manage.py migrate
