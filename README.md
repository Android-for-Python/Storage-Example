# Storage

*Shared storage*

### **Depreciated, use [shared_storage_example](https://github.com/Android-for-Python/shared_storage_example).**



**This example is experimental**

**On devices running Android 10 and higher shared storage is a database not a Linux file system**. Private storage is a Linux file system. [storage.py](https://github.com/Android-for-Python/Storage-Example/blob/main/storage.py) implements an api for database access of this app's public storage.

The shared storage operations provided are insert(), delete(), and recieve(), these copy files between this app's private and shared storage. [More details.](https://github.com/Android-for-Python/Storage-Example/blob/main/API_STORAGE_README.txt)

The example attempts to emulate Android 10+ shared storage on devices running Android <= 9. However the underlying Android api has different functionality which may result in different behavior of this example. Use with caution on devices running Android 9 or less, or better still use the traditional file system model.

Use of the Android file picker to copy files from other app's shared storage is shown.

The buildozer options are documented in [BUILDOZER_README.txt](https://github.com/Android-for-Python/Storage-Example/blob/main/BUILDOZER_README.txt)

