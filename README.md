# s3Checker

Check if a S3 bucket (or a list of buckets) exists and tries to get the bucket ACL to check bucket permissions

```
usage: main.py [-h] [--wordlist wordlist-path] [--single bucket-name] [--only-check-existence [True/False]]

Test for buckets permissions

optional arguments:
  -h, --help            show this help message and exit
  --wordlist wordlist-path
  --single bucket-name
  --only-check-existence [True/False]
```

---

### Example: 

```
./s3Checker.py --only-check-existence --single hackerone
[+] hackerone is a valid bucket
```

---
If you want to contribute just create an issue, I'll be glad to collaborate with you

---
With <3 by @xpl0ited1