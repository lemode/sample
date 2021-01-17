from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def google_drive_authenticate_and_upload(
    dataframe, target_filename, parent_folder_id, team_drive_id=None
):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    dataframe.to_csv(target_filename)

    #   team_drive_id = 'XXXXX'
    #   parent_folder_id = 'XXXXX-YYYYY'

    if team_drive_id:
        gfile = drive.CreateFile(
            {
                "title": target_filename,
                "parents": [
                    {
                        "kind": "drive#fileLink",
                        "teamDriveId": team_drive_id,
                        "id": parent_folder_id,
                    }
                ],
            }
        )
    else:
        gfile = drive.CreateFile(
            {
                "title": target_filename,
                "parents": [{"kind": "drive#fileLink", "id": parent_folder_id}],
            }
        )

    gfile.SetContentFile(target_filename)

    gfile.Upload(param={"supportsTeamDrives": True})
