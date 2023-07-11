# CLI

```
./version_maintainer cli "folder/job-name 1.0"
./version_maintainer cli -u "folder/job-name 1.0"
```

# HTTP Server

```
curl -sd "folder/job-name 1.0" localhost:8080
curl -X PATCH -d "folder/job-name 1.0" localhost:8080
```
