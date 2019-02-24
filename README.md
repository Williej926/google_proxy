# google_proxy


# To build new squid image

Within `docker/` 

```
gcloud builds submit --tag gcr.io/tactile-shelter-224523/my-squid-image .
```

# create new password

```
htpasswd -cm <password file> <username>
```