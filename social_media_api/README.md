Document API endpoints:

POST /posts/ → Create a post

GET /posts/ → List all posts (supports pagination and search)

GET /posts/{id}/ → Retrieve a single post

PUT /posts/{id}/ → Update a post (only the author can)

DELETE /posts/{id}/ → Delete a post (only the author can)

POST /comments/ → Comment on a post

GET /comments/ → List comments