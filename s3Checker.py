#!/usr/bin/python

#With <3 by Bastian Muhlhauser aka xpl0ited1 / xpl0ited11

import argparse
import boto3
import botocore
import random
import string
import hashlib


s3 = boto3.client('s3')

def get_acl(bucket):
    exists = False
    perms = ""
    try:
        result = s3.get_bucket_acl(Bucket=bucket)
        for grant in result["Grants"]:
            perms += grant["Permission"] + " "
        exists = True
    except botocore.exceptions.ClientError as e:
        if "NoSuchBucket" in str(e):
            exists = False
        if "AccessDenied" in str(e):
            exists = True
    return exists, perms


def can_write(bucket):
    filename = create_random_file()
    has_perm = False
    try:
        with open(filename, 'rb') as data:
            result = s3.upload_fileobj(data, bucket, 'test.txt')
            has_perm = True
    except botocore.exceptions.ClientError as e:
        if "NoSuchBucket" in str(e):
            pass
        if "AccessDenied" in str(e):
            has_perm = False
    delete_file(filename)
    return has_perm


def can_read(bucket):
    has_perm = False
    try:
        result = s3.list_objects(Bucket=bucket)
        has_perm = True
    except botocore.exceptions.ClientError as e:
        if "NoSuchBucket" in str(e):
            pass
        if "AccessDenied" in str(e):
            has_perm = False
    return has_perm


def can_download(bucket):
    has_perm = False
    try:
        result = s3.download_file(bucket, 'hello.txt', '/tmp/hello.txt')
        has_perm = True
    except botocore.exceptions.ClientError as e:
        if "NoSuchBucket" in str(e):
            pass
        if "AccessDenied" in str(e):
            has_perm = False
        if "Forbidden" in str(e):
            has_perm = False
    return has_perm


def create_random_file():
    letters = string.ascii_lowercase
    filename = ''.join(random.choice(letters) for i in range(10))
    filename = hashlib.md5(filename.encode()).digest().hex()
    f = open(filename+".txt", "a")
    f.write(filename)
    f.close()
    return filename+".txt"


def delete_file(filename):
    import os
    os.remove(filename)


def test_bucket(bucket):
    exists, perms = get_acl(bucket)
    if exists:
        upload_perm = can_write(bucket)
        list_objects_perm = can_read(bucket)
        download_perm = can_download(bucket)
        if upload_perm:
            perms += "WRITE "
        if list_objects_perm:
            perms += "LISTOBJECTS "
        if download_perm:
            perms += "READ "
        if len(perms) > 0:
            print("[+] %s: %s" % (bucket, perms))


def read_file(filename):
    with open(filename, "rb") as file:
        return file.readlines()



def main():
    parser = argparse.ArgumentParser(description="Test for buckets permissions")
    parser.add_argument("--wordlist", metavar="wordlist-path", type=str)
    parser.add_argument("--single", type=str, metavar="bucket-name")
    parser.add_argument("--only-check-existence", metavar="True/False", help="False as default", default=argparse.SUPPRESS, nargs="?")
    args = parser.parse_args()

    try:
        if args.only_check_existence is None:
            if args.wordlist:
                wordlist = args.wordlist
                words = read_file(wordlist)
                for word in words:
                    exists, _ = get_acl(word)
                    if exists:
                        print("[+] %s is a valid bucket" % word)
            else:
                exists, _ = get_acl(args.single)
                if exists:
                    print("[+] %s is a valid bucket" % args.single)
    except AttributeError as e:
        if args.wordlist:
            wordlist = args.wordlist
            words = read_file(wordlist)
            for word in words:
                test_bucket(word)
        else:
            test_bucket(args.single)



if __name__ == '__main__':
    main()
