
# For testing only, we add 3 files types to include in the .apk
source.include_exts = py,png,jpg,kv,atlas  ,ogg,mp3,txt

# READ_EXTERNAL_STORAGE is required to read other app's public storage
# No other STORAGE permissions are required
# Unless the app device api < 29 when WRITE_EXTERNAL_STORAGE is required
android.permissions = READ_EXTERNAL_STORAGE

# android.api >= 29 is required for storage.py
android.api = 30

android.add_src = storage_src
