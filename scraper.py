# ═══════════════════════════════════════════════════════════
# 👑 ANDROID PROJECT FILES - ملفات مشروع أندرويد
# ═══════════════════════════════════════════════════════════

def build_android_project():
    """توليد جميع ملفات مشروع Android تلقائياً"""
    
    # المجلدات الأساسية
    dirs = [
        "android-project",
        "android-project/gradle/wrapper",
        "android-project/app/src/main/java/com/gkom/app",
        "android-project/app/src/main/assets",
        "android-project/app/src/main/res/values"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    # ═══ 1. build.gradle (الرئيسي) ═══
    build_gradle_root = """buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.2.0'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}"""
    
    # ═══ 2. settings.gradle ═══
    settings_gradle = """rootProject.name = "MNAENCA"
include ':app'"""
    
    # ═══ 3. gradle.properties ═══
    gradle_properties = """android.useAndroidX=true
org.gradle.jvmargs=-Xmx2048m"""
    
    # ═══ 4. gradle-wrapper.properties ═══
    gradle_wrapper_properties = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.5-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists"""
    
    # ═══ 5. app/build.gradle ═══
    app_build_gradle = """plugins {
    id 'com.android.application'
}

android {
    namespace 'com.gkom.app'
    compileSdk 34

    defaultConfig {
        applicationId "com.gkom.mnaenca"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "2026.1"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt')
        }
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
}"""
    
    # ═══ 6. AndroidManifest.xml ═══
    android_manifest = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:label="MNAENCA Gold"
        android:icon="@mipmap/ic_launcher"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.NoActionBar">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:configChanges="orientation|screenSize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>"""
    
    # ═══ 7. MainActivity.java ═══
    main_activity = """package com.gkom.app;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        WebView webView = new WebView(this);
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedError(WebView view, int errorCode, 
                                        String description, String failingUrl) {
                // تحميل من assets كاحتياط
                view.loadUrl("file:///android_asset/index.html");
            }
        });
        
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        
        // محاولة تحميل من URL مباشر أولاً
        // webView.loadUrl("https://YOUR_GITHUB_PAGES_URL");
        
        // تحميل من ملفات assets المحلية
        webView.loadUrl("file:///android_asset/index.html");
        
        setContentView(webView);
    }
}"""
    
    # ═══ 8. strings.xml ═══
    strings_xml = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">MNAENCA Gold</string>
</resources>"""
    
    # ═══ كتابة جميع الملفات ═══
    android_files = [
        ("android-project/build.gradle", build_gradle_root),
        ("android-project/settings.gradle", settings_gradle),
        ("android-project/gradle.properties", gradle_properties),
        ("android-project/gradle/wrapper/gradle-wrapper.properties", gradle_wrapper_properties),
        ("android-project/app/build.gradle", app_build_gradle),
        ("android-project/app/src/main/AndroidManifest.xml", android_manifest),
        ("android-project/app/src/main/java/com/gkom/app/MainActivity.java", main_activity),
        ("android-project/app/src/main/res/values/strings.xml", strings_xml),
    ]
    
    for filepath, content in android_files:
        write(filepath, content)
    
    # ═══ 9. نسخ ملفات الويب إلى assets ═══
    web_files = [
        "index.html", "auth.html", "profile.html", "upload.html", 
        "chat.html", "explore.html", "notifications.html", "settings.html",
        "firebase-config.js", "manifest.json", "service-worker.js"
    ]
    
    import shutil
    for wf in web_files:
        if os.path.exists(wf):
            shutil.copy(wf, f"android-project/app/src/main/assets/{wf}")
            print(f"  ✅ نسخ {wf} → assets/{wf}")
    
    print("\n  ✅ جميع ملفات مشروع Android جاهزة!")


def create_gradlew_script():
    """إنشاء سكربت gradlew للتشغيل"""
    gradlew_content = """#!/bin/bash
##############################################################################
## Gradle start up script for UN*X
##############################################################################

# Attempt to set APP_HOME
PRG="$0"
while [ -h "$PRG" ] ; do
    ls=`ls -ld "$PRG"`
    link=`expr "$ls" : '.*-> \\(.*\\)$'`
    if expr "$link" : '/.*' > /dev/null; then
        PRG="$link"
    else
        PRG=`dirname "$PRG"`"/$link"
    fi
done
SAVED="`pwd`"
cd "`dirname \\"$PRG\\"`/" >/dev/null
APP_HOME="`pwd -P`"
cd "$SAVED" >/dev/null

APP_NAME="Gradle"
APP_BASE_NAME=`basename "$0"`
DEFAULT_JVM_OPTS='"-Xmx64m" "-Xms64m"'

# Use the maximum available, or set MAX_FD != -1 to use that value.
MAX_FD="maximum"

warn () {
    echo "$*"
}

die () {
    echo
    echo "$*"
    echo
    exit 1
}

# OS specific support (must be 'true' or 'false').
cygwin=false
msys=false
darwin=false
nonstop=false
case "`uname`" in
  CYGWIN* )
    cygwin=true
    ;;
  Darwin* )
    darwin=true
    ;;
  MINGW* )
    msys=true
    ;;
  NONSTOP* )
    nonstop=true
    ;;
