Document API endpoints:

POST /posts/ → Create a post

GET /posts/ → List all posts (supports pagination and search)

GET /posts/{id}/ → Retrieve a single post

PUT /posts/{id}/ → Update a post (only the author can)

DELETE /posts/{id}/ → Delete a post (only the author can)

Follow a user: POST /api/accounts/follow/{user_id}/

Unfollow a user: POST /api/accounts/unfollow/{user_id}/

Get user feed: GET /api/feed/