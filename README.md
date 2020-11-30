# Blog
### Primitive zero dep blog platform based in md

Decided I wanted to write a blog. Decided I wanted to make the publishing platform. Tried to keep everything basic as less time writing code is more time writing blog posts.

The project makes use of a GitHub actions workflow to build and sync the static site to an s3 bucket, however one could easily integrate this with rsync or any other CI workflow.

### Usage

There are no tests, validation or sanitization. Each post should be written in markdown and conform to the following structure w/ front matter -

```
[category]: <> (General)
[date]: <> (2020-10-24)
[title]: <> (Hello world)

This is the article!
```

Dates should be in ISO format YYYY-MM-DD


To build the website `python main.py articles/*.md`
An example deployment might look like `aws s3 sync build/ s3://AWS_BUCKET --acl public-read`