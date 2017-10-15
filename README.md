# fbcomments
Simple script for downloading all facebook comments and their answers.

## Dependencies
* Python 3.5 +
* urllib

## How to use
```
usage: fbcomments.py [-h] -a ACCESS_TOKEN -p PAGE_URL -i POST_ID -f FILE_NAME
                     [--version]
```

#### Where:
  * [ACCESS_TOKEN](https://developers.facebook.com/docs/facebook-login/access-tokens/): is an opaque character string that identifies a user.
  * PAGE_URL: is the url of the facebook page where is the post, video or image.
  * POST_ID: is the id of the post.
  * FILE_NAME: output file where json result will be wrote.

### Example:

Suppose you want get all comments from this post: https://www.facebook.com/IFeakingLoveScience/posts/1930277590326576

```
fbcomments.py -a XXX... -p https://www.facebook.com/IFeakingLoveScience -i 1930277590326576 -f comments.txt
```


