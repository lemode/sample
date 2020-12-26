cd C:\
cd "Program Files\Google\Drive File Stream"
foreach ($G in dir -s GoogleDriveFS.exe) { cd $G.Directory}
start GoogleDriveFS.exe