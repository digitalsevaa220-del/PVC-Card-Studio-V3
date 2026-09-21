[Setup]
AppName=PVC Card Studio V3
AppVersion=3.0.0
DefaultDirName={autopf}\PVC Card Studio V3
DefaultGroupName=PVC Card Studio V3
OutputDir=Output
OutputBaseFilename=PVC_Card_Studio_V3_Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
WizardStyle=modern

[Files]
Source: "dist\PVC Card Studio V3\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{autoprograms}\PVC Card Studio V3"; Filename: "{app}\PVC Card Studio V3.exe"
Name: "{autodesktop}\PVC Card Studio V3"; Filename: "{app}\PVC Card Studio V3.exe"
