[app]
    title = Contractor BOSS
    package.name = contractor_boss
    package.domain = org.contractorboss
    source.dir = .
    source.include_exts = py,png,jpg,kv,atlas,txt,spec
    version = 1.0.0
    requirements = python3,kivy
    
    orientation = portrait
    
    android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
    
    android.api = 33
    android.minapi = 21
    android.sdk = 24
    android.ndk = 25b
    
    # (other buildozer settings...)
    
