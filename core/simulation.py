import os
import sys
import re
import random
import ipaddress
import socket
import time
from datetime import datetime
import subprocess
import shutil
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import timedelta
import hashlib
import fnmatch
from itertools import zip_longest
import difflib
import locale
import psutil
import platform
import uuid
import getpass
from contextlib import redirect_stdout
import io
import traceback
from .file_system import File, Directory

# Rest of your code...


# Set up logging
logging.basicConfig(filename='command_simulator.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

from typing import Dict, Any

class VirtualFileSystem:
    def __init__(self):
        self.current_directory = "C:\\"
        self.root = Directory("C:")
        self.file_system: Dict[str, Any] = {
            "C:\\": {
                "Windows": {
                    "System32": {
                        "drivers": {
                            "etc": {
                                "hosts": {"content": "# Host file content", "size": 734, "attributes": "A"},
                                "networks": {"content": "# Network configuration", "size": 402, "attributes": "A"},
                                "protocol": {"content": "# Protocol definition", "size": 19530, "attributes": "A"},
                                "services": {"content": "# Network services", "size": 19530, "attributes": "A"},
                            },
                            "NTFS.sys": {"content": "NTFS driver", "size": 2565672, "attributes": "SH"},
                            "tcpip.sys": {"content": "TCP/IP driver", "size": 1897984, "attributes": "SH"},
                            "http.sys": {"content": "HTTP driver", "size": 1265664, "attributes": "SH"},
                            "nvlddmkm.sys": {"content": "NVIDIA driver", "size": 22747136, "attributes": "SH"},
                            "usbhub3.sys": {"content": "USB 3.0 driver", "size": 535040, "attributes": "SH"},
                            "hdaudbus.sys": {"content": "High Definition Audio Bus Driver", "size": 86016, "attributes": "SH"},
                            "ks.sys": {"content": "Kernel Streaming", "size": 311808, "attributes": "SH"},
                            "ndisuio.sys": {"content": "NDIS User mode I/O Driver", "size": 56832, "attributes": "SH"},
                            "netbios.sys": {"content": "NetBIOS driver", "size": 43520, "attributes": "SH"},
                            "rdbss.sys": {"content": "Redirected Drive Buffering SubSystem", "size": 313856, "attributes": "SH"},
                        },
                        "en-US": {
                            "winhlp32.exe.mui": {"content": "Help file", "size": 9216, "attributes": "A"},
                            "notepad.exe.mui": {"content": "Notepad language file", "size": 68608, "attributes": "A"},
                            "charmap.exe.mui": {"content": "Character Map language file", "size": 7168, "attributes": "A"},
                            "mspaint.exe.mui": {"content": "Paint language file", "size": 360448, "attributes": "A"},
                            "calc.exe.mui": {"content": "Calculator language file", "size": 99328, "attributes": "A"},
                        },
                        "config": {
                            "system": {"content": "System configuration", "size": 30720, "attributes": "SH"},
                            "software": {"content": "Software configuration", "size": 61440, "attributes": "SH"},
                            "default": {"content": "Default configuration", "size": 28672, "attributes": "SH"},
                            "sam": {"content": "Security Accounts Manager", "size": 65536, "attributes": "SH"},
                            "security": {"content": "Security configuration", "size": 57344, "attributes": "SH"},
                            "BCD-Template": {"content": "Boot Configuration Data Template", "size": 262144, "attributes": "SH"},
                        },
                        "winevt": {
                            "Logs": {
                                "Application.evtx": {"content": "Application log", "size": 1048576, "attributes": "A"},
                                "System.evtx": {"content": "System log", "size": 1048576, "attributes": "A"},
                                "Security.evtx": {"content": "Security log", "size": 2097152, "attributes": "A"},
                                "Setup.evtx": {"content": "Setup log", "size": 1048576, "attributes": "A"},
                                "ForwardedEvents.evtx": {"content": "Forwarded events", "size": 1048576, "attributes": "A"},
                                "Microsoft-Windows-Diagnostics-Performance%4Operational.evtx": {"content": "Performance diagnostics log", "size": 1048576, "attributes": "A"},
                                "Microsoft-Windows-TaskScheduler%4Operational.evtx": {"content": "Task Scheduler log", "size": 1048576, "attributes": "A"},
                            }
                        },
                        "wbem": {
                            "wmic.exe": {"content": "WMI Command-line", "size": 381440, "attributes": "A"},
                            "WMIC.exe": {"content": "WMI Command-line (another instance)", "size": 381440, "attributes": "A"},
                            "mofcomp.exe": {"content": "MOF Compiler", "size": 74752, "attributes": "A"},
                            "scrcons.exe": {"content": "WMI Standard Event Consumer", "size": 14848, "attributes": "A"},
                        },
                        "WindowsPowerShell": {
                            "v1.0": {
                                "powershell.exe": {"content": "PowerShell executable", "size": 449024, "attributes": "A"},
                                "powershell_ise.exe": {"content": "PowerShell ISE", "size": 743424, "attributes": "A"},
                                "Modules": {
                                    "Microsoft.PowerShell.Management": {
                                        "Microsoft.PowerShell.Management.psd1": {"content": "PowerShell Management Module Manifest", "size": 9826, "attributes": "A"},
                                    },
                                    "Microsoft.PowerShell.Utility": {
                                        "Microsoft.PowerShell.Utility.psd1": {"content": "PowerShell Utility Module Manifest", "size": 21842, "attributes": "A"},
                                    },
                                    "Microsoft.PowerShell.Security": {
                                        "Microsoft.PowerShell.Security.psd1": {"content": "PowerShell Security Module Manifest", "size": 5951, "attributes": "A"},
                                    },
                                }
                            }
                        },
                        "cmd.exe": {"content": "Command Prompt executable", "size": 278528, "attributes": "A"},
                        "notepad.exe": {"content": "Notepad executable", "size": 204800, "attributes": "A"},
                        "regedit.exe": {"content": "Registry Editor executable", "size": 358400, "attributes": "A"},
                        "explorer.exe": {"content": "Windows Explorer", "size": 4618240, "attributes": "A"},
                        "taskmgr.exe": {"content": "Task Manager", "size": 1310720, "attributes": "A"},
                        "mmc.exe": {"content": "Microsoft Management Console", "size": 3186688, "attributes": "A"},
                        "calc.exe": {"content": "Calculator", "size": 28672, "attributes": "A"},
                        "mspaint.exe": {"content": "Paint", "size": 6598656, "attributes": "A"},
                        "services.exe": {"content": "Services and Controller app", "size": 358400, "attributes": "SH"},
                        "lsass.exe": {"content": "Local Security Authority Process", "size": 44032, "attributes": "SH"},
                        "svchost.exe": {"content": "Service Host", "size": 44544, "attributes": "SH"},
                        "winlogon.exe": {"content": "Windows Logon Application", "size": 659456, "attributes": "SH"},
                        "csrss.exe": {"content": "Client Server Runtime Process", "size": 9216, "attributes": "SH"},
                        "conhost.exe": {"content": "Console Window Host", "size": 887296, "attributes": "SH"},
                        "dwm.exe": {"content": "Desktop Window Manager", "size": 266240, "attributes": "SH"},
                        "Utilman.exe": {"content": "Utility Manager", "size": 30720, "attributes": "A"},
                        "mstsc.exe": {"content": "Remote Desktop Connection", "size": 3932160, "attributes": "A"},
                        "winver.exe": {"content": "About Windows", "size": 180224, "attributes": "A"},
                        "control.exe": {"content": "Control Panel", "size": 392704, "attributes": "A"},
                        "wininit.exe": {"content": "Windows Start-Up Application", "size": 315392, "attributes": "SH"},
                        "spoolsv.exe": {"content": "Spooler SubSystem App", "size": 37888, "attributes": "SH"},
                        "SearchIndexer.exe": {"content": "Windows Search Indexer", "size": 427008, "attributes": "A"},
                        "WinSAT.exe": {"content": "Windows System Assessment Tool", "size": 20480, "attributes": "A"},
                        "catroot": {
                            "{F750E6C3-38EE-11D1-85E5-00C04FC295EE}": {
                                "Microsoft-Windows-Client-Desktop-Required-Package.cat": {"content": "Windows Catalog file", "size": 437336, "attributes": "A"},
                            },
                        },
                        "DriverStore": {
                            "FileRepository": {
                                "hdaudio.inf_amd64_neutral_99a74557bf9a7767": {
                                    "hdaudio.sys": {"content": "High Definition Audio Driver", "size": 416768, "attributes": "A"},
                                },
                                "prnhp001.inf_amd64_neutral_7e30faa548628ae8": {
                                    "hpcpp225.dll": {"content": "HP Printer Driver", "size": 2801664, "attributes": "A"},
                                },
                            },
                        },
                        "Speech": {
                            "Engines": {
                                "TTS": {
                                    "en-US": {
                                        "MSSpeech_TTS_en-US_ZiraPro.msi": {"content": "Zira TTS Voice", "size": 7864320, "attributes": "A"},
                                        "M16Base.DLL": {"content": "Microsoft Speech API", "size": 1126400, "attributes": "A"},
                                    },
                                },
                            },
                            "SpeechUX": {
                                "sapi.cpl": {"content": "Speech Control Panel", "size": 608256, "attributes": "A"},
                            },
                        },
                        "migwiz": {
                            "migwiz.exe": {"content": "Windows Easy Transfer", "size": 3010048, "attributes": "A"},
                            "mighost.exe": {"content": "Windows Easy Transfer Host", "size": 72192, "attributes": "A"},
                        },
                        "oobe": {
                            "setup.exe": {"content": "Windows Setup", "size": 145408, "attributes": "A"},
                            "msoobe.exe": {"content": "Windows Out-of-Box Experience", "size": 839168, "attributes": "A"},
                        },
                        "sysprep": {
                            "sysprep.exe": {"content": "System Preparation Tool", "size": 5504, "attributes": "A"},
                        },
                    }
                },
                "Program Files": {
                    "Common Files": {
                        "Microsoft Shared": {
                            "VC": {
                                "v14.0": {
                                    "vcruntime140.dll": {"content": "Visual C++ Runtime", "size": 86016, "attributes": "A"},
                                },
                            },
                            "Windows Live": {
                                "WLIDSVC.EXE": {"content": "Windows Live ID Service", "size": 2330112, "attributes": "A"},
                            },
                        },
                        "Services": {
                            "Microsoft": {
                                "Windows Defender": {
                                    "MpAsDesc.dll": {"content": "Windows Defender Description DLL", "size": 436224, "attributes": "A"},
                                },
                            },
                        },
                        "System": {
                            "Ole DB": {
                                "oledb32.dll": {"content": "OLE DB Core Services", "size": 643072, "attributes": "A"},
                            },
                            "ADO": {
                                "msado15.dll": {"content": "Microsoft ActiveX Data Objects 2.8 Library", "size": 1248768, "attributes": "A"},
                            },
                        },
                    },
                    "Internet Explorer": {
                        "iexplore.exe": {"content": "Internet Explorer executable", "size": 815104, "attributes": "A"},
                        "iediagcmd.exe": {"content": "Internet Explorer Diagnostics", "size": 275968, "attributes": "A"},
                        "ieinstal.exe": {"content": "Internet Explorer Installer", "size": 646656, "attributes": "A"},
                        "ielowutil.exe": {"content": "Internet Explorer Low Rights Utility", "size": 763392, "attributes": "A"},
                        "PLUGINS": {
                            "ieframe.dll": {"content": "Internet Explorer Frame DLL", "size": 15556608, "attributes": "A"},
                        },
                    },
                    "Microsoft": {
                        "Office": {
                            "root": {
                                "Office16": {
                                    "EXCEL.EXE": {"content": "Excel executable", "size": 31532032, "attributes": "A"},
                                    "WINWORD.EXE": {"content": "Word executable", "size": 31532032, "attributes": "A"},
                                    "POWERPNT.EXE": {"content": "PowerPoint executable", "size": 31532032, "attributes": "A"},
                                    "OUTLOOK.EXE": {"content": "Outlook executable", "size": 36700160, "attributes": "A"},
                                    "ONENOTE.EXE": {"content": "OneNote executable", "size": 26214400, "attributes": "A"},
                                    "MSACCESS.EXE": {"content": "Access executable", "size": 22020096, "attributes": "A"},
                                    "MSPUB.EXE": {"content": "Publisher executable", "size": 20971520, "attributes": "A"},
                                    "GROOVE.EXE": {"content": "OneDrive for Business executable", "size": 18874368, "attributes": "A"},
                                    "WINPROJ.EXE": {"content": "Project executable", "size": 24117248, "attributes": "A"},
                                    "VISIO.EXE": {"content": "Visio executable", "size": 23068672, "attributes": "A"},
                                    "LYNC.EXE": {"content": "Skype for Business executable", "size": 21495808, "attributes": "A"},
                                    "MSOIA.EXE": {"content": "Office Installation Assistant", "size": 3145728, "attributes": "A"},
                                },
                                "Templates": {
                                    "1033": {
                                        "NORMAL.DOTM": {"content": "Word Normal Template", "size": 98304, "attributes": "A"},
                                        "BOOK.XLTX": {"content": "Excel Book Template", "size": 81920, "attributes": "A"},
                                        "BLANK.POTX": {"content": "PowerPoint Blank Template", "size": 163840, "attributes": "A"},
                                        
                                        },
                                },
                                "Document Themes": {
                                    "Theme Colors": {
                                        "Office.xml": {"content": "Office Theme Colors", "size": 8192, "attributes": "A"},
                                    },
                                    "Theme Fonts": {
                                        "Office.xml": {"content": "Office Theme Fonts", "size": 4096, "attributes": "A"},
                                    },
                                },
                            },
                            "Data": {
                                "16": {
                                    "PROOFING": {
                                        "PROOF.EN": {"content": "English Proofing Tools", "size": 5242880, "attributes": "A"},
                                        "PROOF.ES": {"content": "Spanish Proofing Tools", "size": 4194304, "attributes": "A"},
                                        "PROOF.FR": {"content": "French Proofing Tools", "size": 4194304, "attributes": "A"},
                                    },
                                },
                            },
                        },
                        "Windows Defender": {
                            "MsMpEng.exe": {"content": "Windows Defender executable", "size": 118784, "attributes": "A"},
                            "MpCmdRun.exe": {"content": "Windows Defender Command Line Utility", "size": 459264, "attributes": "A"},
                            "NisSrv.exe": {"content": "Network Inspection Service", "size": 3190784, "attributes": "A"},
                            "MpOAV.dll": {"content": "Antimalware On-Access Module", "size": 1138688, "attributes": "A"},
                            "MsMpLics.dll": {"content": "Windows Defender Licensing DLL", "size": 321024, "attributes": "A"},
                            "Signatures": {
                                "AntiVirus": {
                                    "EngineVersion.ini": {"content": "Engine Version Information", "size": 1024, "attributes": "A"},
                                },
                                "AntiSpyware": {
                                    "EngineVersion.ini": {"content": "Engine Version Information", "size": 1024, "attributes": "A"},
                                },
                            },
                        },
                        "Edge": {
                            "Application": {
                                "msedge.exe": {"content": "Microsoft Edge executable", "size": 3244032, "attributes": "A"},
                                "msedge.dll": {"content": "Microsoft Edge DLL", "size": 148897792, "attributes": "A"},
                                "pwabuilder.exe": {"content": "PWA Builder", "size": 1048576, "attributes": "A"},
                            },
                            "Extensions": {
                                "1.0.0.0": {
                                    "Microsoft_Adblock": {
                                        "manifest.json": {"content": "Extension Manifest", "size": 2048, "attributes": "A"},
                                    },
                                },
                            },
                            "User Data": {
                                "Default": {
                                    "History": {"content": "Browsing History Database", "size": 5242880, "attributes": "A"},
                                    "Cookies": {"content": "Cookies Database", "size": 1048576, "attributes": "A"},
                                    "Bookmarks": {"content": "Bookmarks File", "size": 262144, "attributes": "A"},
                                },
                            },
                        },
                        "Visual Studio": {
                            "2022": {
                                "Community": {
                                    "Common7": {
                                        "IDE": {
                                            "devenv.exe": {"content": "Visual Studio executable", "size": 95420416, "attributes": "A"},
                                            "Extensions": {
                                                "Microsoft": {
                                                    "VsGraphics": {
                                                        "VsGraphics.dll": {"content": "Visual Studio Graphics Tools", "size": 8388608, "attributes": "A"},
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    "MSBuild": {
                                        "Current": {
                                            "Bin": {
                                                "MSBuild.exe": {"content": "MSBuild executable", "size": 3670016, "attributes": "A"},
                                            },
                                        },
                                    },
                                    "VC": {
                                        "Tools": {
                                            "MSVC": {
                                                "14.32.31326": {
                                                    "bin": {
                                                        "Hostx64": {
                                                            "x64": {
                                                                "cl.exe": {"content": "C++ Compiler", "size": 42377216, "attributes": "A"},
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                    "WindowsApps": {
                        "Microsoft.WindowsStore_12001.1001.1.0_x64__8wekyb3d8bbwe": {
                            "WinStore.App.exe": {"content": "Windows Store app", "size": 22646784, "attributes": "A"},
                        },
                        "Microsoft.XboxGamingOverlay_5.721.10202.0_x64__8wekyb3d8bbwe": {
                            "GameBar.exe": {"content": "Xbox Game Bar", "size": 15728640, "attributes": "A"},
                        },
                        "Microsoft.YourPhone_1.21092.145.0_x64__8wekyb3d8bbwe": {
                            "YourPhone.exe": {"content": "Your Phone app", "size": 18874368, "attributes": "A"},
                        },
                    },
                    "7-Zip": {
                        "7z.exe": {"content": "7-Zip File Manager", "size": 1265664, "attributes": "A"},
                        "7z.dll": {"content": "7-Zip Plugin", "size": 1704448, "attributes": "A"},
                        "7zFM.exe": {"content": "7-Zip File Manager", "size": 1425408, "attributes": "A"},
                        "7zG.exe": {"content": "7-Zip GUI", "size": 1162240, "attributes": "A"},
                        "7-zip.chm": {"content": "7-Zip Help File", "size": 368640, "attributes": "A"},
                    },
                    "Adobe": {
                        "Acrobat Reader DC": {
                            "Reader": {
                                "AcroRd32.exe": {"content": "Adobe Reader executable", "size": 89694208, "attributes": "A"},
                                "AdobeCollabSync.exe": {"content": "Adobe Collaboration Synchronizer", "size": 12058624, "attributes": "A"},
                            },
                            "Esl": {
                                "AdobeLinguistic.dll": {"content": "Adobe Linguistic Library", "size": 940032, "attributes": "A"},
                            },
                        },
                        "Adobe Creative Cloud": {
                            "ACC": {
                                "Creative Cloud.exe": {"content": "Adobe Creative Cloud", "size": 72351744, "attributes": "A"},
                            },
                        },
                    },
                    "NVIDIA Corporation": {
                        "NVIDIA GeForce Experience": {
                            "NVIDIA GeForce Experience.exe": {"content": "NVIDIA GeForce Experience", "size": 28311552, "attributes": "A"},
                        },
                        "PhysX": {
                            "Common": {
                                "PhysXDevice64.dll": {"content": "PhysX System Software", "size": 410624, "attributes": "A"},
                            },
                        },
                    },
                },
                "Program Files (x86)": {
                    "Common Files": {
                        "Adobe": {
                            "Acrobat": {
                                "ActiveX": {
                                    "AcroPDF.dll": {"content": "Adobe PDF ActiveX", "size": 3461120, "attributes": "A"},
                                },
                            },
                        },
                        "Microsoft": {
                            "Visual Studio": {
                                "Shared": {
                                    "MSEnv": {
                                        "msenv.dll": {"content": "Visual Studio Environment DLL", "size": 1425408, "attributes": "A"},
                                    },
                                },
                            },
                        },
                    },
                    "Internet Explorer": {
                        "iexplore.exe": {"content": "32-bit Internet Explorer executable", "size": 815104, "attributes": "A"},
                    },
                    "Microsoft": {
                        "Edge": {
                            "Application": {
                                "msedge.exe": {"content": "32-bit Microsoft Edge executable", "size": 3145728, "attributes": "A"},
                            },
                        },
                        "Visual Studio": {
                            "2022": {
                                "BuildTools": {
                                    "MSBuild": {
                                        "Current": {
                                            "Bin": {
                                                "MSBuild.exe": {"content": "32-bit MSBuild executable", "size": 3145728, "attributes": "A"},
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                    "Google": {
                        "Chrome": {
                            "Application": {
                                "chrome.exe": {"content": "Google Chrome executable", "size": 2265088, "attributes": "A"},
                                "chrome_proxy.exe": {"content": "Chrome Proxy", "size": 1400832, "attributes": "A"},
                            },
                            "User Data": {
                                "Default": {
                                    "History": {"content": "Browsing History Database", "size": 5242880, "attributes": "A"},
                                    "Cookies": {"content": "Cookies Database", "size": 1048576, "attributes": "A"},
                                    "Bookmarks": {"content": "Bookmarks File", "size": 262144, "attributes": "A"},
                                },
                            },
                        },
                    },
                    "Mozilla Firefox": {
                        "firefox.exe": {"content": "Mozilla Firefox executable", "size": 546304, "attributes": "A"},
                        "browser": {
                            "components": {
                                "crashmonitor.dll": {"content": "Crash Monitor", "size": 472064, "attributes": "A"},
                            },
                        },
                        "defaults": {
                            "pref": {
                                "channel-prefs.js": {"content": "Channel Preferences", "size": 1024, "attributes": "A"},
                            },
                        },
                    },
                    "Steam": {
                        "steam.exe": {"content": "Steam Client Bootstrapper", "size": 3186688, "attributes": "A"},
                        "steamapps": {
                            "common": {
                                "Counter-Strike Global Offensive": {
                                    "csgo.exe": {"content": "CS:GO executable", "size": 23068672, "attributes": "A"},
                                },
                                "Dota 2": {
                                    "game": {
                                        "dota.exe": {"content": "Dota 2 executable", "size": 51380224, "attributes": "A"},
                                    },
                                },
                            },
                        },
                    },
                },
                "Users": {
                    "Public": {
                        "Documents": {
                            "Sample Files": {
                                "sample.docx": {"content": "Sample Word document", "size": 12288, "attributes": "A"},
                                "sample.xlsx": {"content": "Sample Excel spreadsheet", "size": 10240, "attributes": "A"},
                                "sample.pptx": {"content": "Sample PowerPoint presentation", "size": 36864, "attributes": "A"},
                            },
                        },
                        "Downloads": {},
                        "Music": {
                            "Sample Music": {
                                "Kalimba.mp3": {"content": "Sample music file", "size": 8192000, "attributes": "A"},
                                "Maid with the Flaxen Hair.mp3": {"content": "Sample music file", "size": 6291456, "attributes": "A"},
                            },
                        },
                        "Pictures": {
                            "Sample Pictures": {
                                "Chrysanthemum.jpg": {"content": "Sample picture", "size": 879616, "attributes": "A"},
                                "Desert.jpg": {"content": "Sample picture", "size": 845824, "attributes": "A"},
                                "Jellyfish.jpg": {"content": "Sample picture", "size": 775168, "attributes": "A"},
                            },
                        },
                        "Videos": {
                            "Sample Videos": {
                                "Wildlife.wmv": {"content": "Sample video", "size": 26214400, "attributes": "A"},
                            },
                        },
                        "Desktop": {},
                        "Libraries": {
                            "Documents.library-ms": {"content": "Documents library", "size": 1024, "attributes": "A"},
                            "Music.library-ms": {"content": "Music library", "size": 1024, "attributes": "A"},
                            "Pictures.library-ms": {"content": "Pictures library", "size": 1024, "attributes": "A"},
                            "Videos.library-ms": {"content": "Videos library", "size": 1024, "attributes": "A"},
                        },
                    },
                    "Default": {
                        "NTUSER.DAT": {"content": "Default User Registry Hive", "size": 16777216, "attributes": "SH"},
                        "AppData": {
                            "Local": {
                                "Microsoft": {
                                    "Windows": {
                                        "UsrClass.dat": {"content": "User Classes Registry Hive", "size": 10485760, "attributes": "SH"},
                                    },
                                },
                            },
                        },
                    },
                    "Administrator": {
                        "Desktop": {
                            "AdminTool.lnk": {"content": "Shortcut to Admin Tool", "size": 1024, "attributes": "A"},
                        },
                        "Documents": {
                            "AdminReports": {
                                "SystemAudit.docx": {"content": "System Audit Report", "size": 524288, "attributes": "A"},
                                "NetworkDiagram.vsdx": {"content": "Network Diagram", "size": 1048576, "attributes": "A"},
                            },
                            "IISExpress": {
                                "config": {
                                    "applicationhost.config": {"content": "IIS Express Configuration", "size": 131072, "attributes": "A"},
                                },
                            },
                        },
                        "Downloads": {
                            "ServerSetup.exe": {"content": "Server Setup Executable", "size": 104857600, "attributes": "A"},
                            "PatchNotes.pdf": {"content": "Latest Patch Notes", "size": 2097152, "attributes": "A"},
                        },
                        "Music": {},
                        "Pictures": {
                            "ServerRacks": {
                                "Rack01.jpg": {"content": "Server Rack Photo", "size": 3145728, "attributes": "A"},
                                "Rack02.jpg": {"content": "Server Rack Photo", "size": 2097152, "attributes": "A"},
                            },
                        },
                        "Videos": {
                            "ServerMaintenance.mp4": {"content": "Server Maintenance Tutorial", "size": 1073741824, "attributes": "A"},
                        },
                        "AppData": {
                            "Local": {
                                "Microsoft": {
                                    "Windows": {
                                        "Explorer": {
                                            "thumbcache_256.db": {"content": "Thumbnail Cache", "size": 16777216, "attributes": "H"},
                                        },
                                        "INetCache": {
                                            "IE": {
                                                "UKX7A2WI": {
                                                    "index.dat": {"content": "Internet Cache Index", "size": 131072, "attributes": "H"},
                                                },
                                            },
                                        },
                                        "INetCookies": {
                                            "Low": {
                                                "index.dat": {"content": "Internet Cookies Index", "size": 32768, "attributes": "H"},
                                            },
                                        },
                                        "History": {
                                            "History.IE5": {
                                                "index.dat": {"content": "Browsing History Index", "size": 524288, "attributes": "H"},
                                            },
                                        },
                                    },
                                },
                                "Temp": {
                                    "TempFile1.tmp": {"content": "Temporary File", "size": 1048576, "attributes": "A"},
                                    "TempFile2.tmp": {"content": "Temporary File", "size": 2097152, "attributes": "A"},
                                },
                                "Google": {
                                    "Chrome": {
                                        "User Data": {
                                            "Default": {
                                                "Cache": {
                                                    "data_0": {"content": "Chrome Cache Data", "size": 16777216, "attributes": "A"},
                                                    "data_1": {"content": "Chrome Cache Data", "size": 20971520, "attributes": "A"},
                                                },
                                                "Cookies": {"content": "Chrome Cookies", "size": 262144, "attributes": "A"},
                                                "History": {"content": "Chrome History", "size": 5242880, "attributes": "A"},
                                            },
                                        },
                                    },
                                },
                            },
                            "LocalLow": {},
                            "Roaming": {
                                "Microsoft": {
                                    "Windows": {
                                        "Start Menu": {
                                            "Programs": {
                                                "Startup": {},
                                            },
                                        },
                                        "Recent": {
                                            "AutomaticDestinations": {
                                                "f01b4d95cf55d32a.automaticDestinations-ms": {"content": "Jump List", "size": 32768, "attributes": "H"},
                                            },
                                        },
                                    },
                                    "Internet Explorer": {
                                        "Quick Launch": {
                                            "User Pinned": {
                                                "TaskBar": {},
                                            },
                                        },
                                    },
                                },
                                "Mozilla": {
                                    "Firefox": {
                                        "Profiles": {
                                            "default": {
                                                "places.sqlite": {"content": "Firefox History and Bookmarks", "size": 5242880, "attributes": "A"},
                                                "cookies.sqlite": {"content": "Firefox Cookies", "size": 1048576, "attributes": "A"},
                                            },
                                        },
                                    },
                                },
                            },
                        },
                        "Favorites": {
                            "Links": {
                                "Desktop.lnk": {"content": "Desktop Shortcut", "size": 1024, "attributes": "A"},
                                "Downloads.lnk": {"content": "Downloads Shortcut", "size": 1024, "attributes": "A"},
                            },
                        },
                        "Searches": {
                            "ServerIssues.search-ms": {"content": "Saved Search", "size": 2048, "attributes": "A"},
                        },
                        "Links": {
                            "ControlPanel.lnk": {"content": "Control Panel Shortcut", "size": 1024, "attributes": "A"},
                        },
                        "Contacts": {},
                        "Saved Games": {},
                        "Searches": {},
                    },
                    "User": {
                        "Desktop": {
                            "document.txt": {"content": "User's document", "size": 1024, "attributes": "A"},
                            "shortcut.lnk": {"content": "Shortcut file", "size": 1369, "attributes": "A"},
                            "MyProject": {
                                "main.py": {"content": "Python script", "size": 2048, "attributes": "A"},
                                "data.csv": {"content": "CSV data file", "size": 5242880, "attributes": "A"},
                            },
                            "Invoices": {
                                "Invoice_2023_01.pdf": {"content": "January Invoice", "size": 524288, "attributes": "A"},
                                "Invoice_2023_02.pdf": {"content": "February Invoice", "size": 589824, "attributes": "A"},
                            },
                        },
                        "Documents": {
                            "My Music": {
                                "Playlist1.m3u": {"content": "Music Playlist", "size": 1024, "attributes": "A"},
                            },
                            "My Pictures": {
                                "Vacation2023": {
                                    "IMG_001.jpg": {"content": "Vacation Photo", "size": 3145728, "attributes": "A"},
                                    "IMG_002.jpg": {"content": "Vacation Photo", "size": 2097152, "attributes": "A"},
                                },
                            },
                            "My Videos": {
                                "FamilyVideo2023.mp4": {"content": "Family Video", "size": 1073741824, "attributes": "A"},
                            },
                            "Visual Studio 2022": {
                                "Projects": {
                                    "MyWebApp": {
                                        "MyWebApp.sln": {"content": "Solution File", "size": 2048, "attributes": "A"},
                                        "MyWebApp": {
                                            "Program.cs": {"content": "C# Source File", "size": 1024, "attributes": "A"},
                                            "Startup.cs": {"content": "C# Source File", "size": 2048, "attributes": "A"},
                                            "appsettings.json": {"content": "Configuration File", "size": 1024, "attributes": "A"},
                                        },
                                    },
                                },
                            },
                            "Word Documents": {
                                "Report2023.docx": {"content": "Annual Report", "size": 1048576, "attributes": "A"},
                                "Meeting Minutes": {
                                    "2023_01_15_Minutes.docx": {"content": "Meeting Minutes", "size": 65536, "attributes": "A"},
                                    "2023_02_22_Minutes.docx": {"content": "Meeting Minutes", "size": 73728, "attributes": "A"},
                                },
                            },
                            "Excel Files": {
                                "Budget2023.xlsx": {"content": "Annual Budget", "size": 524288, "attributes": "A"},
                                "SalesData": {
                                    "Q1_Sales.xlsx": {"content": "Q1 Sales Data", "size": 262144, "attributes": "A"},
                                    "Q2_Sales.xlsx": {"content": "Q2 Sales Data", "size": 278528, "attributes": "A"},
                                },
                            },
                        },
                        "Downloads": {
                            "setup.exe": {"content": "Downloaded setup file", "size": 50331648, "attributes": "A"},
                            "Sample.pdf": {"content": "Sample PDF Document", "size": 1048576, "attributes": "A"},
                            "Drivers": {
                                "GraphicsDriver.exe": {"content": "Graphics Driver Installer", "size": 209715200, "attributes": "A"},
                            },
                            "Software Updates": {
                                "WindowsUpdate.exe": {"content": "Windows Update Package", "size": 104857600, "attributes": "A"},
                            },
                        },
                        "Music": {
                            "iTunes": {
                                "iTunes Media": {
                                    "Music": {
                                        "Artist1": {
                                            "Album1": {
                                                "Track01.mp3": {"content": "Music Track", "size": 8388608, "attributes": "A"},
                                                "Track02.mp3": {"content": "Music Track", "size": 7340032, "attributes": "A"},
                                            },
                                        },
                                        "Artist2": {
                                            "Album1": {
                                                "Track01.mp3": {"content": "Music Track", "size": 6291456, "attributes": "A"},
                                            },
                                        },
                                    },
                                    "Podcasts": {
                                        "TechTalk": {
                                            "Episode1.mp3": {"content": "Podcast Episode", "size": 52428800, "attributes": "A"},
                                        },
                                    },
                                },
                            },
                            "Spotify": {
                                "Offline": {
                                    "Track001.ofs": {"content": "Offline Spotify Track", "size": 10485760, "attributes": "A"},
                                },
                            },
                        },
                        "Pictures": {
                            "Camera Roll": {
                                "IMG_20230101.jpg": {"content": "Camera Photo", "size": 4194304, "attributes": "A"},
                                "IMG_20230102.jpg": {"content": "Camera Photo", "size": 3670016, "attributes": "A"},
                            },
                            "Saved Pictures": {
                                "Wallpaper.jpg": {"content": "Wallpaper Image", "size": 2097152, "attributes": "A"},
                            },
                            "Screenshots": {
                                "Screenshot_20230101.png": {"content": "Screenshot", "size": 1048576, "attributes": "A"},
                            },
                        },
                        "Videos": {
                            "Captures": {
                                "GameCapture_20230101.mp4": {"content": "Game Footage", "size": 1073741824, "attributes": "A"},
                            },
                            "Movies": {
                                "ActionMovie2023.mkv": {"content": "Movie File", "size": 8589934592, "attributes": "A"},
                            },
                        },
                        "AppData": {
                            "Local": {
                                "Microsoft": {
                                    "Windows": {
                                        "Explorer": {
                                            "thumbcache_256.db": {"content": "Thumbnail Cache", "size": 16777216, "attributes": "H"},
                                        },
                                        "INetCache": {
                                            "IE": {
                                                "UKX7A2WI": {
                                                    "index.dat": {"content": "Internet Cache Index", "size": 131072, "attributes": "H"},
                                                },
                                            },
                                        },
                                        "INetCookies": {
                                            "Low": {
                                                "index.dat": {"content": "Internet Cookies Index", "size": 32768, "attributes": "H"},
                                            },
                                        },
                                        "History": {
                                            "History.IE5": {
                                                "index.dat": {"content": "Browsing History Index", "size": 524288, "attributes": "H"},
                                            },
                                        },
                                    },
                                    "Edge": {
                                        "User Data": {
                                            "Default": {
                                                "Cache": {
                                                    "data_0": {"content": "Edge Cache Data", "size": 16777216, "attributes": "A"},
                                                    "data_1": {"content": "Edge Cache Data", "size": 20971520, "attributes": "A"},
                                                },
                                                "Cookies": {"content": "Edge Cookies", "size": 262144, "attributes": "A"},
                                                "History": {"content": "Edge History", "size": 5242880, "attributes": "A"},
                                            },
                                        },
                                    },
                                },
                                "Temp": {
                                    "TempFile1.tmp": {"content": "Temporary File", "size": 1048576, "attributes": "A"},
                                    "TempFile2.tmp": {"content": "Temporary File", "size": 2097152, "attributes": "A"},
                                },
                                "Google": {
                                    "Chrome": {
                                        "User Data": {
                                            "Default": {
                                                "Cache": {
                                                    "data_0": {"content": "Chrome Cache Data", "size": 16777216, "attributes": "A"},
                                                    "data_1": {"content": "Chrome Cache Data", "size": 20971520, "attributes": "A"},
                                                },
                                                "Cookies": {"content": "Chrome Cookies", "size": 262144, "attributes": "A"},
                                                "History": {"content": "Chrome History", "size": 5242880, "attributes": "A"},
                                            },
                                        },
                                    },
                                },
                                "Packages": {
                                    "Microsoft.WindowsStore_8wekyb3d8bbwe": {
                                        "LocalState": {
                                            "AppData.dat": {"content": "Windows Store App Data", "size": 1048576, "attributes": "A"},
                                        },
                                    },
                                },
                            },
                            "LocalLow": {
                                "Sun": {
                                    "Java": {
                                        "Deployment": {
                                            "cache": {
                                                "6.0": {
                                                    "content": {"content": "Java Cache", "size": 10485760, "attributes": "A"},
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                            "Roaming": {
                                "Microsoft": {
                                    "Windows": {
                                        "Start Menu": {
                                            "Programs": {
                                                "Startup": {},
                                            },
                                        },
                                        "Recent": {
                                            "AutomaticDestinations": {
                                                "f01b4d95cf55d32a.automaticDestinations-ms": {"content": "Jump List", "size": 32768, "attributes": "H"},
                                            },
                                        },
                                    },
                                    "Office": {
                                        "16.0": {
                                            "Word": {
                                                "User MRU": {
                                                    "ADAL_B7E7AA2830CA1E5C60A4A1C0A55A2CD6": {
                                                        "Word.RecentFiles": {"content": "Recent Word Files", "size": 4096, "attributes": "H"},
                                                    },
                                                },
                                            },
                                            "Excel": {
                                                "User MRU": {
                                                    "ADAL_B7E7AA2830CA1E5C60A4A1C0A55A2CD6": {
                                                        "Excel.RecentFiles": {"content": "Recent Excel Files", "size": 4096, "attributes": "H"},
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                "Mozilla": {
                                    "Firefox": {
                                        "Profiles": {
                                            "default": {
                                                "places.sqlite": {"content": "Firefox History and Bookmarks", "size": 5242880, "attributes": "A"},
                                                "cookies.sqlite": {"content": "Firefox Cookies", "size": 1048576, "attributes": "A"},
                                                "extensions": {
                                                    "{e4a8a97b-f2ed-450b-b12d-ee082ba24781}": {
                                                        "manifest.json": {"content": "Extension Manifest", "size": 1024, "attributes": "A"},
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                "Adobe": {
                                    "Acrobat": {
                                        "DC": {
                                            "UserCache.bin": {"content": "Acrobat User Cache", "size": 1048576, "attributes": "A"},
                                        },
                                    },
                                },
                                "Macromedia": {
                                    "Flash Player": {
                                        "#SharedObjects": {
                                            "somefile.sol": {"content": "Flash Shared Object", "size": 4096, "attributes": "A"},
                                        },
                                    },
                                },
                                "Discord": {
                                    "Cache": {
                                        "f_000001": {"content": "Discord Cache File", "size": 1048576, "attributes": "A"},
                                    },
                                    "Local Storage": {
                                        "leveldb": {
                                            "000003.log": {"content": "Discord Local Storage", "size": 262144, "attributes": "A"},
                                        },
                                    },
                                },
                                "Spotify": {
                                    "Users": {
                                        "user-account": {
                                            "frecency.pb": {"content": "Spotify User Data", "size": 8192, "attributes": "A"},
                                        },
                                    },
                                },
                                "npm": {
                                    "npmrc": {"content": "NPM Configuration", "size": 1024, "attributes": "A"},
                                },
                                "NuGet": {
                                    "NuGet.Config": {"content": "NuGet Configuration", "size": 2048, "attributes": "A"},
                                },
                            },
                        },
                        "Favorites": {
                            "Links": {},
                            "Contacts": {},
                        },
                        "Searches": {},
                        "Links": {
                            "Desktop.lnk": {"content": "Desktop Shortcut", "size": 1024, "attributes": "A"},
                            "Downloads.lnk": {"content": "Downloads Shortcut", "size": 1024, "attributes": "A"},
                            "Documents.lnk": {"content": "Documents Shortcut", "size": 1024, "attributes": "A"},
                        },
                        "Saved Games": {
                            "Minecraft": {
                                "saves": {
                                    "World1": {
                                        "level.dat": {"content": "Minecraft World Data", "size": 8192, "attributes": "A"},
                                    },
                                },
                            },
                        },
                        "OneDrive": {
                            "Documents": {
                                "WorkProject": {
                                    "Proposal.docx": {"content": "Work Proposal", "size": 524288, "attributes": "A"},
                                    "Budget.xlsx": {"content": "Project Budget", "size": 262144, "attributes": "A"},
                                },
                            },
                            "Pictures": {
                                "Family": {
                                    "Vacation2023": {
                                        "Beach.jpg": {"content": "Vacation Photo", "size": 3145728, "attributes": "A"},
                                        "Mountain.jpg": {"content": "Vacation Photo", "size": 2621440, "attributes": "A"},
                                    },
                                },
                            },
                        },
                        "3D Objects": {
                            "Cube.stl": {"content": "3D Cube Model", "size": 2097152, "attributes": "A"},
                            "Sphere.obj": {"content": "3D Sphere Model", "size": 1048576, "attributes": "A"},
                        },
                    },
                },
                "ProgramData": {
                    "Microsoft": {
                        "Windows": {
                            "Start Menu": {
                                "Programs": {
                                    "Accessories": {
                                        "Notepad.lnk": {"content": "Notepad Shortcut", "size": 1024, "attributes": "A"},
                                    },
                                    "Startup": {},
                                },
                            },
                            "DeviceMetadataStore": {
                                "dmrc.idx": {"content": "Device Metadata Index", "size": 65536, "attributes": "H"},
                            },
                        },
                        "Windows Defender": {
                            "Scans": {
                                "History": {
                                    "Service": {
                                        "DetectionHistory": {
                                            "2.4.7.3": {
                                                "7195870905707014808.td": {"content": "Threat Detection History", "size": 4096, "attributes": "H"},
                                            },
                                        },
                                    },
                                },
                            },
                            "Definition Updates": {
                                "Daily": {
                                    "mpasbase.vdm": {"content": "Base Definitions", "size": 20971520, "attributes": "A"},
                                    "mpavdlta.vdm": {"content": "Delta Definitions", "size": 5242880, "attributes": "A"},
                                },
                            },
                        },
                        "Windows NT": {
                            "CurrentVersion": {
                                "Schedule": {
                                    "TaskCache": {
                                        "Tree": {
                                            "Microsoft": {
                                                "Windows": {
                                                    "WindowsUpdate": {
                                                        "Scheduled Start": {"content": "Scheduled Task", "size": 1024, "attributes": "H"},
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                    "Package Cache": {
                        "{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}": {
                            "cab1.cab": {"content": "Installation Package", "size": 104857600, "attributes": "A"},
                        },
                    },
                    "Adobe": {
                        "Acrobat": {
                            "11.0": {
                                "CMaps": {
                                    "83pv-RKSJ-H": {"content": "Adobe CMap", "size": 16384, "attributes": "A"},
                                },
                            },
                        },
                    },
                    "NVIDIA Corporation": {
                        "Installer2": {
                            "InstallerCache": {
                                "NVI2.CAB": {"content": "NVIDIA Installer Cache", "size": 524288000, "attributes": "A"},
                            },
                        },
                    },
                    "Malwarebytes": {
                        "MBAMService": {
                            "MBAMService.exe": {"content": "Malwarebytes Service", "size": 16777216, "attributes": "A"},
                        },
                    },
                    "Dell": {
                        "UpdateService": {
                            "Downloads": {
                                "BIOS_85GR7_WN32_1.13.0.exe": {"content": "Dell BIOS Update", "size": 8388608, "attributes": "A"},
                            },
                        },
                    },
                },
                "Intel": {
                    "Logs": {
                        "IntelGFX.log": {"content": "Intel Graphics Driver Log", "size": 1048576, "attributes": "A"},
                    },
                    "Drivers": {
                        "Display": {
                            "igfx_win_10.0.19041.3793.exe": {"content": "Intel Graphics Driver", "size": 314572800, "attributes": "A"},
                        },
                    },
                },
                "PerfLogs": {
                    "System": {
                        "Diagnostics": {
                            "WDI": {
                                "LogFiles": {
                                    "{12345678-1234-5678-1234-567890ABCDEF}": {
                                        "trace.etl": {"content": "Windows Diagnostic Infrastructure Trace", "size": 1048576, "attributes": "A"},
                                    },
                                },
                            },
                        },
                    },
                },
                "$Recycle.Bin": {
                    "S-1-5-21-1234567890-1234567890-1234567890-1001": {
                        "$I123456.txt": {"content": "Recycle Bin Metadata", "size": 1024, "attributes": "H"},
                        "$R123456.txt": {"content": "Deleted File", "size": 10485760, "attributes": "H"},
                    },
                },
                "System Volume Information": {
                    "tracking.log": {"content": "System restore tracking log", "size": 1048576, "attributes": "SH"},
                    "{3808876b-c176-4e48-b7ae-04046e6cc752}": {
                        "CiMetadata": {
                            "0x9.cim": {"content": "Code Integrity Metadata", "size": 2097152, "attributes": "SH"},
                        },
                    },
                },
                "Recovery": {
                    "WindowsRE": {
                        "Winre.wim": {"content": "Windows Recovery Environment", "size": 4294967296, "attributes": "SH"},
                    },
                },
                "pagefile.sys": {"content": "Page file", "size": 16106127360, "attributes": "SH"},
                "hiberfil.sys": {"content": "Hibernation file", "size": 8589934592, "attributes": "SH"},
                "swapfile.sys": {"content": "Swap file", "size": 268435456, "attributes": "SH"},
            },
            "D:\\": {
                "Backups": {
                    "Windows": {
                        "System Image": {
                            "WindowsImageBackup": {
                                "Backup 2023-07-01 123456": {
                                    "Backup Files": {
                                        "9b9cfbc3-369e-11e9-a17b-806e6f6e6963.vhd": {"content": "Backup VHD", "size": 107374182400, "attributes": "A"},
                                    },
                                    "Catalog": {
                                        "GlobalCatalog": {"content": "Backup Catalog", "size": 1048576, "attributes": "A"},
                                    },
                                },
                            },
                        },
                    },
                    "Documents": {
                        "2023": {
                            "January": {
                                "Documents_2023_01_01.zip": {"content": "Document Backup", "size": 104857600, "attributes": "A"},
                            },
                            "February": {
                                "Documents_2023_02_01.zip": {"content": "Document Backup", "size": 115343360, "attributes": "A"},
                            },
                        },
                        "2022": {
                            "Annual_Backup_2022.zip": {"content": "Annual Document Backup", "size": 1073741824, "attributes": "A"},
                        },
                    },
                },
                "Games": {
                    "Steam": {
                        "steamapps": {
                            "common": {
                                "Counter-Strike Global Offensive": {
                                    "csgo.exe": {"content": "CS:GO executable", "size": 23068672, "attributes": "A"},
                                    "csgo": {
                                        "maps": {
                                            "de_dust2.bsp": {"content": "Dust II Map", "size": 41943040, "attributes": "A"},
                                            "de_mirage.bsp": {"content": "Mirage Map", "size": 37748736, "attributes": "A"},
                                        },
                                        "models": {
                                            "player": {
                                                "ct_fbi.mdl": {"content": "CT Model", "size": 4194304, "attributes": "A"},
                                                "t_leet.mdl": {"content": "T Model", "size": 4194304, "attributes": "A"},
                                            },
                                        },
                                    },
                                },
                                "Dota 2": {
                                    "dota2.exe": {"content": "Dota 2 executable", "size": 51380224, "attributes": "A"},
                                    "game": {
                                        "dota": {
                                            "maps": {
                                                "dota.vmap": {"content": "Dota 2 Map", "size": 209715200, "attributes": "A"},
                                            },
                                            "models": {
                                                "heroes": {
                                                    "pudge": {
                                                        "pudge.vmdl": {"content": "Pudge Model", "size": 8388608, "attributes": "A"},
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                "Half-Life Alyx": {
                                    "hlvr.exe": {"content": "Half-Life: Alyx executable", "size": 67108864, "attributes": "A"},
                                    "content": {
                                        "hlvr": {
                                            "maps": {
                                                "a1_intro_world.vmap": {"content": "Intro Map", "size": 104857600, "attributes": "A"},
                                            },
                                        },
                                    },
                                },
                            },
                            "workshop": {
                                "content": {
                                    "730": {  # CS:GO Workshop Content
                                        "1885082752": {
                                            "workshop_map.bsp": {"content": "Workshop Map", "size": 52428800, "attributes": "A"},
                                        },
                                    },
                                },
                            },
                        },
                        "Steam.exe": {"content": "Steam client", "size": 3186688, "attributes": "A"},
                        "steamapps": {
                            "libraryfolders.vdf": {"content": "Steam Library Folders", "size": 1024, "attributes": "A"},
                        },
                    },
                    "Epic Games": {
                        "Launcher": {
                            "Portal": {
                                "Binaries": {
                                    "Win32": {
                                        "EpicGamesLauncher.exe": {"content": "Epic Games Launcher", "size": 53477376, "attributes": "A"},
                                    },
                                },
                            },
                        },
                        "FortniteGame": {
                            "FortniteGame": {
                                "Binaries": {
                                    "Win64": {
                                        "FortniteClient-Win64-Shipping.exe": {"content": "Fortnite executable", "size": 83886080, "attributes": "A"},
                                    },
                                },
                                "Content": {
                                    "Paks": {
                                        "pakchunk0-WindowsClient.pak": {"content": "Fortnite Game Data", "size": 10737418240, "attributes": "A"},
                                        "pakchunk1-WindowsClient.pak": {"content": "Fortnite Game Data", "size": 8589934592, "attributes": "A"},
                                    },
                                },
                            },
                        },
                        "RocketLeague": {
                            "Binaries": {
                                "Win64": {
                                    "RocketLeague.exe": {"content": "Rocket League executable", "size": 67108864, "attributes": "A"},
                                },
                            },
                        },
                    },
                    "Origin": {
                        "Origin.exe": {"content": "Origin client", "size": 3670016, "attributes": "A"},
                        "Games": {
                            "Apex Legends": {
                                "r5apex.exe": {"content": "Apex Legends executable", "size": 88080384, "attributes": "A"},
                            },
                            "Battlefield V": {
                                "bfv.exe": {"content": "Battlefield V executable", "size": 104857600, "attributes": "A"},
                            },
                        },
                    },
                    "Ubisoft": {
                        "Ubisoft Game Launcher": {
                            "UbisoftConnect.exe": {"content": "Ubisoft Connect executable", "size": 5242880, "attributes": "A"},
                        },
                        "games": {
                            "Assassin's Creed Valhalla": {
                                "ACValhalla.exe": {"content": "AC Valhalla executable", "size": 125829120, "attributes": "A"},
                            },
                        },
                    },
                    "GOG Galaxy": {
                        "GalaxyClient.exe": {"content": "GOG Galaxy client", "size": 4194304, "attributes": "A"},
                        "Games": {
                            "The Witcher 3": {
                                "bin": {
                                    "x64": {
                                        "witcher3.exe": {"content": "The Witcher 3 executable", "size": 83886080, "attributes": "A"},
                                    },
                                },
                            },
                        },
                    },
                },
                "Projects": {
                    "Python": {
                        "project1": {
                            "main.py": {"content": "Python script", "size": 2048, "attributes": "A"},
                            "requirements.txt": {"content": "Project dependencies", "size": 256, "attributes": "A"},
                            "venv": {
                                "Scripts": {
                                    "activate.bat": {"content": "Activation script", "size": 1024, "attributes": "A"},
                                    "python.exe": {"content": "Python executable", "size": 3145728, "attributes": "A"},
                                },
                                "Lib": {
                                    "site-packages": {
                                        "numpy": {
                                            "__init__.py": {"content": "NumPy initialization", "size": 4096, "attributes": "A"},
                                        },
                                        "pandas": {
                                            "__init__.py": {"content": "Pandas initialization", "size": 4096, "attributes": "A"},
                                        },
                                    },
                                },
                            },
                        },
                        "project2": {
                            "src": {
                                "main.py": {"content": "Main Python script", "size": 4096, "attributes": "A"},
                                "utils.py": {"content": "Utility functions", "size": 2048, "attributes": "A"},
                            },
                            "tests": {
                                "test_main.py": {"content": "Main tests", "size": 1024, "attributes": "A"},
                                "test_utils.py": {"content": "Utility tests", "size": 1024, "attributes": "A"},
                            },
                            "data": {
                                "input.csv": {"content": "Input data", "size": 1048576, "attributes": "A"},
                                "output.csv": {"content": "Output data", "size": 2097152, "attributes": "A"},
                            },
                        },
                    },
                    "Web": {
                        "portfolio": {
                            "index.html": {"content": "HTML file", "size": 4096, "attributes": "A"},
                            "styles": {
                                "main.css": {"content": "CSS file", "size": 2048, "attributes": "A"},
                                "responsive.css": {"content": "Responsive CSS", "size": 1024, "attributes": "A"},
                            },
                            "scripts": {
                                "app.js": {"content": "JavaScript file", "size": 1024, "attributes": "A"},
                                "vendor": {
                                    "jquery.min.js": {"content": "jQuery library", "size": 89088, "attributes": "A"},
                                    "bootstrap.min.js": {"content": "Bootstrap JS", "size": 60928, "attributes": "A"},
                                },
                            },
                            "images": {
                                "logo.png": {"content": "Logo image", "size": 20480, "attributes": "A"},
                                "background.jpg": {"content": "Background image", "size": 2097152, "attributes": "A"},
                            },
                            "fonts": {
                                "OpenSans-Regular.ttf": {"content": "Open Sans font", "size": 224492, "attributes": "A"},
                                "OpenSans-Bold.ttf": {"content": "Open Sans Bold font", "size": 224736, "attributes": "A"},
                            },
                        },
                        "react-app": {
                            "package.json": {"content": "Package configuration", "size": 1024, "attributes": "A"},
                            "src": {
                                "index.js": {"content": "Entry point", "size": 512, "attributes": "A"},
                                "App.js": {"content": "Main app component", "size": 2048, "attributes": "A"},
                                "components": {
                                    "Header.js": {"content": "Header component", "size": 1024, "attributes": "A"},
                                    "Footer.js": {"content": "Footer component", "size": 1024, "attributes": "A"},
                                },
                            },
                            "public": {
                                "index.html": {"content": "HTML template", "size": 1024, "attributes": "A"},
                                "favicon.ico": {"content": "Favicon", "size": 4096, "attributes": "A"},
                            },
                            "node_modules": {
                                "react": {
                                    "package.json": {"content": "React package info", "size": 1024, "attributes": "A"},
                                },
                                "react-dom": {
                                    "package.json": {"content": "React DOM package info", "size": 1024, "attributes": "A"},
                                },
                            },
                        },
                    },
                    "C++": {
                        "OpenGL_Game": {
                            "src": {
                                "main.cpp": {"content": "Main C++ file", "size": 4096, "attributes": "A"},
                                "game.cpp": {"content": "Game logic", "size": 8192, "attributes": "A"},
                                "renderer.cpp": {"content": "Rendering code", "size": 16384, "attributes": "A"},
                            },
                            "include": {
                                "game.h": {"content": "Game header", "size": 1024, "attributes": "A"},
                                "renderer.h": {"content": "Renderer header", "size": 2048, "attributes": "A"},
                            },
                            "libs": {
                                "glfw": {
                                    "glfw3.lib": {"content": "GLFW library", "size": 1048576, "attributes": "A"},
                                },
                                "glm": {
                                    "glm.hpp": {"content": "GLM header", "size": 204800, "attributes": "A"},
                                },
                            },
                            "assets": {
                                "textures": {
                                    "sprite.png": {"content": "Sprite texture", "size": 65536, "attributes": "A"},
                                    "background.jpg": {"content": "Background texture", "size": 2097152, "attributes": "A"},
                                },
                                "shaders": {
                                    "vertex.glsl": {"content": "Vertex shader", "size": 1024, "attributes": "A"},
                                    "fragment.glsl": {"content": "Fragment shader", "size": 1024, "attributes": "A"},
                                },
                            },
                            "build": {
                                "CMakeCache.txt": {"content": "CMake cache", "size": 16384, "attributes": "A"},
                                "OpenGL_Game.exe": {"content": "Game executable", "size": 5242880, "attributes": "A"},
                            },
                        },
                    },
                    "Unity": {
                        "3DPlatformer": {
                            "Assets": {
                                "Scenes": {
                                    "MainMenu.unity": {"content": "Main Menu Scene", "size": 524288, "attributes": "A"},
                                    "Level1.unity": {"content": "Level 1 Scene", "size": 1048576, "attributes": "A"},
                                },
                                "Scripts": {
                                    "PlayerController.cs": {"content": "Player Controller Script", "size": 4096, "attributes": "A"},
                                    "EnemyAI.cs": {"content": "Enemy AI Script", "size": 8192, "attributes": "A"},
                                },
                                "Models": {
                                    "Character.fbx": {"content": "Character 3D Model", "size": 2097152, "attributes": "A"},
                                    "Environment.fbx": {"content": "Environment 3D Model", "size": 4194304, "attributes": "A"},
                                },
                                "Materials": {
                                    "PlayerMaterial.mat": {"content": "Player Material", "size": 1024, "attributes": "A"},
                                    "EnvironmentMaterial.mat": {"content": "Environment Material", "size": 1024, "attributes": "A"},
                                },
                            },
                            "ProjectSettings": {
                                "ProjectSettings.asset": {"content": "Unity Project Settings", "size": 16384, "attributes": "A"},
                            },
                            "Library": {
                                "metadata": {
                                    "00": {
                                        "00": {
                                            "00000000000000001000000000000000.info": {"content": "Unity metadata", "size": 1024, "attributes": "A"},
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
                "Virtual Machines": {
                    "Ubuntu Server": {
                        "Ubuntu Server.vdi": {"content": "Ubuntu Server virtual disk", "size": 10737418240, "attributes": "A"},
                        "Ubuntu Server.vbox": {"content": "VirtualBox settings", "size": 8192, "attributes": "A"},
                    },
                    "Windows 10 Test": {
                        "Windows 10 Test.vdi": {"content": "Windows 10 Test virtual disk", "size": 32212254720, "attributes": "A"},
                        "Windows 10 Test.vbox": {"content": "VirtualBox settings", "size": 8192, "attributes": "A"},
                    },
                    "Kali Linux": {
                        "Kali Linux.vmdk": {"content": "Kali Linux virtual disk", "size": 21474836480, "attributes": "A"},
                        "Kali Linux.vmx": {"content": "VMware settings", "size": 4096, "attributes": "A"},
                    },
                },
                "Work": {
                    "Reports": {
                        "2023": {
                            "Q1_Financial_Report.xlsx": {"content": "Q1 Financial Report", "size": 1048576, "attributes": "A"},
                            "Q2_Financial_Report.xlsx": {"content": "Q2 Financial Report", "size": 1179648, "attributes": "A"},
                        },
                        "2022": {
                            "Annual_Report.docx": {"content": "2022 Annual Report", "size": 5242880, "attributes": "A"},
                        },
                    },
                    "Presentations": {
                        "Company_Overview.pptx": {"content": "Company Overview Presentation", "size": 15728640, "attributes": "A"},
                        "Product_Launch.pptx": {"content": "Product Launch Presentation", "size": 20971520, "attributes": "A"},
                    },
                    "Contracts": {
                        "NDA_Template.docx": {"content": "NDA Template", "size": 524288, "attributes": "A"},
                        "Employee_Contract_Template.docx": {"content": "Employee Contract Template", "size": 786432, "attributes": "A"},
                    },
                    "Client_Projects": {
                        "Client_A": {
                            "Project_Proposal.docx": {"content": "Project Proposal", "size": 1048576, "attributes": "A"},
                            "Contract.pdf": {"content": "Signed Contract", "size": 2097152, "attributes": "A"},
                            "Deliverables": {
                                "Phase_1_Report.pdf": {"content": "Phase 1 Report", "size": 3145728, "attributes": "A"},
                                "Phase_2_Report.pdf": {"content": "Phase 2 Report", "size": 4194304, "attributes": "A"},
                            },
                        },
                        "Client_B": {
                            "Meeting_Notes": {
                                "2023-07-15_Kickoff.docx": {"content": "Kickoff Meeting Notes", "size": 262144, "attributes": "A"},
                                "2023-08-01_Progress.docx": {"content": "Progress Meeting Notes", "size": 294912, "attributes": "A"},
                            },
                            "Design_Files": {
                                "Logo_Concepts.ai": {"content": "Logo Concepts", "size": 15728640, "attributes": "A"},
                                "Website_Mockups.psd": {"content": "Website Mockups", "size": 104857600, "attributes": "A"},
                            },
                        },
                    },
                },
            },
            "E:\\": {
                "Movies": {
                    "Action": {
                        "Die Hard.mp4": {"content": "Action movie", "size": 4294967296, "attributes": "A"},
                        "Mad Max Fury Road.mp4": {"content": "Action movie", "size": 5368709120, "attributes": "A"},
                        "John Wick.mp4": {"content": "Action movie", "size": 4831838208, "attributes": "A"},
                        "The Dark Knight.mp4": {"content": "Action movie", "size": 6442450944, "attributes": "A"},
                        "Inception.mp4": {"content": "Action movie", "size": 5905580032, "attributes": "A"},
                    },
                    "Comedy": {
                        "Superbad.mp4": {"content": "Comedy movie", "size": 3758096384, "attributes": "A"},
                        "Step Brothers.mp4": {"content": "Comedy movie", "size": 4026531840, "attributes": "A"},
                        "The Hangover.mp4": {"content": "Comedy movie", "size": 3221225472, "attributes": "A"},
                        "Bridesmaids.mp4": {"content": "Comedy movie", "size": 4294967296, "attributes": "A"},
                        "Anchorman.mp4": {"content": "Comedy movie", "size": 3489660928, "attributes": "A"},
                    },
                    "Drama": {
                        "The Godfather.mp4": {"content": "Drama movie", "size": 5905580032, "attributes": "A"},
                        "Forrest Gump.mp4": {"content": "Drama movie", "size": 4563402752, "attributes": "A"},
                        "The Shawshank Redemption.mp4": {"content": "Drama movie", "size": 5368709120, "attributes": "A"},
                        "Schindler's List.mp4": {"content": "Drama movie", "size": 6174015488, "attributes": "A"},
                        "Pulp Fiction.mp4": {"content": "Drama movie", "size": 4831838208, "attributes": "A"},
                    },
                    "Sci-Fi": {
                        "Interstellar.mp4": {"content": "Sci-Fi movie", "size": 6442450944, "attributes": "A"},
                        "The Matrix.mp4": {"content": "Sci-Fi movie", "size": 4831838208, "attributes": "A"},
                        "Blade Runner 2049.mp4": {"content": "Sci-Fi movie", "size": 6710886400, "attributes": "A"},
                        "Ex Machina.mp4": {"content": "Sci-Fi movie", "size": 4294967296, "attributes": "A"},
                        "Arrival.mp4": {"content": "Sci-Fi movie", "size": 5368709120, "attributes": "A"},
                    },
                    "Horror": {
                        "The Shining.mp4": {"content": "Horror movie", "size": 4563402752, "attributes": "A"},
                        "Get Out.mp4": {"content": "Horror movie", "size": 4294967296, "attributes": "A"},
                        "A Quiet Place.mp4": {"content": "Horror movie", "size": 3758096384, "attributes": "A"},
                        "Hereditary.mp4": {"content": "Horror movie", "size": 4026531840, "attributes": "A"},
                        "The Conjuring.mp4": {"content": "Horror movie", "size": 3758096384, "attributes": "A"},
                    },
                },
                "TV Shows": {
                    "Game of Thrones": {
                        "Season 1": {
                            "Episode 1.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                            "Episode 2.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                            "Episode 3.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                        },
                        "Season 2": {
                            "Episode 1.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                            "Episode 2.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                            "Episode 3.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                        },
                        "Season 3": {
                            "Episode 1.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                            "Episode 2.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                            "Episode 3.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                        },
                    },
                    "Breaking Bad": {
                        "Season 1": {
                            "Episode 1.mp4": {"content": "TV Episode", "size": 1610612736, "attributes": "A"},
                            "Episode 2.mp4": {"content": "TV Episode", "size": 1610612736, "attributes": "A"},
                            "Episode 3.mp4": {"content": "TV Episode", "size": 1610612736, "attributes": "A"},
                        },
                        "Season 2": {
                            "Episode 1.mp4": {"content": "TV Episode", "size": 1610612736, "attributes": "A"},
                            "Episode 2.mp4": {"content": "TV Episode", "size": 1610612736, "attributes": "A"},
                            "Episode 3.mp4": {"content": "TV Episode", "size": 1610612736, "attributes": "A"},
                        },
                        "Season 3": {
                            "Episode 1.mp4": {"content": "TV Episode", "size": 1610612736, "attributes": "A"},
                            "Episode 2.mp4": {"content": "TV Episode", "size": 1610612736, "attributes": "A"},
                            "Episode 3.mp4": {"content": "TV Episode", "size": 1610612736, "attributes": "A"},
                        },
                    },
                    "The Office": {
                        "Season 1": {
                            "Episode 1.mp4": {"content": "TV Episode", "size": 1073741824, "attributes": "A"},
                            "Episode 2.mp4": {"content": "TV Episode", "size": 1073741824, "attributes": "A"},
                            "Episode 3.mp4": {"content": "TV Episode", "size": 1073741824, "attributes": "A"},
                        },
                        "Season 2": {
                            "Episode 1.mp4": {"content": "TV Episode", "size": 1073741824, "attributes": "A"},
                            "Episode 2.mp4": {"content": "TV Episode", "size": 1073741824, "attributes": "A"},
                            "Episode 3.mp4": {"content": "TV Episode", "size": 1073741824, "attributes": "A"},
                        },
                        "Season 3": {
                            "Episode 1.mp4": {"content": "TV Episode", "size": 1073741824, "attributes": "A"},
                            "Episode 2.mp4": {"content": "TV Episode", "size": 1073741824, "attributes": "A"},
                            "Episode 3.mp4": {"content": "TV Episode", "size": 1073741824, "attributes": "A"},
                        },
                    },
                    "Stranger Things": {
                        "Season 1": {
                            "Episode 1.mp4": {"content": "TV Episode", "size": 2684354560, "attributes": "A"},
                            "Episode 2.mp4": {"content": "TV Episode", "size": 2684354560, "attributes": "A"},
                            "Episode 3.mp4": {"content": "TV Episode", "size": 2684354560, "attributes": "A"},
                        },
                        "Season 2": {
                            "Episode 1.mp4": {"content": "TV Episode", "size": 2684354560, "attributes": "A"},
                            "Episode 2.mp4": {"content": "TV Episode", "size": 2684354560, "attributes": "A"},
                            "Episode 3.mp4": {"content": "TV Episode", "size": 2684354560, "attributes": "A"},
                        },
                    },
                },
                "Music": {
                    "Rock": {
                        "Led Zeppelin - IV.mp3": {"content": "Album", "size": 104857600, "attributes": "A"},
                        "Pink Floyd - The Wall.mp3": {"content": "Album", "size": 157286400, "attributes": "A"},
                        "Queen - A Night at the Opera.mp3": {"content": "Album", "size": 94371840, "attributes": "A"},
                        "The Beatles - Abbey Road.mp3": {"content": "Album", "size": 89128960, "attributes": "A"},
                        "Nirvana - Nevermind.mp3": {"content": "Album", "size": 99614720, "attributes": "A"},
                    },
                    "Pop": {
                        "Michael Jackson - Thriller.mp3": {"content": "Album", "size": 83886080, "attributes": "A"},
                        "Madonna - Like a Virgin.mp3": {"content": "Album", "size": 78643200, "attributes": "A"},
                        "Prince - Purple Rain.mp3": {"content": "Album", "size": 89128960, "attributes": "A"},
                        "Adele - 21.mp3": {"content": "Album", "size": 94371840, "attributes": "A"},
                        "Taylor Swift - 1989.mp3": {"content": "Album", "size": 99614720, "attributes": "A"},
                    },
                    "Classical": {
                        "Beethoven - Symphony No. 9.mp3": {"content": "Classical music", "size": 209715200, "attributes": "A"},
                        "Mozart - Requiem.mp3": {"content": "Classical music", "size": 183500800, "attributes": "A"},
                        "Bach - The Well-Tempered Clavier.mp3": {"content": "Classical music", "size": 262144000, "attributes": "A"},
                        "Tchaikovsky - The Nutcracker.mp3": {"content": "Classical music", "size": 236223488, "attributes": "A"},
                        "Chopin - Nocturnes.mp3": {"content": "Classical music", "size": 157286400, "attributes": "A"},
                    },
                    "Jazz": {
                        "Miles Davis - Kind of Blue.mp3": {"content": "Jazz album", "size": 73400320, "attributes": "A"},
                        "John Coltrane - A Love Supreme.mp3": {"content": "Jazz album", "size": 68157440, "attributes": "A"},
                        "Louis Armstrong - What a Wonderful World.mp3": {"content": "Jazz album", "size": 62914560, "attributes": "A"},
                        "Ella Fitzgerald - Ella Fitzgerald Sings the Cole Porter Songbook.mp3": {"content": "Jazz album", "size": 78643200, "attributes": "A"},
                        "Duke Ellington - Ellington at Newport.mp3": {"content": "Jazz album", "size": 83886080, "attributes": "A"},
                    },
                    "Electronic": {
                        "Daft Punk - Random Access Memories.mp3": {"content": "Electronic album", "size": 104857600, "attributes": "A"},
                        "The Prodigy - Fat of the Land.mp3": {"content": "Electronic album", "size": 94371840, "attributes": "A"},
                        "Aphex Twin - Selected Ambient Works 85-92.mp3": {"content": "Electronic album", "size": 89128960, "attributes": "A"},
                        "Kraftwerk - Trans-Europe Express.mp3": {"content": "Electronic album", "size": 83886080, "attributes": "A"},
                        "Moby - Play.mp3": {"content": "Electronic album", "size": 99614720, "attributes": "A"},
                    },
                },
                "Pictures": {
                    "Vacation": {
                        "Beach.jpg": {"content": "Vacation photo", "size": 5242880, "attributes": "A"},
                        "Mountains.jpg": {"content": "Vacation photo", "size": 7340032, "attributes": "A"},
                        "City.jpg": {"content": "Vacation photo", "size": 6291456, "attributes": "A"},
                        "Resort.jpg": {"content": "Vacation photo", "size": 8388608, "attributes": "A"},
                        "Sunset.jpg": {"content": "Vacation photo", "size": 4194304, "attributes": "A"},
                    },
                    "Family": {
                        "Christmas.jpg": {"content": "Family photo", "size": 8388608, "attributes": "A"},
                        "Birthday.jpg": {"content": "Family photo", "size": 6291456, "attributes": "A"},
                        "Reunion.jpg": {"content": "Family photo", "size": 7340032, "attributes": "A"},
                        "Graduation.jpg": {"content": "Family photo", "size": 9437184, "attributes": "A"},
                        "Thanksgiving.jpg": {"content": "Family photo", "size": 5242880, "attributes": "A"},
                    },
                    "Events": {
                        "Wedding.jpg": {"content": "Event photo", "size": 10485760, "attributes": "A"},
                        "Concert.jpg": {"content": "Event photo", "size": 8388608, "attributes": "A"},
                        "SportingEvent.jpg": {"content": "Event photo", "size": 7340032, "attributes": "A"},
                        "Conference.jpg": {"content": "Event photo", "size": 6291456, "attributes": "A"},
                        "Festival.jpg": {"content": "Event photo", "size": 9437184, "attributes": "A"},
                    },
                    "Nature": {
                        "Forest.jpg": {"content": "Nature photo", "size": 8388608, "attributes": "A"},
                        "Ocean.jpg": {"content": "Nature photo", "size": 6291456, "attributes": "A"},
                        "Desert.jpg": {"content": "Nature photo", "size": 7340032, "attributes": "A"},
                        "Waterfall.jpg": {"content": "Nature photo", "size": 9437184, "attributes": "A"},
                        "Aurora.jpg": {"content": "Nature photo", "size": 10485760, "attributes": "A"},
                    },
                    "Pets": {
                        "Dog.jpg": {"content": "Pet photo", "size": 4194304, "attributes": "A"},
                        "Cat.jpg": {"content": "Pet photo", "size": 3145728, "attributes": "A"},
                        "Hamster.jpg": {"content": "Pet photo", "size": 2097152, "attributes": "A"},
                        "Fish.jpg": {"content": "Pet photo", "size": 3670016, "attributes": "A"},
                        "Parrot.jpg": {"content": "Pet photo", "size": 4718592, "attributes": "A"},
                    },
                },
                "Documents": {
                    "Work": {
                        "Report.docx": {"content": "Work report", "size": 524288, "attributes": "A"},
                        "Presentation.pptx": {"content": "Work presentation", "size": 2097152, "attributes": "A"},
                        "Budget.xlsx": {"content": "Budget spreadsheet", "size": 1048576, "attributes": "A"},
                        "Meeting_Notes.docx": {"content": "Meeting notes", "size": 262144, "attributes": "A"},
                        "Project_Plan.mpp": {"content": "Project plan", "size": 3145728, "attributes": "A"},
                    },
                    "Personal": {
                        "Resume.docx": {"content": "Personal resume", "size": 307200, "attributes": "A"},
                        "CoverLetter.docx": {"content": "Personal cover letter", "size": 262144, "attributes": "A"},
                        "TaxReturns2022.pdf": {"content": "Tax return document", "size": 1572864, "attributes": "A"},
                        "MedicalRecords.pdf": {"content": "Medical records", "size": 2097152, "attributes": "A"},
                        "Insurance_Policies.pdf": {"content": "Insurance policies", "size": 3145728, "attributes": "A"},
                    },
                    "Projects": {
                        "BookDraft.docx": {"content": "Book draft", "size": 1048576, "attributes": "A"},
                        "GardenPlan.xlsx": {"content": "Garden planning", "size": 524288, "attributes": "A"},
                        "HomeRenovation.pdf": {"content": "Home renovation plans", "size": 2097152, "attributes": "A"},
                        "TravelItinerary.docx": {"content": "Travel itinerary", "size": 786432, "attributes": "A"},
                        "RecipeCollection.docx": {"content": "Recipe collection", "size": 1310720, "attributes": "A"},
                    },
                    "School": {
                        "Thesis.docx": {"content": "Thesis document", "size": 3145728, "attributes": "A"},
                        "ResearchNotes.txt": {"content": "Research notes", "size": 262144, "attributes": "A"},
                        "Literature_Review.docx": {"content": "Literature review", "size": 1048576, "attributes": "A"},
                        "Lab_Report.docx": {"content": "Lab report", "size": 786432, "attributes": "A"},
                        "Dissertation.pdf": {"content": "Dissertation", "size": 5242880, "attributes": "A"},
                    },
                    "Financial": {
                        "BankStatements": {
                            "Jan2023.pdf": {"content": "January bank statement", "size": 524288, "attributes": "A"},
                            "Feb2023.pdf": {"content": "February bank statement", "size": 524288, "attributes": "A"},
                            "Mar2023.pdf": {"content": "March bank statement", "size": 524288, "attributes": "A"},
                        },
                        "Investments": {
                            "StockPortfolio.xlsx": {"content": "Stock portfolio tracker", "size": 1048576, "attributes": "A"},
                            "CryptoWallet.pdf": {"content": "Cryptocurrency wallet info", "size": 262144, "attributes": "A"},
                        },
                        "Taxes": {
                            "2022_W2.pdf": {"content": "2022 W2 Form", "size": 131072, "attributes": "A"},
                            "2022_1099.pdf": {"content": "2022 1099 Form", "size": 131072, "attributes": "A"},
                            "2022_TaxReturn.pdf": {"content": "2022 Tax Return", "size": 2097152, "attributes": "A"},
                        },
                    },
                },
                "Software": {
                    "Installers": {
                        "OfficeSetup.exe": {"content": "Microsoft Office Installer", "size": 1073741824, "attributes": "A"},
                        "AdobeCreativeCloud.exe": {"content": "Adobe Creative Cloud Installer", "size": 2147483648, "attributes": "A"},
                        "VisualStudioSetup.exe": {"content": "Visual Studio Installer", "size": 3221225472, "attributes": "A"},
                        "AndroidStudio.exe": {"content": "Android Studio Installer", "size": 1610612736, "attributes": "A"},
                        "Python-3.9.5.exe": {"content": "Python 3.9.5 Installer", "size": 28311552, "attributes": "A"},
                    },
                    "Portable": {
                        "7zip": {
                            "7zFM.exe": {"content": "7-Zip File Manager", "size": 1394688, "attributes": "A"},
                            "7z.dll": {"content": "7-Zip Library", "size": 1684480, "attributes": "A"},
                        },
                        "Notepad++": {
                            "notepad++.exe": {"content": "Notepad++ Executable", "size": 4194304, "attributes": "A"},
                        },
                        "VLC": {
                            "vlc.exe": {"content": "VLC Media Player", "size": 35651584, "attributes": "A"},
                        },
                    },
                    "Drivers": {
                        "NVIDIA-GeForce-Driver-460.79-win10-win8-win7-64bit.exe": {"content": "NVIDIA Graphics Driver", "size": 536870912, "attributes": "A"},
                        "Intel-WiFi-Driver-21.40.5.exe": {"content": "Intel WiFi Driver", "size": 209715200, "attributes": "A"},
                        "RealTek-Audio-Driver-6.0.8899.1.exe": {"content": "Realtek Audio Driver", "size": 52428800, "attributes": "A"},
                    },
                },
                "Backups": {
                    "System": {
                        "Windows10_System_Backup_2023-07-01.vhd": {"content": "System Backup", "size": 53687091200, "attributes": "A"},
                        "Windows10_System_Backup_2023-06-01.vhd": {"content": "System Backup", "size": 51539607552, "attributes": "A"},
                    },
                    "Documents": {
                        "Documents_Backup_2023-07-15.zip": {"content": "Documents Backup", "size": 5368709120, "attributes": "A"},
                        "Documents_Backup_2023-06-15.zip": {"content": "Documents Backup", "size": 5242880000, "attributes": "A"},
                    },
                    "Photos": {
                        "Photos_Backup_2023-Q2.zip": {"content": "Photos Backup", "size": 10737418240, "attributes": "A"},
                        "Photos_Backup_2023-Q1.zip": {"content": "Photos Backup", "size": 9663676416, "attributes": "A"},
                    },
                },
            },
            "F:\\": {
                "Software": {
                    "Installers": {
                        "python-3.9.7.exe": {"content": "Python installer", "size": 27262976, "attributes": "A"},
                        "node-v14.17.0-x64.msi": {"content": "Node.js installer", "size": 31457280, "attributes": "A"},
                        "jdk-16.0.2_windows-x64_bin.exe": {"content": "Java Development Kit installer", "size": 163577856, "attributes": "A"},
                        "VSCodeUserSetup-x64-1.61.2.exe": {"content": "Visual Studio Code installer", "size": 79691776, "attributes": "A"},
                        "GitHubDesktopSetup-x64.exe": {"content": "GitHub Desktop installer", "size": 52428800, "attributes": "A"},
                    },
                    "Development": {
                        "VSCode": {
                            "Code.exe": {"content": "Visual Studio Code executable", "size": 88080384, "attributes": "A"},
                            "data": {
                                "extensions": {
                                    "ms-python.python-2021.9.1246542782": {
                                        "extension.vsixmanifest": {"content": "Extension manifest", "size": 2048, "attributes": "A"},
                                    },
                                },
                            },
                        },
                        "PyCharm": {
                            "bin": {
                                "pycharm64.exe": {"content": "PyCharm executable", "size": 2097152, "attributes": "A"},
                            },
                            "plugins": {
                                "python": {
                                    "lib": {
                                        "python-skeletons": {
                                            "pytest": {
                                                "__init__.py": {"content": "pytest skeleton", "size": 4096, "attributes": "A"},
                                            },
                                        },
                                    },
                                },
                            },
                        },
                        "Eclipse": {
                            "eclipse.exe": {"content": "Eclipse IDE executable", "size": 295698432, "attributes": "A"},
                            "plugins": {
                                "org.eclipse.jdt_3.18.800.v20210809-1701.jar": {"content": "Java Development Tools", "size": 16777216, "attributes": "A"},
                            },
                        },
                        "AndroidStudio": {
                            "bin": {
                                "studio64.exe": {"content": "Android Studio executable", "size": 2097152, "attributes": "A"},
                            },
                            "plugins": {
                                "android": {
                                    "lib": {
                                        "android.jar": {"content": "Android SDK", "size": 41943040, "attributes": "A"},
                                    },
                                },
                            },
                        },
                    },
                    "Media": {
                        "VLC": {
                            "vlc.exe": {"content": "VLC Media Player executable", "size": 40960000, "attributes": "A"},
                            "plugins": {
                                "access": {
                                    "libcdda_plugin.dll": {"content": "CD Audio input plugin", "size": 229376, "attributes": "A"},
                                },
                            },
                        },
                        "GIMP": {
                            "bin": {
                                "gimp-2.10.exe": {"content": "GIMP executable", "size": 30408704, "attributes": "A"},
                            },
                            "lib": {
                                "gimp": {
                                    "2.0": {
                                        "plug-ins": {
                                            "file-jpeg": {"content": "JPEG plugin", "size": 172032, "attributes": "A"},
                                        },
                                    },
                                },
                            },
                        },
                        "Audacity": {
                            "audacity.exe": {"content": "Audacity executable", "size": 65011712, "attributes": "A"},
                            "Plug-Ins": {
                                "analyze.ny": {"content": "Analyze plugin", "size": 2048, "attributes": "A"},
                            },
                        },
                        "OBS Studio": {
                            "bin": {
                                "64bit": {
                                    "obs64.exe": {"content": "OBS Studio executable", "size": 81788928, "attributes": "A"},
                                },
                            },
                            "data": {
                                "obs-plugins": {
                                    "win-capture": {
                                        "graphics-hook32.dll": {"content": "32-bit graphics capture", "size": 294912, "attributes": "A"},
                                        "graphics-hook64.dll": {"content": "64-bit graphics capture", "size": 368640, "attributes": "A"},
                                    },
                                },
                            },
                        },
                    },
                    "Utilities": {
                        "CCleaner": {
                            "CCleaner64.exe": {"content": "CCleaner executable", "size": 9961472, "attributes": "A"},
                        },
                        "WinRAR": {
                            "WinRAR.exe": {"content": "WinRAR executable", "size": 3145728, "attributes": "A"},
                        },
                        "TeamViewer": {
                            "TeamViewer.exe": {"content": "TeamViewer executable", "size": 28311552, "attributes": "A"},
                        },
                        "FileZilla": {
                            "filezilla.exe": {"content": "FileZilla executable", "size": 12582912, "attributes": "A"},
                        },
                        "CPU-Z": {
                            "cpuz.exe": {"content": "CPU-Z executable", "size": 2097152, "attributes": "A"},
                        },
                    },
                },
                "Archives": {
                    "2021": {
                        "January.zip": {"content": "January 2021 archives", "size": 1073741824, "attributes": "A"},
                        "February.zip": {"content": "February 2021 archives", "size": 1181116006, "attributes": "A"},
                        "March.zip": {"content": "March 2021 archives", "size": 1288490188, "attributes": "A"},
                        "April.zip": {"content": "April 2021 archives", "size": 1395864371, "attributes": "A"},
                        "May.zip": {"content": "May 2021 archives", "size": 1503238553, "attributes": "A"},
                        "June.zip": {"content": "June 2021 archives", "size": 1610612736, "attributes": "A"},
                    },
                    "2020": {
                        "Q1.zip": {"content": "Q1 2020 archives", "size": 3221225472, "attributes": "A"},
                        "Q2.zip": {"content": "Q2 2020 archives", "size": 3435973836, "attributes": "A"},
                        "Q3.zip": {"content": "Q3 2020 archives", "size": 3650722201, "attributes": "A"},
                        "Q4.zip": {"content": "Q4 2020 archives", "size": 3865470566, "attributes": "A"},
                    },
                    "2019": {
                        "FirstHalf.zip": {"content": "First half of 2019 archives", "size": 5368709120, "attributes": "A"},
                        "SecondHalf.zip": {"content": "Second half of 2019 archives", "size": 5767168000, "attributes": "A"},
                    },
                },
                "Databases": {
                    "SQLite": {
                        "customers.db": {"content": "Customer database", "size": 52428800, "attributes": "A"},
                        "inventory.db": {"content": "Inventory database", "size": 104857600, "attributes": "A"},
                        "transactions.db": {"content": "Transaction database", "size": 209715200, "attributes": "A"},
                    },
                    "MySQL": {
                        "data": {
                            "mysqldb": {
                                "user.ibd": {"content": "User table data", "size": 1048576, "attributes": "A"},
                                "product.ibd": {"content": "Product table data", "size": 2097152, "attributes": "A"},
                                "order.ibd": {"content": "Order table data", "size": 4194304, "attributes": "A"},
                            },
                        },
                        "my.ini": {"content": "MySQL configuration file", "size": 4096, "attributes": "A"},
                    },
                    "MongoDB": {
                        "data": {
                            "db": {
                                "collection-0-1234567890123456789.wt": {"content": "MongoDB collection data", "size": 67108864, "attributes": "A"},
                                "index-1-1234567890123456789.wt": {"content": "MongoDB index data", "size": 33554432, "attributes": "A"},
                            },
                        },
                        "mongod.cfg": {"content": "MongoDB configuration file", "size": 2048, "attributes": "A"},
                    },
                    "PostgreSQL": {
                        "data": {
                            "base": {
                                "1": {
                                    "12345": {"content": "PostgreSQL table data", "size": 8388608, "attributes": "A"},
                                    "12346": {"content": "PostgreSQL index data", "size": 4194304, "attributes": "A"},
                                },
                            },
                        },
                        "postgresql.conf": {"content": "PostgreSQL configuration file", "size": 8192, "attributes": "A"},
                    },
                },
                "VirtualBox VMs": {
                    "Ubuntu Server": {
                        "Ubuntu Server.vdi": {"content": "Ubuntu Server virtual disk", "size": 10737418240, "attributes": "A"},
                        "Ubuntu Server.vbox": {"content": "VirtualBox configuration", "size": 8192, "attributes": "A"},
                    },
                    "Windows 10 Test": {
                        "Windows 10 Test.vdi": {"content": "Windows 10 Test virtual disk", "size": 32212254720, "attributes": "A"},
                        "Windows 10 Test.vbox": {"content": "VirtualBox configuration", "size": 8192, "attributes": "A"},
                    },
                    "Kali Linux": {
                        "Kali Linux.vdi": {"content": "Kali Linux virtual disk", "size": 21474836480, "attributes": "A"},
                        "Kali Linux.vbox": {"content": "VirtualBox configuration", "size": 8192, "attributes": "A"},
                    },
                    "CentOS": {
                        "CentOS.vdi": {"content": "CentOS virtual disk", "size": 16106127360, "attributes": "A"},
                        "CentOS.vbox": {"content": "VirtualBox configuration", "size": 8192, "attributes": "A"},
                    },
                },
                "Workspace": {
                    "Project_A": {
                        "src": {
                            "main.py": {"content": "Python source code", "size": 4096, "attributes": "A"},
                            "utils.py": {"content": "Utility functions", "size": 2048, "attributes": "A"},
                            "config.py": {"content": "Configuration file", "size": 1024, "attributes": "A"},
                        },
                        "tests": {
                            "test_main.py": {"content": "Main tests", "size": 3072, "attributes": "A"},
                            "test_utils.py": {"content": "Utility tests", "size": 2048, "attributes": "A"},
                        },
                        "docs": {
                            "api.md": {"content": "API documentation", "size": 16384, "attributes": "A"},
                            "setup.md": {"content": "Setup instructions", "size": 8192, "attributes": "A"},
                        },
                        "requirements.txt": {"content": "Project dependencies", "size": 1024, "attributes": "A"},
                        "README.md": {"content": "Project readme", "size": 4096, "attributes": "A"},
                    },
                    "Project_B": {
                        "frontend": {
                            "src": {
                                "components": {
                                    "Header.js": {"content": "React component", "size": 2048, "attributes": "A"},
                                    "Footer.js": {"content": "React component", "size": 1536, "attributes": "A"},
                                    "Sidebar.js": {"content": "React component", "size": 3072, "attributes": "A"},
                                },
                                "pages": {
                                    "Home.js": {"content": "React page component", "size": 4096, "attributes": "A"},
                                    "About.js": {"content": "React page component", "size": 3584, "attributes": "A"},
                                    "Contact.js": {"content": "React page component", "size": 3072, "attributes": "A"},
                                },
                                "App.js": {"content": "Main React app", "size": 2560, "attributes": "A"},
                                "index.js": {"content": "Entry point", "size": 1024, "attributes": "A"},
                            },
                            "public": {
                                "index.html": {"content": "HTML template", "size": 2048, "attributes": "A"},
                                "favicon.ico": {"content": "Favicon", "size": 4096, "attributes": "A"},
                            },
                            "package.json": {"content": "NPM package file", "size": 1536, "attributes": "A"},
                        },
                        "backend": {
                            "src": {
                                "controllers": {
                                    "userController.js": {"content": "User controller", "size": 4096, "attributes": "A"},
                                    "productController.js": {"content": "Product controller", "size": 5120, "attributes": "A"},
                                },
                                "models": {
                                    "userModel.js": {"content": "User model", "size": 2048, "attributes": "A"},
                                    "productModel.js": {"content": "Product model", "size": 2560, "attributes": "A"},
                                },
                                "routes": {
                                    "userRoutes.js": {"content": "User routes", "size": 1536, "attributes": "A"},
                                    "productRoutes.js": {"content": "Product routes", "size": 2048, "attributes": "A"},
                                },
                                "config": {
                                    "database.js": {"content": "Database configuration", "size": 1024, "attributes": "A"},
                                },
                                "server.js": {"content": "Main server file", "size": 3072, "attributes": "A"},
                            },
                            "package.json": {"content": "NPM package file", "size": 1536, "attributes": "A"},
                        },
                        "README.md": {"content": "Project readme", "size": 5120, "attributes": "A"},
                    },
                    "Project_C": {
                        "src": {
                            "main": {
                                "java": {
                                    "com": {
                                        "example": {
                                            "project": {
                                                "Main.java": {"content": "Main Java class", "size": 2048, "attributes": "A"},
                                                "service": {
                                                    "UserService.java": {"content": "User service", "size": 4096, "attributes": "A"},
                                                    "ProductService.java": {"content": "Product service", "size": 5120, "attributes": "A"},
                                                },
                                                "repository": {
                                                    "UserRepository.java": {"content": "User repository", "size": 3072, "attributes": "A"},
                                                    "ProductRepository.java": {"content": "Product repository", "size": 3584, "attributes": "A"},
                                                },
                                                "model": {
                                                    "User.java": {"content": "User model", "size": 1536, "attributes": "A"},
                                                    "Product.java": {"content": "Product model", "size": 2048, "attributes": "A"},
                                                },
                                            },
                                        },
                                    },
                                },
                                "resources": {
                                    "application.properties": {"content": "Application properties", "size": 1024, "attributes": "A"},
                                },
                            },
                            "test": {
                                "java": {
                                    "com": {
                                        "example": {
                                            "project": {
                                                "service": {
                                                    "UserServiceTest.java": {"content": "User service tests", "size": 3072, "attributes": "A"},
                                                    "ProductServiceTest.java": {"content": "Product service tests", "size": 4096, "attributes": "A"},
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                        "pom.xml": {"content": "Maven configuration", "size": 4096, "attributes": "A"},
                        "README.md": {"content": "Project readme", "size": 3072, "attributes": "A"},
                    },
                },
                "Personal": {
                    "Documents": {
                        "Resume": {
                            "MyResume_2023.docx": {"content": "Current resume", "size": 524288, "attributes": "A"},
                            "CoverLetter_Template.docx": {"content": "Cover letter template", "size": 262144, "attributes": "A"},
                        },
                        "Financial": {
                            "Budget_2023.xlsx": {"content": "Annual budget spreadsheet", "size": 1048576, "attributes": "A"},
                            "Investments": {
                                "StockPortfolio.xlsx": {"content": "Stock portfolio tracker", "size": 786432, "attributes": "A"},
                                "CryptoHoldings.xlsx": {"content": "Cryptocurrency holdings", "size": 524288, "attributes": "A"},
                            },
                            "TaxReturns": {
                                "2022_TaxReturn.pdf": {"content": "2022 Tax return", "size": 3145728, "attributes": "A"},
                                "2021_TaxReturn.pdf": {"content": "2021 Tax return", "size": 2097152, "attributes": "A"},
                            },
                        },
                        "Health": {
                            "MedicalRecords": {
                                "VaccinationRecord.pdf": {"content": "Vaccination history", "size": 1048576, "attributes": "A"},
                                "AnnualCheckup_2023.pdf": {"content": "Annual checkup results", "size": 2097152, "attributes": "A"},
                            },
                            "InsurancePolicies": {
                                "HealthInsurance_2023.pdf": {"content": "Health insurance policy", "size": 1572864, "attributes": "A"},
                                "LifeInsurance.pdf": {"content": "Life insurance policy", "size": 2097152, "attributes": "A"},
                            },
                        },
                        "Education": {
                            "Transcripts": {
                                "UniversityTranscript.pdf": {"content": "University academic transcript", "size": 1048576, "attributes": "A"},
                            },
                            "Certificates": {
                                "Python_DataScience_Cert.pdf": {"content": "Data Science certification", "size": 2097152, "attributes": "A"},
                                "AWS_Solutions_Architect.pdf": {"content": "AWS certification", "size": 1572864, "attributes": "A"},
                            },
                        },
                    },
                    "Photos": {
                        "2023": {
                            "Summer_Vacation": {
                                "Beach_Day1.jpg": {"content": "Vacation photo", "size": 6291456, "attributes": "A"},
                                "Beach_Day2.jpg": {"content": "Vacation photo", "size": 5242880, "attributes": "A"},
                                "HikingTrip.jpg": {"content": "Vacation photo", "size": 7340032, "attributes": "A"},
                            },
                            "Family_Reunion": {
                                "GroupPhoto.jpg": {"content": "Family photo", "size": 8388608, "attributes": "A"},
                                "Candid_Shots": {
                                    "Candid1.jpg": {"content": "Candid family photo", "size": 4194304, "attributes": "A"},
                                    "Candid2.jpg": {"content": "Candid family photo", "size": 3145728, "attributes": "A"},
                                },
                            },
                        },
                        "2022": {
                            "Christmas": {
                                "ChristmasEve.jpg": {"content": "Christmas photo", "size": 5242880, "attributes": "A"},
                                "ChristmasMorning.jpg": {"content": "Christmas photo", "size": 6291456, "attributes": "A"},
                            },
                            "NewYearsEve": {
                                "Fireworks.jpg": {"content": "New Year's photo", "size": 7340032, "attributes": "A"},
                                "Friends.jpg": {"content": "New Year's photo", "size": 5242880, "attributes": "A"},
                            },
                        },
                    },
                    "Videos": {
                        "HomeMovies": {
                            "BirthdayParty_2023.mp4": {"content": "Birthday video", "size": 1073741824, "attributes": "A"},
                            "WeddingAnniversary.mp4": {"content": "Anniversary video", "size": 2147483648, "attributes": "A"},
                        },
                        "TravelVlogs": {
                            "EuropeTrip2022": {
                                "Paris.mp4": {"content": "Travel vlog", "size": 3221225472, "attributes": "A"},
                                "Rome.mp4": {"content": "Travel vlog", "size": 2684354560, "attributes": "A"},
                            },
                        },
                    },
                    "Music": {
                        "Playlists": {
                            "Workout.m3u": {"content": "Workout playlist", "size": 4096, "attributes": "A"},
                            "Relaxation.m3u": {"content": "Relaxation playlist", "size": 3072, "attributes": "A"},
                        },
                        "MyRecordings": {
                            "GuitarPractice_2023-07-15.mp3": {"content": "Guitar recording", "size": 15728640, "attributes": "A"},
                            "BandRehersal_2023-08-01.mp3": {"content": "Band rehearsal recording", "size": 31457280, "attributes": "A"},
                        },
                    },
                },
                "Games": {
                    "Steam": {
                        "steamapps": {
                            "common": {
                                "Counter-Strike Global Offensive": {
                                    "csgo.exe": {"content": "CS:GO executable", "size": 47185920, "attributes": "A"},
                                    "csgo": {
                                        "maps": {
                                            "de_dust2.bsp": {"content": "Dust II map file", "size": 52428800, "attributes": "A"},
                                            "de_mirage.bsp": {"content": "Mirage map file", "size": 47185920, "attributes": "A"},
                                        },
                                        "materials": {
                                            "models": {
                                                "weapons": {
                                                    "v_models": {
                                                        "v_knife_default_ct.vtf": {"content": "Knife texture", "size": 1048576, "attributes": "A"},
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                "Dota 2": {
                                    "dota2.exe": {"content": "Dota 2 executable", "size": 52428800, "attributes": "A"},
                                    "game": {
                                        "dota": {
                                            "maps": {
                                                "dota.vmap": {"content": "Dota 2 map file", "size": 104857600, "attributes": "A"},
                                            },
                                            "cfg": {
                                                "autoexec.cfg": {"content": "Auto-execute config", "size": 4096, "attributes": "A"},
                                            },
                                        },
                                    },
                                },
                            },
                            "downloading": {
                                "231450": {
                                    "231450_2701924531.patch": {"content": "Game update patch", "size": 209715200, "attributes": "A"},
                                },
                            },
                        },
                        "userdata": {
                            "12345678": {
                                "730": {
                                    "local": {
                                        "cfg": {
                                            "config.cfg": {"content": "CS:GO user config", "size": 16384, "attributes": "A"},
                                        },
                                    },
                                },
                            },
                        },
                    },
                    "Epic Games": {
                        "Fortnite": {
                            "FortniteGame": {
                                "Binaries": {
                                    "Win64": {
                                        "FortniteClient-Win64-Shipping.exe": {"content": "Fortnite executable", "size": 83886080, "attributes": "A"},
                                    },
                                },
                                "Content": {
                                    "Paks": {
                                        "pakchunk0-WindowsClient.pak": {"content": "Game content", "size": 10737418240, "attributes": "A"},
                                    },
                                },
                            },
                        },
                    },
                    "Minecraft": {
                        "minecraft.exe": {"content": "Minecraft launcher", "size": 26214400, "attributes": "A"},
                        ".minecraft": {
                            "versions": {
                                "1.19.2": {
                                    "1.19.2.jar": {"content": "Minecraft 1.19.2", "size": 209715200, "attributes": "A"},
                                },
                            },
                            "saves": {
                                "New World": {
                                    "level.dat": {"content": "World data", "size": 8192, "attributes": "A"},
                                    "region": {
                                        "r.0.0.mca": {"content": "Region file", "size": 8388608, "attributes": "A"},
                                    },
                                },
                            },
                            "resourcepacks": {
                                "HD_Textures.zip": {"content": "Texture pack", "size": 104857600, "attributes": "A"},
                            },
                        },
                    },
                },
                "Temp": {
                    "download_3fa0eb.tmp": {"content": "Temporary download file", "size": 104857600, "attributes": "A"},
                    "print_job_78d2c1.spl": {"content": "Print spool file", "size": 2097152, "attributes": "A"},
                    "~WRL0003.tmp": {"content": "Temporary Word file", "size": 524288, "attributes": "A"},
                    "setup_log_93ab7f.txt": {"content": "Setup log file", "size": 1048576, "attributes": "A"},
                    "crashdump_20230715_141523.dmp": {"content": "Crash dump file", "size": 67108864, "attributes": "A"},
                },
                "Drivers": {
                    "NVIDIA": {
                        "Display.Driver": {
                            "nvcpl.dll": {"content": "NVIDIA Control Panel DLL", "size": 8388608, "attributes": "A"},
                            "nvwgf2umx.dll": {"content": "NVIDIA OpenGL driver", "size": 31457280, "attributes": "A"},
                        },
                    },
                    "Intel": {
                        "Graphics": {
                            "igfxEM.exe": {"content": "Intel Graphics Executable", "size": 2097152, "attributes": "A"},
                            "igfxHK.exe": {"content": "Intel Graphics Hotkey Executable", "size": 1048576, "attributes": "A"},
                        },
                    },
                    "Realtek": {
                        "Audio": {
                            "RtkNGUI64.exe": {"content": "Realtek HD Audio Manager", "size": 15728640, "attributes": "A"},
                            "RTHDCPL.exe": {"content": "Realtek HD Audio CPL", "size": 10485760, "attributes": "A"},
                        },
                    },
                },
                "Programs": {
                    "AutoHotkey": {
                        "AutoHotkey.exe": {"content": "AutoHotkey Executable", "size": 1048576, "attributes": "A"},
                        "Scripts": {
                            "text_expander.ahk": {"content": "Text Expander Script", "size": 4096, "attributes": "A"},
                            "window_manager.ahk": {"content": "Window Management Script", "size": 8192, "attributes": "A"},
                        },
                    },
                    "Wireshark": {
                        "Wireshark.exe": {"content": "Wireshark Network Protocol Analyzer", "size": 83886080, "attributes": "A"},
                        "WiresharkPortable.exe": {"content": "Portable Wireshark Launcher", "size": 1048576, "attributes": "A"},
                    },
                    "Blender": {
                        "blender.exe": {"content": "Blender 3D Creation Suite", "size": 209715200, "attributes": "A"},
                        "2.93": {
                            "scripts": {
                                "addons": {
                                    "io_scene_fbx": {
                                        "__init__.py": {"content": "FBX Import/Export Addon", "size": 262144, "attributes": "A"},
                                    },
                                },
                            },
                        },
                    },
                    "OBS Studio": {
                        "bin": {
                            "64bit": {
                                "obs64.exe": {"content": "OBS Studio 64-bit", "size": 83886080, "attributes": "A"},
                            },
                        },
                        "data": {
                            "obs-plugins": {
                                "win-capture": {
                                    "graphics-hook32.dll": {"content": "32-bit Graphics Capture", "size": 1048576, "attributes": "A"},
                                    "graphics-hook64.dll": {"content": "64-bit Graphics Capture", "size": 1310720, "attributes": "A"},
                                },
                            },
                        },
                    },
                },
                "Backups": {
                    "Weekly": {
                        "Documents_2023-07-09.zip": {"content": "Weekly Documents Backup", "size": 1073741824, "attributes": "A"},
                        "Documents_2023-07-16.zip": {"content": "Weekly Documents Backup", "size": 1288490188, "attributes": "A"},
                    },
                    "Monthly": {
                        "FullSystem_2023-06-30.vhd": {"content": "Monthly Full System Backup", "size": 107374182400, "attributes": "A"},
                        "FullSystem_2023-07-31.vhd": {"content": "Monthly Full System Backup", "size": 112742891520, "attributes": "A"},
                    },
                },
            },
            "G:\\": {
                "Media": {
                    "Movies": {
                        "Action": {
                            "The_Dark_Knight_2008.mp4": {"content": "Movie file", "size": 8589934592, "attributes": "A"},
                            "Inception_2010.mp4": {"content": "Movie file", "size": 10737418240, "attributes": "A"},
                            "Mad_Max_Fury_Road_2015.mp4": {"content": "Movie file", "size": 9663676416, "attributes": "A"},
                        },
                        "Comedy": {
                            "The_Hangover_2009.mp4": {"content": "Movie file", "size": 6442450944, "attributes": "A"},
                            "Bridesmaids_2011.mp4": {"content": "Movie file", "size": 7516192768, "attributes": "A"},
                            "Deadpool_2016.mp4": {"content": "Movie file", "size": 8589934592, "attributes": "A"},
                        },
                        "Drama": {
                            "The_Shawshank_Redemption_1994.mp4": {"content": "Movie file", "size": 9663676416, "attributes": "A"},
                            "Forrest_Gump_1994.mp4": {"content": "Movie file", "size": 10737418240, "attributes": "A"},
                            "The_Godfather_1972.mp4": {"content": "Movie file", "size": 11811160064, "attributes": "A"},
                        },
                    },
                    "TV_Shows": {
                        "Game_of_Thrones": {
                            "Season_1": {
                                "Episode_1.mp4": {"content": "TV Episode", "size": 3221225472, "attributes": "A"},
                                "Episode_2.mp4": {"content": "TV Episode", "size": 3221225472, "attributes": "A"},
                                "Episode_3.mp4": {"content": "TV Episode", "size": 3221225472, "attributes": "A"},
                            },
                            "Season_2": {
                                "Episode_1.mp4": {"content": "TV Episode", "size": 3221225472, "attributes": "A"},
                                "Episode_2.mp4": {"content": "TV Episode", "size": 3221225472, "attributes": "A"},
                                "Episode_3.mp4": {"content": "TV Episode", "size": 3221225472, "attributes": "A"},
                            },
                        },
                        "Breaking_Bad": {
                            "Season_1": {
                                "Episode_1.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                                "Episode_2.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                                "Episode_3.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                            },
                            "Season_2": {
                                "Episode_1.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                                "Episode_2.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                                "Episode_3.mp4": {"content": "TV Episode", "size": 2147483648, "attributes": "A"},
                            },
                        },
                    },
                    "Music": {
                        "Rock": {
                            "Queen": {
                                "A_Night_at_the_Opera": {
                                    "01_Death_on_Two_Legs.mp3": {"content": "Music track", "size": 10485760, "attributes": "A"},
                                    "02_Lazing_on_a_Sunday_Afternoon.mp3": {"content": "Music track", "size": 5242880, "attributes": "A"},
                                    "03_I'm_in_Love_with_My_Car.mp3": {"content": "Music track", "size": 8388608, "attributes": "A"},
                                },
                            },
                            "Pink_Floyd": {
                                "The_Wall": {
                                    "01_Another_Brick_in_the_Wall.mp3": {"content": "Music track", "size": 12582912, "attributes": "A"},
                                    "02_The_Happiest_Days_of_Our_Lives.mp3": {"content": "Music track", "size": 6291456, "attributes": "A"},
                                    "03_Another_Brick_in_the_Wall_Part_2.mp3": {"content": "Music track", "size": 10485760, "attributes": "A"},
                                },
                            },
                        },
                        "Pop": {
                            "Michael_Jackson": {
                                "Thriller": {
                                    "01_Wanna_Be_Startin_Somethin.mp3": {"content": "Music track", "size": 11534336, "attributes": "A"},
                                    "02_Baby_Be_Mine.mp3": {"content": "Music track", "size": 9437184, "attributes": "A"},
                                    "03_The_Girl_Is_Mine.mp3": {"content": "Music track", "size": 8388608, "attributes": "A"},
                                },
                            },
                            "Madonna": {
                                "Like_a_Virgin": {
                                    "01_Material_Girl.mp3": {"content": "Music track", "size": 7340032, "attributes": "A"},
                                    "02_Angel.mp3": {"content": "Music track", "size": 6291456, "attributes": "A"},
                                    "03_Like_a_Virgin.mp3": {"content": "Music track", "size": 8388608, "attributes": "A"},
                                },
                            },
                        },
                    },
                },
                "Backups": {
                    "Personal": {
                        "Documents": {
                            "2023_Tax_Documents.zip": {"content": "Archived tax documents", "size": 104857600, "attributes": "A"},
                            "Family_Photos_2022.zip": {"content": "Archived family photos", "size": 1073741824, "attributes": "A"},
                            "Important_Certificates.zip": {"content": "Archived certificates", "size": 52428800, "attributes": "A"},
                        },
                        "Financial": {
                            "Bank_Statements_2022.pdf": {"content": "Bank statements", "size": 10485760, "attributes": "A"},
                            "Investment_Portfolio_2023.xlsx": {"content": "Investment tracking", "size": 1048576, "attributes": "A"},
                        },
                    },
                    "Work": {
                        "Projects": {
                            "Project_X_Final_Deliverables.zip": {"content": "Project deliverables", "size": 536870912, "attributes": "A"},
                            "Client_Presentations_2023.zip": {"content": "Client presentations", "size": 268435456, "attributes": "A"},
                        },
                        "Reports": {
                            "Annual_Report_2022.pdf": {"content": "Annual company report", "size": 26214400, "attributes": "A"},
                            "Quarterly_Reports_2023.zip": {"content": "Quarterly reports", "size": 104857600, "attributes": "A"},
                        },
                    },
                },
                "Software": {
                    "Operating_Systems": {
                        "Windows": {
                            "Windows_10_64bit.iso": {"content": "Windows 10 installation media", "size": 5368709120, "attributes": "A"},
                            "Windows_11_64bit.iso": {"content": "Windows 11 installation media", "size": 6442450944, "attributes": "A"},
                        },
                        "Linux": {
                            "Ubuntu_22.04_LTS.iso": {"content": "Ubuntu installation media", "size": 3758096384, "attributes": "A"},
                            "Fedora_37_Workstation.iso": {"content": "Fedora installation media", "size": 2684354560, "attributes": "A"},
                        },
                    },
                    "Development": {
                        "IDEs": {
                            "VSCode": {
                                "VSCodeUserSetup-x64-1.70.2.exe": {"content": "VS Code installer", "size": 79691776, "attributes": "A"},
                            },
                            "IntelliJ_IDEA": {
                                "ideaIU-2023.1.3.exe": {"content": "IntelliJ IDEA installer", "size": 944504832, "attributes": "A"},
                            },
                        },
                        "SDKs": {
                            "JDK": {
                                "jdk-17_windows-x64_bin.exe": {"content": "Java Development Kit installer", "size": 179306496, "attributes": "A"},
                            },
                            "Python": {
                                "python-3.11.0-amd64.exe": {"content": "Python installer", "size": 27262976, "attributes": "A"},
                            },
                        },
                    },
                },
                "Virtual_Machines": {
                    "Development_VM": {
                        "Dev_VM.vdi": {"content": "Development VM disk", "size": 68719476736, "attributes": "A"},
                        "Dev_VM.vbox": {"content": "Development VM config", "size": 8192, "attributes": "A"},
                    },
                    "Testing_VM": {
                        "Test_VM.vdi": {"content": "Testing VM disk", "size": 42949672960, "attributes": "A"},
                        "Test_VM.vbox": {"content": "Testing VM config", "size": 8192, "attributes": "A"},
                    },
                },
            },
        }
        self.permissions: Dict[str, str] = {}

    
    def set_default_directory(self, path):
        try:
            normalized_path = os.path.normpath(path)
            if normalized_path == '.':
                normalized_path = 'C:\\'
            self.interpreter.file_system.set_default_directory(normalized_path)
            print(f"Default directory set to: {normalized_path}")
        except ValueError as e:
            print(f"Error setting default directory: {str(e)}")
            # If setting the directory fails, fall back to C:\
            self.interpreter.file_system.set_default_directory("C:\\")
            print("Fallback: Default directory set to C:\\")


    def find(self, path: str, search_string: str, case_sensitive: bool = False) -> None:
        target_path = self._normalize_path(path)
        if not self._path_exists(target_path):
            print(f"The system cannot find the path specified: {target_path}")
            return

        def search_in_file(file_path: str, content: str):
            lines = content.splitlines()
            for i, line in enumerate(lines, 1):
                if (search_string in line) if case_sensitive else (search_string.lower() in line.lower()):
                    print(f"{file_path}({i}): {line.strip()}")

        def search_recursive(current_path: str):
            items = self._get_directory_contents(current_path)
            for item in items:
                item_path = os.path.join(current_path, item['name'])
                if self._is_directory(item_path):
                    search_recursive(item_path)
                else:
                    content = self._get_file_content(item_path)
                    search_in_file(item_path, content)

        search_recursive(target_path)

    def findstr(self, search_string: str, file_patterns: List[str], path: str = "", case_sensitive: bool = False, line_numbers: bool = False, recursive: bool = False, exclude_patterns: List[str] = None, whole_word: bool = False, quiet: bool = False) -> None:
        target_path = self._normalize_path(path) if path else self.current_directory
        if not self._path_exists(target_path):
            print(f"The system cannot find the path specified: {target_path}")
            return

        def match_pattern(filename: str, patterns: List[str]) -> bool:
            return any(fnmatch.fnmatch(filename.lower(), pattern.lower()) for pattern in patterns)

        def exclude_pattern(filename: str, patterns: List[str]) -> bool:
            return any(fnmatch.fnmatch(filename.lower(), pattern.lower()) for pattern in patterns) if patterns else False

        def search_in_file(file_path: str, content: str):
            lines = content.splitlines()
            for i, line in enumerate(lines, 1):
                if whole_word:
                    words = line.split()
                    if not any((search_string == word) if case_sensitive else (search_string.lower() == word.lower()) for word in words):
                        continue
                elif not ((search_string in line) if case_sensitive else (search_string.lower() in line.lower())):
                    continue

                if not quiet:
                    if line_numbers:
                        print(f"{file_path}({i}): {line.strip()}")
                    else:
                        print(f"{file_path}: {line.strip()}")

        def search_recursive(current_path: str):
            items = self._get_directory_contents(current_path)
            for item in items:
                item_path = os.path.join(current_path, item['name'])
                if self._is_directory(item_path):
                    if recursive:
                        search_recursive(item_path)
                elif match_pattern(item['name'], file_patterns) and not exclude_pattern(item['name'], exclude_patterns):
                    content = self._get_file_content(item_path)
                    search_in_file(item_path, content)

        search_recursive(target_path)

    def xcopy(self, source: str, destination: str, subdirectories: bool = False, empty_directories: bool = False, overwrite: bool = False, exclude: List[str] = None, include: List[str] = None, quiet: bool = False) -> None:
        source_path = self._normalize_path(source)
        dest_path = self._normalize_path(destination)

        if not self._path_exists(source_path):
            print(f"The system cannot find the path specified: {source_path}")
            return

        def should_copy(item_name: str) -> bool:
            if exclude and any(fnmatch.fnmatch(item_name, pattern) for pattern in exclude):
                return False
            if include:
                return any(fnmatch.fnmatch(item_name, pattern) for pattern in include)
            return True

        def copy_recursive(src: str, dst: str):
            if self._is_directory(src):
                if not self._path_exists(dst):
                    self._create_directory(dst)
                if subdirectories:
                    items = self._get_directory_contents(src)
                    for item in items:
                        src_item = os.path.join(src, item['name'])
                        dst_item = os.path.join(dst, item['name'])
                        if should_copy(item['name']):
                            copy_recursive(src_item, dst_item)
            elif empty_directories or not self._is_directory(src):
                if overwrite or not self._path_exists(dst):
                    self._copy_file(src, dst)
                    if not quiet:
                        print(f"Copied: {dst}")
                elif not quiet:
                    print(f"Skipped: {dst} (already exists)")

        copy_recursive(source_path, dest_path)
        if not quiet:
            print("XCopy operation completed.")

    def robocopy(self, source: str, destination: str, files: List[str] = None, options: Dict[str, Any] = None) -> None:
        source_path = self._normalize_path(source)
        dest_path = self._normalize_path(destination)

        if not self._path_exists(source_path):
            print(f"The system cannot find the path specified: {source_path}")
            return

        if options is None:
            options = {}

        def should_copy(filename: str) -> bool:
            if not files:
                return True
            return any(fnmatch.fnmatch(filename.lower(), pattern.lower()) for pattern in files)
        
        

        def copy_recursive(src: str, dst: str):
            if self._is_directory(src):
                if not self._path_exists(dst):
                    self._create_directory(dst)
                items = self._get_directory_contents(src)
                for item in items:
                    src_item = os.path.join(src, item['name'])
                    dst_item = os.path.join(dst, item['name'])
                    copy_recursive(src_item, dst_item)
            elif should_copy(os.path.basename(src)):
                if options.get('mir') and self._path_exists(dst):
                    self._delete_file(dst)
                self._copy_file(src, dst)
                print(f"Copied: {dst}")

        copy_recursive(source_path, dest_path)
        print("Robocopy operation completed.")

    def comp(self, file1: str, file2: str, line_number: bool = False, number_of_differences: int = None, case_sensitive: bool = True) -> None:
        file1_path = self._normalize_path(file1)
        file2_path = self._normalize_path(file2)

        if not self._path_exists(file1_path):
            print(f"The system cannot find the file specified: {file1_path}")
            return
        if not self._path_exists(file2_path):
            print(f"The system cannot find the file specified: {file2_path}")
            return

        content1 = self._get_file_content(file1_path)
        content2 = self._get_file_content(file2_path)

        if not case_sensitive:
            content1 = content1.lower()
            content2 = content2.lower()

        if content1 == content2:
            print("Files compare OK")
        else:
            lines1 = content1.splitlines()
            lines2 = content2.splitlines()
            differences = 0
            for i, (line1, line2) in enumerate(zip_longest(lines1, lines2), 1):
                if line1 != line2:
                    if line_number:
                        print(f"Difference found at line {i}")
                    print(f"File 1: {line1}")
                    print(f"File 2: {line2}")
                    differences += 1
                    if number_of_differences and differences >= number_of_differences:
                        print(f"Reached maximum number of differences ({number_of_differences})")
                        break

    def fc(self, file1: str, file2: str, ignore_case: bool = False, ignore_blank_lines: bool = False, line_number: bool = False, brief: bool = False) -> None:
        file1_path = self._normalize_path(file1)
        file2_path = self._normalize_path(file2)

        if not self._path_exists(file1_path):
            print(f"The system cannot find the file specified: {file1_path}")
            return
        if not self._path_exists(file2_path):
            print(f"The system cannot find the file specified: {file2_path}")
            return

        content1 = self._get_file_content(file1_path)
        content2 = self._get_file_content(file2_path)

        lines1 = content1.splitlines()
        lines2 = content2.splitlines()

        if ignore_blank_lines:
            lines1 = [line for line in lines1 if line.strip()]
            lines2 = [line for line in lines2 if line.strip()]

        if ignore_case:
            lines1 = [line.lower() for line in lines1]
            lines2 = [line.lower() for line in lines2]

        differ = difflib.Differ()
        diff = list(differ.compare(lines1, lines2))

        if all(line.startswith('  ') for line in diff):
            print("FC: no differences encountered")
        else:
            print(f"Comparing files {file1_path} and {file2_path}")
            if brief:
                print("Files differ")
            else:
                for i, line in enumerate(diff, 1):
                    if not line.startswith('  '):
                        if line_number:
                            print(f"Line {i}: {line}")
                        else:
                            print(line)

    def forfiles(self, path: str = "", command: str = "", include: str = "*", exclude: str = "", recursive: bool = False, days: int = None, min_size: int = None, max_size: int = None) -> None:
        target_path = self._normalize_path(path) if path else self.current_directory
        if not self._path_exists(target_path):
            print(f"The system cannot find the path specified: {target_path}")
            return

        def process_file(file_path: str):
            file_name = os.path.basename(file_path)
            dir_name = os.path.dirname(file_path)
            cmd = command.replace("@file", f'"{file_name}"')
            cmd = cmd.replace("@path", f'"{file_path}"')
            cmd = cmd.replace("@relpath", f'"{os.path.relpath(file_path, target_path)}"')
            cmd = cmd.replace("@name", f'"{os.path.splitext(file_name)[0]}"')
            cmd = cmd.replace("@ext", f'"{os.path.splitext(file_name)[1]}"')
            cmd = cmd.replace("@dir", f'"{dir_name}"')
            os.system(cmd)

        def should_process(item: Dict[str, Any]) -> bool:
            if not fnmatch.fnmatch(item['name'].lower(), include.lower()):
                return False
            if exclude and fnmatch.fnmatch(item['name'].lower(), exclude.lower()):
                return False
            if days is not None:
                # This is a simplification. In a real system, you'd check the actual file modification time
                return True
            if min_size is not None and item.get('size', 0) < min_size:
                return False
            if max_size is not None and item.get('size', 0) > max_size:
                return False
            return True

        def process_recursive(current_path: str):
            items = self._get_directory_contents(current_path)
            for item in items:
                item_path = os.path.join(current_path, item['name'])
                if self._is_directory(item_path):
                    if recursive:
                        process_recursive(item_path)
                elif should_process(item):
                    process_file(item_path)

        process_recursive(target_path)

    def takeown(self, path: str, recursive: bool = False, user: str = None) -> None:
        target_path = self._normalize_path(path)
        if not self._path_exists(target_path):
            print(f"The system cannot find the path specified: {target_path}")
            return

        def take_ownership(item_path: str):
            # In a real system, this would change the owner of the file or directory
            # For our virtual file system, we'll just print a message
            owner = user if user else "current user"
            print(f"Ownership of {item_path} taken by {owner}.")

        def process_recursive(current_path: str):
            take_ownership(current_path)
            if recursive and self._is_directory(current_path):
                items = self._get_directory_contents(current_path)
                for item in items:
                    item_path = os.path.join(current_path, item['name'])
                    process_recursive(item_path)

        process_recursive(target_path)

    def icacls(self, path: str, action: str, permissions: str, recursive: bool = False, quiet: bool = False) -> None:
        target_path = self._normalize_path(path)
        if not self._path_exists(target_path):
            print(f"The system cannot find the path specified: {target_path}")
            return

        def modify_permissions(item_path: str):
            # In a real system, this would modify the permissions of the file or directory
            # For our virtual file system, we'll just print a message
            if not quiet:
                print(f"Permissions of {item_path} modified: {action} {permissions}")

        def process_recursive(current_path: str):
            modify_permissions(current_path)
            if recursive and self._is_directory(current_path):
                items = self._get_directory_contents(current_path)
                for item in items:
                    item_path = os.path.join(current_path, item['name'])
                    process_recursive(item_path)

        process_recursive(target_path)

    def compact(self, path: str, compress: bool = True, recursive: bool = False, quiet: bool = False) -> None:
        target_path = self._normalize_path(path)
        if not self._path_exists(target_path):
            print(f"The system cannot find the path specified: {target_path}")
            return

        def compress_item(item_path: str):
            # In a real system, this would compress or uncompress the file or directory
            # For our virtual file system, we'll just print a message
            action = "Compressed" if compress else "Uncompressed"
            if not quiet:
                print(f"{action} {item_path}")

        def process_recursive(current_path: str):
            compress_item(current_path)
            if recursive and self._is_directory(current_path):
                items = self._get_directory_contents(current_path)
                for item in items:
                    item_path = os.path.join(current_path, item['name'])
                    process_recursive(item_path)

        process_recursive(target_path)
        
    def to_dict(self):
        def node_to_dict(node):
            if isinstance(node, File):
                return {'type': 'file', 'name': node.name, 'content': node.content}
            elif isinstance(node, Directory):
                return {
                    'type': 'directory',
                    'name': node.name,
                    'contents': {name: node_to_dict(child) for name, child in node.contents.items()}
                }
        
        return node_to_dict(self.root)

    def cipher(self, path: str, encrypt: bool = True, recursive: bool = False, force: bool = False) -> None:
        target_path = self._normalize_path(path)
        if not self._path_exists(target_path):
            print(f"The system cannot find the path specified: {target_path}")
            return

        def encrypt_decrypt_item(item_path: str):
            # In a real system, this would encrypt or decrypt the file or directory
            # For our virtual file system, we'll just print a message
            action = "Encrypted" if encrypt else "Decrypted"
            print(f"{action} {item_path}")

        def process_recursive(current_path: str):
            encrypt_decrypt_item(current_path)
            if recursive and self._is_directory(current_path):
                items = self._get_directory_contents(current_path)
                for item in items:
                    item_path = os.path.join(current_path, item['name'])
                    process_recursive(item_path)

        if force or input(f"Are you sure you want to {'encrypt' if encrypt else 'decrypt'} {target_path}? (Y/N) ").lower() == 'y':
            process_recursive(target_path)
        else:
            print("Operation cancelled.")

    def fsutil(self, command: str, *args) -> None:
        if command == "fsinfo":
            self._fsutil_fsinfo(*args)
        elif command == "file":
            self._fsutil_file(*args)
        elif command == "volume":
            self._fsutil_volume(*args)
        elif command == "quota":
            self._fsutil_quota(*args)
        elif command == "8dot3name":
            self._fsutil_8dot3name(*args)
        else:
            print(f"Unknown fsutil command: {command}")

    def _fsutil_fsinfo(self, subcommand: str, *args) -> None:
        if subcommand == "drives":
            print("Available drives: C: D: E: F:")
        elif subcommand == "drivetype":
            drive = args[0] if args else "C:"
            print(f"{drive} - Fixed")
        elif subcommand == "volumeinfo":
            drive = args[0] if args else "C:"
            print(f"Volume information for {drive}:")
            print("Volume Name: Windows")
            print("File System: NTFS")
            print("Serial Number: 1234-5678")
        elif subcommand == "ntfsinfo":
            drive = args[0] if args else "C:"
            print(f"NTFS Volume Serial Number : 1234-5678")
            print("Version : 3.1")
            print("Number Sectors : 123456789")
            print("Total Clusters : 123456789")
            print("Free Clusters : 123456789")
            print("Total Reserved : 123456789")
            print("Bytes Per Sector : 512")
            print("Bytes Per Cluster : 4096")
            print("Bytes Per FileRecord Segment : 1024")
            print("Clusters Per FileRecord Segment : 1")
            print("Mft Valid Data Length : 123456789")
            print("Mft Start Lcn : 123456")
            print("Mft2 Start Lcn : 123456")
            print("Mft Zone Start : 123456")
            print("Mft Zone End : 123456")
        else:
            print(f"Unknown fsutil fsinfo subcommand: {subcommand}")

    def _fsutil_file(self, subcommand: str, *args) -> None:
        if subcommand == "queryallocranges":
            file_path = self._normalize_path(args[0])
            print(f"Allocation ranges for {file_path}:")
            print("0x0000000000000000 - 0x0000000000001000")
        elif subcommand == "setshortname":
            file_path = self._normalize_path(args[0])
            short_name = args[1]
            print(f"Short name for {file_path} set to {short_name}")
        elif subcommand == "setvaliddata":
            file_path = self._normalize_path(args[0])
            valid_data_length = args[1]
            print(f"Valid data length for {file_path} set to {valid_data_length}")
        elif subcommand == "setzerodata":
            file_path = self._normalize_path(args[0])
            start_offset = args[1]
            end_offset = args[2]
            print(f"Zero data set for {file_path} from {start_offset} to {end_offset}")
        else:
            print(f"Unknown fsutil file subcommand: {subcommand}")

    def _fsutil_volume(self, subcommand: str, *args) -> None:
        if subcommand == "diskfree":
            drive = args[0] if args else "C:"
            print(f"Disk free space for {drive}:")
            print("Total # of free bytes: 107374182400")
            print("Total # of bytes: 256060514304")
            print("Total # of avail free bytes: 107374182400")
        elif subcommand == "dismount":
            drive = args[0]
            print(f"Volume {drive} dismounted successfully")
        elif subcommand == "extend":
            drive = args[0]
            size = args[1]
            print(f"Volume {drive} extended by {size} bytes")
        else:
            print(f"Unknown fsutil volume subcommand: {subcommand}")

    def _fsutil_quota(self, subcommand: str, *args) -> None:
        if subcommand == "track":
            drive = args[0]
            print(f"Quota tracking {'enabled' if args[1].lower() == 'on' else 'disabled'} for {drive}")
        elif subcommand == "violations":
            drive = args[0]
            print(f"Quota violations for {drive}:")
            print("No violations found")
        elif subcommand == "modify":
            drive = args[0]
            threshold = args[1]
            limit = args[2]
            print(f"Quota modified for {drive}: Threshold = {threshold}, Limit = {limit}")
        else:
            print(f"Unknown fsutil quota subcommand: {subcommand}")

    def _fsutil_8dot3name(self, subcommand: str, *args) -> None:
        if subcommand == "query":
            drive = args[0] if args else "C:"
            print(f"8dot3 name creation is {'enabled' if random.choice([True, False]) else 'disabled'} on {drive}")
        elif subcommand == "set":
            drive = args[0]
            state = args[1]
            print(f"8dot3 name creation {'enabled' if state == '1' else 'disabled'} on {drive}")
        else:
            print(f"Unknown fsutil 8dot3name subcommand: {subcommand}")

    def subst(self, drive_letter: str, path: str = None) -> None:
        if path:
            target_path = self._normalize_path(path)
            if not self._path_exists(target_path):
                print(f"The system cannot find the path specified: {target_path}")
                return
            print(f"Virtual drive {drive_letter} created for {target_path}")
        else:
            print(f"Virtual drive {drive_letter} removed")

    def mklink(self, link_name: str, target: str, type: str = "file") -> None:
        link_path = self._normalize_path(link_name)
        target_path = self._normalize_path(target)

        if self._path_exists(link_path):
            print(f"The file already exists: {link_path}")
            return

        if not self._path_exists(target_path):
            print(f"The system cannot find the path specified: {target_path}")
            return

        if type == "file":
            print(f"Symbolic link created for {link_path} << {target_path}")
        elif type == "dir":
            print(f"Junction created for {link_path} << {target_path}")
        elif type == "hardlink":
            print(f"Hard link created for {link_path} << {target_path}")
        else:
            print(f"Invalid link type: {type}")

    def change_directory(self, path: str = "") -> None:
        print(f"Changing directory to: {path}")

        if not path:
            print(self.current_directory)
            return

        try:
            if path == "..":
                new_path = os.path.dirname(self.current_directory)
            elif path == "/" or path.lower() == "c:":
                new_path = "C:\\"
            elif os.path.isabs(path):
                new_path = self._normalize_path(path)
            else:
                new_path = self._normalize_path(os.path.join(self.current_directory, path))

            print(f"Normalized path: {new_path}")

            if self._directory_exists(new_path):
                self.current_directory = new_path
                print(f"Current directory: {self.current_directory}")
            else:
                raise FileNotFoundError(f"The system cannot find the path specified: {new_path}")
        except Exception as e:
            print(f"Error in change_directory: {str(e)}")
            print(f"The system cannot find the path specified: {path}")

    def list_directory(self, path: str = "", **options) -> None:
        try:
            target_dir = self._normalize_path(path) if path else self.current_directory
            if target_dir == '.':
                target_dir = self.current_directory
            if not self._directory_exists(target_dir):
                print(f"The system cannot find the path specified: {target_dir}")
                return

            current = self._get_directory_dict(target_dir)
            items = self._get_directory_contents(target_dir)

            # Process options
            show_hidden = 'a' in options
            bare_format = 'b' in options
            lower_case = 'l' in options
            new_long_format = 'n' in options
            sort_order = options.get('o', 'N')  # Default to Name
            pause = 'p' in options
            owner = 'q' in options
            recursive = 's' in options
            time_field = options.get('t', 'W')  # Default to Write time
            wide_format = 'w' in options
            short_names = 'x' in options

            if not show_hidden:
                items = [item for item in items if 'H' not in item.get('attributes', '')]

            # Sort items
            reverse = False
            if sort_order.startswith('-'):
                reverse = True
                sort_order = sort_order[1:]
            sort_key = {
                'N': lambda x: x['name'].lower(),
                'S': lambda x: x['size'],
                'E': lambda x: x['name'].split('.')[-1].lower(),
                'D': lambda x: x.get('created_time', datetime.now()),
                'G': lambda x: x['name'].lower(),  # Group directories first
                'C': lambda x: x.get('created_time', datetime.now()),
                'A': lambda x: x.get('last_access_time', datetime.now()),
            }.get(sort_order.upper(), lambda x: x['name'].lower())
            
            sorted_items = sorted(items, key=sort_key, reverse=reverse)
            
            if sort_order.upper() == 'G':
                directories = [item for item in sorted_items if self._is_directory(os.path.join(target_dir, item['name']))]
                files = [item for item in sorted_items if not self._is_directory(os.path.join(target_dir, item['name']))]
                sorted_items = directories + files

            if not bare_format:
                print(f" Directory of {target_dir}\n")

            if wide_format:
                for i, item in enumerate(sorted_items):
                    name = item['name']
                    if lower_case:
                        name = name.lower()
                    if short_names:
                        name = self._get_short_name(name)
                    print(f"{name:<30}", end="\n" if (i + 1) % 5 == 0 else "")
                print()
            else:
                for item in sorted_items:
                    if bare_format:
                        print(item['name'])
                    else:
                        name = item['name']
                        if lower_case:
                            name = name.lower()
                        if short_names:
                            short_name = self._get_short_name(name)
                            name = f"{short_name:<12} {name}"
                        size = item['size'] if 'size' in item else ''
                        attr = item.get('attributes', '')
                        date_time = datetime.now().strftime('%d/%m/%Y  %H:%M %p')
                        
                        if new_long_format:
                            owner_info = "OWNER" if owner else ""
                            print(f"{date_time}  {'<DIR>' if self._is_directory(os.path.join(target_dir, item['name'])) else size:>10}  {attr:<5} {owner_info:<10} {name}")
                        else:
                            print(f"{date_time}  {'<DIR>' if self._is_directory(os.path.join(target_dir, item['name'])) else size:>10}  {name}")

            if not bare_format:
                files = [item for item in sorted_items if not self._is_directory(os.path.join(target_dir, item['name']))]
                directories = [item for item in sorted_items if self._is_directory(os.path.join(target_dir, item['name']))]
                print(f"\n     {len(files)} File(s)  {sum(f['size'] for f in files if 'size' in f):>15,} bytes")
                print(f"     {len(directories)} Dir(s)  {self._get_free_space():>16,} bytes free")

            if pause:
                input("Press Enter to continue...")

            if recursive:
                for item in sorted_items:
                    if self._is_directory(os.path.join(target_dir, item['name'])):
                        print(f"\n{os.path.join(target_dir, item['name'])}")
                        self.list_directory(os.path.join(target_dir, item['name']), **options)

        except Exception as e:
            logging.error(f"Error in list_directory: {str(e)}")
            print(f"Error: {str(e)}")

    def _get_short_name(self, name: str) -> str:
        # This is a simplified version. In a real system, this would generate actual 8.3 format names
        if len(name) <= 12:
            return name
        name_parts = name.split('.')
        if len(name_parts) > 1:
            return f"{name_parts[0][:6]}~1.{name_parts[-1][:3]}"
        else:
            return f"{name[:6]}~1"

    def tree(self, path: str = "", show_files: bool = False, ascii_only: bool = False) -> None:
        target_dir = self._normalize_path(path) if path else self.current_directory
        if not self._directory_exists(target_dir):
            print(f"The system cannot find the path specified: {target_dir}")
            return

        def print_tree(directory: Dict[str, Any], prefix: str = "", is_last: bool = True) -> None:
            branch = '└── ' if is_last else '├── '
            print(prefix + (branch if not ascii_only else '+-- ') + os.path.basename(directory))
            prefix += '    ' if is_last else '│   '
            if not ascii_only:
                prefix = prefix.replace('│', '|')
            
            items = list(directory.items())
            for i, (name, item) in enumerate(items):
                if isinstance(item, dict) and 'content' not in item:
                    print_tree(item, prefix, i == len(items) - 1)
                elif show_files:
                    print(prefix + (branch if i == len(items) - 1 else '├── ') + name)

        print(f"Folder PATH listing for volume {target_dir[0]}")
        print(f"Volume serial number is {self._generate_volume_serial()}")
        print(target_dir)
        print_tree(self._get_directory_dict(target_dir))

    def clear_screen(self) -> None:
        print("\033[H\033[J", end="")

    def create_directory(self, name: str) -> None:
        try:
            new_dir = self._normalize_path(name)
            if self._path_exists(new_dir):
                raise FileExistsError(f"A subdirectory or file {name} already exists.")
            self._create_directory(new_dir)
            print(f"        1 dir(s) created.")
        except Exception as e:
            logging.error(f"Error in create_directory: {str(e)}")
            print(f"The system cannot create the directory.")

    def remove_directory(self, name: str, recursive: bool = False, quiet: bool = False) -> None:
        target_dir = self._normalize_path(name)
        if not self._directory_exists(target_dir):
            print(f"The system cannot find the path specified: {target_dir}")
            return

        try:
            if not recursive:
                if self._directory_is_empty(target_dir):
                    self._remove_directory(target_dir)
                    print(f"Directory removed: {target_dir}")
                else:
                    print(f"The directory is not empty.")
            else:
                if not quiet:
                    confirm = input(f"Are you sure you want to remove {target_dir} and all its contents? (Y/N) ")
                    if confirm.lower() != 'y':
                        print("Operation cancelled.")
                        return
                self._remove_directory_recursive(target_dir)
                print(f"Directory and its contents removed: {target_dir}")
        except Exception as e:
            logging.error(f"Error in remove_directory: {str(e)}")
            print(f"The system cannot remove the directory.")

    def copy_file(self, source: str, destination: str, verify: bool = False) -> None:
        source_path = self._normalize_path(source)
        dest_path = self._normalize_path(destination)
        
        if not self._path_exists(source_path):
            print(f"The system cannot find the file specified: {source_path}")
            return
        
        try:
            self._copy_file(source_path, dest_path)
            print(f"1 file(s) copied.")
            if verify:
                if self._verify_files(source_path, dest_path):
                    print("File successfully copied and verified.")
                else:
                    print("Warning: File copy verification failed.")
        except Exception as e:
            logging.error(f"Error in copy_file: {str(e)}")
            print(f"The system cannot copy the file.")

    def move_file(self, source: str, destination: str) -> None:
        source_path = self._normalize_path(source)
        dest_path = self._normalize_path(destination)
        
        if not self._path_exists(source_path):
            print(f"The system cannot find the file specified: {source_path}")
            return
        
        try:
            self._move_file(source_path, dest_path)
            print(f"1 file(s) moved.")
        except Exception as e:
            logging.error(f"Error in move_file: {str(e)}")
            print(f"The system cannot move the file.")

    def delete_file(self, name: str, force: bool = False, quiet: bool = False, recursive: bool = False) -> None:
        target_file = self._normalize_path(name)
        if not self._path_exists(target_file):
            print(f"The system cannot find the file specified: {target_file}")
            return

        try:
            if self._is_directory(target_file):
                if recursive:
                    self.remove_directory(target_file, recursive=True, quiet=quiet)
                else:
                    raise IsADirectoryError(f"{name} is a directory, not a file.")
            else:
                if not force and not quiet:
                    confirm = input(f"Are you sure you want to delete {target_file}? (Y/N) ")
                    if confirm.lower() != 'y':
                        print("Operation cancelled.")
                        return

                self._delete_file(target_file)
                print(f"1 file(s) deleted.")
        except Exception as e:
            logging.error(f"Error in delete_file: {str(e)}")
            print(f"The system cannot delete the file.")

    def rename(self, old_name: str, new_name: str) -> None:
        old_path = self._normalize_path(old_name)
        new_path = self._normalize_path(new_name)
        
        if not self._path_exists(old_path):
            print(f"The system cannot find the file specified: {old_path}")
            return
        
        if self._path_exists(new_path):
            print(f"A file with the name {new_name} already exists.")
            return
        
        try:
            self._rename(old_path, new_path)
            print(f"1 file(s) renamed.")
        except Exception as e:
            logging.error(f"Error in rename: {str(e)}")
            print(f"The system cannot rename the file.")

    def type_file(self, name: str) -> None:
        file_path = self._normalize_path(name)
        if not self._path_exists(file_path):
            print(f"The system cannot find the file specified: {file_path}")
            return

        try:
            content = self._get_file_content(file_path)
            print(content)
        except Exception as e:
            logging.error(f"Error in type_file: {str(e)}")
            print(f"The system cannot display the contents of the file.")

    def set_attributes(self, path: str, attributes: str) -> None:
        target_path = self._normalize_path(path)
        if not self._path_exists(target_path):
            print(f"The system cannot find the file specified: {target_path}")
            return

        try:
            current_attributes = self._get_attributes(target_path)
            new_attributes = current_attributes

            for attr in attributes:
                if attr == '+':
                    continue
                elif attr == '-':
                    continue
                elif attr.upper() in "RASH":
                    if attributes[0] == '+':
                        new_attributes += attr.upper()
                    elif attributes[0] == '-':
                        new_attributes = new_attributes.replace(attr.upper(), '')

            self._set_attributes(target_path, ''.join(sorted(set(new_attributes))))
            print(f"Attributes of {path} set to: {new_attributes}")
        except Exception as e:
            logging.error(f"Error in set_attributes: {str(e)}")
            print(f"The system cannot set the attributes.")

    # Helper methods
    def _get_free_space(self) -> int:
        return 107374182400  # 100 GB

    def _normalize_path(self, path: str) -> str:
        # Replace forward slashes with backslashes
        path = path.replace('/', '\\')
        
        # Normalize the path
        normalized = os.path.normpath(path)
        
        # Ensure the path starts with 'C:\' if it's an absolute path
        if os.path.isabs(normalized) and not normalized.startswith('C:\\'):
            normalized = 'C:' + normalized

        # Remove any double backslashes
        while '\\\\' in normalized:
            normalized = normalized.replace('\\\\', '\\')

        return normalized

    def _directory_exists(self, path: str) -> bool:
        if path.lower() == "c:\\":
            return True
        
        parts = self._split_path(path)
        current = self.file_system["C:\\"]
        
        for part in parts[1:]:  # Skip 'C:' part
            if part.lower() in [k.lower() for k in current.keys()]:
                current = current[[k for k in current.keys() if k.lower() == part.lower()][0]]
                if not isinstance(current, dict):
                    return False
            else:
                return False
        
        return True

    def _path_exists(self, path: str) -> bool:
        try:
            self._get_item_from_path(path)
            return True
        except KeyError:
            return False

    def _is_directory(self, path: str) -> bool:
        try:
            item = self._get_item_from_path(path)
            return isinstance(item, dict) and 'content' not in item
        except KeyError:
            return False

    def _split_path(self, path: str) -> List[str]:
        # Always use Windows-style splitting for the simulation
        return [p for p in path.replace('/', '\\').split('\\') if p]

    def _get_directory_contents(self, path: str) -> List[Dict[str, Any]]:
        directory = self._get_item_from_path(path)
        return [{"name": k, **v} for k, v in directory.items()]

    def _get_directory_dict(self, path: str) -> Dict[str, Any]:
       current = self.file_system["C:\\"]
       for part in path.split("\\"):
           if part and part != "C:":
               current = current[part]
       return current

    def _create_directory(self, path: str) -> None:
       parts = self._split_path(path)
       current = self.file_system[parts[0] + "\\"]
       for part in parts[1:-1]:
           current = current[part]
       current[parts[-1]] = {}

    def _remove_directory(self, path: str) -> None:
       parent_dir, dir_name = os.path.split(path)
       parent = self._get_item_from_path(parent_dir)
       del parent[dir_name]

    def _directory_is_empty(self, path: str) -> bool:
       return len(self._get_item_from_path(path)) == 0

    def _remove_directory_recursive(self, path: str) -> None:
       parent_dir, dir_name = os.path.split(path)
       parent = self._get_item_from_path(parent_dir)
       del parent[dir_name]

    def _copy_file(self, source: str, destination: str) -> None:
       content = self._get_file_content(source)
       self._create_file(destination, content)

    def _move_file(self, source: str, destination: str) -> None:
       content = self._get_file_content(source)
       self._create_file(destination, content)
       self._delete_file(source)

    def delete_file(self, name: str, force: bool = False, quiet: bool = False, recursive: bool = False) -> None:
        print(f"Debug: delete_file called with name={name}, force={force}, quiet={quiet}, recursive={recursive}")

        target_file = self._normalize_path(name)
        if not self._path_exists(target_file):
            print(f"The system cannot find the file specified: {target_file}")
            return

        try:
            if self._is_directory(target_file):
                if recursive:
                    self.remove_directory(target_file, recursive=True, quiet=quiet)
                else:
                    raise IsADirectoryError(f"{name} is a directory, not a file.")
            else:
                if not force and not quiet:
                    confirm = input(f"Are you sure you want to delete {target_file}? (Y/N) ")
                    if confirm.lower() != 'y':
                        print("Operation cancelled.")
                        return

                self._delete_file(target_file)
                print(f"1 file(s) deleted.")
        except Exception as e:
            logging.error(f"Error in delete_file: {str(e)}")
            print(f"The system cannot delete the file.")


    def _rename(self, old_path: str, new_path: str) -> None:
        content = self._get_file_content(old_path)
        self._create_file(new_path, content)
        self._delete_file(old_path)

    def _get_file_content(self, path: str) -> str:
        file = self._get_item_from_path(path)
        return file.get('content', '')

    def _create_file(self, path: str, content: str) -> None:
        parent_dir, file_name = os.path.split(path)
        parent = self._get_item_from_path(parent_dir)
        parent[file_name] = {"content": content, "size": len(content), "attributes": "A"}

    def _get_item_from_path(self, path: str) -> Dict[str, Any]:
        parts = self._split_path(path)
        current = self.file_system[parts[0] + "\\"]
        for part in parts[1:]:
            current = current[part]
        return current

    def _get_attributes(self, path: str) -> str:
        item = self._get_item_from_path(path)
        return item.get('attributes', '')

    def _set_attributes(self, path: str, attributes: str) -> None:
        item = self._get_item_from_path(path)
        item['attributes'] = attributes

    def _generate_volume_serial(self) -> str:
        return f"{random.randint(0, 9999):04d}-{random.randint(0, 9999):04d}"

    def _verify_files(self, source: str, destination: str) -> bool:
        source_content = self._get_file_content(source)
        dest_content = self._get_file_content(destination)
        return source_content == dest_content
    
    def attrib(self, filename: str, attributes: str) -> None:
        file_path = self._normalize_path(filename)
        if not self._path_exists(file_path):
            print(f"File not found - {file_path}")
            return

        current_attributes = self._get_attributes(file_path)
        new_attributes = set(current_attributes)

        for attr in attributes:
            if attr == '+':
                continue
            elif attr == '-':
                continue
            elif attr.upper() in "RASH":
                if attributes[0] == '+':
                    new_attributes.add(attr.upper())
                elif attributes[0] == '-':
                    new_attributes.discard(attr.upper())

        self._set_attributes(file_path, ''.join(sorted(new_attributes)))
        print(f"Attributes of {filename} set to: {''.join(sorted(new_attributes))}")

    def dir(self, path: str = "", attributes: str = "", order: str = "N") -> None:
        options = {
            'a': True,  # Include files with specified attributes
            'o': order  # Specify the sort order
        }
        self.list_directory(path, **options)

    def more(self, filename: str) -> None:
        file_path = self._normalize_path(filename)
        if not self._path_exists(file_path):
            print(f"File not found - {file_path}")
            return

        content = self._get_file_content(file_path)
        lines = content.split('\n')
        
        for i in range(0, len(lines), 24):
            print('\n'.join(lines[i:i+24]))
            if i + 24 < len(lines):
                input("-- More --")

    def assoc(self, file_extension: str = None) -> None:
        file_associations = {
            ".txt": "txtfile",
            ".doc": "Word.Document.8",
            ".docx": "Word.Document.12",
            ".xls": "Excel.Sheet.8",
            ".xlsx": "Excel.Sheet.12",
            ".ppt": "PowerPoint.Show.8",
            ".pptx": "PowerPoint.Show.12",
            ".pdf": "AcroExch.Document.11",
            ".jpg": "jpegfile",
            ".png": "pngfile",
            ".gif": "giffile",
            ".mp3": "mpegfile",
            ".mp4": "mp4file",
            ".avi": "avifile",
            ".zip": "CompressedFolder",
            ".rar": "RARFile",
            ".exe": "exefile",
            ".bat": "batfile",
            ".py": "Python.File",
            ".html": "htmlfile",
            ".css": "cssfile",
            ".js": "JSFile",
            ".json": "jsonfile",
            ".xml": "xmlfile"
        }

        if file_extension is None:
            for ext, assoc in file_associations.items():
                print(f"{ext}={assoc}")
        elif file_extension in file_associations:
            print(f"{file_extension}={file_associations[file_extension]}")
        else:
            print(f"File association not found for {file_extension}")

    def attrib(self, filename: str, attributes: str) -> None:
        file_path = self._normalize_path(filename)
        if not self._path_exists(file_path):
            print(f"File not found - {file_path}")
            return

        current_attributes = self._get_attributes(file_path)
        new_attributes = set(current_attributes)

        for attr in attributes:
            if attr == '+':
                continue
            elif attr == '-':
                continue
            elif attr.upper() in "RASH":
                if attributes[0] == '+':
                    new_attributes.add(attr.upper())
                elif attributes[0] == '-':
                    new_attributes.discard(attr.upper())

        self._set_attributes(file_path, ''.join(sorted(new_attributes)))
        print(f"Attributes of {filename} set to: {''.join(sorted(new_attributes))}")

    def expand(self, source: str, destination: str) -> None:
        source_path = self._normalize_path(source)
        dest_path = self._normalize_path(destination)

        if not self._path_exists(source_path):
            print(f"Source file not found - {source_path}")
            return

        content = self._get_file_content(source_path)
        expanded_content = os.path.expandvars(content)  # This is a simplification
        self._create_file(dest_path, expanded_content)
        print(f"Expanded {source} to {destination}")

    def fc(self, file1: str, file2: str, ignore_case: bool = False, ignore_blank_lines: bool = False, line_number: bool = False) -> None:
        file1_path = self._normalize_path(file1)
        file2_path = self._normalize_path(file2)

        if not self._path_exists(file1_path):
            print(f"File not found - {file1_path}")
            return
        if not self._path_exists(file2_path):
            print(f"File not found - {file2_path}")
            return

        content1 = self._get_file_content(file1_path)
        content2 = self._get_file_content(file2_path)

        lines1 = content1.splitlines()
        lines2 = content2.splitlines()

        if ignore_blank_lines:
            lines1 = [line for line in lines1 if line.strip()]
            lines2 = [line for line in lines2 if line.strip()]

        if ignore_case:
            lines1 = [line.lower() for line in lines1]
            lines2 = [line.lower() for line in lines2]

        differ = difflib.Differ()
        diff = list(differ.compare(lines1, lines2))

        if all(line.startswith('  ') for line in diff):
            print("FC: no differences encountered")
        else:
            print(f"Comparing files {file1_path} and {file2_path}")
            for i, line in enumerate(diff, 1):
                if not line.startswith('  '):
                    if line_number:
                        print(f"Line {i}: {line}")
                    else:
                        print(line)

    def find(self, search_string: str, file_path: str) -> None:
        target_path = self._normalize_path(file_path)
        if not self._path_exists(target_path):
            print(f"File not found - {target_path}")
            return

        content = self._get_file_content(target_path)
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            if search_string in line:
                print(f"[{i}]{line}")

    def format(self, drive: str, file_system: str = "NTFS", quick: bool = False) -> None:
        print(f"WARNING: ALL DATA ON NON-REMOVABLE DISK DRIVE {drive} WILL BE LOST!")
        confirm = input("Proceed with format (Y/N)? ")
        if confirm.lower() != 'y':
            print("Format cancelled.")
            return

        print(f"Formatting {drive} as {file_system}")
        if quick:
            print("Performing quick format...")
        else:
            print("Performing full format...")
        
        # Simulating format process
        for i in range(0, 101, 10):
            print(f"Format progress: {i}% complete")
            time.sleep(0.5)
        
        print(f"Format complete on {drive}")
        print("Volume label (32 characters, ENTER for none)? ", end="")
        label = input()
        if label:
            print(f"Volume label set to: {label}")

    def label(self, drive: str, new_label: str = None) -> None:
        if new_label is None:
            print(f"Volume in drive {drive} is SYSTEM")
            print(f"Volume Serial Number is {self._generate_volume_serial()}")
            return

        print(f"Volume label set to: {new_label}")

    def move(self, source: str, destination: str) -> None:
        source_path = self._normalize_path(source)
        dest_path = self._normalize_path(destination)

        if not self._path_exists(source_path):
            print(f"Source not found - {source_path}")
            return

        try:
            self._move_file(source_path, dest_path)
            print(f"1 file(s) moved.")
        except Exception as e:
            logging.error(f"Error in move: {str(e)}")
            print(f"The system cannot move the file.")

    def print_file(self, filename: str) -> None:
        file_path = self._normalize_path(filename)
        if not self._path_exists(file_path):
            print(f"File not found - {file_path}")
            return

        print(f"Printing {filename}")
        print("File sent to printer.")

    def recover(self, filename: str) -> None:
        file_path = self._normalize_path(filename)
        print(f"Attempting to recover {filename}")
        print("This command is not fully implemented in the virtual file system.")
        print("In a real system, it would attempt to recover deleted files.")

    def replace(self, source: str, destination: str) -> None:
        source_path = self._normalize_path(source)
        dest_path = self._normalize_path(destination)

        if not self._path_exists(source_path):
            print(f"Source not found - {source_path}")
            return

        if self._path_exists(dest_path):
            confirm = input(f"Replace {dest_path}? (Y/N) ")
            if confirm.lower() != 'y':
                print("Replace cancelled.")
                return

        self._copy_file(source_path, dest_path)
        print(f"Replaced {dest_path} with {source_path}")

    def sort(self, input_file: str, output_file: str = None, reverse: bool = False, remove_duplicates: bool = False) -> None:
        input_path = self._normalize_path(input_file)
        if not self._path_exists(input_path):
            print(f"Input file not found - {input_path}")
            return

        content = self._get_file_content(input_path)
        lines = content.splitlines()
        
        sorted_lines = sorted(lines, reverse=reverse)
        
        if remove_duplicates:
            sorted_lines = list(dict.fromkeys(sorted_lines))
        
        sorted_content = '\n'.join(sorted_lines)
        
        if output_file:
            output_path = self._normalize_path(output_file)
            self._create_file(output_path, sorted_content)
            print(f"Sorted content written to {output_file}")
        else:
            print(sorted_content)

    def where(self, search_pattern: str, starting_path: str = None) -> None:
        if starting_path is None:
            starting_path = self.current_directory
        else:
            starting_path = self._normalize_path(starting_path)

        if not self._directory_exists(starting_path):
            print(f"Directory not found - {starting_path}")
            return

        def search_recursive(current_path: str):
            items = self._get_directory_contents(current_path)
            for item in items:
                item_path = os.path.join(current_path, item['name'])
                if fnmatch.fnmatch(item['name'], search_pattern):
                    print(item_path)
                if self._is_directory(item_path):
                    search_recursive(item_path)

        search_recursive(starting_path)

class UserManager:
    def __init__(self):
        self.users = {
            "Administrator": {
                "password": self._hash_password("Admin123!"),
                "groups": ["Administrators"],
                "last_login": None,
                "password_last_set": datetime.now(),
                "account_locked": False,
                "failed_login_attempts": 0
            }
        }
        self.groups = {
            "Administrators": ["Administrator"],
            "Users": [],
            "Guests": ["Guest"],
            "Power Users": []
        }
        self.max_failed_attempts = 5
        self.lockout_duration = timedelta(minutes=30)

    def _hash_password(self, password):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt + key

    def _verify_password(self, stored_password, provided_password):
        salt = stored_password[:32]
        stored_key = stored_password[32:]
        new_key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
        return stored_key == new_key

    def create_user(self, username, password, groups=None):
        if username in self.users:
            raise ValueError(f"User '{username}' already exists.")
        if not groups:
            groups = ["Users"]
        self.users[username] = {
            "password": self._hash_password(password),
            "groups": groups,
            "last_login": None,
            "password_last_set": datetime.now(),
            "account_locked": False,
            "failed_login_attempts": 0
        }
        for group in groups:
            if group in self.groups:
                self.groups[group].append(username)
            else:
                self.groups[group] = [username]
        print(f"User '{username}' created successfully.")

    def delete_user(self, username):
        if username not in self.users:
            raise ValueError(f"User '{username}' does not exist.")
        del self.users[username]
        for group in self.groups.values():
            if username in group:
                group.remove(username)
        print(f"User '{username}' deleted successfully.")

    def change_password(self, username, old_password, new_password):
        if username not in self.users:
            raise ValueError(f"User '{username}' does not exist.")
        if not self._verify_password(self.users[username]["password"], old_password):
            raise ValueError("Incorrect old password.")
        self.users[username]["password"] = self._hash_password(new_password)
        self.users[username]["password_last_set"] = datetime.now()
        print(f"Password for user '{username}' changed successfully.")

    def login(self, username, password):
        if username not in self.users:
            print("Invalid username or password.")
            return False
        user = self.users[username]
        if user["account_locked"]:
            if datetime.now() - user["last_login"] > self.lockout_duration:
                user["account_locked"] = False
                user["failed_login_attempts"] = 0
            else:
                print(f"Account is locked. Please try again later or contact an administrator.")
                return False
        if self._verify_password(user["password"], password):
            user["last_login"] = datetime.now()
            user["failed_login_attempts"] = 0
            print(f"User '{username}' logged in successfully.")
            return True
        else:
            user["failed_login_attempts"] += 1
            if user["failed_login_attempts"] >= self.max_failed_attempts:
                user["account_locked"] = True
                print(f"Account locked due to too many failed attempts.")
            else:
                print("Invalid username or password.")
            return False

    def logout(self, username):
        if username not in self.users:
            raise ValueError(f"User '{username}' does not exist.")
        print(f"User '{username}' logged out successfully.")

    def add_to_group(self, username, group):
        if username not in self.users:
            raise ValueError(f"User '{username}' does not exist.")
        if group not in self.groups:
            self.groups[group] = []
        if username not in self.groups[group]:
            self.groups[group].append(username)
            self.users[username]["groups"].append(group)
            print(f"User '{username}' added to group '{group}'.")
        else:
            print(f"User '{username}' is already in group '{group}'.")

    def remove_from_group(self, username, group):
        if username not in self.users:
            raise ValueError(f"User '{username}' does not exist.")
        if group not in self.groups:
            raise ValueError(f"Group '{group}' does not exist.")
        if username in self.groups[group]:
            self.groups[group].remove(username)
            self.users[username]["groups"].remove(group)
            print(f"User '{username}' removed from group '{group}'.")
        else:
            print(f"User '{username}' is not in group '{group}'.")

    def list_users(self):
        print("Users:")
        for username, user_info in self.users.items():
            groups = ", ".join(user_info["groups"])
            last_login = user_info["last_login"].strftime("%Y-%m-%d %H:%M:%S") if user_info["last_login"] else "Never"
            print(f"  {username}: Groups: {groups}, Last Login: {last_login}")

    def list_groups(self):
        print("Groups:")
        for group, members in self.groups.items():
            print(f"  {group}: {', '.join(members)}")

    def get_user_info(self, username):
        if username not in self.users:
            raise ValueError(f"User '{username}' does not exist.")
        user_info = self.users[username]
        print(f"User Information for '{username}':")
        print(f"  Groups: {', '.join(user_info['groups'])}")
        print(f"  Last Login: {user_info['last_login']}")
        print(f"  Password Last Set: {user_info['password_last_set']}")
        print(f"  Account Locked: {user_info['account_locked']}")
        print(f"  Failed Login Attempts: {user_info['failed_login_attempts']}")

    def reset_password(self, username, new_password):
        if username not in self.users:
            raise ValueError(f"User '{username}' does not exist.")
        self.users[username]["password"] = self._hash_password(new_password)
        self.users[username]["password_last_set"] = datetime.now()
        self.users[username]["account_locked"] = False
        self.users[username]["failed_login_attempts"] = 0
        print(f"Password for user '{username}' has been reset.")

    def set_account_lockout_policy(self, max_attempts, lockout_duration_minutes):
        self.max_failed_attempts = max_attempts
        self.lockout_duration = timedelta(minutes=lockout_duration_minutes)
        print(f"Account lockout policy updated: {max_attempts} max attempts, {lockout_duration_minutes} minutes lockout duration.")
    
    def net_user(self, username=None):
        if username:
            self.get_user_info(username)
        else:
            self.list_users()

    def useradd(self, username, password, groups=None):
        # This is essentially the same as the existing create_user method
        self.create_user(username, password, groups)

    def passwd(self, username, new_password):
        if username not in self.users:
            raise ValueError(f"User '{username}' does not exist.")
        self.users[username]["password"] = self._hash_password(new_password)
        self.users[username]["password_last_set"] = datetime.now()
        print(f"Password for user '{username}' changed successfully.")

    def usermod(self, username, **kwargs):
        if username not in self.users:
            raise ValueError(f"User '{username}' does not exist.")
        user = self.users[username]
        
        if 'new_username' in kwargs:
            new_username = kwargs['new_username']
            self.users[new_username] = self.users.pop(username)
            for group in self.groups.values():
                if username in group:
                    group.remove(username)
                    group.append(new_username)
            print(f"Username changed from '{username}' to '{new_username}'.")
            username = new_username

        if 'groups' in kwargs:
            new_groups = kwargs['groups']
            old_groups = user['groups']
            for group in old_groups:
                if group not in new_groups:
                    self.groups[group].remove(username)
            for group in new_groups:
                if group not in self.groups:
                    self.groups[group] = []
                if username not in self.groups[group]:
                    self.groups[group].append(username)
            user['groups'] = new_groups
            print(f"Groups updated for user '{username}'.")

        print(f"User '{username}' modified successfully.")

    def userdel(self, username):
        # This is the same as the existing delete_user method
        self.delete_user(username)

    def groupadd(self, group_name):
        if group_name in self.groups:
            print(f"Group '{group_name}' already exists.")
        else:
            self.groups[group_name] = []
            print(f"Group '{group_name}' created successfully.")

    def groupmod(self, old_group_name, new_group_name):
        if old_group_name not in self.groups:
            raise ValueError(f"Group '{old_group_name}' does not exist.")
        if new_group_name in self.groups:
            raise ValueError(f"Group '{new_group_name}' already exists.")
        
        self.groups[new_group_name] = self.groups.pop(old_group_name)
        for user in self.users.values():
            if old_group_name in user['groups']:
                user['groups'].remove(old_group_name)
                user['groups'].append(new_group_name)
        
        print(f"Group '{old_group_name}' renamed to '{new_group_name}'.")

    def groupdel(self, group_name):
        if group_name not in self.groups:
            raise ValueError(f"Group '{group_name}' does not exist.")
        
        for user in self.users.values():
            if group_name in user['groups']:
                user['groups'].remove(group_name)
        
        del self.groups[group_name]
        print(f"Group '{group_name}' deleted successfully.")

    def id(self, username):
        if username not in self.users:
            raise ValueError(f"User '{username}' does not exist.")
        
        user = self.users[username]
        uid = hash(username) % 10000  # Generate a pseudo-UID
        gid = hash(user['groups'][0]) % 10000  # Use the first group as primary group
        
        print(f"uid={uid}({username}) gid={gid}({user['groups'][0]}) groups={','.join(user['groups'])}")

class NetworkSimulator:
    def __init__(self):
        self.interfaces = {
            "Ethernet": {
                "name": "Ethernet",
                "description": "Intel(R) I211 Gigabit Network Connection",
                "physical_address": "00-11-22-33-44-55",
                "status": "Up",
                "speed": "1.0 Gbps",
                "ip_address": "192.168.1.100",
                "subnet_mask": "255.255.255.0",
                "default_gateway": "192.168.1.1",
                "dhcp_enabled": True,
                "dhcp_server": "192.168.1.1",
                "dns_servers": ["8.8.8.8", "8.8.4.4"],
                "wins_servers": [],
                "lease_obtained": "July 10, 2024 12:00:00 PM",
                "lease_expires": "July 11, 2024 12:00:00 PM"
            },
            "Wi-Fi": {
                "name": "Wi-Fi",
                "description": "Intel(R) Wireless-AC 9560 160MHz",
                "physical_address": "AA-BB-CC-DD-EE-FF",
                "status": "Up",
                "speed": "866.7 Mbps",
                "ssid": "HomeNetwork",
                "bssid": "00:11:22:33:44:55",
                "network_type": "802.11ac",
                "radio_type": "802.11ac",
                "authentication": "WPA2-Personal",
                "cipher": "CCMP",
                "connection_mode": "Auto Connect",
                "channel": 36,
                "receive_rate": "780.0 Mbps",
                "transmit_rate": "780.0 Mbps",
                "signal": "Excellent",
                "profile": "HomeNetwork",
                "hosted_network_status": "Not available",
                "ip_address": "192.168.1.101",
                "subnet_mask": "255.255.255.0",
                "default_gateway": "192.168.1.1",
                "dhcp_enabled": True,
                "dhcp_server": "192.168.1.1",
                "dns_servers": ["8.8.8.8", "8.8.4.4"],
                "wins_servers": [],
                "lease_obtained": "July 10, 2024 12:30:00 PM",
                "lease_expires": "July 11, 2024 12:30:00 PM"
            },
            "Loopback Pseudo-Interface 1": {
                "name": "Loopback Pseudo-Interface 1",
                "description": "Software Loopback Interface 1",
                "physical_address": "",
                "status": "Up",
                "ip_address": "127.0.0.1",
                "subnet_mask": "255.0.0.0",
                "default_gateway": "",
                "dhcp_enabled": False,
                "dns_servers": [],
                "wins_servers": []
            }
        }
        self.dns_cache: Dict[str, str] = {}
        self.vlans: Dict[int, Dict[str, str]] = {
            1: {"name": "Default", "ip_range": "192.168.1.0/24"},
            10: {"name": "Management", "ip_range": "10.0.0.0/24"},
            20: {"name": "Guest", "ip_range": "172.16.0.0/24"}
        }
        self.routing_table: List[Dict[str, Any]] = [
            {"destination": "0.0.0.0", "netmask": "0.0.0.0", "gateway": "192.168.1.1", "interface": "Ethernet", "metric": 10},
            {"destination": "127.0.0.0", "netmask": "255.0.0.0", "gateway": "On-link", "interface": "Loopback Pseudo-Interface 1", "metric": 1},
            {"destination": "192.168.1.0", "netmask": "255.255.255.0", "gateway": "On-link", "interface": "Ethernet", "metric": 1},
            {"destination": "192.168.1.255", "netmask": "255.255.255.255", "gateway": "On-link", "interface": "Ethernet", "metric": 1},
            {"destination": "224.0.0.0", "netmask": "240.0.0.0", "gateway": "On-link", "interface": "Ethernet", "metric": 1},
            {"destination": "255.255.255.255", "netmask": "255.255.255.255", "gateway": "On-link", "interface": "Ethernet", "metric": 1}
        ]
        self.arp_cache: Dict[str, str] = {
            "192.168.1.1": "00-11-22-33-44-55",
            "192.168.1.2": "AA-BB-CC-DD-EE-FF",
            "192.168.1.3": "11-22-33-44-55-66"
        }
        self.network_shares: Dict[str, Dict[str, str]] = {
            "C$": {"path": "C:\\", "type": "Default share"},
            "IPC$": {"path": "", "type": "Remote IPC"},
            "ADMIN$": {"path": "C:\\Windows", "type": "Remote Admin"}
        }
        self.network_protocols: List[str] = [
            "DHCP Client",
            "DNS Client",
            "Link-Layer Topology Discovery Mapper I/O Driver",
            "Link-Layer Topology Discovery Responder",
            "NetBIOS over TCP/IP",
            "TCP/IP NetBIOS Helper",
            "Workstation"
        ]
        self.firewall_rules: List[Dict[str, Any]] = [
            {"name": "Allow HTTP", "direction": "Inbound", "protocol": "TCP", "local_port": 80, "remote_port": "Any", "action": "Allow"},
            {"name": "Allow HTTPS", "direction": "Inbound", "protocol": "TCP", "local_port": 443, "remote_port": "Any", "action": "Allow"},
            {"name": "Block Telnet", "direction": "Inbound", "protocol": "TCP", "local_port": 23, "remote_port": "Any", "action": "Block"}
        ]
        self.network_drivers: List[Dict[str, str]] = [
            {"name": "Intel(R) I211 Gigabit Network Connection", "version": "12.18.9.23", "date": "6/15/2023"},
            {"name": "Intel(R) Wireless-AC 9560 160MHz", "version": "22.10.0.7", "date": "4/22/2023"}
        ]

    def ipconfig(self, option: Optional[str] = None) -> None:
        try:
            if option is None:
                self._ipconfig_basic()
            elif option.lower() == "/all":
                self._ipconfig_all()
            elif option.lower() == "/release":
                self._ipconfig_release()
            elif option.lower() == "/renew":
                self._ipconfig_renew()
            elif option.lower() == "/flushdns":
                self._ipconfig_flushdns()
            elif option.lower() == "/registerdns":
                self._ipconfig_registerdns()
            elif option.lower() == "/displaydns":
                self._ipconfig_displaydns()
            elif option.lower() == "/showclassid":
                self._ipconfig_showclassid()
            elif option.lower() == "/setclassid":
                self._ipconfig_setclassid()
            else:
                print(f"Error: unrecognized option {option}")
                print("Valid options are:")
                print("   /all             : Display full configuration information.")
                print("   /release         : Release the IPv4 address for the specified adapter.")
                print("   /renew           : Renew the IPv4 address for the specified adapter.")
                print("   /flushdns        : Purges the DNS Resolver cache.")
                print("   /registerdns     : Refreshes all DHCP leases and re-registers DNS names.")
                print("   /displaydns      : Display the contents of the DNS Resolver Cache.")
                print("   /showclassid     : Displays all the dhcp class IDs allowed for adapter.")
                print("   /setclassid      : Modifies the dhcp class id.")
        except Exception as e:
            logging.error(f"Error in ipconfig: {str(e)}")
            print(f"Error: {str(e)}")

    def _ipconfig_all(self) -> None:
        print("\nWindows IP Configuration\n")
        print(f"   Host Name . . . . . . . . . . . . : {socket.gethostname()}")
        print(f"   Primary DNS Suffix . . . . . . . : ")
        print(f"   Node Type . . . . . . . . . . . . : Hybrid")
        print(f"   IP Routing Enabled. . . . . . . . : No")
        print(f"   WINS Proxy Enabled. . . . . . . . : No")
        print(f"   DNS Suffix Search List. . . . . . : localdomain\n")

        for interface_name, interface in self.interfaces.items():
            print(f"{interface_name}:")
            print(f"   Connection-specific DNS Suffix  . : localdomain")
            print(f"   Description . . . . . . . . . . . : {interface['description']}")
            print(f"   Physical Address. . . . . . . . . : {interface['physical_address']}")
            print(f"   DHCP Enabled. . . . . . . . . . . : {'Yes' if interface['dhcp_enabled'] else 'No'}")
            print(f"   Autoconfiguration Enabled . . . . : Yes")
            print(f"   IPv4 Address. . . . . . . . . . . : {interface['ip_address']} (Preferred)")
            print(f"   Subnet Mask . . . . . . . . . . . : {interface['subnet_mask']}")
            print(f"   Default Gateway . . . . . . . . . : {interface['default_gateway']}")
            print(f"   DHCP Server . . . . . . . . . . . : {interface['dhcp_server']}")
            print(f"   DNS Servers . . . . . . . . . . . : {' '.join(interface['dns_servers'])}")
            if interface['wins_servers']:
                print(f"   WINS Servers . . . . . . . . . . : {' '.join(interface['wins_servers'])}")
            if 'lease_obtained' in interface:
                print(f"   Lease Obtained. . . . . . . . . . : {interface['lease_obtained']}")
                print(f"   Lease Expires . . . . . . . . . . : {interface['lease_expires']}")
            print()

    def _ipconfig_basic(self) -> None:
        print("\nWindows IP Configuration\n")
        for interface_name, interface in self.interfaces.items():
            if interface['status'] == 'Up':
                print(f"{interface_name}:")
                print(f"   IPv4 Address. . . . . . . . . . . : {interface['ip_address']}")
                print(f"   Subnet Mask . . . . . . . . . . . : {interface['subnet_mask']}")
                print(f"   Default Gateway . . . . . . . . . : {interface['default_gateway']}")
                print()

    def _ipconfig_release(self) -> None:
        for interface in self.interfaces.values():
            if interface['dhcp_enabled']:
                interface['ip_address'] = "0.0.0.0"
                interface['subnet_mask'] = "0.0.0.0"
                interface['default_gateway'] = ""
                print(f"IP address released for interface {interface['name']}")
            else:
                print(f"No operation can be performed on {interface['name']} while it has its media disconnected.")

    def _ipconfig_renew(self) -> None:
        for interface in self.interfaces.values():
            if interface['dhcp_enabled']:
                interface['ip_address'] = f"192.168.1.{random.randint(100, 200)}"
                print(f"IP address renewed for interface {interface['name']}")
                print(f"New IP Address: {interface['ip_address']}")
            else:
                print(f"No operation can be performed on {interface['name']} while it has its media disconnected.")

    def _ipconfig_flushdns(self) -> None:
        self.dns_cache.clear()
        print("\nWindows IP Configuration")
        print("\nSuccessfully flushed the DNS Resolver Cache.")

    def _ipconfig_registerdns(self) -> None:
        print("\nWindows IP Configuration")
        print("\nRegistration of the DNS resource records for all adapters of this computer has been initiated.")
        time.sleep(2)
        print("Registration of the DNS resource records for all adapters of this computer has been completed.")

    def _ipconfig_displaydns(self) -> None:
        print("\nWindows IP Configuration")
        if not self.dns_cache:
            print("\nDNS Resolver Cache is empty.")
        else:
            print("\nDNS Resolver Cache:")
            for domain, ip in self.dns_cache.items():
                print(f"    {domain}")
                print(f"        Record Name . . . . . : {domain}")
                print(f"        Record Type . . . . . : 1")
                print(f"        Time To Live  . . . . : 3600")
                print(f"        Data Length . . . . . : 4")
                print(f"        Section . . . . . . . : Answer")
                print(f"        A (Host) Record . . . : {ip}")
                print()

    def _ipconfig_showclassid(self) -> None:
        for interface_name, interface in self.interfaces.items():
            print(f"{interface_name}")
            print(f"    DHCP Class ID . . . . . . . : {interface.get('dhcp_class_id', 'No DHCP Class ID configured')}")

    def _ipconfig_setclassid(self) -> None:
        print("Command not implemented in this simulation.")

    def ping(self, destination: str, options: Optional[List[str]] = None) -> None:
        try:
            if destination.lower() == "localhost" or destination == "127.0.0.1":
                self._ping_localhost()
            else:
                self._ping_remote(destination, options)
        except Exception as e:
            logging.error(f"Error in ping: {str(e)}")
            print(f"Ping request could not find host {destination}. Please check the name and try again.")

    def _ping_localhost(self) -> None:
        print(f"\nPinging {socket.gethostname()} [127.0.0.1] with 32 bytes of data:")
        for _ in range(4):
            time.sleep(0.1)  # Simulate network delay
            print("Reply from 127.0.0.1: bytes=32 time<1ms TTL=128")
        print(f"\nPing statistics for 127.0.0.1:")
        print("    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),")
        print("Approximate round trip times in milli-seconds:")
        print("    Minimum = 0ms, Maximum = 0ms, Average = 0ms")

    def _ping_remote(self, destination: str, options: Optional[List[str]] = None) -> None:
        packet_size = 32
        count = 4
        timeout = 4000  # in milliseconds

        if options:
            for i, option in enumerate(options):
                if option.lower() == "-n" and i + 1 < len(options):
                    count = int(options[i + 1])
                elif option.lower() == "-l" and i + 1 < len(options):
                    packet_size = int(options[i + 1])
                elif option.lower() == "-w" and i + 1 < len(options):
                    timeout = int(options[i + 1])

        print(f"\nPinging {destination} with {packet_size} bytes of data:")
        
        successful_pings = 0
        total_time = 0
        min_time = float('inf')
        max_time = 0

        for _ in range(count):
            time.sleep(0.5)  # Simulate network delay
            latency = random.randint(1, 100)
            total_time += latency
            min_time = min(min_time, latency)
            max_time = max(max_time, latency)
            
            if latency < timeout:
                print(f"Reply from {destination}: bytes={packet_size} time={latency}ms TTL=64")
                successful_pings += 1
            else:
                print(f"Request timed out.")

        loss_percentage = ((count - successful_pings) / count) * 100
        avg_time = total_time / count if successful_pings > 0 else 0

        print(f"\nPing statistics for {destination}:")
        print(f"    Packets: Sent = {count}, Received = {successful_pings}, Lost = {count - successful_pings} ({loss_percentage:.0f}% loss),")
        if successful_pings > 0:
            print("Approximate round trip times in milli-seconds:")
            print(f"    Minimum = {min_time}ms, Maximum = {max_time}ms, Average = {avg_time:.0f}ms")

    def tracert(self, destination: str) -> None:
        try:
            print(f"\nTracing route to {destination} over a maximum of 30 hops:\n")
            for i in range(1, random.randint(5, 15)):
                ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
                times = [random.randint(1, 20) for _ in range(3)]
                print(f"  {i}    {times[0]} ms    {times[1]} ms    {times[2]} ms    {ip}")
                time.sleep(0.5)  # Simulate network delay
            print(f"  {i+1}    {random.randint(1, 20)} ms    {random.randint(1, 20)} ms    {random.randint(1, 20)} ms    {destination}")
            print("\nTrace complete.")
        except Exception as e:
            logging.error(f"Error in tracert: {str(e)}")
            print(f"Unable to resolve target system name {destination}.")

    def nslookup(self, domain: str) -> None:
        try:
            print(f"Server:  UnKnown")
            print(f"Address:  {self.interfaces['Ethernet']['dns_servers'][0]}\n")
            print(f"Non-authoritative answer:")
            print(f"Name:    {domain}")
            ip = socket.gethostbyname(domain)
            print(f"Address:  {ip}")
            self.dns_cache[domain] = ip  # Add to DNS cache
        except socket.gaierror:
            print(f"*** UnKnown can't find {domain}: Non-existent domain")
        except Exception as e:
            logging.error(f"Error in nslookup: {str(e)}")
            print(f"*** UnKnown can't find {domain}: Server failed")

    def netstat(self, options: Optional[List[str]] = None) -> None:
        try:
            show_all = "-a" in options if options else False
            show_numeric = "-n" in options if options else False
            
            if "-h" in options or "--help" in options:
                print("Displays protocol statistics and current TCP/IP network connections.\n")
                print("NETSTAT [-a] [-n] [-p proto] [-r] [-s] [interval]\n")
                print("  -a            Displays all connections and listening ports.")
                print("  -n            Displays addresses and port numbers in numerical form.")
                print("  -p proto      Shows connections for the protocol specified by proto.")
                print("  -r            Displays the routing table.")
                print("  -s            Displays per-protocol statistics.")
                print("  interval      Redisplays selected statistics every interval seconds.")
                return

            print("Active Connections\n")
            print("  Proto  Local Address          Foreign Address        State")
            
            states = ["ESTABLISHED", "TIME_WAIT", "CLOSE_WAIT"] if show_all else ["ESTABLISHED"]
            for _ in range(random.randint(5, 15)):
                proto = random.choice(["TCP", "UDP"])
                local = f"{self.interfaces['Ethernet']['ip_address']}:{random.randint(1024, 65535)}"
                foreign = f"{'.'.join([str(random.randint(1, 255)) for _ in range(4)])}:{random.randint(1, 65535)}"
                state = random.choice(states) if proto == "TCP" else ""
                
                if show_numeric:
                    print(f"  {proto.ljust(6)} {local.ljust(22)} {foreign.ljust(22)} {state}")
                else:
                    local_name = f"localhost:{local.split(':')[1]}"
                    foreign_name = f"{self._generate_domain()}:{foreign.split(':')[1]}"
                    print(f"  {proto.ljust(6)} {local_name.ljust(22)} {foreign_name.ljust(22)} {state}")
        except Exception as e:
            logging.error(f"Error in netstat: {str(e)}")
            print(f"Error: {str(e)}")

    def _generate_domain(self) -> str:
        domains = ["example.com", "test.org", "demo.net", "sample.edu"]
        return random.choice(domains)

    def route(self, command: str, *args: Any) -> None:
        try:
            if command.lower() == "print":
                self._route_print()
            elif command.lower() == "add":
                self._route_add(*args)
            elif command.lower() == "delete":
                self._route_delete(*args)
            else:
                print(f"The route {command} command is not supported.")
                print("Usage: route [COMMAND [DESTINATION] [MASK] [GATEWAY] [METRIC]]")
                print("  print         - Prints the entire routing table")
                print("  add           - Adds a route")
                print("  delete        - Deletes a route")
        except Exception as e:
            logging.error(f"Error in route: {str(e)}")
            print(f"Error: {str(e)}")

    def _route_print(self) -> None:
        print("===========================================================================")
        print("Interface List")
        print("0x1 ........................... Microsoft Kernel Debug Network Adapter")
        print("0x2 ...00 11 22 33 44 55 ...... Intel(R) I211 Gigabit Network Connection")
        print("0x3 ...AA BB CC DD EE FF ...... Intel(R) Wireless-AC 9560 160MHz")
        print("===========================================================================")
        print("IPv4 Route Table")
        print("===========================================================================")
        print("Active Routes:")
        print("Network Destination        Netmask          Gateway       Interface  Metric")
        for route in self.routing_table:
            print(f"{route['destination'].ljust(25)} {route['netmask'].ljust(16)} {route['gateway'].ljust(15)} {route['interface'].ljust(11)} {route['metric']}")
        print("===========================================================================")

    def _route_add(self, *args: Any) -> None:
        if len(args) < 4:
            print("Usage: route ADD <destination> MASK <subnet_mask> <gateway> [METRIC <metric>] [IF <interface>]")
            return
        
        destination = args[0]
        netmask = args[2]
        gateway = args[3]
        metric = 1
        interface = "Ethernet"

        for i in range(4, len(args), 2):
            if args[i].upper() == "METRIC":
                metric = int(args[i+1])
            elif args[i].upper() == "IF":
                interface = args[i+1]

        new_route = {
            "destination": destination,
            "netmask": netmask,
            "gateway": gateway,
            "interface": interface,
            "metric": metric
        }
        self.routing_table.append(new_route)
        print(f"OK!")

    def _route_delete(self, *args: Any) -> None:
        if len(args) < 1:
            print("Usage: route DELETE <destination>")
            return
        
        destination = args[0]
        initial_length = len(self.routing_table)
        self.routing_table = [route for route in self.routing_table if route['destination'] != destination]
        
        if len(self.routing_table) < initial_length:
            print(f"OK!")
        else:
            print(f"The route deletion failed: The specified route was not found.")

    def arp(self, option: Optional[str] = None, *args: Any) -> None:
        try:
            if option is None or option.lower() == "-a":
                self._arp_display_cache()
            elif option.lower() == "-d":
                self._arp_delete_entry(*args)
            elif option.lower() == "-s":
                self._arp_add_entry(*args)
            else:
                print("Invalid ARP option. Usage:")
                print("  arp -a                             Displays current ARP entries")
                print("  arp -d <ip_address>                Deletes an ARP entry")
                print("  arp -s <ip_address> <mac_address>  Adds a static ARP entry")
        except Exception as e:
            logging.error(f"Error in arp: {str(e)}")
            print(f"Error: {str(e)}")

    def _arp_display_cache(self) -> None:
        print("Interface: 192.168.1.100 --- 0x2")
        print("  Internet Address      Physical Address      Type")
        for ip, mac in self.arp_cache.items():
            print(f"  {ip.ljust(20)} {mac.ljust(20)} {'dynamic' if random.choice([True, False]) else 'static'}")

    def _arp_delete_entry(self, *args: Any) -> None:
        if not args:
            print("Error: IP address must be specified.")
            return
        ip = args[0]
        if ip in self.arp_cache:
            del self.arp_cache[ip]
            print(f"ARP entry for {ip} has been deleted.")
        else:
            print(f"No ARP entry found for {ip}.")

    def _arp_add_entry(self, *args: Any) -> None:
        if len(args) < 2:
            print("Error: Both IP address and MAC address must be specified.")
            return
        ip, mac = args[0], args[1]
        self.arp_cache[ip] = mac
        print(f"ARP entry for {ip} has been added.")

    def netsh(self, *args: str) -> None:
        try:
            if len(args) == 0:
                print("The following commands are available:\n")
                print("Commands in this context:")
                print("?              - Displays a list of commands.")
                print("add            - Adds a configuration entry to a list of entries.")
                print("advfirewall    - Changes to the `netsh advfirewall' context.")
                print("bridge         - Changes to the `netsh bridge' context.")
                print("delete         - Deletes a configuration entry from a list of entries.")
                print("dump           - Displays a configuration script.")
                print("exec           - Runs a script file.")
                print("firewall       - Changes to the `netsh firewall' context.")
                print("help           - Displays a list of commands.")
                print("http           - Changes to the `netsh http' context.")
                print("interface      - Changes to the `netsh interface' context.")
                print("ipsec          - Changes to the `netsh ipsec' context.")
                print("lan            - Changes to the `netsh lan' context.")
                print("namespace      - Changes to the `netsh namespace' context.")
                print("netio          - Changes to the `netsh netio' context.")
                print("p2p            - Changes to the `netsh p2p' context.")
                print("ras            - Changes to the `netsh ras' context.")
                print("rpc            - Changes to the `netsh rpc' context.")
                print("set            - Updates configuration settings.")
                print("show           - Displays information.")
                print("trace          - Changes to the `netsh trace' context.")
                print("wfp            - Changes to the `netsh wfp' context.")
                print("winhttp        - Changes to the `netsh winhttp' context.")
                print("winsock        - Changes to the `netsh winsock' context.")
                return

            if args[0] == "wlan" and args[1] == "show" and args[2] == "profiles":
                self._netsh_wlan_show_profiles()
            elif args[0] == "interface" and args[1] == "show" and args[2] == "interface":
                self._netsh_interface_show_interface()
            elif args[0] == "advfirewall" and args[1] == "show" and args[2] == "currentprofile":
                self._netsh_advfirewall_show_currentprofile()
            else:
                print(f"The following command was not found: {' '.join(args)}")
        except Exception as e:
            logging.error(f"Error in netsh: {str(e)}")
            print(f"Error: {str(e)}")

    def _netsh_wlan_show_profiles(self) -> None:
        print("Profiles on interface Wi-Fi:")
        print("Group policy profiles (read only)")
        print("---------------------------------")
        print("    <None>")
        print("\nUser profiles")
        print("-------------")
        print("    All User Profile     : HomeNetwork")
        print("    All User Profile     : CoffeeShopWiFi")
        print("    All User Profile     : WorkNetwork")

    def _netsh_interface_show_interface(self) -> None:
        print("Admin State    State          Type             Interface Name")
        print("-------------------------------------------------------------------------")
        for interface in self.interfaces.values():
            admin_state = "Enabled" if interface['status'] == "Up" else "Disabled"
            state = interface['status']
            interface_type = "Dedicated" if interface['name'] != "Loopback Pseudo-Interface 1" else "Loopback"
            print(f"{admin_state.ljust(14)} {state.ljust(14)} {interface_type.ljust(16)} {interface['name']}")

    def _netsh_advfirewall_show_currentprofile(self) -> None:
        print("Public Profile Settings:")
        print("----------------------------------------------------------------------")
        print("State                                 ON")
        print("Firewall Policy                       BlockInbound,AllowOutbound")
        print("LocalFirewallRules                    N/A (GPO-store only)")
        print("LocalConSecRules                      N/A (GPO-store only)")
        print("InboundUserNotification               Enable")
        print("RemoteManagement                      Disable")
        print("UnicastResponseToMulticast            Enable")
        print("Logging:")
        print("LogAllowedConnections                 Disable")
        print("LogDroppedConnections                 Enable")
        print("FileName %systemroot%\\system32\\LogFiles\\Firewall\\pfirewall.log")
        print("MaxFileSize                           4096")

    def pathping(self, destination: str) -> None:
        try:
            print(f"\nTracing route to {destination} over a maximum of 30 hops:\n")
            for i in range(1, random.randint(5, 15)):
                ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
                times = [random.randint(1, 20) for _ in range(3)]
                print(f"{i}  {ip}")
                time.sleep(0.5)  # Simulate network delay
            print(f"{i+1}  {destination}\n")
            
            print(f"Computing statistics for 175 seconds...")
            time.sleep(2)  # Simulate computation time
            print(f"            Source to Here   This Node/Link")
            print(f"Hop  RTT    Lost/Sent = Pct  Lost/Sent = Pct  Address")
            print(f"  0                                           {self.interfaces['Ethernet']['ip_address']}")
            
            for i in range(1, i+2):
                rtt = random.randint(1, 100)
                lost = random.randint(0, 10)
                sent = 100
                pct_lost = (lost / sent) * 100
                print(f"{i:>3}  {rtt:>4}ms  {lost:>3}/{sent} = {pct_lost:>3}%   {lost:>3}/{sent} = {pct_lost:>3}%  {ip if i != i+1 else destination}")

            print("\nTrace complete.")
        except Exception as e:
            logging.error(f"Error in pathping: {str(e)}")
            print(f"Unable to resolve target system name {destination}.")

    def telnet(self, host: str, port: int) -> None:
        try:
            print(f"\nConnecting To {host}...")
            time.sleep(2)  # Simulate connection time
            
            if random.random() < 0.2:  # 20% chance of connection failure
                print(f"Could not open connection to the host, on port {port}: Connect failed")
                return
            
            print(f"Escape character is '^]'.")
            print("\nWelcome to the simulated Telnet session.")
            print("Press Ctrl+C to exit.")
            
            while True:
                try:
                    command = input("> ")
                    if command.lower() in ['exit', 'quit']:
                        print("Connection to host lost.")
                        break
                    print(f"Command '{command}' not recognized in this simulation.")
                except KeyboardInterrupt:
                    print("\nConnection closed by foreign host.")
                    break
        except Exception as e:
            logging.error(f"Error in telnet: {str(e)}")
            print(f"Error: {str(e)}")

    def nbtstat(self, option: Optional[str] = None) -> None:
        try:
            if option is None:
                print("Displays protocol statistics and current TCP/IP connections using NBT")
                print("(NetBIOS over TCP/IP).\n")
                print("NBTSTAT [ [-a RemoteName] [-A IP address] [-c] [-n] [-r] [-R] [-RR] [-s] [-S] [interval] ]")
                return
            
            if option.lower() == "-a":
                print("NetBIOS Remote Machine Name Table\n")
                print("Name               Type         Status")
                print("---------------------------------------------")
                print("DESKTOP-PC      <00>  UNIQUE      Registered")
                print("WORKGROUP       <00>  GROUP       Registered")
                print("DESKTOP-PC      <20>  UNIQUE      Registered")
            elif option.lower() == "-c":
                print("NetBIOS Remote Cache Name Table\n")
                print("Name               Type       Host Address    Life [sec]")
                print("----------------------------------------------------")
                print("FILESERVER      <20>  UNIQUE  192.168.1.100     360")
            else:
                print(f"Invalid option: {option}")
        except Exception as e:
            logging.error(f"Error in nbtstat: {str(e)}")
            print(f"Error: {str(e)}")

    def getmac(self, option: Optional[str] = None) -> None:
        try:
            if option == "/?":
                print("Displays the MAC address for network adapters on this machine.\n")
                print("GETMAC [/S system [/U username [/P [password]]]] [/FO format] [/NH] [/V]")
                return
            
            print("Physical Address    Transport Name")
            print("=================== ==========================================================")
            for interface in self.interfaces.values():
                if interface['physical_address']:
                    print(f"{interface['physical_address']}   \\Device\\Tcpip_{{{random.randint(10000, 99999)}}}")
        except Exception as e:
            logging.error(f"Error in getmac: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_wlan_show_all(self) -> None:
        try:
            print("Interface name : Wi-Fi")
            print("    There are 3 networks currently visible.")
            print("\nSSID 1 : HomeNetwork")
            print("    Network type            : Infrastructure")
            print("    Authentication          : WPA2-Personal")
            print("    Encryption              : CCMP")
            print("    BSSID 1                 : 00:11:22:33:44:55")
            print("         Signal             : 90%")
            print("         Radio type         : 802.11ac")
            print("         Channel            : 36")
            print("         Basic rates (Mbps) : 6 12 24")
            print("         Other rates (Mbps) : 9 18 36 48 54")
            print("\nSSID 2 : CoffeeShopWiFi")
            print("    Network type            : Infrastructure")
            print("    Authentication          : Open")
            print("    Encryption              : None")
            print("    BSSID 1                 : AA:BB:CC:DD:EE:FF")
            print("         Signal             : 60%")
            print("         Radio type         : 802.11n")
            print("         Channel            : 1")
            print("         Basic rates (Mbps) : 1 2 5.5 11")
            print("         Other rates (Mbps) : 6 9 12 18 24 36 48 54")
            print("\nSSID 3 : NeighborNetwork")
            print("    Network type            : Infrastructure")
            print("    Authentication          : WPA2-Personal")
            print("    Encryption              : CCMP")
            print("    BSSID 1                 : 11:22:33:44:55:66")
            print("         Signal             : 40%")
            print("         Radio type         : 802.11n")
            print("         Channel            : 11")
            print("         Basic rates (Mbps) : 1 2 5.5 11")
            print("         Other rates (Mbps) : 6 9 12 18 24 36 48 54")
        except Exception as e:
            logging.error(f"Error in netsh_wlan_show_all: {str(e)}")
            print(f"Error: {str(e)}")

    def ipv6_config(self) -> None:
        try:
            print("Windows IP Configuration\n")
            print("Ethernet adapter Ethernet:")
            print("   Connection-specific DNS Suffix  . : localdomain")
            print("   IPv6 Address. . . . . . . . . . . : 2001:0db8:85a3:0000:0000:8a2e:0370:7334")
            print("   Link-local IPv6 Address . . . . . : fe80::5efe:192.168.1.100%10")
            print("   Default Gateway . . . . . . . . . : fe80::1%10")
            print("\nWireless LAN adapter Wi-Fi:")
            print("   Connection-specific DNS Suffix  . : ")
            print("   IPv6 Address. . . . . . . . . . . : 2001:0db8:85a3:0000:0000:8a2e:0370:7335")
            print("   Temporary IPv6 Address. . . . . . : 2001:0db8:85a3:0000:0000:8a2e:0370:7336")
            print("   Link-local IPv6 Address . . . . . : fe80::5efe:192.168.1.101%12")
            print("   Default Gateway . . . . . . . . . : fe80::1%12")
        except Exception as e:
            logging.error(f"Error in ipv6_config: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_interface_ipv4_show_addresses(self) -> None:
        try:
            for interface in self.interfaces.values():
                print(f"\nConfiguration for interface \"{interface['name']}\"")
                print("    DHCP enabled:                         Yes")
                print(f"    IP Address:                            {interface['ip_address']}")
                print(f"    Subnet Prefix:                         {interface['subnet_mask']} (mask {interface['subnet_mask']})")
                print(f"    Default Gateway:                       {interface['default_gateway']}")
                print(f"    Gateway Metric:                        0")
                print("    InterfaceMetric:                      25")
        except Exception as e:
            logging.error(f"Error in netsh_interface_ipv4_show_addresses: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_interface_ipv4_show_subinterfaces(self) -> None:
        try:
            print("   MTU  MediaSenseState   Bytes In  Bytes Out  Interface")
            for interface in self.interfaces.values():
                mtu = 1500
                media_sense_state = "Connected"
                bytes_in = random.randint(1000000, 10000000)
                bytes_out = random.randint(1000000, 10000000)
                print(f"{mtu:5d} {media_sense_state:17} {bytes_in:9d} {bytes_out:10d}  {interface['name']}")
        except Exception as e:
            logging.error(f"Error in netsh_interface_ipv4_show_subinterfaces: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_wlan_show_drivers(self) -> None:
        try:
            print("Interface name: Wi-Fi")
            print("\nDriver                    : Intel(R) Wireless-AC 9560 160MHz")
            print("Vendor                    : Intel Corporation")
            print("Provider                  : Intel")
            print("Date                      : 4/22/2023")
            print("Version                   : 22.10.0.7")
            print("INF file                  : oem35.inf")
            print("Type                      : Native Wi-Fi Driver")
            print("Radio types supported     : 802.11b 802.11g 802.11n 802.11a 802.11ac")
            print("FIPS 140-2 mode supported : Yes")
            print("802.11w Management Frame Protection supported : Yes")
            print("Hosted network supported  : Yes")
            print("Authentication and cipher supported in infrastructure mode:")
            print("    Open            None")
            print("    WPA2-Personal   CCMP")
            print("    WPA2-Enterprise CCMP")
        except Exception as e:
            logging.error(f"Error in netsh_wlan_show_drivers: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_advfirewall_show_allprofiles(self) -> None:
        try:
            profiles = ["Domain Profile", "Private Profile", "Public Profile"]
            for profile in profiles:
                print(f"{profile} Settings:")
                print("----------------------------------------------------------------------")
                print("State                                 ON")
                print("Firewall Policy                       BlockInbound,AllowOutbound")
                print("LocalFirewallRules                    N/A (GPO-store only)")
                print("LocalConSecRules                      N/A (GPO-store only)")
                print("InboundUserNotification               Enable")
                print("RemoteManagement                      Disable")
                print("UnicastResponseToMulticast            Enable")
                print("\nLogging:")
                print("LogAllowedConnections                 Disable")
                print("LogDroppedConnections                 Enable")
                print(r"FileName %systemroot%\system32\LogFiles\Firewall\pfirewall.log")
                print("MaxFileSize                           4096")
                print("\n")
        except Exception as e:
            logging.error(f"Error in netsh_advfirewall_show_allprofiles: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_http_show_urlacl(self) -> None:
        try:
            print("Reserved URL            : http://+:80/Temporary_Listen_Addresses/")
            print(" User: NT AUTHORITY\\LOCAL SERVICE")
            print("        Listen: Yes")
            print("        Delegate: No")
            print("        SDDL: D:(A;;GX;;;LS)")
            print("\nReserved URL            : https://+:443/Temporary_Listen_Addresses/")
            print(" User: NT AUTHORITY\\LOCAL SERVICE")
            print("        Listen: Yes")
            print("        Delegate: No")
            print("        SDDL: D:(A;;GX;;;LS)")
        except Exception as e:
            logging.error(f"Error in netsh_http_show_urlacl: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_wlan_show_hostednetwork(self) -> None:
        try:
            print("Hosted network settings")
            print("-----------------------")
            print("    Mode                   : Allowed")
            print("    SSID name              : \"MyHostedNetwork\"")
            print("    Max number of clients  : 100")
            print("    Authentication         : WPA2-Personal")
            print("    Cipher                 : CCMP")
            print("\nHosted network status")
            print("---------------------")
            print("    Status                 : Not started")
        except Exception as e:
            logging.error(f"Error in netsh_wlan_show_hostednetwork: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_winhttp_show_proxy(self) -> None:
        try:
            print("Current WinHTTP proxy settings:")
            print("    Direct access (no proxy server).")
        except Exception as e:
            logging.error(f"Error in netsh_winhttp_show_proxy: {str(e)}")
            print(f"Error: {str(e)}")

    def show_network_connections(self) -> None:
        try:
            print("Network Connections:")
            print("====================")
            for interface in self.interfaces.values():
                status = "Connected" if interface['status'] == "Up" else "Disconnected"
                print(f"{interface['name']}:")
                print(f"    Status: {status}")
                print(f"    IP Address: {interface['ip_address']}")
                print(f"    Subnet Mask: {interface['subnet_mask']}")
                print(f"    Default Gateway: {interface['default_gateway']}")
                print()
        except Exception as e:
            logging.error(f"Error in show_network_connections: {str(e)}")
            print(f"Error: {str(e)}")

    def show_network_protocols(self) -> None:
        try:
            print("Enabled Network Protocols:")
            print("==========================")
            for protocol in self.network_protocols:
                print(f"- {protocol}")
        except Exception as e:
            logging.error(f"Error in show_network_protocols: {str(e)}")
            print(f"Error: {str(e)}")

    def show_network_shares(self) -> None:
        try:
            print("Network Shares:")
            print("===============")
            for share_name, share_info in self.network_shares.items():
                print(f"Share Name: {share_name}")
                print(f"    Path: {share_info['path']}")
                print(f"    Type: {share_info['type']}")
                print()
        except Exception as e:
            logging.error(f"Error in show_network_shares: {str(e)}")
            print(f"Error: {str(e)}")

    def show_firewall_rules(self) -> None:
        try:
            print("Firewall Rules:")
            print("===============")
            for rule in self.firewall_rules:
                print(f"Rule Name: {rule['name']}")
                print(f"    Direction: {rule['direction']}")
                print(f"    Protocol: {rule['protocol']}")
                print(f"    Local Port: {rule['local_port']}")
                print(f"    Remote Port: {rule['remote_port']}")
                print(f"    Action: {rule['action']}")
                print()
        except Exception as e:
            logging.error(f"Error in show_firewall_rules: {str(e)}")
            print(f"Error: {str(e)}")

    def show_network_drivers(self) -> None:
        try:
            print("Network Drivers:")
            print("================")
            for driver in self.network_drivers:
                print(f"Driver Name: {driver['name']}")
                print(f"    Version: {driver['version']}")
                print(f"    Date: {driver['date']}")
                print()
        except Exception as e:
            logging.error(f"Error in show_network_drivers: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_winhttp_reset_proxy(self) -> None:
        try:
            print("Current WinHTTP proxy settings:")
            print("    Direct access (no proxy server).")
            print("\nResetting the winhttp proxy")
            print("\nCurrent WinHTTP proxy settings:")
            print("    Direct access (no proxy server).")
        except Exception as e:
            logging.error(f"Error in netsh_winhttp_reset_proxy: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_interface_ipv4_set_address(self, interface: str, static: bool, ip: str, subnet: str, gateway: str) -> None:
        try:
            if interface not in self.interfaces:
                print(f"The following command was not found: interface ipv4 set address name={interface}")
                return

            if static:
                self.interfaces[interface]['ip_address'] = ip
                self.interfaces[interface]['subnet_mask'] = subnet
                self.interfaces[interface]['default_gateway'] = gateway
                self.interfaces[interface]['dhcp_enabled'] = False
                print(f"IP address successfully set on interface {interface}.")
            else:
                self.interfaces[interface]['dhcp_enabled'] = True
                print(f"DHCP successfully enabled on interface {interface}.")
        except Exception as e:
            logging.error(f"Error in netsh_interface_ipv4_set_address: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_interface_ipv4_set_dns(self, interface: str, static: bool, dns: str) -> None:
        try:
            if interface not in self.interfaces:
                print(f"The following command was not found: interface ipv4 set dns name={interface}")
                return

            if static:
                self.interfaces[interface]['dns_servers'] = [dns]
                print(f"DNS server address successfully set on interface {interface}.")
            else:
                self.interfaces[interface]['dns_servers'] = []
                print(f"DNS server addresses successfully removed from interface {interface}.")
        except Exception as e:
            logging.error(f"Error in netsh_interface_ipv4_set_dns: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_advfirewall_set_allprofiles_state(self, state: str) -> None:
        try:
            if state.lower() not in ['on', 'off']:
                print("Invalid state. Use 'on' or 'off'.")
                return

            print(f"Ok.")
            print(f"\nFirewall state successfully set to {state}.")
        except Exception as e:
            logging.error(f"Error in netsh_advfirewall_set_allprofiles_state: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_advfirewall_firewall_add_rule(self, name: str, dir: str, action: str, program: str) -> None:
        try:
            new_rule = {
                "name": name,
                "direction": dir,
                "action": action,
                "program": program,
                "protocol": "Any",
                "local_port": "Any",
                "remote_port": "Any"
            }
            self.firewall_rules.append(new_rule)
            print(f"Ok.")
            print(f"\nRule {name} successfully added.")
        except Exception as e:
            logging.error(f"Error in netsh_advfirewall_firewall_add_rule: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_advfirewall_firewall_delete_rule(self, name: str) -> None:
        try:
            initial_length = len(self.firewall_rules)
            self.firewall_rules = [rule for rule in self.firewall_rules if rule['name'] != name]
            if len(self.firewall_rules) < initial_length:
                print(f"Deleted {initial_length - len(self.firewall_rules)} rule(s).")
                print("Ok.")
            else:
                print(f"No rules matched the specified criteria.")
        except Exception as e:
            logging.error(f"Error in netsh_advfirewall_firewall_delete_rule: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_wlan_connect(self, ssid: str) -> None:
        try:
            print(f"Connection request was completed successfully.")
            print(f"Connection to {ssid} is in progress...")
            time.sleep(2)
            print(f"Successfully connected to {ssid}.")
        except Exception as e:
            logging.error(f"Error in netsh_wlan_connect: {str(e)}")
            print(f"Error: {str(e)}")

    def netsh_wlan_disconnect(self) -> None:
        try:
            print("Disconnection request was completed successfully.")
            time.sleep(1)
            print("Successfully disconnected from the wireless network.")
        except Exception as e:
            logging.error(f"Error in netsh_wlan_disconnect: {str(e)}")
            print(f"Error: {str(e)}")

    def net_use(self, command: str, drive: str, path: str, user: Optional[str] = None, password: Optional[str] = None) -> None:
        try:
            if command.lower() == "add":
                print(f"The command completed successfully.")
                print(f"Drive {drive} is now connected to {path}")
            elif command.lower() == "delete":
                print(f"Drive {drive} was successfully deleted.")
            else:
                print(f"System error 85 has occurred.")
                print(f"The local device name is already in use.")
        except Exception as e:
            logging.error(f"Error in net_use: {str(e)}")
            print(f"Error: {str(e)}")

    def net_share(self, command: str, name: str, path: Optional[str] = None) -> None:
        try:
            if command.lower() == "add":
                self.network_shares[name] = {"path": path, "type": "File Share"}
                print(f"{name} was shared successfully.")
            elif command.lower() == "delete":
                if name in self.network_shares:
                    del self.network_shares[name]
                    print(f"{name} was deleted successfully.")
                else:
                    print(f"Share name {name} does not exist.")
            else:
                print(f"The syntax of this command is:")
                print(f"NET SHARE sharename=drive:path [/GRANT:user,[READ|CHANGE|FULL]]")
                print(f"                [/USERS:number | /UNLIMITED]")
                print(f"                [/REMARK:\"text\"]")
                print(f"                [/CACHE:Manual | Documents | Programs | BranchCache | None]")
        except Exception as e:
            logging.error(f"Error in net_share: {str(e)}")
            print(f"Error: {str(e)}")

    def net_view(self) -> None:
        try:
            print("Server Name            Remark")
            print("--------------------------------------------")
            print("\\\\DESKTOP-PC          John's Computer")
            print("\\\\LAPTOP-USER         Sarah's Laptop")
            print("\\\\FILE-SERVER         Main File Server")
            print("\nThe command completed successfully.")
        except Exception as e:
            logging.error(f"Error in net_view: {str(e)}")
            print(f"Error: {str(e)}")

    def net_start(self, service: str) -> None:
        try:
            print(f"The {service} service is starting.")
            time.sleep(2)
            print(f"The {service} service was started successfully.")
        except Exception as e:
            logging.error(f"Error in net_start: {str(e)}")
            print(f"Error: {str(e)}")

    def net_stop(self, service: str) -> None:
        try:
            print(f"The {service} service is stopping.")
            time.sleep(2)
            print(f"The {service} service was stopped successfully.")
        except Exception as e:
            logging.error(f"Error in net_stop: {str(e)}")
            print(f"Error: {str(e)}")

    def systeminfo(self) -> None:
        try:
            print("Host Name:                 DESKTOP-PC")
            print("OS Name:                   Microsoft Windows 10 Pro")
            print("OS Version:                10.0.19042 N/A Build 19042")
            print("OS Manufacturer:           Microsoft Corporation")
            print("OS Configuration:          Member Workstation")
            print("OS Build Type:             Multiprocessor Free")
            print("Registered Owner:          Windows User")
            print("Registered Organization:   N/A")
            print("Product ID:                00000-00000-00000-AA000")
            print("Original Install Date:     7/10/2023, 9:00:00 AM")
            print("System Boot Time:          7/11/2024, 8:30:15 AM")
            print("System Manufacturer:       Dell Inc.")
            print("System Model:              Latitude 5510")
            print("System Type:               x64-based PC")
            print("Processor(s):              1 Processor(s) Installed.")
            print("                           [01]: Intel64 Family 6 Model 142 Stepping 12 GenuineIntel ~2300 Mhz")
            print("BIOS Version:              Dell Inc. 1.5.3, 2/15/2023")
            print("Windows Directory:         C:\\WINDOWS")
            print("System Directory:          C:\\WINDOWS\\system32")
            print("Boot Device:               \\Device\\HarddiskVolume1")
            print("System Locale:             en-us;English (United States)")
            print("Input Locale:              en-us;English (United States)")
            print("Time Zone:                 (UTC-08:00) Pacific Time (US & Canada)")
            print("Total Physical Memory:     16,384 MB")
            print("Available Physical Memory: 8,192 MB")
            print("Virtual Memory: Max Size:  18,432 MB")
            print("Virtual Memory: Available: 7,168 MB")
            print("Virtual Memory: In Use:    11,264 MB")
            print("Page File Location(s):     C:\\pagefile.sys")
            print("Domain:                    WORKGROUP")
            print("Logon Server:              \\\\DESKTOP-PC")
            print("Hotfix(s):                 10 Hotfix(s) Installed.")
            print("Network Card(s):           2 NIC(s) Installed.")
            print("                           [01]: Intel(R) Wi-Fi 6 AX201 160MHz")
            print("                                 Connection Name: Wi-Fi")
            print("                                 DHCP Enabled:    Yes")
            print("                                 DHCP Server:     192.168.1.1")
            print("                                 IP address(es)")
            print("                                 [01]: 192.168.1.100")
            print("                                 [02]: fe80::5efe:192.168.1.100")
            print("                           [02]: Intel(R) I211 Gigabit Network Connection")
            print("                                 Connection Name: Ethernet")
            print("                                 Status:          Media disconnected")
            print("Hyper-V Requirements:      VM Monitor Mode Extensions: Yes")
            print("                           Virtualization Enabled In Firmware: Yes")
            print("                           Second Level Address Translation: Yes")
            print("                           Data Execution Prevention Available: Yes")
        except Exception as e:
            logging.error(f"Error in systeminfo: {str(e)}")
            print(f"Error: {str(e)}")
            
    
    def ssh(self, host: str, user: str):
        try:
            print(f"Connecting to {host}...")
            time.sleep(1)
            print(f"{user}@{host}'s password: ")
            time.sleep(1)
            print(f"Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-77-generic x86_64)")
            while True:
                command = input(f"{user}@{host}:~$ ")
                if command.lower() == 'exit':
                    print("Connection to {host} closed.")
                    break
                else:
                    print(f"Command '{command}' not implemented in this simulation")
        except Exception as e:
            logging.error(f"Error in ssh: {str(e)}")
            print(f"Error: {str(e)}")

    def nmap(self, target: str):
        try:
            print(f"Starting Nmap 7.91 ( https://nmap.org ) at {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}")
            print(f"Nmap scan report for {target}")
            print("Host is up (0.0098s latency).")
            print("Not shown: 998 closed ports")
            print("PORT   STATE SERVICE")
            print("22/tcp open  ssh")
            print("80/tcp open  http")
            print(f"Nmap done: 1 IP address (1 host up) scanned in 0.03 seconds")
        except Exception as e:
            logging.error(f"Error in nmap: {str(e)}")
            print(f"Error: {str(e)}")

    def curl(self, url: str):
        try:
            print(f"  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current")
            print(f"                                 Dload  Upload   Total   Spent    Left  Speed")
            print(f"100  1256  100  1256    0     0  62800      0 --:--:-- --:--:-- --:--:-- 62800")
            print(f"<!DOCTYPE html>")
            print(f"<html>")
            print(f"<head>")
            print(f"    <title>Example Domain</title>")
            print(f"</head>")
            print(f"<body>")
            print(f"    <h1>Example Domain</h1>")
            print(f"    <p>This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.</p>")
            print(f"</body>")
            print(f"</html>")
        except Exception as e:
            logging.error(f"Error in curl: {str(e)}")
            print(f"Error: {str(e)}")

    def wget(self, url: str):
        try:
            print(f"--2024-07-12 10:15:30--  {url}")
            print(f"Resolving {url.split('//')[1].split('/')[0]}... 93.184.216.34, 2606:2800:220:1:248:1893:25c8:1946")
            print(f"Connecting to {url.split('//')[1].split('/')[0]}|93.184.216.34|:80... connected.")
            print(f"HTTP request sent, awaiting response... 200 OK")
            print(f"Length: 1256 (1.2K) [text/html]")
            print(f"Saving to: 'index.html'")
            print(f"")
            print(f"index.html          100%[===================>]   1.23K  --.-KB/s    in 0s      ")
            print(f"")
            print(f"2024-07-12 10:15:30 (23.4 MB/s) - 'index.html' saved [1256/1256]")
        except Exception as e:
            logging.error(f"Error in wget: {str(e)}")
            print(f"Error: {str(e)}")

    def tcpdump(self, interface: str):
        try:
            print(f"tcpdump: verbose output suppressed, use -v[v]... for full protocol decode")
            print(f"listening on {interface}, link-type EN10MB (Ethernet), snapshot length 262144 bytes")
            for _ in range(10):
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                src_ip = f"192.168.1.{random.randint(1, 255)}"
                dst_ip = f"192.168.1.{random.randint(1, 255)}"
                src_port = random.randint(1024, 65535)
                dst_port = random.choice([80, 443, 22, 21])
                print(f"{timestamp} IP {src_ip}.{src_port} > {dst_ip}.{dst_port}: Flags [S], seq 1505345020, win 29200, options [mss 1460,sackOK,TS val 3371504820 ecr 0,nop,wscale 7], length 0")
                time.sleep(0.5)
            print(f"10 packets captured")
            print(f"10 packets received by filter")
            print(f"0 packets dropped by kernel")
        except Exception as e:
            logging.error(f"Error in tcpdump: {str(e)}")
            print(f"Error: {str(e)}")

    def wireshark(self):
        print("Wireshark is a GUI application and cannot be simulated in a command-line environment.")
        print("Please use the actual Wireshark application for packet analysis.")

    def netdom(self, command: str, *args):
        try:
            if command.lower() == "query":
                print(f"Querying domain information...")
                print(f"Domain: WORKGROUP")
                print(f"Domain Controller: N/A (Workgroup environment)")
            elif command.lower() == "join":
                print(f"Joining domain {args[0]}...")
                print(f"The command completed successfully.")
            else:
                print(f"Command '{command}' not implemented in this simulation")
        except Exception as e:
            logging.error(f"Error in netdom: {str(e)}")
            print(f"Error: {str(e)}")

    def nltest(self, command: str):
        try:
            if command.lower() == "/dclist":
                print(f"Get list of DCs in domain 'WORKGROUP' from '\\\\DESKTOP-PC'")
                print(f"    DESKTOP-PC (PDC)")
                print(f"The command completed successfully")
            elif command.lower() == "/dsgetdc":
                print(f"DC: \\\\DESKTOP-PC")
                print(f"Address: \\\\192.168.1.100")
                print(f"Dom Guid: 00000000-0000-0000-0000-000000000000")
                print(f"Dom Name: WORKGROUP")
                print(f"Forest Name: WORKGROUP")
                print(f"Dc Site Name: Default-First-Site-Name")
                print(f"Our Site Name: Default-First-Site-Name")
                print(f"Flags: PDC GC DS LDAP KDC TIMESERV WRITABLE DNS_FOREST CLOSE_SITE FULL_SECRET WS")
                print(f"The command completed successfully")
            else:
                print(f"Command '{command}' not implemented in this simulation")
        except Exception as e:
            logging.error(f"Error in nltest: {str(e)}")
            print(f"Error: {str(e)}")

    def ipmonitor(self):
        try:
            print(f"IP Monitor started. Press Ctrl+C to stop.")
            while True:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                interface = random.choice(list(self.interfaces.keys()))
                old_ip = self.interfaces[interface]['ip_address']
                new_ip = f"192.168.1.{random.randint(100, 200)}"
                print(f"[{timestamp}] IP address changed on {interface}: {old_ip} -> {new_ip}")
                self.interfaces[interface]['ip_address'] = new_ip
                time.sleep(5)
        except KeyboardInterrupt:
            print("\nIP Monitor stopped.")
        except Exception as e:
            logging.error(f"Error in ipmonitor: {str(e)}")
            print(f"Error: {str(e)}")

    def netdiag(self):
        try:
            print(f"Checking computer name resolution...")
            print(f"Computer name resolves correctly.")
            print(f"\nChecking WINS resolution...")
            print(f"WINS resolution is functioning correctly.")
            print(f"\nChecking default gateway...")
            print(f"Default gateway is reachable.")
            print(f"\nChecking NetBIOS name resolution...")
            print(f"NetBIOS name resolution is functioning correctly.")
            print(f"\nChecking network card configuration...")
            print(f"Network cards are configured correctly.")
            print(f"\nChecking for IP address conflicts...")
            print(f"No IP address conflicts detected.")
            print(f"\nNetwork diagnostic completed successfully.")
        except Exception as e:
            logging.error(f"Error in netdiag: {str(e)}")
            print(f"Error: {str(e)}")

    def tcpview(self):
        try:
            print(f"TCPView v4.35 - Copyright (C) 1998-2020 Mark Russinovich")
            print(f"Sysinternals - www.sysinternals.com")
            print(f"\nProto Local Address           Foreign Address         State        PID  Process")
            for _ in range(10):
                proto = random.choice(["TCP", "UDP"])
                local = f"192.168.1.{random.randint(1, 255)}:{random.randint(1024, 65535)}"
                foreign = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}:{random.randint(1, 65535)}"
                state = "ESTABLISHED" if proto == "TCP" else ""
                pid = random.randint(1000, 9999)
                process = random.choice(["chrome.exe", "firefox.exe", "svchost.exe", "explorer.exe"])
                print(f"{proto:<5} {local:<23} {foreign:<23} {state:<12} {pid:<5} {process}")
            print(f"\nPress Ctrl+C to exit.")
            input()
        except KeyboardInterrupt:
            print("\nTCPView stopped.")
        except Exception as e:
            logging.error(f"Error in tcpview: {str(e)}")
            print(f"Error: {str(e)}")

    def portqry(self, target: str, port: int):
        try:
            print(f"Querying target system called:")
            print(f" {target}")
            print(f"\nQuerying the {port} port on the target system\n")
            if random.choice([True, False]):
                print(f"TCP port {port} (unknown service): LISTENING")
            else:
                print(f"TCP port {port} (unknown service): NOT LISTENING")
        except Exception as e:
            logging.error(f"Error in portqry: {str(e)}")
            print(f"Error: {str(e)}")

    def netscan(self):
        try:
            print(f"Starting network scan...")
            print(f"\nIP Address       MAC Address        Hostname")
            print(f"-----------------------------------------------")
            for i in range(1, 11):
                ip = f"192.168.1.{random.randint(1, 255)}"
                mac = ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])
                hostname = f"Device-{random.choice(['PC', 'Laptop', 'Phone', 'Printer'])}-{i}"
                print(f"{ip:<16} {mac:<19} {hostname}")
            print(f"\nNetwork scan completed.")
        except Exception as e:
            logging.error(f"Error in netscan: {str(e)}")
            print(f"Error: {str(e)}")
            
    def ftp(self, host: str, user: str, password: str):
        try:
            print(f"Connecting to {host}...")
            time.sleep(1)
            print("220 FTP server ready")
            print(f"User ({host}:{user}): {user}")
            print("331 Password required for {user}")
            print("Password:")
            time.sleep(1)
            print("230 User {user} logged in")
            print("Remote system type is UNIX")
            print("Using binary mode to transfer files")
            while True:
                command = input("ftp> ")
                if command.lower() in ['quit', 'exit', 'bye']:
                    print("221 Goodbye")
                    break
                else:
                    print(f"Command '{command}' not implemented in this simulation")
        except Exception as e:
            logging.error(f"Error in ftp: {str(e)}")
            print(f"Error: {str(e)}")
                
class HardwareSimulator:
    def __init__(self):
        self.cpu = self._generate_cpu()
        self.ram = self._generate_ram()
        self.storage = self._generate_storage()
        self.gpu = self._generate_gpu()
        self.motherboard = self._generate_motherboard()
        self.network_adapters = self._generate_network_adapters()
        self.sound_card = self._generate_sound_card()
        self.power_supply = self._generate_power_supply()

    def _generate_cpu(self) -> Dict[str, Any]:
        cpu_brands = ["Intel", "AMD"]
        cpu_models = {
            "Intel": ["Core i3", "Core i5", "Core i7", "Core i9"],
            "AMD": ["Ryzen 3", "Ryzen 5", "Ryzen 7", "Ryzen 9"]
        }
        brand = random.choice(cpu_brands)
        model = random.choice(cpu_models[brand])
        cores = random.choice([2, 4, 6, 8, 12, 16])
        threads = cores * 2
        base_clock = round(random.uniform(2.0, 3.5), 1)
        boost_clock = round(base_clock + random.uniform(0.5, 1.5), 1)
        cache = random.choice([4, 8, 12, 16, 24, 32])

        return {
            "brand": brand,
            "model": f"{model}-{random.randint(1000, 9999)}",
            "cores": cores,
            "threads": threads,
            "base_clock": base_clock,
            "boost_clock": boost_clock,
            "cache": cache,
            "temperature": round(random.uniform(30, 70), 1)
        }

    def _generate_ram(self) -> Dict[str, Any]:
        total_capacity = random.choice([4, 8, 16, 32, 64, 128])
        speed = random.choice([2133, 2400, 2666, 3000, 3200, 3600])
        modules = random.choice([1, 2, 4])
        capacity_per_module = total_capacity // modules

        return {
            "total_capacity": total_capacity,
            "speed": speed,
            "modules": modules,
            "capacity_per_module": capacity_per_module,
            "type": "DDR4" if speed >= 2133 else "DDR3",
            "manufacturer": random.choice(["Corsair", "G.Skill", "Kingston", "Crucial"])
        }

    def _generate_storage(self) -> List[Dict[str, Any]]:
        storage_devices = []
        types = ["SSD", "HDD"]
        capacities = [128, 256, 512, 1024, 2048, 4096]
        
        for _ in range(random.randint(1, 3)):
            device_type = random.choice(types)
            capacity = random.choice(capacities)
            
            if device_type == "SSD":
                interface = random.choice(["SATA", "NVMe"])
                read_speed = random.randint(300, 3500)
                write_speed = random.randint(200, 3000)
            else:
                interface = "SATA"
                read_speed = random.randint(80, 160)
                write_speed = random.randint(70, 150)

            storage_devices.append({
                "type": device_type,
                "capacity": capacity,
                "interface": interface,
                "manufacturer": random.choice(["Western Digital", "Seagate", "Samsung", "Crucial"]),
                "model": f"{device_type}-{capacity}GB-{random.randint(1000, 9999)}",
                "read_speed": read_speed,
                "write_speed": write_speed
            })

        return storage_devices

    def _generate_gpu(self) -> Dict[str, Any]:
        gpu_brands = ["NVIDIA", "AMD"]
        gpu_models = {
            "NVIDIA": ["GeForce GTX", "GeForce RTX"],
            "AMD": ["Radeon RX"]
        }
        brand = random.choice(gpu_brands)
        model = random.choice(gpu_models[brand])
        vram = random.choice([2, 4, 6, 8, 11, 16, 24])

        return {
            "brand": brand,
            "model": f"{model} {random.randint(1000, 9999)}",
            "vram": vram,
            "memory_type": "GDDR6",
            "manufacturer": random.choice(["ASUS", "MSI", "Gigabyte", "EVGA"]),
            "core_clock": round(random.uniform(1.0, 2.0), 2),
            "boost_clock": round(random.uniform(1.5, 2.5), 2),
            "temperature": round(random.uniform(30, 80), 1)
        }

    def _generate_motherboard(self) -> Dict[str, Any]:
        manufacturers = ["ASUS", "MSI", "Gigabyte", "ASRock"]
        chipsets = ["B450", "X570", "Z490", "B550"]
        form_factors = ["ATX", "Micro-ATX", "Mini-ITX"]

        return {
            "manufacturer": random.choice(manufacturers),
            "model": f"{random.choice(chipsets)}-{random.randint(1000, 9999)}",
            "chipset": random.choice(chipsets),
            "form_factor": random.choice(form_factors),
            "max_ram": random.choice([32, 64, 128, 256]),
            "ram_slots": random.choice([2, 4]),
            "pcie_slots": random.randint(1, 4)
        }

    def _generate_network_adapters(self) -> List[Dict[str, Any]]:
        adapters = []
        for _ in range(random.randint(1, 2)):
            adapter_type = random.choice(["Ethernet", "Wi-Fi"])
            if adapter_type == "Ethernet":
                speed = random.choice([100, 1000, 2500, 10000])
                adapters.append({
                    "type": adapter_type,
                    "speed": speed,
                    "manufacturer": random.choice(["Realtek", "Intel", "Broadcom"]),
                    "model": f"ETH-{speed}-{random.randint(1000, 9999)}",
                    "mac_address": ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])
                })
            else:
                adapters.append({
                    "type": adapter_type,
                    "standard": random.choice(["802.11n", "802.11ac", "802.11ax"]),
                    "manufacturer": random.choice(["Intel", "Broadcom", "Qualcomm"]),
                    "model": f"WIFI-{random.randint(1000, 9999)}",
                    "mac_address": ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])
                })
        return adapters

    def _generate_sound_card(self) -> Dict[str, Any]:
        return {
            "manufacturer": random.choice(["Realtek", "Creative", "ASUS"]),
            "model": f"Audio-{random.randint(1000, 9999)}",
            "channels": random.choice([2, 5.1, 7.1]),
            "interface": random.choice(["Integrated", "PCIe"])
        }

    def _generate_power_supply(self) -> Dict[str, Any]:
        return {
            "manufacturer": random.choice(["Corsair", "EVGA", "Seasonic"]),
            "model": f"PSU-{random.randint(1000, 9999)}",
            "wattage": random.choice([450, 550, 650, 750, 850, 1000]),
            "efficiency": random.choice(["80+ Bronze", "80+ Silver", "80+ Gold", "80+ Platinum"])
        }

    def get_system_info(self) -> None:
        print("System Hardware Information:")
        print(f"CPU: {self.cpu['brand']} {self.cpu['model']}")
        print(f"RAM: {self.ram['total_capacity']}GB {self.ram['type']} @ {self.ram['speed']}MHz")
        print(f"GPU: {self.gpu['brand']} {self.gpu['model']}")
        print(f"Motherboard: {self.motherboard['manufacturer']} {self.motherboard['model']}")
        print(f"Storage Devices: {len(self.storage)}")
        print(f"Network Adapters: {len(self.network_adapters)}")
        print(f"Sound Card: {self.sound_card['manufacturer']} {self.sound_card['model']}")
        print(f"Power Supply: {self.power_supply['manufacturer']} {self.power_supply['model']} {self.power_supply['wattage']}W")

    def get_cpu_info(self) -> None:
        print("CPU Information:")
        for key, value in self.cpu.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    def get_ram_info(self) -> None:
        print("RAM Information:")
        for key, value in self.ram.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    def get_storage_info(self) -> None:
        print("Storage Information:")
        for i, device in enumerate(self.storage, 1):
            print(f"Device {i}:")
            for key, value in device.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
            print()

    def get_gpu_info(self) -> None:
        print("GPU Information:")
        for key, value in self.gpu.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    def get_motherboard_info(self) -> None:
        print("Motherboard Information:")
        for key, value in self.motherboard.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    def get_network_info(self) -> None:
        print("Network Adapter Information:")
        for i, adapter in enumerate(self.network_adapters, 1):
            print(f"Adapter {i}:")
            for key, value in adapter.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
            print()

    def get_sound_card_info(self) -> None:
        print("Sound Card Information:")
        for key, value in self.sound_card.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    def get_power_supply_info(self) -> None:
        print("Power Supply Information:")
        for key, value in self.power_supply.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    def update_cpu_temperature(self) -> None:
        self.cpu['temperature'] = round(random.uniform(30, 70), 1)

    def update_gpu_temperature(self) -> None:
        self.gpu['temperature'] = round(random.uniform(30, 80), 1)
            
class SystemInfo:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.os_name = platform.system() + " " + platform.release()
        self.os_version = platform.version()
        self.system_manufacturer = self._get_system_manufacturer()
        self.system_model = self._get_system_model()
        self.system_type = platform.machine()
        self.processor = platform.processor()
        self.bios_version = self._get_bios_version()
        self.total_physical_memory = psutil.virtual_memory().total
        self.available_physical_memory = psutil.virtual_memory().available
        self.virtual_memory_max_size = psutil.swap_memory().total
        self.virtual_memory_available = psutil.swap_memory().free
        self.virtual_memory_in_use = psutil.swap_memory().used
        self.network_adapter = self._get_network_adapter()
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
        self.disk_drive = self._get_disk_info()
        self.disk_size = psutil.disk_usage('/').total
        self.free_space = psutil.disk_usage('/').free
        self.gpu = self._get_gpu_info()
        self.gpu_memory = self._get_gpu_memory()

    def _get_system_manufacturer(self):
        try:
            return subprocess.check_output("wmic csproduct get vendor", shell=True).decode().split('\n')[1].strip()
        except:
            return "Unknown"

    def _get_system_model(self):
        try:
            return subprocess.check_output("wmic csproduct get name", shell=True).decode().split('\n')[1].strip()
        except:
            return "Unknown"

    def _get_bios_version(self):
        try:
            return subprocess.check_output("wmic bios get smbiosbiosversion", shell=True).decode().split('\n')[1].strip()
        except:
            return "Unknown"

    def _get_network_adapter(self):
        try:
            return psutil.net_if_addrs()[psutil.net_if_stats().keys()[0]][0].address
        except:
            return "Unknown"

    def _get_disk_info(self):
        try:
            return subprocess.check_output("wmic diskdrive get model", shell=True).decode().split('\n')[1].strip()
        except:
            return "Unknown"

    def _get_gpu_info(self):
        try:
            return subprocess.check_output("wmic path win32_VideoController get name", shell=True).decode().split('\n')[1].strip()
        except:
            return "Unknown"

    def _get_gpu_memory(self):
        try:
            return subprocess.check_output("wmic path win32_VideoController get adapterram", shell=True).decode().split('\n')[1].strip()
        except:
            return "Unknown"

    def systeminfo(self) -> None:
        try:
            print(f"Host Name:                 {self.hostname}")
            print(f"OS Name:                   {self.os_name}")
            print(f"OS Version:                {self.os_version}")
            print(f"OS Manufacturer:           Microsoft Corporation")
            print(f"OS Configuration:          Member Workstation")
            print(f"OS Build Type:             Multiprocessor Free")
            print(f"Registered Owner:          {getpass.getuser()}")
            print(f"Registered Organization:   ")
            print(f"Product ID:                00000-00000-00000-AA000")
            print(f"Original Install Date:     {datetime.fromtimestamp(psutil.boot_time()).strftime('%d/%m/%Y, %I:%M:%S %p')}")
            print(f"System Boot Time:          {datetime.now().strftime('%d/%m/%Y, %I:%M:%S %p')}")
            print(f"System Manufacturer:       {self.system_manufacturer}")
            print(f"System Model:              {self.system_model}")
            print(f"System Type:               {self.system_type}")
            print(f"Processor(s):              1 Processor(s) Installed.")
            print(f"                           [{self.processor}]")
            print(f"BIOS Version:              {self.bios_version}")
            print(f"Windows Directory:         C:\\Windows")
            print(f"System Directory:          C:\\Windows\\system32")
            print(f"Boot Device:               \\Device\\HarddiskVolume1")
            print(f"System Locale:             {locale.getdefaultlocale()[0]}")
            print(f"Input Locale:              {locale.getdefaultlocale()[0]}")
            print(f"Time Zone:                 {time.tzname[0]}")
            print(f"Total Physical Memory:     {self.total_physical_memory / (1024**3):.2f} GB")
            print(f"Available Physical Memory: {self.available_physical_memory / (1024**3):.2f} GB")
            print(f"Virtual Memory: Max Size:  {self.virtual_memory_max_size / (1024**3):.2f} GB")
            print(f"Virtual Memory: Available: {self.virtual_memory_available / (1024**3):.2f} GB")
            print(f"Virtual Memory: In Use:    {self.virtual_memory_in_use / (1024**3):.2f} GB")
            print(f"Network Adapter:           {self.network_adapter}")
            print(f"IP Address:                {self.ip_address}")
            print(f"MAC Address:               {self.mac_address}")
            print(f"Disk Drive:                {self.disk_drive}")
            print(f"Disk Size:                 {self.disk_size / (1024**3):.2f} GB")
            print(f"Free Space:                {self.free_space / (1024**3):.2f} GB")
            print(f"Graphics Card:             {self.gpu}")
            print(f"GPU Memory:                {int(self.gpu_memory) / (1024**3):.2f} GB")
        except Exception as e:
            logging.error(f"Error in systeminfo: {str(e)}")
            print(f"Error: {str(e)}")

    def msinfo32(self) -> None:
       try:
           print("System Information report:")
           print(f"OS Name: {self.os_name}")
           print(f"Version: {self.os_version}")
           print(f"System Manufacturer: {self.system_manufacturer}")
           print(f"System Model: {self.system_model}")
           print(f"System Type: {self.system_type}")
           print(f"Processor: {self.processor}")
           print(f"BIOS Version: {self.bios_version}")
           print("Windows Directory: C:\\Windows")
           print("System Directory: C:\\Windows\\system32")
           print("Boot Device: \\Device\\HarddiskVolume1")
           print(f"System Locale: {locale.getdefaultlocale()[0]}")
           print(f"Input Locale: {locale.getdefaultlocale()[0]}")
           print(f"Time Zone: {time.tzname[0]}")
           print(f"Total Physical Memory: {self.total_physical_memory / (1024**3):.2f} GB")
           print(f"Available Physical Memory: {self.available_physical_memory / (1024**3):.2f} GB")
           print(f"Virtual Memory: Max Size: {self.virtual_memory_max_size / (1024**3):.2f} GB")
           print(f"Virtual Memory: Available: {self.virtual_memory_available / (1024**3):.2f} GB")
           print(f"Virtual Memory: In Use: {self.virtual_memory_in_use / (1024**3):.2f} GB")
       except Exception as e:
           logging.error(f"Error in msinfo32: {str(e)}")
           print(f"Error: {str(e)}")

    def dxdiag(self) -> None:
       try:
           print("------------------")
           print("DxDiag Notes")
           print("------------------")
           print("Display Tab 1: No problems found.")
           print("Sound Tab 1: No problems found.")
           print("Input Tab: No problems found.")
           print("--------------------")
           print("DirectX Debug Levels")
           print("--------------------")
           print("Direct3D:    0/4 (retail)")
           print("DirectDraw:  0/4 (retail)")
           print("DirectInput: 0/5 (retail)")
           print("DirectMusic: 0/5 (retail)")
           print("DirectPlay:  0/9 (retail)")
           print("DirectSound: 0/5 (retail)")
           print("DirectShow:  0/6 (retail)")
           print("---------------")
           print("Display Devices")
           print("---------------")
           print(f"Card name: {self.gpu}")
           print(f"Manufacturer: {self.gpu.split()[0]}")
           print(f"Chip type: {self.gpu}")
           print("DAC type: Integrated RAMDAC")
           print("Device Type: Full Device (POST)")
           print(f"Display Memory: {int(self.gpu_memory) / (1024**3):.2f} GB")
           print(f"Dedicated Memory: {int(self.gpu_memory) / (1024**3):.2f} GB")
           print("Shared Memory: 0 MB")
           print("Current Mode: 1920 x 1080 (32 bit) (60Hz)")
       except Exception as e:
           logging.error(f"Error in dxdiag: {str(e)}")
           print(f"Error: {str(e)}")

    def msconfig(self) -> None:
       try:
           print("System Configuration")
           print("1. General")
           print("2. Boot")
           print("3. Services")
           print("4. Startup")
           print("5. Tools")
           choice = input("Enter a number to view details (or 'q' to quit): ")
           if choice == '1':
               self._msconfig_general()
           elif choice == '2':
               self._msconfig_boot()
           elif choice == '3':
               self._msconfig_services()
           elif choice == '4':
               self._msconfig_startup()
           elif choice == '5':
               self._msconfig_tools()
           elif choice.lower() == 'q':
               return
           else:
               print("Invalid choice.")
       except Exception as e:
           logging.error(f"Error in msconfig: {str(e)}")
           print(f"Error: {str(e)}")

    def _msconfig_general(self) -> None:
       print("General settings:")
       print("- Normal startup")
       print("- Load system services: Enabled")
       print("- Load startup items: Enabled")

    def _msconfig_boot(self) -> None:
       print("Boot options:")
       print(f"- Default OS: {self.os_name}")
       print("- Timeout: 30 seconds")

    def _msconfig_services(self) -> None:
       print("Services:")
       print("- Hide all Microsoft services: [ ]")
       print("- Enable all")

    def _msconfig_startup(self) -> None:
       print("Startup items:")
       startup_items = psutil.Popen(['wmic', 'startup', 'get', 'caption,command'], stdout=psutil.PIPE).communicate()[0]
       for line in startup_items.decode().split('\n')[1:]:
           if line.strip():
               print(f"- {line.strip()}")

    def _msconfig_tools(self) -> None:
       print("Tools:")
       print("- System Information")
       print("- Registry Editor")
       print("- Command Prompt")

    def winver(self) -> None:
        try:
            print(f"Microsoft {self.os_name}")
            print(f"Version {self.os_version}")
            print("© Microsoft Corporation. All rights reserved.")
        except Exception as e:
            logging.error(f"Error in winver: {str(e)}")
            print(f"Error: {str(e)}")

    def ver(self) -> None:
        try:
            print(f"Microsoft {self.os_name} [Version {self.os_version}]")
        except Exception as e:
            logging.error(f"Error in ver: {str(e)}")
            print(f"Error: {str(e)}")

    def gpresult(self) -> None:
        try:
            print("Microsoft (R) Windows (R) Operating System Group Policy Result tool v2.0")
            print(f"© Microsoft Corporation. All rights reserved.\n")
            print(f"Created on {datetime.now().strftime('%d/%m/%Y')} at {datetime.now().strftime('%I:%M:%S %p')}\n")
            print("RSOP data for NT AUTHORITY\\SYSTEM on {self.hostname} : Logging Mode")
            print("------------------------------------------------------------\n")
            print("OS Configuration:            Member Workstation")
            print(f"OS Version:                  {self.os_version}")
            print(f"Site Name:                   N/A")
            print(f"Roaming Profile:             N/A")
            print(f"Local Profile:               C:\\Users\\{getpass.getuser()}")
            print("Last time Group Policy was applied: {datetime.now().strftime('%d/%m/%Y')} at {datetime.now().strftime('%I:%M:%S %p')}")
            print("Group Policy was applied from:      N/A")
            print("Group Policy slow link threshold:   500 kbps")
            print("Domain Name:                        WORKGROUP")
            print(f"Domain Type:                        Workstation")
        except Exception as e:
            logging.error(f"Error in gpresult: {str(e)}")
            print(f"Error: {str(e)}")

    def whoami(self) -> None:
        try:
            print(f"{socket.gethostname()}\\{getpass.getuser()}")
        except Exception as e:
            logging.error(f"Error in whoami: {str(e)}")
            print(f"Error: {str(e)}")

    def hostname(self) -> None:
        try:
            print(self.hostname)
        except Exception as e:
            logging.error(f"Error in hostname: {str(e)}")
            print(f"Error: {str(e)}")

    def sysinfo(self) -> None:
        try:
            print("Detailed System Information:")
            print(f"Hostname: {self.hostname}")
            print(f"OS: {self.os_name} {self.os_version}")
            print(f"Kernel: {platform.release()}")
            print(f"Architecture: {platform.machine()}")
            print(f"CPU: {self.processor}")
            print(f"CPU Cores: {psutil.cpu_count(logical=False)}")
            print(f"CPU Threads: {psutil.cpu_count(logical=True)}")
            print(f"RAM: {psutil.virtual_memory().total / (1024**3):.2f} GB")
            print(f"Swap: {psutil.swap_memory().total / (1024**3):.2f} GB")
            print(f"Disk: {self.disk_drive}")
            print(f"Disk Size: {self.disk_size / (1024**3):.2f} GB")
            print(f"Free Space: {self.free_space / (1024**3):.2f} GB")
            print(f"GPU: {self.gpu}")
            print(f"GPU Memory: {int(self.gpu_memory) / (1024**3):.2f} GB")
            print(f"Network Adapter: {self.network_adapter}")
            print(f"IP Address: {self.ip_address}")
            print(f"MAC Address: {self.mac_address}")
            print(f"BIOS Version: {self.bios_version}")
            print(f"Boot Time: {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Current User: {getpass.getuser()}")
        except Exception as e:
            logging.error(f"Error in sysinfo: {str(e)}")
            print(f"Error: {str(e)}")
        
        
    def dmidecode(self) -> None:
        try:
            print("SMBIOS Information:")
            print(f"Manufacturer: {self.system_manufacturer}")
            print(f"Product Name: {self.system_model}")
            print(f"Version: {self.bios_version}")
            print(f"Serial Number: {self._get_serial_number()}")
            print(f"UUID: {self._get_uuid()}")
            print(f"Wake-up Type: Power Switch")
            print("\nProcessor Information:")
            print(f"Socket Designation: CPU Socket - U3E1")
            print(f"Type: Central Processor")
            print(f"Family: Core i7")
            print(f"Manufacturer: Intel")
            print(f"ID: {self.processor}")
            print(f"Version: Intel(R) Core(TM) i7 CPU")
            print(f"Voltage: 1.2 V")
            print(f"External Clock: 100 MHz")
            print(f"Max Speed: 4500 MHz")
            print(f"Current Speed: {psutil.cpu_freq().current} MHz")
            print(f"Status: Populated, Enabled")
            print(f"Upgrade: Other")
            print(f"L1 Cache Handle: 0x0004")
            print(f"L2 Cache Handle: 0x0005")
            print(f"L3 Cache Handle: 0x0006")
            print(f"Serial Number: None")
            print(f"Asset Tag: None")
            print(f"Part Number: None")
        except Exception as e:
            logging.error(f"Error in dmidecode: {str(e)}")
            print(f"Error: {str(e)}")

    def _get_serial_number(self):
        try:
            return subprocess.check_output("wmic bios get serialnumber", shell=True).decode().split('\n')[1].strip()
        except:
            return "Unknown"

    def _get_uuid(self):
        try:
            return subprocess.check_output("wmic csproduct get uuid", shell=True).decode().split('\n')[1].strip()
        except:
            return "Unknown"

    def lshw(self) -> None:
        try:
            print("Hardware Lister (lshw-like output):")
            print(f"{self.hostname}")
            print(f"    description: Computer")
            print(f"    product: {self.system_model}")
            print(f"    vendor: {self.system_manufacturer}")
            print(f"    version: {self.bios_version}")
            print(f"    serial: {self._get_serial_number()}")
            print(f"    width: 64 bits")
            print(f"    capabilities: smbios-3.0 dmi-3.0 smp vsyscall32")
            print(f"    configuration: boot=normal chassis=laptop uuid={self._get_uuid()}")
            print(f"  *-core")
            print(f"       description: Motherboard")
            print(f"       product: {self.system_model}")
            print(f"       vendor: {self.system_manufacturer}")
            print(f"       physical id: 0")
            print(f"       version: {self.bios_version}")
            print(f"       serial: {self._get_serial_number()}")
            print(f"     *-cpu")
            print(f"          description: CPU")
            print(f"          product: {self.processor}")
            print(f"          vendor: Intel Corp.")
            print(f"          physical id: 1")
            print(f"          bus info: cpu@0")
            print(f"          version: Intel(R) Core(TM) i7")
            print(f"          slot: U3E1")
            print(f"          size: {psutil.cpu_freq().current}MHz")
            print(f"          capacity: 4500MHz")
            print(f"          width: 64 bits")
            print(f"     *-memory")
            print(f"          description: System memory")
            print(f"          physical id: 2")
            print(f"          size: {psutil.virtual_memory().total / (1024**3):.2f}GiB")
        except Exception as e:
            logging.error(f"Error in lshw: {str(e)}")
            print(f"Error: {str(e)}")

    def hwinfo(self) -> None:
        try:
            print("Hardware Information:")
            print(f"  CPU:")
            print(f"    Model: {self.processor}")
            print(f"    Cores: {psutil.cpu_count(logical=False)}")
            print(f"    Threads: {psutil.cpu_count(logical=True)}")
            print(f"    Current Speed: {psutil.cpu_freq().current} MHz")
            print(f"    Max Speed: {psutil.cpu_freq().max} MHz")
            print(f"  Memory:")
            print(f"    Total: {psutil.virtual_memory().total / (1024**3):.2f} GB")
            print(f"    Available: {psutil.virtual_memory().available / (1024**3):.2f} GB")
            print(f"    Used: {psutil.virtual_memory().used / (1024**3):.2f} GB")
            print(f"  Disk:")
            print(f"    Model: {self.disk_drive}")
            print(f"    Total: {self.disk_size / (1024**3):.2f} GB")
            print(f"    Free: {self.free_space / (1024**3):.2f} GB")
            print(f"  GPU:")
            print(f"    Model: {self.gpu}")
            print(f"    Memory: {int(self.gpu_memory) / (1024**3):.2f} GB")
            print(f"  Network:")
            print(f"    Adapter: {self.network_adapter}")
            print(f"    IP Address: {self.ip_address}")
            print(f"    MAC Address: {self.mac_address}")
        except Exception as e:
            logging.error(f"Error in hwinfo: {str(e)}")
            print(f"Error: {str(e)}")

    def lscpu(self) -> None:
        try:
            print("CPU Information:")
            print(f"Architecture:                    {platform.machine()}")
            print(f"CPU op-mode(s):                  32-bit, 64-bit")
            print(f"Byte Order:                      Little Endian")
            print(f"CPU(s):                          {psutil.cpu_count(logical=True)}")
            print(f"On-line CPU(s) list:             0-{psutil.cpu_count(logical=True)-1}")
            print(f"Thread(s) per core:              {psutil.cpu_count(logical=True) // psutil.cpu_count(logical=False)}")
            print(f"Core(s) per socket:              {psutil.cpu_count(logical=False)}")
            print(f"Socket(s):                       1")
            print(f"Vendor ID:                       GenuineIntel")
            print(f"CPU family:                      6")
            print(f"Model:                           {self.processor}")
            print(f"Stepping:                        3")
            print(f"CPU MHz:                         {psutil.cpu_freq().current}")
            print(f"CPU max MHz:                     {psutil.cpu_freq().max}")
            print(f"CPU min MHz:                     {psutil.cpu_freq().min}")
            print(f"BogoMIPS:                        {psutil.cpu_freq().max * 2}")
            print(f"Virtualization:                  VT-x")
            print(f"L1d cache:                       32K")
            print(f"L1i cache:                       32K")
            print(f"L2 cache:                        256K")
            print(f"L3 cache:                        12288K")
        except Exception as e:
            logging.error(f"Error in lscpu: {str(e)}")
            print(f"Error: {str(e)}")

    def lsusb(self) -> None:
        try:
            print("USB Devices:")
            usb_devices = psutil.Popen(['wmic', 'path', 'win32_usbcontroller', 'get', 'manufacturer,name'], stdout=psutil.PIPE).communicate()[0]
            for line in usb_devices.decode().split('\n')[1:]:
                if line.strip():
                    print(f"- {line.strip()}")
        except Exception as e:
            logging.error(f"Error in lsusb: {str(e)}")
            print(f"Error: {str(e)}")

    def lspci(self) -> None:
        try:
            print("PCI Devices:")
            pci_devices = psutil.Popen(['wmic', 'path', 'win32_pnpentity', 'get', 'name'], stdout=psutil.PIPE).communicate()[0]
            for line in pci_devices.decode().split('\n')[1:]:
                if line.strip():
                    print(f"- {line.strip()}")
        except Exception as e:
            logging.error(f"Error in lspci: {str(e)}")
            print(f"Error: {str(e)}")

class ProcessManager:
    def __init__(self):
        self.processes = [
            {"name": "System Idle Process", "pid": 0, "session": "Services", "mem_usage": "8 K", "cpu_usage": "0%", "status": "Running", "user": "SYSTEM"},
            {"name": "System", "pid": 4, "session": "Services", "mem_usage": "144 K", "cpu_usage": "0%", "status": "Running", "user": "SYSTEM"},
            {"name": "Registry", "pid": 96, "session": "Services", "mem_usage": "52,504 K", "cpu_usage": "0%", "status": "Running", "user": "SYSTEM"},
            {"name": "smss.exe", "pid": 228, "session": "Services", "mem_usage": "1,024 K", "cpu_usage": "0%", "status": "Running", "user": "SYSTEM"},
            {"name": "csrss.exe", "pid": 372, "session": "Services", "mem_usage": "4,256 K", "cpu_usage": "0%", "status": "Running", "user": "SYSTEM"},
            {"name": "wininit.exe", "pid": 464, "session": "Services", "mem_usage": "4,960 K", "cpu_usage": "0%", "status": "Running", "user": "SYSTEM"},
            {"name": "services.exe", "pid": 552, "session": "Services", "mem_usage": "7,880 K", "cpu_usage": "0%", "status": "Running", "user": "SYSTEM"},
            {"name": "lsass.exe", "pid": 560, "session": "Services", "mem_usage": "14,284 K", "cpu_usage": "0%", "status": "Running", "user": "SYSTEM"},
            {"name": "svchost.exe", "pid": 656, "session": "Services", "mem_usage": "22,640 K", "cpu_usage": "0%", "status": "Running", "user": "SYSTEM"},
            {"name": "fontdrvhost.exe", "pid": 744, "session": "Services", "mem_usage": "3,132 K", "cpu_usage": "0%", "status": "Running", "user": "SYSTEM"},
            {"name": "WUDFHost.exe", "pid": 816, "session": "Services", "mem_usage": "7,480 K", "cpu_usage": "0%", "status": "Running", "user": "SYSTEM"},
            {"name": "winlogon.exe", "pid": 924, "session": "Console", "mem_usage": "6,736 K", "cpu_usage": "0%", "status": "Running", "user": "SYSTEM"},
            {"name": "dwm.exe", "pid": 1052, "session": "Console", "mem_usage": "70,680 K", "cpu_usage": "1%", "status": "Running", "user": "USER"},
            {"name": "explorer.exe", "pid": 3788, "session": "Console", "mem_usage": "77,436 K", "cpu_usage": "0%", "status": "Running", "user": "USER"},
            {"name": "RuntimeBroker.exe", "pid": 5724, "session": "Console", "mem_usage": "22,308 K", "cpu_usage": "0%", "status": "Running", "user": "USER"},
            {"name": "SearchUI.exe", "pid": 6100, "session": "Console", "mem_usage": "53,620 K", "cpu_usage": "0%", "status": "Running", "user": "USER"},
            {"name": "SearchIndexer.exe", "pid": 6372, "session": "Services", "mem_usage": "33,252 K", "cpu_usage": "0%", "status": "Running", "user": "SYSTEM"},
            {"name": "chrome.exe", "pid": 7164, "session": "Console", "mem_usage": "157,052 K", "cpu_usage": "2%", "status": "Running", "user": "USER"},
            {"name": "MsMpEng.exe", "pid": 3052, "session": "Services", "mem_usage": "205,184 K", "cpu_usage": "1%", "status": "Running", "user": "SYSTEM"},
            {"name": "spoolsv.exe", "pid": 1500, "session": "Services", "mem_usage": "11,640 K", "cpu_usage": "0%", "status": "Running", "user": "SYSTEM"}
        ]
        self.next_pid = 8000
        self.scheduled_tasks = []
        self.services = [
            {"name": "Windows Update", "status": "Running", "start_type": "Automatic"},
            {"name": "Windows Defender", "status": "Running", "start_type": "Automatic"},
            {"name": "Print Spooler", "status": "Running", "start_type": "Automatic"},
            {"name": "Remote Desktop Services", "status": "Stopped", "start_type": "Manual"},
        ]

    def tasklist(self, *args) -> None:
        try:
            filter_name = None
            filter_pid = None
            
            for i, arg in enumerate(args):
                if arg.lower() == "/fi":
                    if i + 1 < len(args) and args[i+1].startswith("IMAGENAME eq "):
                        filter_name = args[i+1].split("eq ")[1]
                    elif i + 1 < len(args) and args[i+1].startswith("PID eq "):
                        filter_pid = int(args[i+1].split("eq ")[1])

            print("Image Name                     PID Session Name        Session#    Mem Usage")
            print("========================= ======== ================ =========== ============")
            for process in self.processes:
                if (filter_name and filter_name.lower() not in process['name'].lower()) or (filter_pid and filter_pid != process['pid']):
                    continue
                session_name = process['session']
                session_number = "0" if session_name == "Services" else "1" if session_name == "Console" else ""
                print(f"{process['name']:<25} {process['pid']:>8} {session_name:<16} {session_number:>11} {process['mem_usage']:>12}")
        except Exception as e:
            logging.error(f"Error in tasklist: {str(e)}")
            print(f"Error: {str(e)}")

    def taskkill(self, *args) -> None:
        try:
            force = "/F" in args
            pid = None
            image_name = None

            for i, arg in enumerate(args):
                if arg == "/PID" and i + 1 < len(args):
                    try:
                        pid = int(args[i + 1])
                    except ValueError:
                        print(f"ERROR: Invalid PID {args[i + 1]}")
                        return
                elif arg == "/IM" and i + 1 < len(args):
                    image_name = args[i + 1]

            if pid is not None:
                self._taskkill_by_pid(pid, force)
            elif image_name:
                self._taskkill_by_name(image_name, force)
            else:
                print("ERROR: Invalid argument/option - '/PID pid' or '/IM imagename' must be specified.")
        except Exception as e:
            logging.error(f"Error in taskkill: {str(e)}")
            print(f"Error: {str(e)}")

    def _taskkill_by_pid(self, pid: int, force: bool) -> None:
        for process in self.processes:
            if process['pid'] == pid:
                if process['name'] in ["System Idle Process", "System", "Registry", "smss.exe", "csrss.exe", "wininit.exe", "services.exe", "lsass.exe"] and not force:
                    print(f"ERROR: Access is denied.")
                    return
                self.processes.remove(process)
                print(f"SUCCESS: The process with PID {pid} has been terminated.")
                return
        print(f"ERROR: The process \"{pid}\" not found.")

    def _taskkill_by_name(self, image_name: str, force: bool) -> None:
        found = False
        for process in self.processes[:]:
            if process['name'].lower() == image_name.lower():
                if process['name'] in ["System Idle Process", "System", "Registry", "smss.exe", "csrss.exe", "wininit.exe", "services.exe", "lsass.exe"] and not force:
                    print(f"ERROR: Access is denied.")
                    return
                self.processes.remove(process)
                found = True
        if found:
            print(f"SUCCESS: Sent termination signal to the process \"{image_name}\".")
        else:
            print(f"ERROR: The process \"{image_name}\" not found.")

    def start_process(self, name: str, user: str = "USER") -> None:
        new_process = {
            "name": name,
            "pid": self.next_pid,
            "session": "Console",
            "mem_usage": f"{random.randint(1000, 100000)} K",
            "cpu_usage": f"{random.randint(0, 5)}%",
            "status": "Running",
            "user": user
        }
        self.processes.append(new_process)
        self.next_pid += 1
        print(f"Process {name} started with PID {new_process['pid']}")

    def sfc(self, option: Optional[str] = None) -> None:
        try:
            if option == "/scannow":
                print("Beginning system scan. This process will take some time.")
                for i in range(0, 101, 10):
                    time.sleep(1)
                    print(f"Verification {i}% complete.")
                print("\nWindows Resource Protection did not find any integrity violations.")
            elif option == "/verifyonly":
                print("Beginning system scan. This process will take some time.")
                for i in range(0, 101, 20):
                    time.sleep(0.5)
                    print(f"Verification {i}% complete.")
                print("\nWindows Resource Protection did not find any integrity violations.")
            elif option == "/scanfile":
                print("Scanning specific file...")
                time.sleep(2)
                print("Scan complete. No integrity violations found.")
            elif option == "/verifyfile":
                print("Verifying specific file...")
                time.sleep(1)
                print("Verification complete. File integrity intact.")
            else:
                print("Usage: sfc [/scannow] [/verifyonly] [/scanfile=<file>] [/verifyfile=<file>]")
        except Exception as e:
            logging.error(f"Error in sfc: {str(e)}")
            print(f"Error: {str(e)}")

    def wmic_process(self, filter: Optional[str] = None) -> None:
        try:
            print("ProcessId  Name                  ExecutablePath")
            print("=========  ====================  ====================================")
            for process in self.processes:
                if filter and filter.lower() not in process['name'].lower():
                    continue
                print(f"{process['pid']:<10} {process['name']:<22} C:\\Windows\\System32\\{process['name']}")
        except Exception as e:
            logging.error(f"Error in wmic process: {str(e)}")
            print(f"Error: {str(e)}")

    def sc(self, action: str, service_name: str) -> None:
        try:
            service = next((s for s in self.services if s['name'].lower() == service_name.lower()), None)
            if not service:
                print(f"[SC] OpenService FAILED 1060:\nThe specified service does not exist as an installed service.\n")
                return

            if action.lower() == "query":
                print(f"SERVICE_NAME: {service['name']}")
                print(f"        TYPE               : 10  WIN32_OWN_PROCESS")
                print(f"        STATE              : 4  {service['status']}")
                print(f"        WIN32_EXIT_CODE    : 0  (0x0)")
                print(f"        SERVICE_EXIT_CODE  : 0  (0x0)")
                print(f"        CHECKPOINT         : 0x0")
                print(f"        WAIT_HINT          : 0x0")
            elif action.lower() == "start":
                if service['status'] == "Running":
                    print(f"[SC] StartService FAILED 1056:\nAn instance of the service is already running.\n")
                else:
                    service['status'] = "Running"
                    print(f"[SC] StartService SUCCESS")
            elif action.lower() == "stop":
                if service['status'] == "Stopped":
                    print(f"[SC] ControlService FAILED 1062:\nThe service has not been started.\n")
                else:
                    service['status'] = "Stopped"
                    print(f"[SC] ControlService SUCCESS")
            else:
                print(f"[SC] {action} is not a valid command. Type 'sc' for usage.")
        except Exception as e:
            logging.error(f"Error in sc: {str(e)}")
            print(f"Error: {str(e)}")

    def shutdown(self, option: str) -> None:
        try:
            if option == "/s":
                print("Shutting down the system...")
                time.sleep(2)
                print("The system is shutting down.")
            elif option == "/r":
                print("Restarting the system...")
                time.sleep(2)
                print("The system is restarting.")
            elif option == "/l":
                print("Logging off the current user...")
                time.sleep(1)
                print("The user has been logged off.")
            elif option == "/a":
                print("Aborting system shutdown...")
                time.sleep(1)
                print("The system shutdown has been aborted.")
            else:
                print("Invalid option. Use /s for shutdown, /r for restart, /l for logoff, or /a to abort shutdown.")
        except Exception as e:
            logging.error(f"Error in shutdown: {str(e)}")
            print(f"Error: {str(e)}")

    def runas(self, username: str, command: str) -> None:
        try:
            print(f"Attempting to run '{command}' as user '{username}'...")
            time.sleep(1)
            print(f"Command executed successfully as user '{username}'.")
        except Exception as e:
            logging.error(f"Error in runas: {str(e)}")
            print(f"Error: {str(e)}")

    def at(self, time: str, command: str) -> None:
        try:
            task_id = len(self.scheduled_tasks) + 1
            self.scheduled_tasks.append({
                "id": task_id,
                "time": time,
                "command": command,
                "status": "Scheduled"
            })
            print(f"Added a new task with ID {task_id}")
            print(f"Status ID   Day                 Time          Command Line")
            print(f"============================================================================")
            print(f"       {task_id}    Each M T W Th F    {time}     {command}")
        except Exception as e:
            logging.error(f"Error in at: {str(e)}")
            print(f"Error: {str(e)}")

    def schtasks(self, action: str, task_name: str = "", schedule: str = "") -> None:
        try:
            if action.lower() == "create":
                task_id = len(self.scheduled_tasks) + 1
                self.scheduled_tasks.append({
                    "id": task_id,
                    "name": task_name,
                    "schedule": schedule,
                    "status": "Ready"
                })
                print(f"SUCCESS: The scheduled task \"{task_name}\" has successfully been created.")
            elif action.lower() == "query":
                print("TaskName                                 Next Run Time          Status")
                print("========================================= ====================== ===============")
                for task in self.scheduled_tasks:
                    print(f"{task['name']:<41} {datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')} {task['status']}")
            elif action.lower() == "delete":
                self.scheduled_tasks = [task for task in self.scheduled_tasks if task['name'] != task_name]
                print(f"SUCCESS: The scheduled task \"{task_name}\" was successfully deleted.")
            else:
                print("Invalid action. Use 'create', 'query', or 'delete'.")
        except Exception as e:
            logging.error(f"Error in schtasks: {str(e)}")
            print(f"Error: {str(e)}")

    def qprocess(self) -> None:
        try:
            print(" SESSIONNAME       USERNAME                 PID  IMAGE")
            print("================ ================ ==================== ========================")
            for process in self.processes:
                print(f" {process['session']:<16} {process['user']:<16} {process['pid']:<20} {process['name']}")
        except Exception as e:
            logging.error(f"Error in qprocess: {str(e)}")
            print(f"Error: {str(e)}")

    def qwinsta(self) -> None:
        try:
            print(" SESSIONNAME       USERNAME                 ID  STATE   TYPE        DEVICE")
            print("================ ================ =========== ======= =========== ==========")
            print(" Services                               0  Disc")
            print(" Console          USER                  1  Active")
            print(">rdp-tcp                               65536  Listen  RDP-Tcp")
        except Exception as e:
            logging.error(f"Error in qwinsta: {str(e)}")
            print(f"Error: {str(e)}")

    def tskill(self, pid_or_name: str) -> None:
        try:
            if pid_or_name.isdigit():
                self._taskkill_by_pid(int(pid_or_name), force=True)
            else:
                self._taskkill_by_name(pid_or_name, force=True)
        except Exception as e:
            logging.error(f"Error in tskill: {str(e)}")
            print(f"Error: {str(e)}")

    def pskill(self, pid_or_name: str) -> None:
        try:
            if pid_or_name.isdigit():
                pid = int(pid_or_name)
                process = next((p for p in self.processes if p['pid'] == pid), None)
                if process:
                    self.processes.remove(process)
                    print(f"Process with PID {pid} has been terminated.")
                else:
                    print(f"No process found with PID {pid}.")
            else:
                killed = [p for p in self.processes if p['name'].lower() == pid_or_name.lower()]
                for process in killed:
                    self.processes.remove(process)
                if killed:
                    print(f"Killed {len(killed)} instance(s) of process '{pid_or_name}'.")
                else:
                    print(f"No processes found with name '{pid_or_name}'.")
        except Exception as e:
            logging.error(f"Error in pskill: {str(e)}")
            print(f"Error: {str(e)}")

    def psexec(self, computer: str, command: str) -> None:
        try:
            print(f"Connecting to {computer}...")
            time.sleep(1)
            print(f"Starting {command} on {computer}...")
            time.sleep(2)
            print(f"Command completed on {computer}.")
        except Exception as e:
            logging.error(f"Error in psexec: {str(e)}")
            print(f"Error: {str(e)}")

    def procexp(self) -> None:
        try:
            print("Process Explorer 16.32 - Copyright (C) 2021 Mark Russinovich")
            print("Sysinternals - www.sysinternals.com")
            print("\nProcess    PID   CPU   Private Bytes    Working Set    Description")
            print("=====================================================================")
            for process in sorted(self.processes, key=lambda x: x['cpu_usage'], reverse=True):
                print(f"{process['name']:<10} {process['pid']:<5} {process['cpu_usage']:<5} {process['mem_usage']:<15} {process['mem_usage']:<15} {process['name']}")
        except Exception as e:
            logging.error(f"Error in procexp: {str(e)}")
            print(f"Error: {str(e)}")

    def procmon(self) -> None:
        try:
            print("Process Monitor v3.85 - Copyright (C) 2021 Mark Russinovich")
            print("Sysinternals - www.sysinternals.com")
            print("\nTime     Process Name    PID   Operation    Path")
            print("===========================================================")
            for _ in range(10):  # Simulate 10 events
                process = random.choice(self.processes)
                operation = random.choice(["ReadFile", "WriteFile", "RegOpenKey", "TCP Connect", "UDP Send"])
                path = f"C:\\Windows\\System32\\{process['name']}" if operation in ["ReadFile", "WriteFile"] else "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"
                print(f"{datetime.datetime.now().strftime('%H:%M:%S')} {process['name']:<15} {process['pid']:<5} {operation:<12} {path}")
                time.sleep(0.5)
        except Exception as e:
            logging.error(f"Error in procmon: {str(e)}")
            print(f"Error: {str(e)}")

    def run_command(self, command: str) -> None:
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "tasklist":
            self.tasklist(*args)
        elif cmd == "taskkill":
            self.taskkill(*args)
        elif cmd == "sfc":
            self.sfc(*args)
        elif cmd == "start":
            self.start_process(*args)
        elif cmd == "wmic":
            if args[0].lower() == "process":
                self.wmic_process(*args[1:])
        elif cmd == "sc":
            self.sc(*args)
        elif cmd == "shutdown":
            self.shutdown(*args)
        elif cmd == "runas":
            self.runas(*args)
        elif cmd == "at":
            self.at(*args)
        elif cmd == "schtasks":
            self.schtasks(*args)
        elif cmd == "qprocess":
            self.qprocess()
        elif cmd == "qwinsta":
            self.qwinsta()
        elif cmd == "tskill":
            self.tskill(*args)
        elif cmd == "pskill":
            self.pskill(*args)
        elif cmd == "psexec":
            self.psexec(*args)
        elif cmd == "procexp":
            self.procexp()
        elif cmd == "procmon":
            self.procmon()
        else:
            print(f"'{cmd}' is not recognized as an internal or external command, operable program or batch file.")

class SecurityManager:
    def __init__(self):
        self.users = {
            "Administrator": {"password": "admin123", "groups": ["Administrators"], "permissions": ["read", "write", "execute"]},
            "User": {"password": "password123", "groups": ["Users"], "permissions": ["read", "execute"]}
        }
        self.firewall_rules = [
            {"name": "Allow_HTTP", "port": 80, "protocol": "TCP", "direction": "Inbound", "action": "Allow"},
            {"name": "Block_FTP", "port": 21, "protocol": "TCP", "direction": "Inbound", "action": "Block"}
        ]

    def create_user(self, username: str, password: str, groups: List[str]) -> None:
        if username in self.users:
            raise ValueError(f"User {username} already exists.")
        self.users[username] = {"password": password, "groups": groups, "permissions": ["read"]}
        print(f"User {username} created successfully.")

    def delete_user(self, username: str) -> None:
        if username not in self.users:
            raise ValueError(f"User {username} does not exist.")
        del self.users[username]
        print(f"User {username} deleted successfully.")

    def change_password(self, username: str, new_password: str) -> None:
        if username not in self.users:
            raise ValueError(f"User {username} does not exist.")
        self.users[username]["password"] = new_password
        print(f"Password changed successfully for user {username}.")

    def add_to_group(self, username: str, group: str) -> None:
        if username not in self.users:
            raise ValueError(f"User {username} does not exist.")
        if group not in self.users[username]["groups"]:
            self.users[username]["groups"].append(group)
            print(f"User {username} added to group {group}.")
        else:
            print(f"User {username} is already in group {group}.")

    def remove_from_group(self, username: str, group: str) -> None:
        if username not in self.users:
            raise ValueError(f"User {username} does not exist.")
        if group in self.users[username]["groups"]:
            self.users[username]["groups"].remove(group)
            print(f"User {username} removed from group {group}.")
        else:
            print(f"User {username} is not in group {group}.")

    def grant_permission(self, username: str, permission: str) -> None:
        if username not in self.users:
            raise ValueError(f"User {username} does not exist.")
        if permission not in self.users[username]["permissions"]:
            self.users[username]["permissions"].append(permission)
            print(f"Permission {permission} granted to user {username}.")
        else:
            print(f"User {username} already has permission {permission}.")

    def revoke_permission(self, username: str, permission: str) -> None:
        if username not in self.users:
            raise ValueError(f"User {username} does not exist.")
        if permission in self.users[username]["permissions"]:
            self.users[username]["permissions"].remove(permission)
            print(f"Permission {permission} revoked from user {username}.")
        else:
            print(f"User {username} does not have permission {permission}.")

    def list_users(self) -> None:
        print("Users:")
        for username, data in self.users.items():
            print(f"- {username}")
            print(f"  Groups: {', '.join(data['groups'])}")
            print(f"  Permissions: {', '.join(data['permissions'])}")

    def net_user(self, username: Optional[str] = None) -> None:
        try:
            if username:
                self._net_user_details(username)
            else:
                self._net_user_list()
        except Exception as e:
            logging.error(f"Error in net_user: {str(e)}")
            print(f"Error: {str(e)}")

    def _net_user_details(self, username: str) -> None:
        if username in self.users:
            print(f"User name                    {username}")
            print(f"Full Name                    {username}")
            print(f"Comment                      ")
            print(f"User's comment               ")
            print(f"Country/region code          000 (System Default)")
            print(f"Account active               Yes")
            print(f"Account expires              Never")
            print(f"\nPassword last set            Never")
            print(f"Password expires             Never")
            print(f"Password changeable          Never")
            print(f"Password required            Yes")
            print(f"User may change password     Yes")
            print(f"\nWorkstations allowed         All")
            print(f"Logon script                 ")
            print(f"User profile                 ")
            print(f"Home directory               ")
            print(f"Last logon                   Never")
            print(f"\nLogon hours allowed          All")
            print(f"\nLocal Group Memberships      *{', *'.join(self.users[username]['groups'])}")
            print(f"Global Group memberships     *None")
        else:
            raise ValueError(f"The user name could not be found: {username}")

    def _net_user_list(self) -> None:
        print("User accounts for \\DESKTOP-PC")
        print("\n-------------------------------------------------------------------------------")
        for user in self.users:
            print(user)
        print("The command completed successfully.")

    def net_localgroup(self, group: Optional[str] = None) -> None:
        try:
            groups = {
                "Administrators": ["Administrator"],
                "Users": ["User"],
                "Guests": [],
                "Power Users": []
            }
            if group:
                self._net_localgroup_details(group, groups)
            else:
                self._net_localgroup_list(groups)
        except Exception as e:
            logging.error(f"Error in net_localgroup: {str(e)}")
            print(f"Error: {str(e)}")

    def _net_localgroup_details(self, group: str, groups: Dict[str, List[str]]) -> None:
        if group in groups:
            print(f"Alias name     {group}")
            print(f"Comment        ")
            print(f"\nMembers")
            print(f"\n-------------------------------------------------------------------------------")
            for member in groups[group]:
                print(member)
            print("The command completed successfully.")
        else:
            raise ValueError(f"The local group name could not be found: {group}")

    def _net_localgroup_list(self, groups: Dict[str, List[str]]) -> None:
        print("Aliases for \\\\DESKTOP-PC")
        print("\n-------------------------------------------------------------------------------")
        for group in groups:
            print(group)
        print("The command completed successfully.")

    def net_share(self, share_name: Optional[str] = None) -> None:
        try:
            shares = {
                "C$": {"path": "C:\\", "type": "Default share"},
                "IPC$": {"path": "", "type": "Remote IPC"},
                "ADMIN$": {"path": "C:\\Windows", "type": "Remote Admin"}
            }
            if share_name:
                self._net_share_details(share_name, shares)
            else:
                self._net_share_list(shares)
        except Exception as e:
            logging.error(f"Error in net_share: {str(e)}")
            print(f"Error: {str(e)}")

    def _net_share_details(self, share_name: str, shares: Dict[str, Dict[str, str]]) -> None:
        if share_name in shares:
            print(f"Share name {share_name}")
            print(f"Path       {shares[share_name]['path']}")
            print(f"Remark     {shares[share_name]['type']}")
        else:
            raise ValueError(f"Share name {share_name} does not exist.")

    def _net_share_list(self, shares: Dict[str, Dict[str, str]]) -> None:
        print("Share name   Resource                        Remark")
        print("-----------------------------------------------------")
        for name, info in shares.items():
            print(f"{name.ljust(12)} {info['path'].ljust(30)} {info['type']}")

    def net_start(self, service: Optional[str] = None) -> None:
        try:
            services = ["Windows Event Log", "Windows Update", "Windows Firewall"]
            if service:
                self._net_start_service(service, services)
            else:
                self._net_start_list(services)
        except Exception as e:
            logging.error(f"Error in net_start: {str(e)}")
            print(f"Error: {str(e)}")

    def _net_start_service(self, service: str, services: List[str]) -> None:
        if service in services:
            print(f"The {service} service is starting.")
            time.sleep(2)
            print(f"The {service} service was started successfully.")
        else:
            raise ValueError(f"The service name is invalid.")

    def _net_start_list(self, services: List[str]) -> None:
        print("These Windows services are started:")
        for s in services:
            print(s)

    def net_stop(self, service: str) -> None:
        try:
            services = ["Windows Event Log", "Windows Update", "Windows Firewall"]
            if service in services:
                print(f"The {service} service is stopping.")
                time.sleep(2)
                print(f"The {service} service was stopped successfully.")
            else:
                raise ValueError(f"The service name is invalid.")
        except Exception as e:
            logging.error(f"Error in net_stop: {str(e)}")
            print(f"Error: {str(e)}")

    def netplwiz(self) -> None:
        try:
            print("User Accounts")
            print("1. Change an account")
            print("2. Add a user account")
            print("3. Remove a user account")
            print("4. Change advanced user account control settings")
            print("5. List all users")
            print("6. Change user password")
            print("7. Add user to group")
            print("8. Remove user from group")
            print("9. Grant permission to user")
            print("10. Revoke permission from user")
            choice = input("Enter a number to perform an action (or 'q' to quit): ")
            if choice == '1':
                self._netplwiz_change_account()
            elif choice == '2':
                self._netplwiz_add_account()
            elif choice == '3':
                self._netplwiz_remove_account()
            elif choice == '4':
                self._netplwiz_change_uac()
            elif choice == '5':
                self.list_users()
            elif choice == '6':
                self._netplwiz_change_password()
            elif choice == '7':
                self._netplwiz_add_to_group()
            elif choice == '8':
                self._netplwiz_remove_from_group()
            elif choice == '9':
                self._netplwiz_grant_permission()
            elif choice == '10':
                self._netplwiz_revoke_permission()
            elif choice.lower() == 'q':
                return
            else:
                print("Invalid choice.")
        except Exception as e:
            logging.error(f"Error in netplwiz: {str(e)}")
            print(f"Error: {str(e)}")

    def _netplwiz_change_account(self) -> None:
        print("Select an account to change:")
        for user in self.users:
            print(f"- {user}")

    def _netplwiz_add_account(self) -> None:
        new_user = input("Enter new username: ")
        password = input("Enter password: ")
        groups = input("Enter groups (comma-separated): ").split(',')
        self.create_user(new_user, password, groups)

    def _netplwiz_remove_account(self) -> None:
        user_to_remove = input("Enter username to remove: ")
        self.delete_user(user_to_remove)

    def _netplwiz_change_uac(self) -> None:
        print("Advanced user account control settings:")
        print("- User Account Control: Enabled")
        print("- Admin Approval Mode: Enabled")

    def _netplwiz_change_password(self) -> None:
        username = input("Enter username: ")
        new_password = input("Enter new password: ")
        self.change_password(username, new_password)

    def _netplwiz_add_to_group(self) -> None:
        username = input("Enter username: ")
        group = input("Enter group name: ")
        self.add_to_group(username, group)

    def _netplwiz_remove_from_group(self) -> None:
        username = input("Enter username: ")
        group = input("Enter group name: ")
        self.remove_from_group(username, group)

    def _netplwiz_grant_permission(self) -> None:
        username = input("Enter username: ")
        permission = input("Enter permission to grant: ")
        self.grant_permission(username, permission)

    def _netplwiz_revoke_permission(self) -> None:
        username = input("Enter username: ")
        permission = input("Enter permission to revoke: ")
        self.revoke_permission(username, permission)

    # New methods for the additional commands

    def icacls(self, path: str, args: List[str]) -> None:
        try:
            print(f"Changing permissions for {path}")
            for arg in args:
                print(f"Applying {arg}")
            print("Successfully processed 1 file; Failed processing 0 files")
        except Exception as e:
            logging.error(f"Error in icacls: {str(e)}")
            print(f"Error: {str(e)}")

    def cipher(self, drive: str) -> None:
        try:
            print(f"Listing data on drive {drive}")
            print("Files with encrypted attribute:")
            print("No files found.")
            print("\nFiles with compressed attribute:")
            print("C:\\example\\compressed_file.txt")
        except Exception as e:
            logging.error(f"Error in cipher: {str(e)}")
            print(f"Error: {str(e)}")

    def auditpol(self, subcategory: str, action: str) -> None:
        try:
            print(f"Configuring audit policy for {subcategory}")
            print(f"Action: {action}")
            print("The command was successfully executed.")
        except Exception as e:
            logging.error(f"Error in auditpol: {str(e)}")
            print(f"Error: {str(e)}")

    def gpedit(self) -> None:
        print("Launching Group Policy Editor (gpedit.msc)...")
        print("This would typically open the Group Policy Editor.")
        print("In this simulation, we'll display some common policies:")
        print("1. Password Policy")
        print("2. Account Lockout Policy")
        print("3. Audit Policy")
        print("4. User Rights Assignment")

    def secedit(self, action: str, cfg_file: str) -> None:
        try:
            if action == "export":
                print(f"Exporting current security configuration to {cfg_file}")
            elif action == "import":
                print(f"Importing security configuration from {cfg_file}")
            else:
                print(f"Unknown action: {action}")
            print("The operation completed successfully.")
        except Exception as e:
            logging.error(f"Error in secedit: {str(e)}")
            print(f"Error: {str(e)}")

    def cacls(self, file: str, args: List[str]) -> None:
        try:
            print(f"Changing ACLs for {file}")
            for arg in args:
                print(f"Applying {arg}")
            print("Successfully processed 1 file")
        except Exception as e:
            logging.error(f"Error in cacls: {str(e)}")
            print(f"Error: {str(e)}")

    def wmic_useraccount(self, action: str, args: Dict[str, str]) -> None:
        try:
            if action == "create":
                print(f"Creating new user account: {args.get('Name', 'Unknown')}")
            elif action == "delete":
                print(f"Deleting user account: {args.get('Name', 'Unknown')}")
            elif action == "list":
                print("Listing all user accounts:")
                for user in self.users:
                    print(f"- {user}")
            else:
                print(f"Unknown action: {action}")
        except Exception as e:
            logging.error(f"Error in wmic_useraccount: {str(e)}")
            print(f"Error: {str(e)}")

    def nltest(self, command: str) -> None:
        try:
            if command == "/dsgetdc":
                print("DC: \\\\DC01")
                print("Address: \\\\192.168.1.100")
                print("Dom Guid: 4f8846ed-47b3-4605-bfc7-b9744a666cde")
                print("Dom Name: CONTOSO")
                print("Forest Name: contoso.com")
                print("Dc Site Name: Default-First-Site-Name")
                print("Our Site Name: Default-First-Site-Name")
                print("Flags: PDC GC DS LDAP KDC TIMESERV WRITABLE DNS_DC DNS_DOMAIN DNS_FOREST CLOSE_SITE FULL_SECRET WS")
            elif command == "/sc_query":
                print("Trusted DC Name \\\\DC01")
                print("Trusted DC Connection Status: Success")
            else:
                print(f"Unknown command: {command}")
        except Exception as e:
            logging.error(f"Error in nltest: {str(e)}")
            print(f"Error: {str(e)}")

    def certutil(self, action: str, args: List[str]) -> None:
        try:
            if action == "-list":
                print("Listing certificates in the personal store:")
                print("================ Certificate 0 ================")
                print("Serial Number: 1234567890abcdef")
                print("Issuer: CN=Contoso-CA, DC=contoso, DC=com")
                print("Subject: CN=DESKTOP-PC")
                print("NotBefore: 5/1/2023 12:00 AM")
                print("NotAfter: 5/1/2024 11:59 PM")
            elif action == "-addstore":
                print(f"Adding certificate to store: {args[0]}")
            elif action == "-delstore":
                print(f"Deleting certificate from store: {args[0]}")
            else:
                print(f"Unknown action: {action}")
        except Exception as e:
            logging.error(f"Error in certutil: {str(e)}")
            print(f"Error: {str(e)}")

    def manage_bde(self, action: str, drive: str, args: List[str]) -> None:
        try:
            if action == "on":
                print(f"Turning on BitLocker for drive {drive}")
                print("BitLocker Drive Encryption: Configuration Tool version 10.0.19041")
                print(f"Copyright (C) 2013 Microsoft Corporation. All rights reserved.")
                print(f"\nStarting encryption on volume {drive}...")
                print("Preparing volume for encryption...")
                print("Initializing encryption...")
                print(f"Encryption in progress on volume {drive}...")
            elif action == "off":
                print(f"Turning off BitLocker for drive {drive}")
                print("BitLocker Drive Encryption: Configuration Tool version 10.0.19041")
                print(f"Copyright (C) 2013 Microsoft Corporation. All rights reserved.")
                print(f"\nStarting decryption on volume {drive}...")
                print(f"Decryption in progress on volume {drive}...")
            elif action == "status":
                print(f"Checking BitLocker status for drive {drive}")
                print("BitLocker Drive Encryption: Configuration Tool version 10.0.19041")
                print(f"Copyright (C) 2013 Microsoft Corporation. All rights reserved.")
                print(f"\nVolume C: [{drive}]")
                print("    [Data Volume]")
                print("    Size:                 256 GB")
                print("    BitLocker Version:    2.0")
                print("    Conversion Status:    Fully Encrypted")
                print("    Percentage Encrypted: 100.0%")
                print("    Encryption Method:    XTS-AES 256")
            else:
                print(f"Unknown action: {action}")
        except Exception as e:
            logging.error(f"Error in manage_bde: {str(e)}")
            print(f"Error: {str(e)}")

    def security_commands(self, cmd: str, args: List[str]) -> None:
        try:
            if cmd == "net user":
                self.net_user(args[0] if args else None)
            elif cmd == "net localgroup":
                self.net_localgroup(args[0] if args else None)
            elif cmd == "net share":
                self.net_share(args[0] if args else None)
            elif cmd == "net start":
                self.net_start(args[0] if args else None)
            elif cmd == "net stop":
                self.net_stop(args[0])
            elif cmd == "netplwiz":
                self.netplwiz()
            elif cmd == "icacls":
                self.icacls(args[0], args[1:])
            elif cmd == "cipher":
                self.cipher(args[0])
            elif cmd == "auditpol":
                self.auditpol(args[0], args[1])
            elif cmd == "gpedit.msc":
                self.gpedit()
            elif cmd == "secedit":
                self.secedit(args[0], args[1])
            elif cmd == "cacls":
                self.cacls(args[0], args[1:])
            elif cmd == "wmic useraccount":
                self.wmic_useraccount(args[0], {arg.split('=')[0]: arg.split('=')[1] for arg in args[1:] if '=' in arg})
            elif cmd == "nltest":
                self.nltest(args[0])
            elif cmd == "certutil":
                self.certutil(args[0], args[1:])
            elif cmd == "manage-bde":
                self.manage_bde(args[0], args[1], args[2:])
            else:
                print(f"Unknown security command: {cmd}")
        except Exception as e:
            logging.error(f"Error in security_commands: {str(e)}")
            print(f"Error: {str(e)}")
        
class PerformanceMonitor:
    def __init__(self):
        self.cpu_usage = 0
        self.memory_usage = 0
        self.disk_usage = 0
        self.network_usage = 0
        self.processes = [
            {"name": "System Idle Process", "pid": 0, "session": "Services", "mem_usage": "8 K"},
            {"name": "System", "pid": 4, "session": "Services", "mem_usage": "144 K"},
            {"name": "smss.exe", "pid": 228, "session": "Services", "mem_usage": "1,024 K"},
            {"name": "csrss.exe", "pid": 380, "session": "Services", "mem_usage": "4,512 K"},
            {"name": "wininit.exe", "pid": 468, "session": "Services", "mem_usage": "4,628 K"}
        ]

    def update_metrics(self) -> None:
        self.cpu_usage = random.randint(0, 100)
        self.memory_usage = random.randint(0, 100)
        self.disk_usage = random.randint(0, 100)
        self.network_usage = random.randint(0, 100)

    def perfmon(self) -> None:
        try:
            print("Performance Monitor")
            print("-------------------")
            self.update_metrics()
            print(f"CPU Usage:    {self.cpu_usage}%")
            print(f"Memory Usage: {self.memory_usage}%")
            print(f"Disk Usage:   {self.disk_usage}%")
            print(f"Network Usage:{self.network_usage}%")
        except Exception as e:
            logging.error(f"Error in perfmon: {str(e)}")
            print(f"Error: {str(e)}")

    def resmon(self) -> None:
        try:
            print("Resource Monitor")
            print("----------------")
            self.update_metrics()
            print("CPU")
            print(f"  Usage: {self.cpu_usage}%")
            print("Memory")
            print(f"  Usage: {self.memory_usage}%")
            print("Disk")
            print(f"  Active time: {self.disk_usage}%")
            print("Network")
            print(f"  Utilization: {self.network_usage}%")
        except Exception as e:
            logging.error(f"Error in resmon: {str(e)}")
            print(f"Error: {str(e)}")

    def eventvwr(self) -> None:
        try:
            event_types = ["Information", "Warning", "Error"]
            sources = ["System", "Application", "Security"]
            print("Event Viewer")
            print("------------")
            for _ in range(10):
                event_type = random.choice(event_types)
                source = random.choice(sources)
                event_id = random.randint(1000, 9999)
                print(f"Log: {source}")
                print(f"Type: {event_type}")
                print(f"Event ID: {event_id}")
                print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("----")
        except Exception as e:
            logging.error(f"Error in eventvwr: {str(e)}")
            print(f"Error: {str(e)}")

    def wmic(self, query: str) -> None:
        try:
            if query == "cpu get loadpercentage":
                print("LoadPercentage")
                print(f"{random.randint(0, 100)}")
            elif query == "memorychip get capacity":
                print("Capacity")
                print("8589934592")
                print("8589934592")
            elif query == "diskdrive get size":
                print("Size")
                print("256060514304")
                print("1000204886016")
            else:
                print("Invalid query")
        except Exception as e:
            logging.error(f"Error in wmic: {str(e)}")
            print(f"Error: {str(e)}")

    def powercfg(self, option: str) -> None:
        try:
            if option == "/list":
                print("Existing Power Schemes (* Active)")
                print("-----------------------------------")
                print("Power Scheme GUID: 381b4222-f694-41f0-9685-ff5bb260df2e  (Balanced) *")
                print("Power Scheme GUID: 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c  (High performance)")
                print("Power Scheme GUID: a1841308-3541-4fab-bc81-f71556f20b4a  (Power saver)")
            else:
                print("Invalid option")
        except Exception as e:
            logging.error(f"Error in powercfg: {str(e)}")
            print(f"Error: {str(e)}")

    def typeperf(self, counters: List[str], interval: int = 1, samples: int = 5) -> None:
        try:
            print('"(PDH-CSV 4.0)","\\\\DESKTOP-123ABC\\Processor(_Total)\\% Processor Time"')
            for _ in range(samples):
                timestamp = datetime.now().strftime('"%m/%d/%Y %H:%M:%S.000"')
                value = random.uniform(0, 100)
                print(f'{timestamp},"{value:.6f}"')
                time.sleep(interval)
        except Exception as e:
            logging.error(f"Error in typeperf: {str(e)}")
            print(f"Error: {str(e)}")

    def logman(self, command: str, *args) -> None:
        try:
            if command == "create":
                print(f"Successfully created data collector set: {args[0]}")
            elif command == "start":
                print(f"Started data collector set: {args[0]}")
            elif command == "stop":
                print(f"Stopped data collector set: {args[0]}")
            elif command == "delete":
                print(f"Successfully deleted data collector set: {args[0]}")
            else:
                print("Invalid command")
        except Exception as e:
            logging.error(f"Error in logman: {str(e)}")
            print(f"Error: {str(e)}")

    def xperf(self, options: str) -> None:
        try:
            if "-on" in options:
                print("Starting trace...")
                time.sleep(2)
                print("Trace started successfully.")
            elif "-off" in options:
                print("Stopping trace...")
                time.sleep(2)
                print("Trace stopped successfully.")
            else:
                print("Invalid options")
        except Exception as e:
            logging.error(f"Error in xperf: {str(e)}")
            print(f"Error: {str(e)}")

    def psinfo(self) -> None:
        try:
            print("System information:")
            print("Hostname:      DESKTOP-123ABC")
            print("OS Version:    Windows 10 Pro")
            print("Kernel Version:10.0.19041")
            print("Product Type:  WorkStation")
            print("CPU:           Intel(R) Core(TM) i7-10700K CPU @ 3.80GHz")
            print("Physical Memory:32 GB")
        except Exception as e:
            logging.error(f"Error in psinfo: {str(e)}")
            print(f"Error: {str(e)}")

    def pslist(self) -> None:
        try:
            print("Process information:")
            print("Name                Pid    Pri Thd  Hnd   Priv")
            print("---------------- ------ ----- --- ----- ------")
            for process in self.processes:
                pid = process['pid']
                name = process['name']
                pri = random.randint(0, 15)
                thd = random.randint(1, 50)
                hnd = random.randint(50, 1000)
                priv = f"{random.randint(1000, 100000):,} K"
                print(f"{name:<16} {pid:>6} {pri:>5} {thd:>3} {hnd:>5} {priv:>6}")
        except Exception as e:
            logging.error(f"Error in pslist: {str(e)}")
            print(f"Error: {str(e)}")

    def pstack(self, pid: int) -> None:
        try:
            print(f"Call stack for process {pid}:")
            print("0x00007ff65cf3f626 ntdll!NtWaitForSingleObject+0x16")
            print("0x00007ff65aa6e7d4 KERNELBASE!WaitForSingleObjectEx+0x94")
            print("0x00007ff63e2b1fe8 myapp!WinMain+0x123")
            print("0x00007ff63e2b1f42 myapp!__scrt_common_main_seh+0x106")
            print("0x00007ff65cf6531f ntdll!RtlUserThreadStart+0x2f")
        except Exception as e:
            logging.error(f"Error in pstack: {str(e)}")
            print(f"Error: {str(e)}")

    def pmap(self, pid: int) -> None:
        try:
            print(f"Memory map for process {pid}:")
            print("Address           Kbytes     RSS   Dirty Mode  Mapping")
            print("---------------- -------- -------- ------ ----- -------")
            print("00007ff7e8b30000    1024      236      0 r-x-- myapp.exe")
            print("00007ff7e8c30000      64       64     64 r---- myapp.exe")
            print("00007ff7e8c40000      64       60     60 rw--- myapp.exe")
            print("00007ffd7eb10000   2048     1184      0 r-x-- ntdll.dll")
        except Exception as e:
            logging.error(f"Error in pmap: {str(e)}")
            print(f"Error: {str(e)}")

    def vmstat(self) -> None:
        try:
            print("procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----")
            print(" r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st")
            for _ in range(5):
                r = random.randint(0, 5)
                b = random.randint(0, 2)
                swpd = random.randint(0, 1000000)
                free = random.randint(100000, 1000000)
                buff = random.randint(10000, 100000)
                cache = random.randint(100000, 1000000)
                si = random.randint(0, 100)
                so = random.randint(0, 100)
                bi = random.randint(0, 1000)
                bo = random.randint(0, 1000)
                in_ = random.randint(0, 1000)
                cs = random.randint(0, 1000)
                us = random.randint(0, 100)
                sy = random.randint(0, 100)
                id_ = random.randint(0, 100)
                wa = random.randint(0, 10)
                st = 0
                print(f"{r:2d} {b:2d} {swpd:7d} {free:7d} {buff:6d} {cache:6d} {si:4d} {so:4d} {bi:5d} {bo:5d} {in_:4d} {cs:4d} {us:2d} {sy:2d} {id_:2d} {wa:2d} {st:2d}")
                time.sleep(1)
        except Exception as e:
            logging.error(f"Error in vmstat: {str(e)}")
            print(f"Error: {str(e)}")

    def iostat(self) -> None:
        try:
            print("Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util")
            for _ in range(5):
                device = f"sda{random.randint(1, 5)}"
                rrqm = random.uniform(0, 10)
                wrqm = random.uniform(0, 20)
                r = random.uniform(0, 100)
                w = random.uniform(0, 200)
                rkb = random.uniform(0, 1000)
                wkb = random.uniform(0, 2000)
                avgrq_sz = random.uniform(0, 100)
                avgqu_sz = random.uniform(0, 10)
                await_ = random.uniform(0, 50)
                r_await = random.uniform(0, 50)
                w_await = random.uniform(0, 50)
                svctm = random.uniform(0, 10)
                util = random.uniform(0, 100)
                print(f"{device:7s} {rrqm:10.2f} {wrqm:8.2f} {r:7.2f} {w:7.2f} {rkb:8.2f} {wkb:8.2f} {avgrq_sz:8.2f} {avgqu_sz:8.2f} {await_:7.2f} {r_await:7.2f} {w_await:7.2f} {svctm:6.2f} {util:6.2f}")
                time.sleep(1)
        except Exception as e:
            logging.error(f"Error in iostat: {str(e)}")
            print(f"Error: {str(e)}")

class DiskManager:
    def __init__(self):
        self.disks: Dict[str, Dict[str, str]] = {
            "C:": {"file_system": "NTFS", "total_size": "256 GB", "used_space": "120 GB", "free_space": "136 GB"},
            "D:": {"file_system": "NTFS", "total_size": "512 GB", "used_space": "200 GB", "free_space": "312 GB"}
        }

    def chkdsk(self, drive: str) -> None:
        try:
            if drive in self.disks:
                print(f"The type of the file system is {self.disks[drive]['file_system']}.")
                print(f"Volume label is {drive[0]}")
                print("\nWindows is verifying files and folders...")
                time.sleep(2)
                print("File and folder verification is complete.")
                print("\nWindows has scanned the file system and found no problems.")
                print("No further action is required.")
                print(f"\n   {self.disks[drive]['total_size']} total disk space.")
                print(f"   {self.disks[drive]['used_space']} in {random.randint(100000, 500000)} files.")
                print(f"   {self.disks[drive]['free_space']} available on disk.")
            else:
                raise ValueError(f"The drive {drive} does not exist.")
        except Exception as e:
            logging.error(f"Error in chkdsk: {str(e)}")
            print(f"Error: {str(e)}")

    def diskpart(self) -> None:
        try:
            print("Microsoft DiskPart version 10.0.19041.964\n")
            print("Copyright (C) Microsoft Corporation.")
            print("On computer: DESKTOP-PC\n")
            while True:
                command = input("DISKPART> ").lower()
                if command == "exit":
                    break
                elif command == "list disk":
                    self._diskpart_list_disk()
                elif command == "list volume":
                    self._diskpart_list_volume()
                else:
                    print(f"'{command}' is not recognized as an internal or external command,")
                    print("operable program or batch file.")
        except Exception as e:
            logging.error(f"Error in diskpart: {str(e)}")
            print(f"Error: {str(e)}")

    def _diskpart_list_disk(self) -> None:
        print("\n  Disk ###  Status         Size     Free     Dyn  Gpt")
        print("  --------  -------------  -------  -------  ---  ---")
        print("  Disk 0    Online          256 GB      0 B        *")
        print("  Disk 1    Online          512 GB      0 B        *")

    def _diskpart_list_volume(self) -> None:
        print("\n  Volume ###  Ltr  Label        Fs     Type        Size     Status     Info")
        print("  ----------  ---  -----------  -----  ----------  -------  ---------  --------")
        print("  Volume 0     C                NTFS   Partition    256 GB  Healthy    Boot")
        print("  Volume 1     D                NTFS   Partition    512 GB  Healthy")

    def defrag(self, drive: str) -> None:
        try:
            print(f"Defragmenting drive {drive}...")
            for i in range(0, 101, 10):
                time.sleep(1)
                print(f"Progress: {i}% complete")
            print(f"\nDefragmentation of drive {drive} complete.")
        except Exception as e:
            logging.error(f"Error in defrag: {str(e)}")
            print(f"Error: {str(e)}")

    def fsutil(self, args: List[str]) -> None:
        try:
            if not args:
                print("Usage: fsutil [command]")
                return

            command = args[0].lower()
            if command == "fsinfo":
                if len(args) < 2:
                    print("Usage: fsutil fsinfo [volumeinfo] <drive>")
                    return
                drive = args[1]
                if drive in self.disks:
                    print(f"File System Type: {self.disks[drive]['file_system']}")
                    print(f"Total Size: {self.disks[drive]['total_size']}")
                    print(f"Used Space: {self.disks[drive]['used_space']}")
                    print(f"Free Space: {self.disks[drive]['free_space']}")
                else:
                    print(f"Drive {drive} not found.")
            else:
                print(f"Unrecognized fsutil command: {command}")
        except Exception as e:
            logging.error(f"Error in fsutil: {str(e)}")
            print(f"Error: {str(e)}")

    def format(self, drive: str, file_system: str = "NTFS", quick: bool = False) -> None:
        try:
            if drive not in self.disks:
                raise ValueError(f"The drive {drive} does not exist.")
            
            print(f"Formatting drive {drive}...")
            time.sleep(2)
            
            if quick:
                print("Performing quick format...")
            else:
                print("Performing full format...")
                for i in range(0, 101, 10):
                    time.sleep(1)
                    print(f"Progress: {i}% complete")
            
            self.disks[drive]["file_system"] = file_system
            self.disks[drive]["used_space"] = "0 GB"
            self.disks[drive]["free_space"] = self.disks[drive]["total_size"]
            
            print(f"\nFormat complete. Drive {drive} is now formatted with {file_system}.")
        except Exception as e:
            logging.error(f"Error in format: {str(e)}")
            print(f"Error: {str(e)}")

    def label(self, drive: str, new_label: str) -> None:
        try:
            if drive not in self.disks:
                raise ValueError(f"The drive {drive} does not exist.")
            
            print(f"Changing volume label of drive {drive} to '{new_label}'...")
            time.sleep(1)
            print(f"Volume label changed successfully.")
        except Exception as e:
            logging.error(f"Error in label: {str(e)}")
            print(f"Error: {str(e)}")

    def convert(self, drive: str, target_fs: str) -> None:
        try:
            if drive not in self.disks:
                raise ValueError(f"The drive {drive} does not exist.")
            
            current_fs = self.disks[drive]["file_system"]
            if current_fs == target_fs:
                print(f"Drive {drive} is already {target_fs}.")
                return
            
            print(f"Converting drive {drive} from {current_fs} to {target_fs}...")
            time.sleep(2)
            print(f"Conversion complete. Drive {drive} is now {target_fs}.")
            self.disks[drive]["file_system"] = target_fs
        except Exception as e:
            logging.error(f"Error in convert: {str(e)}")
            print(f"Error: {str(e)}")

    def vssadmin(self, args: List[str]) -> None:
        try:
            if not args:
                print("Usage: vssadmin [command]")
                return

            command = args[0].lower()
            if command == "list":
                if len(args) < 2:
                    print("Usage: vssadmin list [shadows|writers|providers]")
                    return
                subcommand = args[1].lower()
                if subcommand == "shadows":
                    print("Contents of shadow copies:")
                    print("No shadow copies found.")
                elif subcommand == "writers":
                    print("Writer name: 'System Writer'")
                    print("   Writer Id: {e8132975-6f93-4464-a53e-1050253ae220}")
                    print("   Writer Instance Id: {b8a24bae-7260-4b8c-8d85-4b3e0f1c1d93}")
                    print("   State: [1] Stable")
                    print("   Last error: No error")
                elif subcommand == "providers":
                    print("Provider name: 'Microsoft Software Shadow Copy provider 1.0'")
                    print("   Provider Id: {b5946137-7b9f-4925-af80-51abd60b20d5}")
                    print("   Version: 1.0.0.7")
                else:
                    print(f"Unrecognized vssadmin list subcommand: {subcommand}")
            else:
                print(f"Unrecognized vssadmin command: {command}")
        except Exception as e:
            logging.error(f"Error in vssadmin: {str(e)}")
            print(f"Error: {str(e)}")

    def diskmgmt(self) -> None:
        print("Launching Disk Management (diskmgmt.msc)...")
        print("This would typically open the graphical Disk Management tool.")
        print("In this simulation, we'll display a text representation of the disks:")
        self._diskpart_list_disk()
        self._diskpart_list_volume()

    def wbadmin(self, args: List[str]) -> None:
        try:
            if not args:
                print("Usage: wbadmin [command]")
                return

            command = args[0].lower()
            if command == "start":
                if "backup" in args:
                    print("Starting Windows Backup...")
                    for i in range(0, 101, 10):
                        time.sleep(1)
                        print(f"Backup progress: {i}% complete")
                    print("Backup completed successfully.")
                else:
                    print("Unknown wbadmin start command. Use 'wbadmin start backup'.")
            elif command == "get":
                if "versions" in args:
                    print("Backup time: 7/12/2024 10:00 AM")
                    print("Backup target: D:\\WindowsImageBackup\\")
                    print("Version identifier: 07/12/2024-00001")
                else:
                    print("Unknown wbadmin get command. Use 'wbadmin get versions'.")
            else:
                print(f"Unrecognized wbadmin command: {command}")
        except Exception as e:
            logging.error(f"Error in wbadmin: {str(e)}")
            print(f"Error: {str(e)}")

    def imdisk(self, args: List[str]) -> None:
        try:
            if not args:
                print("Usage: imdisk [command]")
                return

            command = args[0].lower()
            if command == "create":
                print("Creating new virtual disk...")
                time.sleep(1)
                print("Virtual disk created successfully.")
            elif command == "remove":
                print("Removing virtual disk...")
                time.sleep(1)
                print("Virtual disk removed successfully.")
            else:
                print(f"Unrecognized imdisk command: {command}")
        except Exception as e:
            logging.error(f"Error in imdisk: {str(e)}")
            print(f"Error: {str(e)}")

    def diskspd(self, args: List[str]) -> None:
        try:
            print("Running DiskSpd storage performance test...")
            time.sleep(2)
            print("Test results:")
            print("  Read I/O: 500 MB/s")
            print("  Write I/O: 350 MB/s")
            print("  IOPS: 10,000")
            print("Test completed successfully.")
        except Exception as e:
            logging.error(f"Error in diskspd: {str(e)}")
            print(f"Error: {str(e)}")

    def ddrescue(self, source: str, destination: str) -> None:
        try:
            print(f"Starting data recovery from {source} to {destination}...")
            for i in range(0, 101, 10):
                time.sleep(1)
                print(f"Recovery progress: {i}% complete")
            print("Data recovery completed. Check the log file for details.")
        except Exception as e:
            logging.error(f"Error in ddrescue: {str(e)}")
            print(f"Error: {str(e)}")

    def smartctl(self, drive: str) -> None:
        try:
            print(f"S.M.A.R.T. information for drive {drive}:")
            print("=== START OF INFORMATION SECTION ===")
            print(f"Model Family:     Generic SSD")
            print(f"Device Model:     Generic_SSD_1TB")
            print(f"Serial Number:    ABCD1234EFGH5678")
            print(f"Firmware Version: 1.0")
            print(f"User Capacity:    1,000,204,886,016 bytes [1.00 TB]")
            print(f"Sector Size:      512 bytes logical/physical")
            print("=== START OF SMART DATA SECTION ===")
            print(f"SMART overall-health self-assessment test result: PASSED")
            print(f"")
            print(f"SMART Attributes:")
            print(f"ID# ATTRIBUTE_NAME          VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE")
            print(f"  1 Raw_Read_Error_Rate     100   100   050    Pre-fail  Always       -       0")
            print(f"  9 Power_On_Hours          100   100   000    Old_age   Always       -       8760")
            print(f"12 Power_Cycle_Count        100   100   000    Old_age   Always       -       100")
            print(f"")
            print(f"SMART Error Log not supported")
        except Exception as e:
            logging.error(f"Error in smartctl: {str(e)}")
            print(f"Error: {str(e)}")
            
class PrinterManager:
    def __init__(self):
        self.printers: Dict[str, Dict[str, Any]] = {
            "HP-LaserJet-1": {"type": "Laser", "status": "Ready", "location": "Office 1"},
            "Epson-WF-3720": {"type": "Inkjet", "status": "Low on ink", "location": "Reception"}
        }

    def list_printers(self) -> None:
        print("Printer Name         Type    Status          Location")
        print("----------------------------------------------------")
        for name, info in self.printers.items():
            print(f"{name:<20} {info['type']:<7} {info['status']:<15} {info['location']}")

    def add_printer(self, name: str, printer_type: str, location: str) -> None:
        if name in self.printers:
            print(f"Error: Printer '{name}' already exists.")
        else:
            self.printers[name] = {"type": printer_type, "status": "Ready", "location": location}
            print(f"Printer '{name}' added successfully.")

    def remove_printer(self, name: str) -> None:
        if name in self.printers:
            del self.printers[name]
            print(f"Printer '{name}' removed successfully.")
        else:
            print(f"Error: Printer '{name}' not found.")

    def print_test_page(self, name: str) -> None:
        if name in self.printers:
            print(f"Sending test page to printer '{name}'...")
            time.sleep(2)
            print("Test page printed successfully.")
        else:
            print(f"Error: Printer '{name}' not found.")

    def troubleshoot_printer(self, name: str) -> None:
        if name in self.printers:
            print(f"Troubleshooting printer '{name}'...")
            print("1. Checking printer connection...")
            time.sleep(1)
            print("2. Verifying printer driver...")
            time.sleep(1)
            print("3. Checking print spooler service...")
            time.sleep(1)
            print("4. Inspecting print queue...")
            time.sleep(1)
            print("Troubleshooting complete. No issues found.")
        else:
            print(f"Error: Printer '{name}' not found.")

    def get_printer_status(self, name: str) -> None:
        if name in self.printers:
            print(f"Status of printer '{name}': {self.printers[name]['status']}")
        else:
            print(f"Error: Printer '{name}' not found.")

    def set_printer_status(self, name: str, status: str) -> None:
        if name in self.printers:
            self.printers[name]['status'] = status
            print(f"Status of printer '{name}' updated to: {status}")
        else:
            print(f"Error: Printer '{name}' not found.")

    def print_job(self, name: str, document: str) -> None:
        if name in self.printers:
            print(f"Sending document '{document}' to printer '{name}'...")
            time.sleep(2)
            print(f"Document '{document}' printed successfully on '{name}'.")
        else:
            print(f"Error: Printer '{name}' not found.")

    def cancel_print_job(self, name: str, job_id: int) -> None:
        if name in self.printers:
            print(f"Cancelling print job {job_id} on printer '{name}'...")
            time.sleep(1)
            print(f"Print job {job_id} cancelled successfully.")
        else:
            print(f"Error: Printer '{name}' not found.")

    def get_printer_queue(self, name: str) -> None:
        if name in self.printers:
            print(f"Print queue for printer '{name}':")
            print("Job ID  Document Name  Status")
            print("--------------------------------")
            # Simulating a print queue
            for i in range(3):
                print(f"{1001+i:<7} Document{i+1}.pdf  Pending")
        else:
            print(f"Error: Printer '{name}' not found.")

    def update_printer_driver(self, name: str) -> None:
        if name in self.printers:
            print(f"Updating driver for printer '{name}'...")
            time.sleep(2)
            print(f"Driver for printer '{name}' updated successfully.")
        else:
            print(f"Error: Printer '{name}' not found.")
            
class VirtualizationManager:
    def __init__(self):
        self.vms: Dict[str, Dict[str, Any]] = {
            "Win10-Dev": {"status": "Running", "cpu": 2, "ram": 4096, "hdd": 50, "type": "Hyper-V"},
            "Ubuntu-Server": {"status": "Stopped", "cpu": 1, "ram": 2048, "hdd": 20, "type": "VirtualBox"}
        }
        self.containers: Dict[str, Dict[str, Any]] = {
            "web-server": {"status": "Running", "image": "nginx:latest", "type": "Docker"},
            "database": {"status": "Stopped", "image": "mysql:5.7", "type": "LXC"}
        }

    def list_vms(self) -> None:
        print("VM Name         Status   CPU   RAM (MB)   HDD (GB)   Type")
        print("------------------------------------------------------------")
        for name, info in self.vms.items():
            print(f"{name:<15} {info['status']:<8} {info['cpu']:<5} {info['ram']:<10} {info['hdd']:<10} {info['type']}")

    def list_containers(self) -> None:
        print("Container Name   Status   Image            Type")
        print("------------------------------------------------")
        for name, info in self.containers.items():
            print(f"{name:<16} {info['status']:<8} {info['image']:<16} {info['type']}")

    def start_vm(self, name: str) -> None:
        if name in self.vms:
            if self.vms[name]['status'] == "Running":
                print(f"VM '{name}' is already running.")
            else:
                self.vms[name]['status'] = "Running"
                print(f"Starting VM '{name}'...")
                time.sleep(2)
                print(f"VM '{name}' is now running.")
        else:
            print(f"Error: VM '{name}' not found.")

    def stop_vm(self, name: str) -> None:
        if name in self.vms:
            if self.vms[name]['status'] == "Stopped":
                print(f"VM '{name}' is already stopped.")
            else:
                self.vms[name]['status'] = "Stopped"
                print(f"Stopping VM '{name}'...")
                time.sleep(2)
                print(f"VM '{name}' has been stopped.")
        else:
            print(f"Error: VM '{name}' not found.")

    def create_vm(self, name: str, cpu: int, ram: int, hdd: int, vm_type: str) -> None:
        if name in self.vms:
            print(f"Error: VM '{name}' already exists.")
        else:
            self.vms[name] = {"status": "Stopped", "cpu": cpu, "ram": ram, "hdd": hdd, "type": vm_type}
            print(f"VM '{name}' created successfully.")

    def delete_vm(self, name: str) -> None:
        if name in self.vms:
            del self.vms[name]
            print(f"VM '{name}' deleted successfully.")
        else:
            print(f"Error: VM '{name}' not found.")

    def start_container(self, name: str) -> None:
        if name in self.containers:
            if self.containers[name]['status'] == "Running":
                print(f"Container '{name}' is already running.")
            else:
                self.containers[name]['status'] = "Running"
                print(f"Starting container '{name}'...")
                time.sleep(1)
                print(f"Container '{name}' is now running.")
        else:
            print(f"Error: Container '{name}' not found.")

    def stop_container(self, name: str) -> None:
        if name in self.containers:
            if self.containers[name]['status'] == "Stopped":
                print(f"Container '{name}' is already stopped.")
            else:
                self.containers[name]['status'] = "Stopped"
                print(f"Stopping container '{name}'...")
                time.sleep(1)
                print(f"Container '{name}' has been stopped.")
        else:
            print(f"Error: Container '{name}' not found.")

    def create_container(self, name: str, image: str, container_type: str) -> None:
        if name in self.containers:
            print(f"Error: Container '{name}' already exists.")
        else:
            self.containers[name] = {"status": "Stopped", "image": image, "type": container_type}
            print(f"Container '{name}' created successfully.")

    def delete_container(self, name: str) -> None:
        if name in self.containers:
            del self.containers[name]
            print(f"Container '{name}' deleted successfully.")
        else:
            print(f"Error: Container '{name}' not found.")

    def virt_command(self, args: List[str]) -> None:
        if not args:
            print("Usage: virt <subcommand> [options]")
            return
        subcommand = args[0]
        if subcommand == "list":
            self.list_vms()
        elif subcommand == "start":
            self.start_vm(args[1]) if len(args) > 1 else print("Usage: virt start <vm_name>")
        elif subcommand == "stop":
            self.stop_vm(args[1]) if len(args) > 1 else print("Usage: virt stop <vm_name>")
        else:
            print(f"Unknown virt subcommand: {subcommand}")

    def docker_command(self, args: List[str]) -> None:
        if not args:
            print("Usage: docker <subcommand> [options]")
            return
        subcommand = args[0]
        if subcommand == "ps":
            self.list_containers()
        elif subcommand == "run":
            if len(args) >= 3:
                self.create_container(args[1], args[2], "Docker")
            else:
                print("Usage: docker run <container_name> <image>")
        elif subcommand == "start":
            self.start_container(args[1]) if len(args) > 1 else print("Usage: docker start <container_name>")
        elif subcommand == "stop":
            self.stop_container(args[1]) if len(args) > 1 else print("Usage: docker stop <container_name>")
        else:
            print(f"Unknown docker subcommand: {subcommand}")

    def vagrant_command(self, args: List[str]) -> None:
        if not args:
            print("Usage: vagrant <subcommand> [options]")
            return
        subcommand = args[0]
        if subcommand == "up":
            self.start_vm(args[1]) if len(args) > 1 else print("Usage: vagrant up <vm_name>")
        elif subcommand == "halt":
            self.stop_vm(args[1]) if len(args) > 1 else print("Usage: vagrant halt <vm_name>")
        elif subcommand == "status":
            self.list_vms()
        else:
            print(f"Unknown vagrant subcommand: {subcommand}")

    def virtualbox_command(self, args: List[str]) -> None:
        if not args:
            print("Usage: VBoxManage <subcommand> [options]")
            return
        subcommand = args[0]
        if subcommand == "list":
            self.list_vms()
        elif subcommand == "startvm":
            self.start_vm(args[1]) if len(args) > 1 else print("Usage: VBoxManage startvm <vm_name>")
        elif subcommand == "controlvm":
            if len(args) > 2 and args[2] == "poweroff":
                self.stop_vm(args[1])
            else:
                print("Usage: VBoxManage controlvm <vm_name> poweroff")
        else:
            print(f"Unknown VBoxManage subcommand: {subcommand}")

    def vmware_command(self, args: List[str]) -> None:
        if not args:
            print("Usage: vmrun <subcommand> [options]")
            return
        subcommand = args[0]
        if subcommand == "list":
            self.list_vms()
        elif subcommand == "start":
            self.start_vm(args[1]) if len(args) > 1 else print("Usage: vmrun start <vm_name>")
        elif subcommand == "stop":
            self.stop_vm(args[1]) if len(args) > 1 else print("Usage: vmrun stop <vm_name>")
        else:
            print(f"Unknown vmrun subcommand: {subcommand}")

    def qemu_command(self, args: List[str]) -> None:
        if not args:
            print("Usage: qemu-system-x86_64 [options]")
            return
        if "-name" in args:
            name_index = args.index("-name")
            if name_index + 1 < len(args):
                vm_name = args[name_index + 1]
                self.create_vm(vm_name, 1, 1024, 10, "QEMU")
                self.start_vm(vm_name)
            else:
                print("Usage: qemu-system-x86_64 -name <vm_name> [other options]")
        else:
            print("Usage: qemu-system-x86_64 -name <vm_name> [other options]")

    def lxc_command(self, args: List[str]) -> None:
        if not args:
            print("Usage: lxc <subcommand> [options]")
            return
        subcommand = args[0]
        if subcommand == "list":
            self.list_containers()
        elif subcommand == "start":
            self.start_container(args[1]) if len(args) > 1 else print("Usage: lxc start <container_name>")
        elif subcommand == "stop":
            self.stop_container(args[1]) if len(args) > 1 else print("Usage: lxc stop <container_name>")
        elif subcommand == "create":
            if len(args) >= 3:
                self.create_container(args[1], args[2], "LXC")
            else:
                print("Usage: lxc create <container_name> <template>")
        else:
            print(f"Unknown lxc subcommand: {subcommand}")

class MobileDeviceManager:
   def __init__(self):
       self.devices = {
           "iPhone-001": {"type": "iOS", "os_version": "14.5", "status": "Enrolled"},
           "Galaxy-001": {"type": "Android", "os_version": "11", "status": "Not enrolled"}
       }

   def list_devices(self) -> None:
       print("Device ID       Type     OS Version   Status")
       print("---------------------------------------------")
       for name, info in self.devices.items():
           print(f"{name:<15} {info['type']:<8} {info['os_version']:<12} {info['status']}")

   def enroll_device(self, device_id: str) -> None:
       if device_id in self.devices:
           if self.devices[device_id]['status'] == "Enrolled":
               print(f"Device '{device_id}' is already enrolled.")
           else:
               self.devices[device_id]['status'] = "Enrolled"
               print(f"Enrolling device '{device_id}'...")
               time.sleep(2)
               print(f"Device '{device_id}' has been enrolled successfully.")
       else:
           print(f"Error: Device '{device_id}' not found.")

   def unenroll_device(self, device_id: str) -> None:
       if device_id in self.devices:
           if self.devices[device_id]['status'] == "Not enrolled":
               print(f"Device '{device_id}' is not enrolled.")
           else:
               self.devices[device_id]['status'] = "Not enrolled"
               print(f"Unenrolling device '{device_id}'...")
               time.sleep(2)
               print(f"Device '{device_id}' has been unenrolled successfully.")
       else:
           print(f"Error: Device '{device_id}' not found.")

   def configure_email(self, device_id: str, email: str) -> None:
       if device_id in self.devices:
           print(f"Configuring email for device '{device_id}'...")
           print(f"Setting up email account: {email}")
           time.sleep(2)
           print("Email configuration complete.")
       else:
           print(f"Error: Device '{device_id}' not found.")

   def troubleshoot_device(self, device_id: str) -> None:
       if device_id in self.devices:
           print(f"Troubleshooting device '{device_id}'...")
           print("1. Checking device connectivity...")
           time.sleep(1)
           print("2. Verifying MDM enrollment status...")
           time.sleep(1)
           print("3. Checking for available updates...")
           time.sleep(1)
           print("4. Analyzing device logs...")
           time.sleep(1)
           print("Troubleshooting complete. No issues found.")
       else:
           print(f"Error: Device '{device_id}' not found.")

class CloudServiceManager:
   def __init__(self):
       self.services = {
           "AWS-EC2-1": {"type": "Compute", "status": "Running", "region": "us-west-2"},
           "Azure-Blob-1": {"type": "Storage", "status": "Available", "region": "eastus"}
       }

   def list_services(self) -> None:
       print("Service Name    Type     Status     Region")
       print("-------------------------------------------")
       for name, info in self.services.items():
           print(f"{name:<15} {info['type']:<8} {info['status']:<10} {info['region']}")

   def start_service(self, name: str) -> None:
       if name in self.services:
           if self.services[name]['status'] == "Running":
               print(f"Service '{name}' is already running.")
           else:
               self.services[name]['status'] = "Running"
               print(f"Starting service '{name}'...")
               time.sleep(2)
               print(f"Service '{name}' is now running.")
       else:
           print(f"Error: Service '{name}' not found.")

   def stop_service(self, name: str) -> None:
       if name in self.services:
           if self.services[name]['status'] == "Stopped":
               print(f"Service '{name}' is already stopped.")
           else:
               self.services[name]['status'] = "Stopped"
               print(f"Stopping service '{name}'...")
               time.sleep(2)
               print(f"Service '{name}' has been stopped.")
       else:
           print(f"Error: Service '{name}' not found.")

   def create_storage(self, name: str, region: str) -> None:
       if name in self.services:
           print(f"Error: Service '{name}' already exists.")
       else:
           self.services[name] = {"type": "Storage", "status": "Available", "region": region}
           print(f"Storage service '{name}' created successfully in region {region}.")

   def sync_files(self, local_path: str, cloud_path: str) -> None:
       print(f"Syncing files from {local_path} to {cloud_path}...")
       time.sleep(2)
       print("File synchronization complete.")

class RemoteAccessManager:
    def __init__(self):
        self.rdp_sessions = {
            "user1": {
                "status": "Connected",
                "ip": "192.168.1.100",
                "port": 3389,
                "encryption": "TLS 1.2",
                "color_depth": "32-bit",
                "resolution": "1920x1080"
            },
            "user2": {
                "status": "Disconnected",
                "ip": "192.168.1.101",
                "port": 3389,
                "encryption": "TLS 1.3",
                "color_depth": "16-bit",
                "resolution": "1280x720"
            }
        }
        self.vpn_connections = {
            "office-vpn": {
                "status": "Connected",
                "protocol": "OpenVPN",
                "encryption": "AES-256",
                "auth_method": "Certificate",
                "tunnel_type": "Full Tunnel",
                "ip_assignment": "Dynamic"
            },
            "branch-vpn": {
                "status": "Disconnected",
                "protocol": "IPSec",
                "encryption": "3DES",
                "auth_method": "Pre-shared Key",
                "tunnel_type": "Split Tunnel",
                "ip_assignment": "Static"
            }
        }

    def connect_vpn(self, vpn_name, protocol, encryption, auth_method, tunnel_type, ip_assignment):
        if vpn_name in self.vpn_connections:
            self.vpn_connections[vpn_name] = {
                "status": "Connected",
                "protocol": protocol,
                "encryption": encryption,
                "auth_method": auth_method,
                "tunnel_type": tunnel_type,
                "ip_assignment": ip_assignment
            }
            return f"VPN {vpn_name} connected successfully."
        else:
            return f"VPN {vpn_name} not found."

    def disconnect_vpn(self, vpn_name):
        if vpn_name in self.vpn_connections:
            self.vpn_connections[vpn_name]["status"] = "Disconnected"
            return f"VPN {vpn_name} disconnected successfully."
        else:
            return f"VPN {vpn_name} not found."

    def start_rdp_session(self, username, ip, port=3389, encryption="TLS 1.2", color_depth="32-bit", resolution="1920x1080"):
        if username in self.rdp_sessions:
            self.rdp_sessions[username] = {
                "status": "Connected",
                "ip": ip,
                "port": port,
                "encryption": encryption,
                "color_depth": color_depth,
                "resolution": resolution
            }
            return f"RDP session for {username} started successfully."
        else:
            return f"User {username} not found."

    def end_rdp_session(self, username):
        if username in self.rdp_sessions:
            self.rdp_sessions[username]["status"] = "Disconnected"
            return f"RDP session for {username} ended successfully."
        else:
            return f"User {username} not found."

    def get_vpn_status(self, vpn_name):
        if vpn_name in self.vpn_connections:
            return self.vpn_connections[vpn_name]
        else:
            return f"VPN {vpn_name} not found."

    def get_rdp_status(self, username):
        if username in self.rdp_sessions:
            return self.rdp_sessions[username]
        else:
            return f"User {username} not found."

    def list_all_connections(self):
        return {
            "VPN Connections": self.vpn_connections,
            "RDP Sessions": self.rdp_sessions
        }

    def list_rdp_sessions(self) -> None:
       print("Username    Status        IP Address")
       print("---------------------------------------")
       for name, info in self.rdp_sessions.items():
           print(f"{name:<12} {info['status']:<13} {info['ip']}")

    def connect_rdp(self, username: str, ip: str) -> None:
       if username in self.rdp_sessions:
           print(f"Error: RDP session for '{username}' already exists.")
       else:
           self.rdp_sessions[username] = {"status": "Connected", "ip": ip}
           print(f"Connecting to {ip} as {username}...")
           time.sleep(2)
           print(f"RDP session established for {username}.")

    def disconnect_rdp(self, username: str) -> None:
       if username in self.rdp_sessions:
           del self.rdp_sessions[username]
           print(f"Disconnecting RDP session for {username}...")
           time.sleep(1)
           print(f"RDP session for {username} has been disconnected.")
       else:
           print(f"Error: No active RDP session found for '{username}'.")

    def list_vpn_connections(self) -> None:
       print("VPN Name     Status        Protocol")
       print("---------------------------------------")
       for name, info in self.vpn_connections.items():
           print(f"{name:<12} {info['status']:<13} {info['protocol']}")

    def connect_vpn(self, name: str) -> None:
       if name in self.vpn_connections:
           if self.vpn_connections[name]['status'] == "Connected":
               print(f"VPN '{name}' is already connected.")
           else:
               self.vpn_connections[name]['status'] = "Connected"
               print(f"Connecting to VPN '{name}'...")
               time.sleep(2)
               print(f"VPN connection '{name}' established.")
       else:
           print(f"Error: VPN '{name}' not found.")

    def disconnect_vpn(self, name: str) -> None:
       if name in self.vpn_connections:
           if self.vpn_connections[name]['status'] == "Disconnected":
               print(f"VPN '{name}' is already disconnected.")
           else:
               self.vpn_connections[name]['status'] = "Disconnected"
               print(f"Disconnecting from VPN '{name}'...")
               time.sleep(1)
               print(f"VPN connection '{name}' has been terminated.")
       else:
           print(f"Error: VPN '{name}' not found.")

class SOHONetworkManager:
    def __init__(self):
        self.devices = {
            "Router": {"type": "Router", "ip": "192.168.1.1", "status": "Online", "mac": "00:11:22:33:44:55"},
            "Switch": {"type": "Switch", "ip": "192.168.1.2", "status": "Online", "mac": "AA:BB:CC:DD:EE:FF"},
            "AP-1": {"type": "Access Point", "ip": "192.168.1.3", "status": "Online", "mac": "11:22:33:44:55:66"}
        }
        self.dhcp_pool = {"start": "192.168.1.100", "end": "192.168.1.200"}
        self.dns_servers = ["8.8.8.8", "8.8.4.4"]
        self.firewall_rules = []
        self.port_forwarding_rules = []
        self.dmz_host = None
        self.vlans = {}
        self.wifi_config = {
            "ssid": "DefaultSSID",
            "password": "DefaultPassword",
            "security": "WPA2",
            "channel": 6,
            "band": "2.4GHz"
        }

    def list_devices(self) -> None:
        print("Device Name   Type           IP Address     Status       MAC Address")
        print("--------------------------------------------------------------------")
        for name, info in self.devices.items():
            print(f"{name:<13} {info['type']:<14} {info['ip']:<14} {info['status']:<12} {info['mac']}")

    def add_device(self, name: str, device_type: str, ip: str, mac: str) -> None:
        self.devices[name] = {"type": device_type, "ip": ip, "status": "Online", "mac": mac}
        print(f"Added {device_type} '{name}' to the network.")

    def remove_device(self, name: str) -> None:
        if name in self.devices:
            del self.devices[name]
            print(f"Removed device '{name}' from the network.")
        else:
            print(f"Device '{name}' not found in the network.")

    def configure_router(self, ssid: str, password: str) -> None:
        print(f"Configuring router...")
        print(f"Setting SSID: {ssid}")
        print(f"Setting password: {'*' * len(password)}")
        time.sleep(2)
        print("Router configuration complete.")

    def configure_port_forwarding(self, external_port: int, internal_ip: str, internal_port: int, protocol: str) -> None:
        rule = f"{external_port} -> {internal_ip}:{internal_port} ({protocol})"
        self.port_forwarding_rules.append(rule)
        print(f"Port forwarding rule added: {rule}")

    def configure_dmz(self, dmz_host_ip: str) -> None:
        self.dmz_host = dmz_host_ip
        print(f"DMZ host set to: {dmz_host_ip}")

    def configure_switch(self, vlan: int, ports: List[int]) -> None:
        print(f"Configuring switch...")
        print(f"Creating VLAN {vlan}")
        print(f"Assigning ports {', '.join(map(str, ports))} to VLAN {vlan}")
        time.sleep(2)
        print("Switch configuration complete.")

    def configure_vlan(self, vlan_id: int, vlan_name: str, ports: List[int]) -> None:
        self.vlans[vlan_id] = {"name": vlan_name, "ports": ports}
        print(f"VLAN {vlan_id} '{vlan_name}' configured with ports: {', '.join(map(str, ports))}")

    def configure_dhcp(self, start_ip: str, end_ip: str) -> None:
        self.dhcp_pool["start"] = start_ip
        self.dhcp_pool["end"] = end_ip
        print(f"DHCP pool configured: {start_ip} - {end_ip}")

    def configure_dns(self, primary_dns: str, secondary_dns: str) -> None:
        self.dns_servers = [primary_dns, secondary_dns]
        print(f"DNS servers configured: Primary - {primary_dns}, Secondary - {secondary_dns}")

    def add_firewall_rule(self, rule: str) -> None:
        self.firewall_rules.append(rule)
        print(f"Firewall rule added: {rule}")

    def configure_wifi(self, ssid: str, password: str, security: str, channel: int, band: str) -> None:
        self.wifi_config = {
            "ssid": ssid,
            "password": password,
            "security": security,
            "channel": channel,
            "band": band
        }
        print(f"Wi-Fi configured: SSID: {ssid}, Security: {security}, Channel: {channel}, Band: {band}")

    def troubleshoot_network(self) -> None:
        print("Troubleshooting SOHO network...")
        print("1. Checking internet connectivity...")
        time.sleep(1)
        print("2. Verifying router configuration...")
        time.sleep(1)
        print("3. Testing Wi-Fi signal strength...")
        time.sleep(1)
        print("4. Checking for IP conflicts...")
        time.sleep(1)
        print("5. Analyzing network traffic...")
        time.sleep(1)
        print("Troubleshooting complete. No major issues found.")

    def update_firmware(self, device_name: str) -> None:
        if device_name in self.devices:
            print(f"Updating firmware for {device_name}...")
            time.sleep(3)
            print(f"Firmware update complete for {device_name}.")
        else:
            print(f"Device '{device_name}' not found in the network.")

    def run_speed_test(self) -> Dict[str, float]:
        print("Running network speed test...")
        time.sleep(3)
        download_speed = round(random.uniform(50, 100), 2)
        upload_speed = round(random.uniform(10, 50), 2)
        ping = round(random.uniform(5, 30), 2)
        print(f"Download: {download_speed} Mbps")
        print(f"Upload: {upload_speed} Mbps")
        print(f"Ping: {ping} ms")
        return {"download": download_speed, "upload": upload_speed, "ping": ping}

    def backup_config(self) -> None:
        print("Backing up network configuration...")
        time.sleep(2)
        print("Network configuration backup completed.")

    def restore_config(self) -> None:
        print("Restoring network configuration from backup...")
        time.sleep(2)
        print("Network configuration restored successfully.")

    def scan_for_vulnerabilities(self) -> None:
        print("Scanning network for vulnerabilities...")
        time.sleep(3)
        print("Vulnerability scan complete. No critical issues found.")

    def display_network_topology(self) -> None:
        print("Network Topology:")
        print("Internet")
        print("   |")
        print("Router")
        print("   |")
        print("Switch")
        print(" /    \\")
        print("AP-1  Other Devices")

    def display_vlan_config(self) -> None:
        print("VLAN Configuration:")
        for vlan_id, vlan_info in self.vlans.items():
            print(f"VLAN {vlan_id} - {vlan_info['name']}:")
            print(f"  Ports: {', '.join(map(str, vlan_info['ports']))}")

    def display_router_config(self) -> None:
        print("Router Configuration:")
        print(f"Port Forwarding Rules:")
        for rule in self.port_forwarding_rules:
            print(f"  {rule}")
        print(f"DMZ Host: {self.dmz_host if self.dmz_host else 'Not configured'}")
        print(f"Wi-Fi Configuration:")
        for key, value in self.wifi_config.items():
            print(f"  {key}: {value}")

class LicensingManager:
   def __init__(self):
       self.licenses = {
           "Windows 10 Pro": {"key": "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX", "status": "Activated"},
           "Office 365": {"key": "YYYYY-YYYYY-YYYYY-YYYYY-YYYYY", "status": "Not Activated"}
       }

   def list_licenses(self) -> None:
       print("Software         License Key                      Status")
       print("----------------------------------------------------------")
       for name, info in self.licenses.items():
           print(f"{name:<16} {info['key']:<30} {info['status']}")

   def activate_license(self, software: str) -> None:
       if software in self.licenses:
           if self.licenses[software]['status'] == "Activated":
               print(f"{software} is already activated.")
           else:
               print(f"Activating {software}...")
               time.sleep(2)
               self.licenses[software]['status'] = "Activated"
               print(f"{software} has been successfully activated.")
       else:
           print(f"Error: No license found for {software}.")

   def deactivate_license(self, software: str) -> None:
       if software in self.licenses:
           if self.licenses[software]['status'] == "Not Activated":
               print(f"{software} is not currently activated.")
           else:
               print(f"Deactivating {software}...")
               time.sleep(2)
               self.licenses[software]['status'] = "Not Activated"
               print(f"{software} has been deactivated.")
       else:
           print(f"Error: No license found for {software}.")

class EnvironmentalControlManager:
   def __init__(self):
       self.temperature = 22.0  # in Celsius
       self.humidity = 45.0  # in percentage
       self.power_status = "Normal"

   def get_environmental_status(self) -> None:
       print(f"Current Temperature: {self.temperature}°C")
       print(f"Current Humidity: {self.humidity}%")
       print(f"Power Status: {self.power_status}")

   def set_temperature(self, temp: float) -> None:
       self.temperature = temp
       print(f"Temperature set to {self.temperature}°C")

   def set_humidity(self, humidity: float) -> None:
       self.humidity = humidity
       print(f"Humidity set to {self.humidity}%")

   def simulate_power_outage(self) -> None:
       print("Simulating power outage...")
       self.power_status = "Outage"
       time.sleep(2)
       print("Power outage detected. Switching to backup power.")
       time.sleep(2)
       self.power_status = "Backup"
       print("System running on backup power.")

   def restore_power(self) -> None:
       if self.power_status != "Normal":
           print("Restoring main power...")
           time.sleep(2)
           self.power_status = "Normal"
           print("Main power restored. Switching from backup power.")
       else:
           print("Power is already functioning normally.")

class DocumentationManager:
   def __init__(self):
       self.documents = {
           "Network Diagram": "network_diagram.pdf",
           "Disaster Recovery Plan": "disaster_recovery.docx",
           "User Manual": "user_manual.pdf"
       }

   def list_documents(self) -> None:
       print("Available Documentation:")
       for doc, filename in self.documents.items():
           print(f"- {doc}: {filename}")

   def view_document(self, doc_name: str) -> None:
       if doc_name in self.documents:
           print(f"Opening {doc_name}...")
           print(f"Content of {self.documents[doc_name]}:")
           print("-----------------------------")
           print("This is a simulated document content.")
           print("In a real system, this would open the actual document.")
           print("-----------------------------")
       else:
           print(f"Error: Document '{doc_name}' not found.")

   def create_document(self, doc_name: str, filename: str) -> None:
       if doc_name in self.documents:
           print(f"Error: Document '{doc_name}' already exists.")
       else:
           self.documents[doc_name] = filename
           print(f"Document '{doc_name}' created with filename '{filename}'.")

   def update_document(self, doc_name: str) -> None:
       if doc_name in self.documents:
           print(f"Updating {doc_name}...")
           print("Please enter the new content (type 'END' on a new line to finish):")
           content = []
           while True:
               line = input()
               if line == "END":
                   break
               content.append(line)
           print(f"Document '{doc_name}' has been updated.")
       else:
           print(f"Error: Document '{doc_name}' not found.")

class DisasterRecoveryManager:
   def __init__(self):
       self.backup_status = "No recent backup"
       self.last_backup_date = None
       self.recovery_points = []

   def perform_backup(self) -> None:
       print("Initiating system backup...")
       for i in range(5):
           print(f"Backing up data: {i*20}% complete")
           time.sleep(1)
       self.backup_status = "Backup complete"
       self.last_backup_date = datetime.now()
       self.recovery_points.append(self.last_backup_date)
       print(f"Backup completed successfully at {self.last_backup_date}")

   def restore_from_backup(self, recovery_point: datetime) -> None:
       if recovery_point in self.recovery_points:
           print(f"Initiating system restore from backup point: {recovery_point}")
           for i in range(5):
               print(f"Restoring data: {i*20}% complete")
               time.sleep(1)
           print("System restore completed successfully.")
       else:
           print(f"Error: No recovery point found for {recovery_point}")

   def get_backup_status(self) -> None:
       print(f"Current Backup Status: {self.backup_status}")
       if self.last_backup_date:
           print(f"Last Backup Performed: {self.last_backup_date}")
       print("Available Recovery Points:")
       for point in self.recovery_points:
           print(f"- {point}")

   def create_disaster_recovery_plan(self) -> None:
       print("Creating Disaster Recovery Plan...")
       print("1. Identifying critical systems and data")
       time.sleep(1)
       print("2. Defining recovery time objectives (RTO) and recovery point objectives (RPO)")
       time.sleep(1)
       print("3. Establishing backup and recovery procedures")
       time.sleep(1)
       print("4. Defining roles and responsibilities")
       time.sleep(1)
       print("5. Creating communication plans")
       time.sleep(1)
       print("Disaster Recovery Plan created successfully.")

class AccessibilityManager:
   def __init__(self):
       self.features = {
           "Screen Reader": False,
           "High Contrast": False,
           "Magnifier": False,
           "On-Screen Keyboard": False
       }

   def list_features(self) -> None:
       print("Accessibility Features:")
       for feature, status in self.features.items():
           print(f"- {feature}: {'Enabled' if status else 'Disabled'}")

   def toggle_feature(self, feature: str) -> None:
       if feature in self.features:
           self.features[feature] = not self.features[feature]
           status = "enabled" if self.features[feature] else "disabled"
           print(f"{feature} has been {status}.")
       else:
           print(f"Error: Feature '{feature}' not found.")

   def configure_screen_reader(self) -> None:
       if self.features["Screen Reader"]:
           print("Configuring Screen Reader...")
           print("1. Adjusting speech rate")
           time.sleep(1)
           print("2. Setting voice preference")
           time.sleep(1)
           print("3. Customizing reading order")
           time.sleep(1)
           print("Screen Reader configuration complete.")
       else:
           print("Error: Screen Reader is not enabled. Please enable it first.")

   def set_high_contrast_theme(self, theme: str) -> None:
       if self.features["High Contrast"]:
           print(f"Setting High Contrast theme to {theme}...")
           time.sleep(1)
           print(f"High Contrast theme {theme} applied successfully.")
       else:
           print("Error: High Contrast is not enabled. Please enable it first.")

class ScriptingEnvironment:
   def __init__(self):
       self.batch_scripts = {}
       self.powershell_scripts = {}

   def create_batch_script(self, name: str) -> None:
       print(f"Creating batch script '{name}'...")
       print("Enter the script content (type 'END' on a new line to finish):")
       content = []
       while True:
           line = input()
           if line == "END":
               break
           content.append(line)
       self.batch_scripts[name] = "\n".join(content)
       print(f"Batch script '{name}' created successfully.")

   def run_batch_script(self, name: str) -> None:
       if name in self.batch_scripts:
           print(f"Running batch script '{name}'...")
           print("Script output:")
           print("-----------------------------")
           for line in self.batch_scripts[name].split("\n"):
               print(f">{line}")
               time.sleep(0.5)
           print("-----------------------------")
           print("Batch script execution complete.")
       else:
           print(f"Error: Batch script '{name}' not found.")

   def create_powershell_script(self, name: str) -> None:
       print(f"Creating PowerShell script '{name}'...")
       print("Enter the script content (type 'END' on a new line to finish):")
       content = []
       while True:
           line = input()
           if line == "END":
               break
           content.append(line)
       self.powershell_scripts[name] = "\n".join(content)
       print(f"PowerShell script '{name}' created successfully.")

   def run_powershell_script(self, name: str) -> None:
       if name in self.powershell_scripts:
           print(f"Running PowerShell script '{name}'...")
           print("Script output:")
           print("-----------------------------")
           for line in self.powershell_scripts[name].split("\n"):
               print(f">{line}")
               time.sleep(0.5)
           print("-----------------------------")
           print("PowerShell script execution complete.")
       else:
           print(f"Error: PowerShell script '{name}' not found.")

class TroubleshootingScenarios:
   def __init__(self):
       self.scenarios = {
           "slow_network": self.slow_network_scenario,
           "blue_screen": self.blue_screen_scenario,
           "software_conflict": self.software_conflict_scenario
       }

   def run_scenario(self, scenario_name: str) -> None:
       if scenario_name in self.scenarios:
           self.scenarios[scenario_name]()
       else:
           print(f"Error: Scenario '{scenario_name}' not found.")

   def slow_network_scenario(self) -> None:
       print("Scenario: Slow Network Connection")
       print("A user reports that their internet connection is unusually slow.")
       print("Steps to troubleshoot:")
       steps = [
           "Check physical network connections",
           "Run a speed test to quantify the issue",
           "Verify if the problem affects all devices or just one",
           "Check for background downloads or updates",
           "Restart the router and modem",
           "Contact the ISP if the problem persists"
       ]
       for i, step in enumerate(steps, 1):
           input(f"Press Enter to proceed with step {i}")
           print(f"Step {i}: {step}")
           time.sleep(1)
       print("Scenario complete. The network speed has been restored.")

   def blue_screen_scenario(self) -> None:
       print("Scenario: Blue Screen of Death (BSOD)")
       print("A Windows 10 computer is repeatedly showing a blue screen with error code: IRQL_NOT_LESS_OR_EQUAL")
       print("Steps to troubleshoot:")
       steps = [
           "Record the exact error message and code",
           "Check for recent hardware or software changes",
           "Boot into Safe Mode",
           "Update or rollback device drivers",
           "Run Windows Memory Diagnostic tool",
           "Perform a system restore to a point before the issue started",
           "If all else fails, consider reinstalling Windows"
       ]
       for i, step in enumerate(steps, 1):
           input(f"Press Enter to proceed with step {i}")
           print(f"Step {i}: {step}")
           time.sleep(1)
       print("Scenario complete. The BSOD issue has been resolved.")

   def software_conflict_scenario(self) -> None:
       print("Scenario: Software Conflict")
       print("After installing a new application, other programs are crashing randomly.")
       print("Steps to troubleshoot:")
       steps = [
           "Identify the newly installed application",
           "Check system and application logs for error messages",
           "Temporarily uninstall the new application to see if it resolves the issue",
           "Update all affected applications to their latest versions",
           "Run a malware scan to rule out infection",
           "Use System Restore to revert to a point before the new application was installed",
           "If the issue persists, consider clean installing the operating system"
       ]
       for i, step in enumerate(steps, 1):
           input(f"Press Enter to proceed with step {i}")
           print(f"Step {i}: {step}")
           time.sleep(1)
       print("Scenario complete. The software conflict has been resolved.")

class OSInstallationManager:
   def __init__(self):
       self.installation_status = "Not started"
       self.current_step = 0
       self.total_steps = 10

   def start_installation(self, os_type: str) -> None:
       print(f"Starting {os_type} installation...")
       self.installation_status = "In progress"
       self.current_step = 0
       self.total_steps = 10

       steps = [
           "Preparing installation media",
           "Booting from installation media",
           "Selecting language and region",
           "Accepting license terms",
           "Choosing installation type (clean install or upgrade)",
           "Partitioning the disk",
           "Copying files",
           "Installing features and updates",
           "Configuring settings",
           "Finalizing installation"
       ]

       for step in steps:
           self.current_step += 1
           print(f"Step {self.current_step}/{self.total_steps}: {step}")
           time.sleep(2)  # Simulating the time taken for each step

       self.installation_status = "Completed"
       print(f"{os_type} installation completed successfully.")

   def upgrade_os(self, current_os: str, target_os: str) -> None:
       print(f"Starting upgrade from {current_os} to {target_os}...")
       self.installation_status = "Upgrade in progress"
       self.current_step = 0
       self.total_steps = 8

       steps = [
           "Checking system compatibility",
           "Downloading upgrade files",
           "Preparing for upgrade",
           "Backing up current system",
           "Installing new OS files",
           "Migrating user data and settings",
           "Installing updates",
           "Finalizing upgrade"
       ]

       for step in steps:
           self.current_step += 1
           print(f"Step {self.current_step}/{self.total_steps}: {step}")
           time.sleep(2)  # Simulating the time taken for each step

       self.installation_status = "Upgrade completed"
       print(f"Upgrade to {target_os} completed successfully.")

   def get_installation_status(self) -> None:
       print(f"Installation Status: {self.installation_status}")
       if self.installation_status == "In progress":
           print(f"Current Step: {self.current_step}/{self.total_steps}")

class NetworkSecurityManager:
    def __init__(self):
        self.firewall_rules: List[Dict[str, Union[str, int]]] = [
            {"name": "Allow_HTTP", "protocol": "TCP", "port": 80, "source_ip": "Any", "destination_ip": "Any", "action": "Allow"},
            {"name": "Block_FTP", "protocol": "TCP", "port": 21, "source_ip": "Any", "destination_ip": "Any", "action": "Block"}
        ]
        self.antivirus_status: str = "Enabled"
        self.last_scan_date: Union[datetime, None] = None
        self.ids_status: str = "Enabled"
        self.ids_log: List[str] = []
        self.vpn_status: str = "Disconnected"
        self.encrypted_drives: List[str] = []

    def list_firewall_rules(self) -> List[Dict[str, Union[str, int]]]:
        return self.firewall_rules

    def add_firewall_rule(self, name: str, protocol: str, port: int, source_ip: str, destination_ip: str, action: str) -> bool:
        if any(rule['name'] == name for rule in self.firewall_rules):
            raise ValueError(f"Firewall rule with name '{name}' already exists.")
        if protocol not in ['TCP', 'UDP']:
            raise ValueError("Protocol must be either 'TCP' or 'UDP'.")
        if not 0 <= port <= 65535:
            raise ValueError("Port must be between 0 and 65535.")
        if action not in ['Allow', 'Block']:
            raise ValueError("Action must be either 'Allow' or 'Block'.")

        new_rule = {
            "name": name,
            "protocol": protocol,
            "port": port,
            "source_ip": source_ip,
            "destination_ip": destination_ip,
            "action": action
        }
        self.firewall_rules.append(new_rule)
        return True

    def remove_firewall_rule(self, name: str) -> bool:
        initial_length = len(self.firewall_rules)
        self.firewall_rules = [rule for rule in self.firewall_rules if rule['name'] != name]
        return len(self.firewall_rules) < initial_length

    def run_antivirus_scan(self) -> Dict[str, Union[str, int]]:
        scan_result = {"status": "Completed", "threats_found": 0}
        for _ in range(5):
            time.sleep(0.5)  # Simulating scan time
        self.last_scan_date = datetime.now()
        return scan_result

    def get_antivirus_status(self) -> Dict[str, Union[str, datetime]]:
        return {
            "status": self.antivirus_status,
            "last_scan_date": self.last_scan_date
        }

    def toggle_ids(self, enable: bool) -> str:
        self.ids_status = "Enabled" if enable else "Disabled"
        return self.ids_status

    def simulate_network_traffic(self) -> List[str]:
        traffic_types = [
            "Normal HTTP traffic",
            "Potential port scan",
            "Suspicious SSH login attempt",
            "Normal HTTPS traffic",
            "Potential DDoS attack"
        ]
        
        detected_traffic = []
        for _ in range(5):
            traffic = random.choice(traffic_types)
            detected_traffic.append(traffic)
            if self.ids_status == "Enabled" and ("Potential" in traffic or "Suspicious" in traffic):
                self.ids_log.append(f"{datetime.now()}: {traffic}")
        
        return detected_traffic

    def get_ids_log(self) -> List[str]:
        return self.ids_log

    def connect_vpn(self, server: str) -> str:
        self.vpn_status = f"Connected to {server}"
        return self.vpn_status

    def disconnect_vpn(self) -> str:
        self.vpn_status = "Disconnected"
        return self.vpn_status

    def encrypt_drive(self, drive_name: str) -> bool:
        if drive_name in self.encrypted_drives:
            return False
        self.encrypted_drives.append(drive_name)
        return True

    def decrypt_drive(self, drive_name: str) -> bool:
        if drive_name not in self.encrypted_drives:
            return False
        self.encrypted_drives.remove(drive_name)
        return True

    def get_encrypted_drives(self) -> List[str]:
        return self.encrypted_drives

    def update_antivirus_definitions(self) -> str:
        # Simulating update process
        time.sleep(2)
        return "Antivirus definitions updated successfully."

    def configure_email_filtering(self, spam_threshold: float) -> Dict[str, Union[str, float]]:
        if not 0 <= spam_threshold <= 1:
            raise ValueError("Spam threshold must be between 0 and 1.")
        return {"status": "Configured", "spam_threshold": spam_threshold}

class UserAccountControlSimulator:
   def __init__(self):
       self.uac_level = "Default"

   def prompt_for_elevation(self, action: str) -> bool:
       print(f"User Account Control")
       print(f"Do you want to allow the following program to make changes to this computer?")
       print(f"Program: {action}")
       response = input("Allow (Y/N)? ").strip().lower()
       return response == 'y'

   def change_uac_level(self, level: str) -> None:
       valid_levels = ["Never notify", "Default", "Always notify"]
       if level in valid_levels:
           self.uac_level = level
           print(f"UAC level changed to: {level}")
       else:
           print(f"Invalid UAC level. Valid levels are: {', '.join(valid_levels)}")

   def get_uac_status(self) -> None:
       print(f"Current UAC Level: {self.uac_level}")

class RAIDManager:
   def __init__(self):
       self.raid_configs = {
           "RAID0": {"disks": ["Disk1", "Disk2"], "status": "Healthy"},
           "RAID1": {"disks": ["Disk3", "Disk4"], "status": "Degraded"}
       }

   def list_raid_configs(self) -> None:
       print("RAID Configurations:")
       for raid, info in self.raid_configs.items():
           print(f"{raid}: Disks: {', '.join(info['disks'])} - Status: {info['status']}")

   def create_raid(self, raid_type: str, disks: List[str]) -> None:
       if raid_type in ["RAID0", "RAID1", "RAID5", "RAID10"]:
           self.raid_configs[raid_type] = {"disks": disks, "status": "Healthy"}
           print(f"{raid_type} created with disks: {', '.join(disks)}")
       else:
           print(f"Unsupported RAID type: {raid_type}")

   def delete_raid(self, raid_type: str) -> None:
       if raid_type in self.raid_configs:
           del self.raid_configs[raid_type]
           print(f"{raid_type} configuration deleted")
       else:
           print(f"RAID configuration not found: {raid_type}")

   def check_raid_status(self, raid_type: str) -> None:
       if raid_type in self.raid_configs:
           print(f"Checking {raid_type} status...")
           time.sleep(2)
           print(f"Status: {self.raid_configs[raid_type]['status']}")
       else:
           print(f"RAID configuration not found: {raid_type}")

class CommandInterpreter:
   def __init__(self):
       self.file_system = VirtualFileSystem()
       self.network = NetworkSimulator()
       self.system_info = SystemInfo()
       self.process_manager = ProcessManager()
       self.disk_manager = DiskManager()
       self.security_manager = SecurityManager()
       self.performance_monitor = PerformanceMonitor()
       self.printer_manager = PrinterManager()
       self.virtualization_manager = VirtualizationManager()
       self.mobile_device_manager = MobileDeviceManager()
       self.cloud_service_manager = CloudServiceManager()
       self.remote_access_manager = RemoteAccessManager()
       self.soho_network_manager = SOHONetworkManager()
       self.licensing_manager = LicensingManager()
       self.environmental_control_manager = EnvironmentalControlManager()
       self.documentation_manager = DocumentationManager()
       self.disaster_recovery_manager = DisasterRecoveryManager()
       self.accessibility_manager = AccessibilityManager()
       self.scripting_environment = ScriptingEnvironment()
       self.troubleshooting_scenarios = TroubleshootingScenarios()
       self.os_installation_manager = OSInstallationManager()
       self.network_security_manager = NetworkSecurityManager()
       self.uac_simulator = UserAccountControlSimulator()
       self.raid_manager = RAIDManager()
       self.hardware_simulator = HardwareSimulator()
       self.user_manager = UserManager()

   def execute_command(self, command: str) -> bool:
    parts = command.split()
    cmd = parts[0].lower()
    args = parts[1:]

    try:
        if cmd == "exit":
            return False
        elif cmd == "help":
            self.show_help()
        
        # File System Commands
        elif cmd in ["cd", "chdir", "dir", "tree", "cls", "md", "mkdir", "rd", "rmdir", "copy", "move", 
                     "del", "erase", "ren", "rename", "type", "attrib", "find", "findstr", "xcopy", 
                     "robocopy", "comp", "fc", "forfiles", "takeown", "icacls", "compact", "cipher", 
                     "fsutil", "subst", "mklink", "more", "assoc", "expand", "format", "label", "print", 
                     "recover", "replace", "sort", "where"]:
            self.file_system_commands(cmd, args)
        
        # Network Commands
        elif cmd in ["ipconfig", "ping", "tracert", "nslookup", "netstat", "route", "arp", "netsh", "pathping", "telnet", "nbtstat", "getmac", "ipv6_config", "show", "net", "systeminfo", "ftp", "ssh", "nmap", "curl", "wget", "tcpdump", "wireshark", "netdom", "nltest", "ipmonitor", "netdiag", "tcpview", "portqry", "netscan"]:
            self.network_commands(cmd, args)
        
        # System Info Commands
        elif cmd in ["systeminfo", "msinfo32", "dxdiag", "msconfig", "winver", "ver", "gpresult", "whoami", "hostname", "sysinfo", "dmidecode", "lshw", "hwinfo", "lscpu", "lsusb", "lspci"]:
            self.system_info_commands(cmd, args)
        
        # Process Commands
        elif cmd in ["tasklist", "taskkill", "start", "sfc", "wmic", "sc", "shutdown", "runas", "at", "schtasks", "qprocess", "qwinsta", "tskill", "pskill", "psexec", "procexp", "procmon"]:
            self.process_commands(cmd, args)
        
        # Disk Commands
        elif cmd in ["chkdsk", "diskpart", "defrag", "fsutil", "format", "label", "convert", "vssadmin", "diskmgmt", "wbadmin", "imdisk", "diskspd", "ddrescue", "smartctl"]:
            self.disk_commands(cmd, args)
        
        # Security Commands
        elif cmd in ["net", "netplwiz", "change_password", "add_to_group", "remove_from_group", "grant_permission", "revoke_permission", "list_users", "icacls", "cipher", "auditpol", "gpedit.msc", "secedit", "cacls", "wmic", "nltest", "certutil", "manage-bde"]:
            self.security_commands(cmd, args)
        
        # Performance Commands
        elif cmd in ["perfmon", "resmon", "eventvwr", "wmic", "powercfg", "typeperf", "logman", "xperf", "psinfo", "pslist", "pstack", "pmap", "vmstat", "iostat"]:
            self.performance_commands(cmd, args)
        
        # Printer Commands
        elif cmd in ["print", "printmgmt.msc", "add_printer", "remove_printer", "print_test_page", "troubleshoot_printer", "get_printer_status", "set_printer_status", "cancel_print_job", "get_printer_queue", "update_printer_driver"]:
            self.printer_commands(cmd, args)
        
        # Virtualization Commands
        elif cmd in ["virt", "vm", "hyper-v", "docker", "vagrant", "virtualbox", "vmware", "qemu", "lxc"]:
            self.virtualization_commands(cmd, args)
        
        # Mobile Device Commands
        elif cmd in ["mdm"]:
            self.mobile_device_commands(cmd, args)
        
        # Cloud Commands
        elif cmd in ["cloud", "aws", "azure"]:
            self.cloud_commands(cmd, args)
        
        # Remote Access Commands
        elif cmd in ["rdp", "vpn", "list"]:
            self.remote_access_commands(cmd, args)
            
        # SOHO Network Commands
        elif cmd in ["soho", "router", "switch", "dhcp", "dns", "firewall", "wifi", "speedtest"]:
            self.soho_network_commands(cmd, args)
        
        # Licensing Commands
        elif cmd in ["license", "activate", "deactivate"]:
            self.licensing_commands(cmd, args)
        
        # Environmental Commands
        elif cmd in ["temp", "humidity", "power"]:
            self.environmental_commands(cmd, args)
        
        # Documentation Commands
        elif cmd in ["doc", "document"]:
            self.documentation_commands(cmd, args)
        
        # Disaster Recovery Commands
        elif cmd in ["backup", "restore", "disaster"]:
            self.disaster_recovery_commands(cmd, args)
        
        # Accessibility Commands
        elif cmd in ["accessibility", "access"]:
            self.accessibility_commands(cmd, args)
        
        # Scripting Commands
        elif cmd in ["script", "batch", "powershell"]:
            self.scripting_commands(cmd, args)
        
        # Troubleshooting Commands
        elif cmd == "scenario":
            self.run_troubleshooting_scenario(args)
        
        # OS Installation Commands
        elif cmd == "os":
            self.os_installation_commands(cmd, args)
        
        # Network Security Commands
        elif cmd in ["firewall", "antivirus", "ids", "ips", "vpn", "encrypt", "decrypt", "email_filter"]:
            self.network_security_commands(cmd, args)
        
        # UAC Commands
        elif cmd == "uac":
            self.uac_commands(cmd, args)
        
        # Hardware Commands
        elif cmd == "hardware":
            self.hardware_commands(args)
        
        # RAID Commands
        elif cmd == "raid":
            self.raid_commands(cmd, args)
        
        # User Management Commands
        elif cmd == "user":
            self.user_commands(args)
        
        else:
            print(f"Command not recognized: {cmd}")
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return True

   def file_system_commands(self, cmd: str, args: List[str]) -> None:
    try:
        if cmd in ["cd", "chdir"]:
            new_dir = args[0] if args else ""
            self.file_system.change_directory(new_dir)
        elif cmd == "dir":
            options = {}
            path = ""
            for arg in args:
                if arg.startswith("/"):
                    option = arg[1:].lower()
                    if option in ['a', 'b', 'c', 'd', 'l', 'n', 'p', 'q', 's', 'w', 'x']:
                        options[option] = True
                    elif option.startswith('t:'):
                        options['t'] = option[2:]
                    elif option.startswith('o:'):
                        options['o'] = option[2:]
                else:
                    path = arg
            self.file_system.list_directory(path, **options)
        elif cmd == "tree":
            show_files = "/f" in args
            ascii_only = "/a" in args
            path = next((arg for arg in args if not arg.startswith("/")), "")
            self.file_system.tree(path, show_files, ascii_only)
        elif cmd == "cls":
            self.file_system.clear_screen()
        elif cmd in ["md", "mkdir"]:
            self.file_system.create_directory(args[0])
        elif cmd in ["rd", "rmdir"]:
            recursive = "/s" in args
            quiet = "/q" in args
            self.file_system.remove_directory(args[0], recursive, quiet)
        elif cmd == "copy":
            verify = "/v" in args
            args = [arg for arg in args if not arg.startswith("/")]
            if len(args) < 2:
                print("Syntax error. Correct syntax is: copy [/v] source destination")
            else:
                self.file_system.copy_file(args[0], args[1], verify)
        elif cmd == "move":
            self.file_system.move_file(args[0], args[1])
        elif cmd in ["del", "erase"]:
            force = "/f" in args
            quiet = "/q" in args
            recursive = "/s" in args
            file_name = next((arg for arg in args if not arg.startswith("/")), "")
            self.file_system.delete_file(file_name, force, quiet, recursive)
        elif cmd in ["ren", "rename"]:
            self.file_system.rename(args[0], args[1])
        elif cmd == "type":
            self.file_system.type_file(args[0])
        elif cmd == "attrib":
            if len(args) < 2:
                print("Syntax error. Correct syntax is: attrib [+/-][attributes] [filename]")
            else:
                attributes = args[0]
                filename = args[1]
                self.file_system.attrib(filename, attributes)
        elif cmd == "find":
            case_sensitive = "/c" in args
            args = [arg for arg in args if not arg.startswith("/")]
            if len(args) < 2:
                print("Syntax error. Correct syntax is: find [/c] \"string\" [path]")
            else:
                search_string = args[0]
                path = args[1] if len(args) > 1 else ""
                self.file_system.find(search_string, path)
        elif cmd == "findstr":
            case_sensitive = "/c" in args
            line_numbers = "/n" in args
            recursive = "/s" in args
            whole_word = "/w" in args
            quiet = "/q" in args
            exclude_patterns = next((arg[3:].split(',') for arg in args if arg.startswith("/e:")), None)
            args = [arg for arg in args if not arg.startswith("/")]
            if len(args) < 2:
                print("Syntax error. Correct syntax is: findstr [/c] [/n] [/s] [/w] [/q] [/e:exclude_patterns] \"string\" [file_patterns]")
            else:
                search_string = args[0]
                file_patterns = args[1:]
                self.file_system.findstr(search_string, file_patterns, "", case_sensitive, line_numbers, recursive, exclude_patterns, whole_word, quiet)
        elif cmd == "xcopy":
            subdirectories = "/s" in args
            empty_directories = "/e" in args
            overwrite = "/y" in args
            exclude = next((arg[3:].split(',') for arg in args if arg.startswith("/exclude:")), None)
            include = next((arg[3:].split(',') for arg in args if arg.startswith("/include:")), None)
            quiet = "/q" in args
            args = [arg for arg in args if not arg.startswith("/")]
            if len(args) < 2:
                print("Syntax error. Correct syntax is: xcopy [/s] [/e] [/y] [/exclude:file1[+file2]...] [/include:file1[+file2]...] [/q] source destination")
            else:
                self.file_system.xcopy(args[0], args[1], subdirectories, empty_directories, overwrite, exclude, include, quiet)
        elif cmd == "robocopy":
            options = {"/s": "/s" in args, "/e": "/e" in args, "/mir": "/mir" in args}
            args = [arg for arg in args if not arg.startswith("/")]
            if len(args) < 2:
                print("Syntax error. Correct syntax is: robocopy source destination [file [file]...] [options]")
            else:
                source, destination = args[:2]
                files = args[2:] if len(args) > 2 else None
                self.file_system.robocopy(source, destination, files, options)
        elif cmd == "comp":
            line_number = "/n" in args
            number_of_differences = next((int(arg[2:]) for arg in args if arg.startswith("/d:")), None)
            case_sensitive = "/c" not in args
            args = [arg for arg in args if not arg.startswith("/")]
            if len(args) < 2:
                print("Syntax error. Correct syntax is: comp [/n] [/d:n] [/c] file1 file2")
            else:
                self.file_system.comp(args[0], args[1], line_number, number_of_differences, case_sensitive)
        elif cmd == "fc":
            ignore_case = "/c" in args
            ignore_blank_lines = "/w" in args
            line_number = "/n" in args
            brief = "/l" in args
            args = [arg for arg in args if not arg.startswith("/")]
            if len(args) < 2:
                print("Syntax error. Correct syntax is: fc [/c] [/w] [/n] [/l] file1 file2")
            else:
                self.file_system.fc(args[0], args[1], ignore_case, ignore_blank_lines, line_number, brief)
        elif cmd == "forfiles":
            recursive = "/s" in args
            days = next((int(arg[3:]) for arg in args if arg.startswith("/d:")), None)
            min_size = next((int(arg[6:]) for arg in args if arg.startswith("/min:")), None)
            max_size = next((int(arg[6:]) for arg in args if arg.startswith("/max:")), None)
            args = [arg for arg in args if not arg.startswith("/")]
            if len(args) < 2:
                print("Syntax error. Correct syntax is: forfiles [/s] [/p path] [/m searchmask] [/c command] [/d days] [/min:size] [/max:size]")
            else:
                path = next((arg[3:] for arg in args if arg.startswith("/p:")), "")
                include = next((arg[3:] for arg in args if arg.startswith("/m:")), "*")
                exclude = next((arg[3:] for arg in args if arg.startswith("/e:")), "")
                command = next((arg[3:] for arg in args if arg.startswith("/c:")), "")
                self.file_system.forfiles(path, command, include, exclude, recursive, days, min_size, max_size)
        elif cmd == "takeown":
            recursive = "/r" in args
            user = next((arg[3:] for arg in args if arg.startswith("/u:")), None)
            args = [arg for arg in args if not arg.startswith("/")]
            if not args:
                print("Syntax error. Correct syntax is: takeown [/r] [/u:user] /f path")
            else:
                self.file_system.takeown(args[0], recursive, user)
        elif cmd == "icacls":
            recursive = "/t" in args
            quiet = "/q" in args
            args = [arg for arg in args if not arg.startswith("/")]
            if len(args) < 3:
                print("Syntax error. Correct syntax is: icacls path [/grant | /deny] permissions [/t] [/q]")
            else:
                self.file_system.icacls(args[0], args[1], args[2], recursive, quiet)
        elif cmd == "compact":
            compress = "/c" in args
            recursive = "/s" in args
            quiet = "/q" in args
            args = [arg for arg in args if not arg.startswith("/")]
            if not args:
                print("Syntax error. Correct syntax is: compact [/c | /u] [/s] [/q] path")
            else:
                self.file_system.compact(args[0], compress, recursive, quiet)
        elif cmd == "cipher":
            encrypt = "/e" in args
            recursive = "/s" in args
            force = "/f" in args
            args = [arg for arg in args if not arg.startswith("/")]
            if not args:
                print("Syntax error. Correct syntax is: cipher [/e | /d] [/s] [/f] path")
            else:
                self.file_system.cipher(args[0], encrypt, recursive, force)
        elif cmd == "fsutil":
            if len(args) < 2:
                print("Syntax error. Correct syntax is: fsutil [command] [options]")
            else:
                self.file_system.fsutil(args[0], *args[1:])
        elif cmd == "subst":
            if not args:
                print("Syntax error. Correct syntax is: subst [drive: path] or subst drive: /d")
            elif args[-1] == "/d":
                self.file_system.subst(args[0])
            else:
                self.file_system.subst(args[0], args[1])
        elif cmd == "mklink":
            link_type = "file"
            if "/d" in args:
                link_type = "dir"
                args.remove("/d")
            elif "/h" in args:
                link_type = "hardlink"
                args.remove("/h")
            if len(args) < 2:
                print("Syntax error. Correct syntax is: mklink [/d | /h] link target")
            else:
                self.file_system.mklink(args[0], args[1], link_type)
        elif cmd == "more":
            self.file_system.more(args[0])
        elif cmd == "assoc":
            file_extension = args[0] if args else None
            self.file_system.assoc(file_extension)
        elif cmd == "expand":
            if len(args) < 2:
                print("Syntax error. Correct syntax is: expand source destination")
            else:
                self.file_system.expand(args[0], args[1])
        elif cmd == "format":
            drive = args[0]
            file_system = next((arg for arg in args if arg.startswith("/fs:")), "NTFS")
            quick = "/q" in args
            self.file_system.format(drive, file_system, quick)
        elif cmd == "label":
            if len(args) < 1:
                print("Syntax error. Correct syntax is: label [drive:][label]")
            else:
                drive = args[0]
                new_label = args[1] if len(args) > 1 else None
                self.file_system.label(drive, new_label)
        elif cmd == "print":
            self.file_system.print_file(args[0])
        elif cmd == "recover":
            self.file_system.recover(args[0])
        elif cmd == "replace":
            if len(args) < 2:
                print("Syntax error. Correct syntax is: replace source destination")
            else:
                self.file_system.replace(args[0], args[1])
        elif cmd == "sort":
            reverse = "/r" in args
            remove_duplicates = "/u" in args
            args = [arg for arg in args if not arg.startswith("/")]
            if len(args) < 1:
                print("Syntax error. Correct syntax is: sort [/r] [/u] input_file [output_file]")
            else:
                input_file = args[0]
                output_file = args[1] if len(args) > 1 else None
                self.file_system.sort(input_file, output_file, reverse, remove_duplicates)
        elif cmd == "where":
            if len(args) < 1:
                print("Syntax error. Correct syntax is: where [/r path] pattern")
            else:
                starting_path = next((arg[3:] for arg in args if arg.startswith("/r:")), None)
                search_pattern = args[-1]
                self.file_system.where(search_pattern, starting_path)
        else:
            print(f"'{cmd}' is not recognized as an internal or external command, operable program or batch file.")
    except FileNotFoundError as e:
        print(f"The system cannot find the path specified: {str(e)}")
    except PermissionError:
        print("Access is denied.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
   def network_commands(self, cmd: str, args: List[str]) -> None:
    if cmd == "ipconfig":
        if len(args) > 0:
            self.network.ipconfig(args[0])
        else:
            self.network.ipconfig()
    elif cmd == "ping":
        self.network.ping(args[0])
    elif cmd == "tracert":
        self.network.tracert(args[0])
    elif cmd == "nslookup":
        self.network.nslookup(args[0])
    elif cmd == "netstat":
        self.network.netstat(args if args else None)
    elif cmd == "route":
        self.network.route(args[0], *args[1:])
    elif cmd == "arp":
        self.network.arp(*args)
    elif cmd == "netsh":
        if args[0] == "wlan" and args[1] == "show" and args[2] == "all":
            self.network.netsh_wlan_show_all()
        elif args[0] == "interface" and args[1] == "ipv4" and args[2] == "show" and args[3] == "addresses":
            self.network.netsh_interface_ipv4_show_addresses()
        elif args[0] == "interface" and args[1] == "ipv4" and args[2] == "show" and args[3] == "subinterfaces":
            self.network.netsh_interface_ipv4_show_subinterfaces()
        elif args[0] == "wlan" and args[1] == "show" and args[2] == "drivers":
            self.network.netsh_wlan_show_drivers()
        elif args[0] == "advfirewall" and args[1] == "show" and args[2] == "allprofiles":
            self.network.netsh_advfirewall_show_allprofiles()
        elif args[0] == "http" and args[1] == "show" and args[2] == "urlacl":
            self.network.netsh_http_show_urlacl()
        elif args[0] == "wlan" and args[1] == "show" and args[2] == "hostednetwork":
            self.network.netsh_wlan_show_hostednetwork()
        elif args[0] == "winhttp" and args[1] == "show" and args[2] == "proxy":
            self.network.netsh_winhttp_show_proxy()
        elif args[0] == "winhttp" and args[1] == "reset" and args[2] == "proxy":
            self.network.netsh_winhttp_reset_proxy()
        elif args[0] == "interface" and args[1] == "ipv4" and args[2] == "set" and args[3] == "address":
            self.network.netsh_interface_ipv4_set_address(args[4], args[5] == "static", args[6], args[7], args[8])
        elif args[0] == "interface" and args[1] == "ipv4" and args[2] == "set" and args[3] == "dns":
            self.network.netsh_interface_ipv4_set_dns(args[4], args[5] == "static", args[6])
        elif args[0] == "advfirewall" and args[1] == "set" and args[2] == "allprofiles" and args[3] == "state":
            self.network.netsh_advfirewall_set_allprofiles_state(args[4])
        elif args[0] == "advfirewall" and args[1] == "firewall" and args[2] == "add" and args[3] == "rule":
            self.network.netsh_advfirewall_firewall_add_rule(args[4], args[5], args[6], args[7])
        elif args[0] == "advfirewall" and args[1] == "firewall" and args[2] == "delete" and args[3] == "rule":
            self.network.netsh_advfirewall_firewall_delete_rule(args[4])
        elif args[0] == "wlan" and args[1] == "connect":
            self.network.netsh_wlan_connect(args[2])
        elif args[0] == "wlan" and args[1] == "disconnect":
            self.network.netsh_wlan_disconnect()
        else:
            self.network.netsh(*args)
    elif cmd == "pathping":
        self.network.pathping(args[0])
    elif cmd == "telnet":
        self.network.telnet(args[0], int(args[1]))
    elif cmd == "nbtstat":
        self.network.nbtstat(*args)
    elif cmd == "getmac":
        self.network.getmac(*args)
    elif cmd == "ipv6_config":
        self.network.ipv6_config()
    elif cmd == "show":
        if args[0] == "network_connections":
            self.network.show_network_connections()
        elif args[0] == "network_protocols":
            self.network.show_network_protocols()
        elif args[0] == "network_shares":
            self.network.show_network_shares()
        elif args[0] == "firewall_rules":
            self.network.show_firewall_rules()
        elif args[0] == "network_drivers":
            self.network.show_network_drivers()
        else:
            print(f"Unknown show command: {args[0]}")
    elif cmd == "net":
        if args[0] == "use":
            self.network.net_use(args[1], args[2], args[3], args[4] if len(args) > 4 else None, args[5] if len(args) > 5 else None)
        elif args[0] == "share":
            self.network.net_share(args[1], args[2], args[3] if len(args) > 3 else None)
        elif args[0] == "view":
            self.network.net_view()
        elif args[0] == "start":
            self.network.net_start(args[1])
        elif args[0] == "stop":
            self.network.net_stop(args[1])
        else:
            print(f"Unknown net command: {args[0]}")
    elif cmd == "systeminfo":
        self.network.systeminfo()
    elif cmd == "ftp":
        self.network.ftp(args[0], args[1], args[2])
    elif cmd == "ssh":
        self.network.ssh(args[0], args[1])
    elif cmd == "nmap":
        self.network.nmap(args[0])
    elif cmd == "curl":
        self.network.curl(args[0])
    elif cmd == "wget":
        self.network.wget(args[0])
    elif cmd == "tcpdump":
        self.network.tcpdump(args[0])
    elif cmd == "wireshark":
        self.network.wireshark()
    elif cmd == "netdom":
        self.network.netdom(args[0], *args[1:])
    elif cmd == "nltest":
        self.network.nltest(args[0])
    elif cmd == "ipmonitor":
        self.network.ipmonitor()
    elif cmd == "netdiag":
        self.network.netdiag()
    elif cmd == "tcpview":
        self.network.tcpview()
    elif cmd == "portqry":
        self.network.portqry(args[0], int(args[1]))
    elif cmd == "netscan":
        self.network.netscan()
    elif cmd == "firewall":
        if args[0] == "list":
            print(self.network_security_manager.list_firewall_rules())
        elif args[0] == "add":
            self.network_security_manager.add_firewall_rule(args[1], args[2], int(args[3]), args[4], args[5], args[6])
        elif args[0] == "remove":
            self.network_security_manager.remove_firewall_rule(args[1])
    elif cmd == "antivirus":
        if args[0] == "scan":
            print(self.network_security_manager.run_antivirus_scan())
        elif args[0] == "status":
            print(self.network_security_manager.get_antivirus_status())
        elif args[0] == "update":
            print(self.network_security_manager.update_antivirus_definitions())
    elif cmd == "ids":
        if args[0] == "toggle":
            print(self.network_security_manager.toggle_ids(args[1].lower() == "on"))
        elif args[0] == "log":
            print(self.network_security_manager.get_ids_log())
    elif cmd == "vpn":
        if args[0] == "connect":
            print(self.network_security_manager.connect_vpn(args[1]))
        elif args[0] == "disconnect":
            print(self.network_security_manager.disconnect_vpn())
    elif cmd == "encrypt":
        print(self.network_security_manager.encrypt_drive(args[0]))
    elif cmd == "decrypt":
        print(self.network_security_manager.decrypt_drive(args[0]))
    elif cmd == "email_filter":
        print(self.network_security_manager.configure_email_filtering(float(args[0])))
    else:
        print(f"Unknown network command: {cmd}")
        
   def system_info_commands(self, cmd: str, args: List[str]) -> None:
    if cmd == "systeminfo":
        self.system_info.systeminfo()
    elif cmd == "msinfo32":
        self.system_info.msinfo32()
    elif cmd == "dxdiag":
        self.system_info.dxdiag()
    elif cmd == "msconfig":
        self.system_info.msconfig()
    elif cmd == "winver":
        self.system_info.winver()
    elif cmd == "ver":
        self.system_info.ver()
    elif cmd == "gpresult":
        self.system_info.gpresult()
    elif cmd == "whoami":
        self.system_info.whoami()
    elif cmd == "hostname":
        self.system_info.hostname()
    elif cmd == "sysinfo":
        self.system_info.sysinfo()
    elif cmd == "dmidecode":
        self.system_info.dmidecode()
    elif cmd == "lshw":
        self.system_info.lshw()
    elif cmd == "hwinfo":
        self.system_info.hwinfo()
    elif cmd == "lscpu":
        self.system_info.lscpu()
    elif cmd == "lsusb":
        self.system_info.lsusb()
    elif cmd == "lspci":
        self.system_info.lspci()
    else:
        print(f"Unknown system info command: {cmd}")
            
   def user_commands(self, args: List[str]) -> None:
    if not args:
        print("User command requires arguments. Type 'help user' for more information.")
        return

    action = args[0].lower()
    if action == "create" or action == "useradd":
        if len(args) < 3:
            print("Usage: user create <username> <password> [group1] [group2] ...")
        else:
            self.user_manager.create_user(args[1], args[2], args[3:] if len(args) > 3 else None)
    elif action == "delete" or action == "userdel":
        if len(args) != 2:
            print("Usage: user delete <username>")
        else:
            self.user_manager.delete_user(args[1])
    elif action == "changepass" or action == "passwd":
        if len(args) != 4:
            print("Usage: user changepass <username> <old_password> <new_password>")
        else:
            self.user_manager.change_password(args[1], args[2], args[3])
    elif action == "login":
        if len(args) != 3:
            print("Usage: user login <username> <password>")
        else:
            self.user_manager.login(args[1], args[2])
    elif action == "logout":
        if len(args) != 2:
            print("Usage: user logout <username>")
        else:
            self.user_manager.logout(args[1])
    elif action == "addgroup":
        if len(args) != 3:
            print("Usage: user addgroup <username> <group>")
        else:
            self.user_manager.add_to_group(args[1], args[2])
    elif action == "removegroup":
        if len(args) != 3:
            print("Usage: user removegroup <username> <group>")
        else:
            self.user_manager.remove_from_group(args[1], args[2])
    elif action == "list" or action == "net":
        if len(args) == 1:
            self.user_manager.list_users()
        elif len(args) == 2:
            self.user_manager.net_user(args[1])
        else:
            print("Usage: user list OR user net [username]")
    elif action == "listgroups":
        self.user_manager.list_groups()
    elif action == "info" or action == "id":
        if len(args) != 2:
            print("Usage: user info <username> OR user id <username>")
        else:
            if action == "info":
                self.user_manager.get_user_info(args[1])
            else:
                self.user_manager.id(args[1])
    elif action == "resetpass":
        if len(args) != 3:
            print("Usage: user resetpass <username> <new_password>")
        else:
            self.user_manager.reset_password(args[1], args[2])
    elif action == "lockoutpolicy":
        if len(args) != 3:
            print("Usage: user lockoutpolicy <max_attempts> <lockout_duration_minutes>")
        else:
            self.user_manager.set_account_lockout_policy(int(args[1]), int(args[2]))
    elif action == "usermod":
        if len(args) < 3:
            print("Usage: user usermod <username> [--new_username <new_username>] [--groups <group1,group2,...]")
        else:
            kwargs = {}
            for i in range(2, len(args), 2):
                if args[i] == "--new_username" and i+1 < len(args):
                    kwargs["new_username"] = args[i+1]
                elif args[i] == "--groups" and i+1 < len(args):
                    kwargs["groups"] = args[i+1].split(",")
            self.user_manager.usermod(args[1], **kwargs)
    elif action == "groupadd":
        if len(args) != 2:
            print("Usage: user groupadd <group_name>")
        else:
            self.user_manager.groupadd(args[1])
    elif action == "groupmod":
        if len(args) != 3:
            print("Usage: user groupmod <old_group_name> <new_group_name>")
        else:
            self.user_manager.groupmod(args[1], args[2])
    elif action == "groupdel":
        if len(args) != 2:
            print("Usage: user groupdel <group_name>")
        else:
            self.user_manager.groupdel(args[1])
    else:
        print(f"Unknown user command: {action}")

   def process_commands(self, cmd: str, args: List[str]) -> None:
    if cmd == "tasklist":
        self.process_manager.tasklist(*args)
    elif cmd == "taskkill":
        self.process_manager.taskkill(*args)
    elif cmd == "start":
        if len(args) < 1:
            print("Usage: start <process_name> [user]")
        else:
            name = args[0]
            user = args[1] if len(args) > 1 else "USER"
            self.process_manager.start_process(name, user)
    elif cmd == "sfc":
        option = args[0] if args else None
        self.process_manager.sfc(option)
    elif cmd == "wmic":
        if args and args[0].lower() == "process":
            filter = args[1] if len(args) > 1 else None
            self.process_manager.wmic_process(filter)
        else:
            print("Invalid wmic command. Use 'wmic process'.")
    elif cmd == "sc":
        if len(args) < 2:
            print("Usage: sc <action> <service_name>")
        else:
            action, service_name = args[0], args[1]
            self.process_manager.sc(action, service_name)
    elif cmd == "shutdown":
        option = args[0] if args else None
        self.process_manager.shutdown(option)
    elif cmd == "runas":
        if len(args) < 2:
            print("Usage: runas <username> <command>")
        else:
            username, command = args[0], " ".join(args[1:])
            self.process_manager.runas(username, command)
    elif cmd == "at":
        if len(args) < 2:
            print("Usage: at <time> <command>")
        else:
            time, command = args[0], " ".join(args[1:])
            self.process_manager.at(time, command)
    elif cmd == "schtasks":
        if len(args) < 2:
            print("Usage: schtasks <action> <task_name> [schedule]")
        else:
            action = args[0]
            task_name = args[1]
            schedule = args[2] if len(args) > 2 else ""
            self.process_manager.schtasks(action, task_name, schedule)
    elif cmd == "qprocess":
        self.process_manager.qprocess()
    elif cmd == "qwinsta":
        self.process_manager.qwinsta()
    elif cmd == "tskill":
        if len(args) < 1:
            print("Usage: tskill <pid_or_name>")
        else:
            pid_or_name = args[0]
            self.process_manager.tskill(pid_or_name)
    elif cmd == "pskill":
        if len(args) < 1:
            print("Usage: pskill <pid_or_name>")
        else:
            pid_or_name = args[0]
            self.process_manager.pskill(pid_or_name)
    elif cmd == "psexec":
        if len(args) < 2:
            print("Usage: psexec <computer> <command>")
        else:
            computer, command = args[0], " ".join(args[1:])
            self.process_manager.psexec(computer, command)
    elif cmd == "procexp":
        self.process_manager.procexp()
    elif cmd == "procmon":
        self.process_manager.procmon()
    else:
        print(f"Unknown process command: {cmd}")

   def disk_commands(self, cmd: str, args: List[str]) -> None:
    try:
        if cmd == "chkdsk":
            self.disk_manager.chkdsk(args[0] if args else "")
        elif cmd == "diskpart":
            self.disk_manager.diskpart()
        elif cmd == "defrag":
            self.disk_manager.defrag(args[0] if args else "")
        elif cmd == "fsutil":
            self.disk_manager.fsutil(args)
        elif cmd == "format":
            drive = args[0] if args else ""
            file_system = args[1] if len(args) > 1 else "NTFS"
            quick = "/q" in args or "-q" in args
            self.disk_manager.format(drive, file_system, quick)
        elif cmd == "label":
            if len(args) >= 2:
                self.disk_manager.label(args[0], args[1])
            else:
                print("Usage: label [drive:] [label]")
        elif cmd == "convert":
            if len(args) >= 2:
                self.disk_manager.convert(args[0], args[1])
            else:
                print("Usage: convert [drive:] [file_system]")
        elif cmd == "vssadmin":
            self.disk_manager.vssadmin(args)
        elif cmd == "diskmgmt":
            self.disk_manager.diskmgmt()
        elif cmd == "wbadmin":
            self.disk_manager.wbadmin(args)
        elif cmd == "imdisk":
            self.disk_manager.imdisk(args)
        elif cmd == "diskspd":
            self.disk_manager.diskspd(args)
        elif cmd == "ddrescue":
            if len(args) >= 2:
                self.disk_manager.ddrescue(args[0], args[1])
            else:
                print("Usage: ddrescue [source] [destination]")
        elif cmd == "smartctl":
            self.disk_manager.smartctl(args[0] if args else "")
        else:
            print(f"Unknown disk command: {cmd}")
    except Exception as e:
        print(f"Error executing disk command: {str(e)}")

   def security_commands(self, cmd: str, args: List[str]) -> None:
    try:
        if cmd == "net":
            if args[0] == "user":
                if len(args) > 2 and args[1] == "add":
                    self.security_manager.create_user(args[2], args[3], args[4:])
                elif len(args) > 2 and args[1] == "delete":
                    self.security_manager.delete_user(args[2])
                else:
                    self.security_manager.net_user(args[1] if len(args) > 1 else None)
            elif args[0] == "localgroup":
                self.security_manager.net_localgroup(args[1] if len(args) > 1 else None)
            elif args[0] == "share":
                self.security_manager.net_share(args[1] if len(args) > 1 else None)
            elif args[0] == "start":
                self.security_manager.net_start(args[1] if len(args) > 1 else None)
            elif args[0] == "stop":
                self.security_manager.net_stop(args[1])
        elif cmd == "netplwiz":
            self.security_manager.netplwiz()
        elif cmd == "change_password":
            if len(args) >= 2:
                self.security_manager.change_password(args[0], args[1])
            else:
                print("Usage: change_password <username> <new_password>")
        elif cmd == "add_to_group":
            if len(args) >= 2:
                self.security_manager.add_to_group(args[0], args[1])
            else:
                print("Usage: add_to_group <username> <group>")
        elif cmd == "remove_from_group":
            if len(args) >= 2:
                self.security_manager.remove_from_group(args[0], args[1])
            else:
                print("Usage: remove_from_group <username> <group>")
        elif cmd == "grant_permission":
            if len(args) >= 2:
                self.security_manager.grant_permission(args[0], args[1])
            else:
                print("Usage: grant_permission <username> <permission>")
        elif cmd == "revoke_permission":
            if len(args) >= 2:
                self.security_manager.revoke_permission(args[0], args[1])
            else:
                print("Usage: revoke_permission <username> <permission>")
        elif cmd == "list_users":
            self.security_manager.list_users()
        elif cmd == "icacls":
            if len(args) >= 2:
                self.security_manager.icacls(args[0], args[1:])
            else:
                print("Usage: icacls <path> [options]")
        elif cmd == "cipher":
            if args:
                self.security_manager.cipher(args[0])
            else:
                print("Usage: cipher <drive>")
        elif cmd == "auditpol":
            if len(args) >= 2:
                self.security_manager.auditpol(args[0], args[1])
            else:
                print("Usage: auditpol <subcategory> <action>")
        elif cmd == "gpedit.msc":
            self.security_manager.gpedit()
        elif cmd == "secedit":
            if len(args) >= 2:
                self.security_manager.secedit(args[0], args[1])
            else:
                print("Usage: secedit <action> <cfg_file>")
        elif cmd == "cacls":
            if len(args) >= 2:
                self.security_manager.cacls(args[0], args[1:])
            else:
                print("Usage: cacls <file> [options]")
        elif cmd == "wmic":
            if args and args[0] == "useraccount":
                self.security_manager.wmic_useraccount(args[1], {arg.split('=')[0]: arg.split('=')[1] for arg in args[2:] if '=' in arg})
            else:
                print("Usage: wmic useraccount <action> [options]")
        elif cmd == "nltest":
            if args:
                self.security_manager.nltest(args[0])
            else:
                print("Usage: nltest <command>")
        elif cmd == "certutil":
            if len(args) >= 1:
                self.security_manager.certutil(args[0], args[1:])
            else:
                print("Usage: certutil <action> [options]")
        elif cmd == "manage-bde":
            if len(args) >= 2:
                self.security_manager.manage_bde(args[0], args[1], args[2:])
            else:
                print("Usage: manage-bde <action> <drive> [options]")
        else:
            print(f"Unknown security command: {cmd}")
    except Exception as e:
        logging.error(f"Error in security_commands: {str(e)}")
        print(f"Error: {str(e)}")
        
   def performance_commands(self, cmd: str, args: List[str]) -> None:
    if cmd == "perfmon":
        self.performance_monitor.perfmon()
    elif cmd == "resmon":
        self.performance_monitor.resmon()
    elif cmd == "eventvwr":
        self.performance_monitor.eventvwr()
    elif cmd == "wmic":
        self.performance_monitor.wmic(" ".join(args))
    elif cmd == "powercfg":
        self.performance_monitor.powercfg(args[0] if args else "")
    elif cmd == "typeperf":
        self.performance_monitor.typeperf(args)
    elif cmd == "logman":
        self.performance_monitor.logman(args[0] if args else "", *args[1:])
    elif cmd == "xperf":
        self.performance_monitor.xperf(" ".join(args))
    elif cmd == "psinfo":
        self.performance_monitor.psinfo()
    elif cmd == "pslist":
        self.performance_monitor.pslist()
    elif cmd == "pstack":
        if args and args[0].isdigit():
            self.performance_monitor.pstack(int(args[0]))
        else:
            print("Error: pstack requires a valid PID")
    elif cmd == "pmap":
        if args and args[0].isdigit():
            self.performance_monitor.pmap(int(args[0]))
        else:
            print("Error: pmap requires a valid PID")
    elif cmd == "vmstat":
        self.performance_monitor.vmstat()
    elif cmd == "iostat":
        self.performance_monitor.iostat()
    else:
        print(f"Unknown performance command: {cmd}")
        
   def printer_commands(self, cmd: str, args: List[str]) -> None:
    if cmd == "print":
        if len(args) >= 2:
            self.printer_manager.print_job(args[0], " ".join(args[1:]))
        else:
            print("Usage: print <printer_name> <document_name>")
    elif cmd == "printmgmt.msc":
        self.printer_manager.list_printers()
    elif cmd == "add_printer":
        if len(args) == 3:
            self.printer_manager.add_printer(args[0], args[1], args[2])
        else:
            print("Usage: add_printer <name> <type> <location>")
    elif cmd == "remove_printer":
        if args:
            self.printer_manager.remove_printer(args[0])
        else:
            print("Usage: remove_printer <name>")
    elif cmd == "print_test_page":
        if args:
            self.printer_manager.print_test_page(args[0])
        else:
            print("Usage: print_test_page <printer_name>")
    elif cmd == "troubleshoot_printer":
        if args:
            self.printer_manager.troubleshoot_printer(args[0])
        else:
            print("Usage: troubleshoot_printer <printer_name>")
    elif cmd == "get_printer_status":
        if args:
            self.printer_manager.get_printer_status(args[0])
        else:
            print("Usage: get_printer_status <printer_name>")
    elif cmd == "set_printer_status":
        if len(args) >= 2:
            self.printer_manager.set_printer_status(args[0], " ".join(args[1:]))
        else:
            print("Usage: set_printer_status <printer_name> <status>")
    elif cmd == "cancel_print_job":
        if len(args) == 2 and args[1].isdigit():
            self.printer_manager.cancel_print_job(args[0], int(args[1]))
        else:
            print("Usage: cancel_print_job <printer_name> <job_id>")
    elif cmd == "get_printer_queue":
        if args:
            self.printer_manager.get_printer_queue(args[0])
        else:
            print("Usage: get_printer_queue <printer_name>")
    elif cmd == "update_printer_driver":
        if args:
            self.printer_manager.update_printer_driver(args[0])
        else:
            print("Usage: update_printer_driver <printer_name>")
    else:
        print(f"Unknown printer command: {cmd}")

   def virtualization_commands(self, cmd: str, args: List[str]) -> None:
    if cmd == "virt":
        self.virtualization_manager.virt_command(args)
    elif cmd == "vm":
        if not args:
            print("Usage: vm <subcommand> [options]")
            return
        subcommand = args[0]
        if subcommand == "create":
            if len(args) == 6:
                self.virtualization_manager.create_vm(args[1], int(args[2]), int(args[3]), int(args[4]), args[5])
            else:
                print("Usage: vm create <name> <cpu> <ram> <hdd> <type>")
        elif subcommand == "delete":
            if len(args) == 2:
                self.virtualization_manager.delete_vm(args[1])
            else:
                print("Usage: vm delete <name>")
        elif subcommand == "list":
            self.virtualization_manager.list_vms()
        else:
            print(f"Unknown vm subcommand: {subcommand}")
    elif cmd == "hyper-v":
        self.virtualization_manager.virt_command(["hyper-v"] + args)
    elif cmd == "docker":
        self.virtualization_manager.docker_command(args)
    elif cmd == "vagrant":
        self.virtualization_manager.vagrant_command(args)
    elif cmd == "virtualbox":
        self.virtualization_manager.virtualbox_command(args)
    elif cmd == "vmware":
        self.virtualization_manager.vmware_command(args)
    elif cmd == "qemu":
        self.virtualization_manager.qemu_command(args)
    elif cmd == "lxc":
        self.virtualization_manager.lxc_command(args)
    else:
        print(f"Unknown virtualization command: {cmd}")

   def mobile_device_commands(self, cmd: str, args: List[str]) -> None:
        if cmd == "mdm":
            if args[0] == "list":
                self.mobile_device_manager.list_devices()
            elif args[0] == "enroll":
                self.mobile_device_manager.enroll_device(args[1])
            elif args[0] == "unenroll":
                self.mobile_device_manager.unenroll_device(args[1])

   def cloud_commands(self, cmd: str, args: List[str]) -> None:
        if cmd == "cloud":
            if args[0] == "list":
                self.cloud_service_manager.list_services()
            elif args[0] == "start":
                self.cloud_service_manager.start_service(args[1])
            elif args[0] == "stop":
                self.cloud_service_manager.stop_service(args[1])
        elif cmd in ["aws", "azure"]:
            print(f"Simulated: Executing {cmd} command: {' '.join(args)}")

   def remote_access_commands(self, cmd: str, args: List[str]) -> str:
    if cmd == "rdp":
        if args[0] == "connect":
            if len(args) < 3:
                return "Usage: rdp connect <username> <ip> [port] [encryption] [color_depth] [resolution]"
            username = args[1]
            ip = args[2]
            port = int(args[3]) if len(args) > 3 else 3389
            encryption = args[4] if len(args) > 4 else "TLS 1.2"
            color_depth = args[5] if len(args) > 5 else "32-bit"
            resolution = args[6] if len(args) > 6 else "1920x1080"
            return self.remote_access_manager.start_rdp_session(username, ip, port, encryption, color_depth, resolution)
        elif args[0] == "disconnect":
            if len(args) < 2:
                return "Usage: rdp disconnect <username>"
            return self.remote_access_manager.end_rdp_session(args[1])
        elif args[0] == "status":
            if len(args) < 2:
                return "Usage: rdp status <username>"
            return str(self.remote_access_manager.get_rdp_status(args[1]))

    elif cmd == "vpn":
        if args[0] == "connect":
            if len(args) < 7:
                return "Usage: vpn connect <vpn_name> <protocol> <encryption> <auth_method> <tunnel_type> <ip_assignment>"
            vpn_name, protocol, encryption, auth_method, tunnel_type, ip_assignment = args[1:7]
            return self.remote_access_manager.connect_vpn(vpn_name, protocol, encryption, auth_method, tunnel_type, ip_assignment)
        elif args[0] == "disconnect":
            if len(args) < 2:
                return "Usage: vpn disconnect <vpn_name>"
            return self.remote_access_manager.disconnect_vpn(args[1])
        elif args[0] == "status":
            if len(args) < 2:
                return "Usage: vpn status <vpn_name>"
            return str(self.remote_access_manager.get_vpn_status(args[1]))

    elif cmd == "list":
        return str(self.remote_access_manager.list_all_connections())

    else:
        return f"Unknown command: {cmd}"

   def soho_network_commands(self, cmd: str, args: List[str]) -> None:
    if cmd == "soho":
        if args[0] == "list":
            self.soho_network_manager.list_devices()
        elif args[0] == "add" and len(args) == 5:
            self.soho_network_manager.add_device(args[1], args[2], args[3], args[4])
        elif args[0] == "remove" and len(args) == 2:
            self.soho_network_manager.remove_device(args[1])
        elif args[0] == "topology":
            self.soho_network_manager.display_network_topology()
        elif args[0] == "troubleshoot":
            self.soho_network_manager.troubleshoot_network()
        elif args[0] == "backup":
            self.soho_network_manager.backup_config()
        elif args[0] == "restore":
            self.soho_network_manager.restore_config()
        elif args[0] == "scan":
            self.soho_network_manager.scan_for_vulnerabilities()
        else:
            print("Invalid SOHO network command.")

    elif cmd == "router":
        if args[0] == "config" and len(args) == 3:
            self.soho_network_manager.configure_router(args[1], args[2])
        elif args[0] == "update":
            self.soho_network_manager.update_firmware("Router")
        elif args[0] == "portforward" and len(args) == 5:
            self.soho_network_manager.configure_port_forwarding(int(args[1]), args[2], int(args[3]), args[4])
        elif args[0] == "dmz" and len(args) == 2:
            self.soho_network_manager.configure_dmz(args[1])
        elif args[0] == "display":
            self.soho_network_manager.display_router_config()
        else:
            print("Invalid router command.")

    elif cmd == "switch":
        if args[0] == "config" and len(args) >= 3:
            self.soho_network_manager.configure_switch(int(args[1]), [int(p) for p in args[2:]])
        elif args[0] == "update":
            self.soho_network_manager.update_firmware("Switch")
        elif args[0] == "vlan" and len(args) >= 4:
            vlan_id = int(args[1])
            vlan_name = args[2]
            ports = [int(p) for p in args[3:]]
            self.soho_network_manager.configure_vlan(vlan_id, vlan_name, ports)
        elif args[0] == "display":
            self.soho_network_manager.display_vlan_config()
        else:
            print("Invalid switch command.")

    elif cmd == "dhcp":
        if args[0] == "config" and len(args) == 3:
            self.soho_network_manager.configure_dhcp(args[1], args[2])
        else:
            print("Invalid DHCP command.")

    elif cmd == "dns":
        if args[0] == "config" and len(args) == 3:
            self.soho_network_manager.configure_dns(args[1], args[2])
        else:
            print("Invalid DNS command.")

    elif cmd == "firewall":
        if args[0] == "add" and len(args) >= 2:
            self.soho_network_manager.add_firewall_rule(" ".join(args[1:]))
        else:
            print("Invalid firewall command.")

    elif cmd == "wifi":
        if args[0] == "config" and len(args) == 6:
            self.soho_network_manager.configure_wifi(args[1], args[2], args[3], int(args[4]), args[5])
        else:
            print("Invalid Wi-Fi command.")

    elif cmd == "speedtest":
        self.soho_network_manager.run_speed_test()

    else:
        print("Invalid command.")

   def licensing_commands(self, cmd: str, args: List[str]) -> None:
        if cmd == "license":
            if args[0] == "list":
                self.licensing_manager.list_licenses()
        elif cmd == "activate":
            self.licensing_manager.activate_license(args[0])
        elif cmd == "deactivate":
            self.licensing_manager.deactivate_license(args[0])

   def environmental_commands(self, cmd: str, args: List[str]) -> None:
        if cmd == "temp":
            if args[0] == "set":
                self.environmental_control_manager.set_temperature(float(args[1]))
        elif cmd == "humidity":
            if args[0] == "set":
                self.environmental_control_manager.set_humidity(float(args[1]))
        elif cmd == "power":
            if args[0] == "status":
                self.environmental_control_manager.get_environmental_status()

   def documentation_commands(self, cmd: str, args: List[str]) -> None:
        if cmd == "doc":
            if args[0] == "list":
                self.documentation_manager.list_documents()
            elif args[0] == "view":
                self.documentation_manager.view_document(args[1])
            elif args[0] == "create":
                self.documentation_manager.create_document(args[1], args[2])
            elif args[0] == "update":
                self.documentation_manager.update_document(args[1])

   def disaster_recovery_commands(self, cmd: str, args: List[str]) -> None:
        if cmd == "backup":
            self.disaster_recovery_manager.perform_backup()
        elif cmd == "restore":
            self.disaster_recovery_manager.restore_from_backup(datetime.fromisoformat(args[0]))
        elif cmd == "disaster":
            if args[0] == "plan":
                self.disaster_recovery_manager.create_disaster_recovery_plan()

   def accessibility_commands(self, cmd: str, args: List[str]) -> None:
        if cmd == "access":
            if args[0] == "list":
                self.accessibility_manager.list_features()
            elif args[0] == "toggle":
                self.accessibility_manager.toggle_feature(args[1])
            elif args[0] == "configure":
                if args[1] == "screen_reader":
                    self.accessibility_manager.configure_screen_reader()
                elif args[1] == "high_contrast":
                    self.accessibility_manager.set_high_contrast_theme(args[2])

   def scripting_commands(self, cmd: str, args: List[str]) -> None:
        if cmd == "script":
            if args[0] == "create":
                if args[1] == "batch":
                    self.scripting_environment.create_batch_script(args[2])
                elif args[1] == "powershell":
                    self.scripting_environment.create_powershell_script(args[2])
            elif args[0] == "run":
                if args[1] == "batch":
                    self.scripting_environment.run_batch_script(args[2])
                elif args[1] == "powershell":
                    self.scripting_environment.run_powershell_script(args[2])

   def run_troubleshooting_scenario(self, args: List[str]) -> None:
        if args[0] == "run":
            self.troubleshooting_scenarios.run_scenario(args[1])

   def os_installation_commands(self, cmd: str, args: List[str]) -> None:
       if args[0] == "install":
           self.os_installation_manager.start_installation(args[1])
       elif args[0] == "upgrade":
           self.os_installation_manager.upgrade_os(args[1], args[2])
       elif args[0] == "status":
           self.os_installation_manager.get_installation_status()

   def firewall_commands(self, cmd: str, args: List[str]) -> None:
        if args[0] == "list":
            self.network_security_manager.list_firewall_rules()
        elif args[0] == "add":
            self.network_security_manager.add_firewall_rule(args[1], int(args[2]), args[3])
        elif args[0] == "remove":
            self.network_security_manager.remove_firewall_rule(args[1])

   def antivirus_commands(self, cmd: str, args: List[str]) -> None:
        if args[0] == "scan":
            self.network_security_manager.run_antivirus_scan()
        elif args[0] == "status":
            self.network_security_manager.get_antivirus_status()

   def uac_commands(self, cmd: str, args: List[str]) -> None:
        if args[0] == "prompt":
            result = self.uac_simulator.prompt_for_elevation(args[1])
            print(f"User {'allowed' if result else 'denied'} the action.")
        elif args[0] == "set":
            self.uac_simulator.change_uac_level(args[1])
        elif args[0] == "status":
            self.uac_simulator.get_uac_status()

   def hardware_commands(self, cmd: str, args: List[str]) -> None:
        if args[0] == "list":
            self.hardware_simulator.list_devices()
        elif args[0] == "update":
            self.hardware_simulator.update_driver(args[1])
        elif args[0] == "troubleshoot":
            self.hardware_simulator.troubleshoot_device(args[1])

   def raid_commands(self, cmd: str, args: List[str]) -> None:
        if args[0] == "list":
            self.raid_manager.list_raid_configs()
        elif args[0] == "create":
            self.raid_manager.create_raid(args[1], args[2:])
        elif args[0] == "delete":
            self.raid_manager.delete_raid(args[1])
        elif args[0] == "status":
            self.raid_manager.check_raid_status(args[1])

   def show_help(self) -> None:
        help_text = """
For more information on a specific command, type HELP command-name

CD             Displays the name of or changes the current directory.
CHDIR          Displays the name of or changes the current directory.
DIR            Displays a list of files and subdirectories in a directory.
MKDIR          Creates a directory.
MD             Creates a directory.
RMDIR          Removes a directory.
RD             Removes a directory.
COPY           Copies one or more files to another location.
MOVE           Moves one or more files from one directory to another directory.
DEL            Deletes one or more files.
REN            Renames a file or files.
RENAME         Renames a file or files.
ATTRIB         Displays or changes file attributes.

IPCONFIG       Display all current TCP/IP network configuration values.
PING           Send echo messages to a remote computer.
TRACERT        Trace the route to a remote host.
NSLOOKUP       Query the DNS for information.
NETSTAT        Display active TCP connections and ports.
ROUTE          View and modify the IP routing table.
ARP            Display and modify the IP-to-Physical address translation tables.
NETSH          Configure network protocols.
PATHPING       Trace the route to a remote host with latency information.
TELNET         Communicate with a remote computer.
NBTSTAT        Display NetBIOS over TCP/IP statistics.
GETMAC         Display the MAC address of network adapters.

SYSTEMINFO     Display detailed configuration information about the computer.
MSINFO32       Display system information.
DXDIAG         Display DirectX diagnostic information.
MSCONFIG       Configure system startup.

TASKLIST       Display currently running processes.
TASKKILL       Terminate a running process.
SFC            Scan and repair Windows system files.

CHKDSK         Check a disk and display a status report.
DISKPART       Display or configure disk partitions.
DEFRAG         Defragment a drive.

NET USER       Add or modify user accounts.
NET LOCALGROUP Manage local groups.
NET SHARE      Manage shared resources.
NET START      Start a network service.
NET STOP       Stop a network service.

PERFMON        Start Performance Monitor.
RESMON         Start Resource Monitor.
EVENTVWR       Start Event Viewer.
WMIC           Display WMI information.
POWERCFG       Manage power settings.

PRINT          Print a text file.
PRINTMGMT.MSC  Open Print Management.

VIRT           Manage virtual machines.
VM             Create or delete virtual machines.

MDM            Manage mobile devices.

CLOUD          Manage cloud services.
AWS            Manage Amazon Web Services.
AZURE          Manage Microsoft Azure services.

RDP            Manage Remote Desktop connections.
VPN            Manage VPN connections.

SOHO           Manage Small Office/Home Office network.
ROUTER         Configure router settings.
SWITCH         Configure switch settings.
DHCP           Configure DHCP settings.
DNS            Configure DNS settings.
WIFI           Configure Wi-Fi settings.

LICENSE        Manage software licenses.

TEMP           Set temperature for environmental controls.
HUMIDITY       Set humidity for environmental controls.
POWER          Check power status.

DOC            Manage documentation.

BACKUP         Perform system backup.
RESTORE        Restore system from backup.

ACCESS         Manage accessibility features.

SCRIPT         Create or run scripts.

SCENARIO       Run troubleshooting scenarios.

OS             Manage operating system installation or upgrade.

UAC            Manage User Account Control settings.

HARDWARE       Manage hardware devices.

RAID           Manage RAID configurations.

USER           Manage user accounts.

EXIT           Exit the program.

For more information on tools see the command-line reference in the online help.
"""

        # Get terminal size
        terminal_size = os.get_terminal_size()
        lines_per_page = terminal_size.lines - 1

        # Split help text into lines
        help_lines = help_text.split('\n')

        # Display help text with paging
        for i in range(0, len(help_lines), lines_per_page):
            print('\n'.join(help_lines[i:i+lines_per_page]))
            if i + lines_per_page < len(help_lines):
                input("-- More --")

        print(f"\n{self.file_system.current_directory}>")





class CommandInterpreterWrapper:
    def __init__(self, default_directory="C:\\"):
        print("Initializing CommandInterpreterWrapper")
        self.interpreter = CommandInterpreter()
        self.command_history = []
        self.set_default_directory(default_directory)

    def set_default_directory(self, path):
        try:
            # Normalize the path to ensure consistent format
            normalized_path = os.path.normpath(path)
            # Check if the path exists in our virtual file system
            if self.interpreter.file_system._directory_exists(normalized_path):
                self.interpreter.file_system.current_directory = normalized_path
                print(f"Default directory set to: {normalized_path}")
            else:
                raise ValueError(f"Directory does not exist: {normalized_path}")
        except Exception as e:
            print(f"Error setting default directory: {str(e)}")
            # If setting the directory fails, fall back to C:\
            self.interpreter.file_system.current_directory = "C:\\"
            print("Fallback: Default directory set to C:\\")

    def execute_command(self, command):
        print(f"CommandInterpreterWrapper received command: {command}")
        
        try:
            output = io.StringIO()
            with redirect_stdout(output):
                result = self.interpreter.execute_command(command)
            
            printed_output = output.getvalue().strip()

            print(f"Command result: {result}")
            print(f"Printed output: {printed_output}")
            print(f"Current directory: {self.interpreter.file_system.current_directory}")

            self.command_history.append(command)

            return {
                'result': result,
                'printed_output': printed_output,
                'current_directory': self.interpreter.file_system.current_directory
            }
        except Exception as e:
            print(f"Error executing command: {str(e)}")
            print(traceback.format_exc())
            return {
                'error': str(e),
                'current_directory': self.interpreter.file_system.current_directory
            }

    def get_current_directory(self):
        return self.interpreter.file_system.current_directory

    def to_json(self):
        return json.dumps({
            'current_directory': self.interpreter.file_system.current_directory,
            'command_history': self.command_history
        })

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        instance = cls()
        instance.set_default_directory(data.get('current_directory', "C:\\"))
        instance.command_history = data.get('command_history', [])
        return instance

    def check_goal_state(self, goal_state):
        current_state = self.get_current_state()
        return self.compare_states(current_state, goal_state)

    def get_current_state(self):
        return {
            'current_directory': self.interpreter.file_system.current_directory,
            'file_system': self.interpreter.file_system.to_dict(),
            'command_history': self.command_history
        }

    def compare_states(self, current_state, goal_state):
        if isinstance(goal_state, str):
            # If goal_state is a string, compare it directly with the command history
            return goal_state in current_state.get('command_history', [])
        elif isinstance(goal_state, dict):
            # If goal_state is a dictionary, compare it with the current state
            for key, value in goal_state.items():
                if key not in current_state or current_state[key] != value:
                    return False
            return True
        else:
            print(f"Unsupported goal state type: {type(goal_state)}")
            return False

def main():
    interpreter = CommandInterpreter()
    print("Welcome to the A+ Exam Simulator")
    print("Type 'help' for a list of available commands, or 'exit' to quit.")

    while True:
        command = input(f"{interpreter.file_system.current_directory}> ")
        if not interpreter.execute_command(command):
            break

    print("Goodbye!")

if __name__ == "__main__":
    main()