esac

CLASSPATH=$APP_HOME/gradle/wrapper/gradle-wrapper.jar

# Determine the Java command to use to start the JVM.
if [ -n "$JAVA_HOME" ] ; then
    if [ -x "$JAVA_HOME/jre/sh/java" ] ; then
        JAVACMD="$JAVA_HOME/jre/sh/java"
    else
        JAVACMD="$JAVA_HOME/bin/java"
    fi
    if [ ! -x "$JAVACMD" ] ; then
        die "ERROR: JAVA_HOME is set to an invalid directory: $JAVA_HOME"
    fi
else
    JAVACMD="java"
    which java >/dev/null 2>&1 || die "ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH."
fi

# Increase the maximum file descriptors if we can.
if [ "$cygwin" = "false" -a "$darwin" = "false" -a "$nonstop" = "false" ] ; then
    MAX_FD_LIMIT=`ulimit -H -n`
    if [ $? -eq 0 ] ; then
        if [ "$MAX_FD" = "maximum" -o "$MAX_FD" = "max" ] ; then
            MAX_FD="$MAX_FD_LIMIT"
        fi
        ulimit -n $MAX_FD
        if [ $? -ne 0 ] ; then
            warn "Could not set maximum file descriptor limit: $MAX_FD"
        fi
    else
        warn "Could not query maximum file descriptor limit: $MAX_FD_LIMIT"
    fi
fi

# For Darwin, add options to specify how the application appears in the dock
if $darwin; then
    GRADLE_OPTS="$GRADLE_OPTS \\"-Xdock:name=$APP_NAME\\" \\"-Xdock:icon=$APP_HOME/media/gradle.icns\\""
fi

# For Cygwin or MSYS, switch paths to Windows format before running java
if [ "$cygwin" = "true" -o "$msys" = "true" ] ; then
    APP_HOME=`cygpath --path --mixed "$APP_HOME"`
    CLASSPATH=`cygpath --path --mixed "$CLASSPATH"`
    JAVACMD=`cygpath --unix "$JAVACMD"`
fi

# Collect all arguments for the java command
eval set -- $DEFAULT_JVM_OPTS $JAVA_OPTS $GRADLE_OPTS "\\"-Dorg.gradle.appname=$APP_BASE_NAME\\"" -classpath "\\"$CLASSPATH\\"" org.gradle.wrapper.GradleWrapperMain "$@"

exec "$JAVACMD" "$@"
"""
    
    write("android-project/gradlew", gradlew_content)
    os.chmod("android-project/gradlew", 0o755)  # جعله قابل للتنفيذ
    print("  ✅ gradlew مع صلاحيات التنفيذ")
