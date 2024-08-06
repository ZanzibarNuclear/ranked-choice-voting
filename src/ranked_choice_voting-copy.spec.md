# Build a Distribution

This is used for packaging. Normally .spec files are ignored because they are generated.
Making this an md file so that I can add a few notes.

Build with `pyinstaller --clean ranked_choice_voting.spec`.

Test the executable found in the `dist` directory.

## More ideas from Claude

Create a distribution package:

- For Windows: You can zip the contents of the dist/RankedChoiceVoting directory.
- For macOS: You can create a DMG file.
- For Linux: You can create a tarball or use a system-specific package format.

(Optional) Create an installer:

- For Windows: You can use tools like NSIS or Inno Setup to create an installer.
- For macOS: You can use tools like Packages or Platypus.
- For Linux: You can create a .deb package for Debian-based systems or an .rpm for Red Hat-based systems.


Additional considerations:

Dependencies: PyInstaller should automatically include most dependencies, but if you're using any unusual libraries, you might need to specify them explicitly.
Cross-platform building: It's best to build on the target operating system. If you want to distribute for Windows, macOS, and Linux, you should ideally build on each platform.
Code signing: For distribution on macOS and Windows, you might want to consider code signing your application.
Updates: Consider how you'll handle updates to your application. You might want to implement an auto-update feature or provide clear instructions for users to update manually.
Documentation: Provide a README file with installation instructions and basic usage guidelines.

## Sample code

Below is the original spec file for reference.

```
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['ranked_choice_voting_gui.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
         a.scripts,
         a.binaries,
         a.zipfiles,
         a.datas,
         [],
         name='RankedChoiceVoting',
         debug=False,
         bootloader_ignore_signals=False,
         strip=False,
         upx=True,
         upx_exclude=[],
         runtime_tmpdir=None,
         console=False )
```
