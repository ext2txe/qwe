#!/usr/bin/env python3
"""
Verify which version of settings_dialog.py you have.
"""

import sys
import os

def check_file(filepath):
    """Check if file is old or new version."""
    if not os.path.exists(filepath):
        print(f"❌ FILE NOT FOUND: {filepath}")
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    size = len(content)
    lines = content.count('\n')
    
    print(f"\n{'='*60}")
    print(f"Checking: {filepath}")
    print(f"{'='*60}")
    print(f"Size: {size:,} characters ({size//1024}KB)")
    print(f"Lines: {lines}")
    print()
    
    # Check for new features
    checks = [
        ('QTabWidget', 'Tabbed interface'),
        ('_create_general_tab', 'General tab method'),
        ('_create_privacy_tab', 'Privacy tab method'),
        ('_create_proxy_tab', 'Proxy tab method'),
        ('_create_logging_tab', 'Logging tab method'),
        ('_create_scripting_tab', 'Scripting tab method'),
        ('_create_advanced_tab', 'Advanced tab method'),
        ('_browse_save_folder', 'Browse folder function'),
        ('headers_global', 'Global headers'),
        ('headers_per_host', 'Per-host headers'),
        ('QFileDialog', 'File dialog'),
        ('auto_launch', 'Auto-launch setting'),
    ]
    
    found_count = 0
    print("Feature Check:")
    print("-" * 60)
    for feature, desc in checks:
        found = feature in content
        status = "✅" if found else "❌"
        print(f"{status} {desc:<30} ({feature})")
        if found:
            found_count += 1
    
    print()
    print(f"Found: {found_count}/{len(checks)} features")
    print()
    
    if found_count == 0:
        print("🔴 THIS IS THE OLD DIALOG (NO NEW FEATURES)")
        print("   - No tabs")
        print("   - Single page layout")
        print("   - ~250 lines, ~12KB")
        return False
    elif found_count < len(checks) // 2:
        print("🟡 PARTIAL OR CORRUPTED FILE")
        return False
    else:
        print("🟢 THIS IS THE NEW ENHANCED DIALOG")
        print("   - 6 tabs")
        print("   - Browse buttons")
        print("   - JSON validation")
        print("   - ~930 lines, ~35KB")
        return True

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        # Default location
        filepath = 'src/qwsengine/ui/settings_dialog.py'
    
    is_new = check_file(filepath)
    
    if not is_new:
        print()
        print("=" * 60)
        print("WHAT TO DO:")
        print("=" * 60)
        print("1. Download: NEW_TABBED_SETTINGS_DIALOG.py")
        print("2. Copy to: src/qwsengine/ui/settings_dialog.py")
        print("3. Clear cache: rm -rf **/__pycache__")
        print("4. Restart app completely")
        print()
    
    sys.exit(0 if is_new else 1)
