# LeanCloud Conversation Creation Profling

```
docker build -t lc-profile .
docker run -it -e LC_APP_ID=YOUR_APP_ID -e LC_MASTER_KEY=YOUR_MASTER_KEY -e NUMBER=50 -e REPEAT=3 -e FUNC=any_task lc-profile
```

or grab network details by curl:

```
gem install descriptive_statistics
export LC_APP_ID=YOUR_APP_ID
export LC_MASTER_KEY=YOUR_MASTER_KEY
ruby profile.rb create_conversation 150
```



