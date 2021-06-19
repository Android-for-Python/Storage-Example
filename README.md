# Storage

*Shared storage, now available on device api >= 21*

On Android shared storage is a database not a Linux file system. Private storage is a Linux file system. [storage.py](https://github.com/RobertFlatt/Android-for-Python/blob/main/storage/storage.py) implements an api for database access of this app's public storage.

The shared storage operations provided are insert(), delete(), and recieve(), these copy files between this app's private and shared storage. [More details.](https://github.com/RobertFlatt/Android-for-Python/blob/main/storage/API_STORAGE_README.txt))

Use of the Android file picker to copy files from other app's shared storage is shown.

The buildozer options are documented in [BUILDOZER_README.txt](https://github.com/RobertFlatt/Android-for-Python/blob/main/storage/BUILDOZER_README.txt)

[Download from the Code Button here](https://github.com/RobertFlatt/Android-for-Python)
