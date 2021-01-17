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

    def google_drive_list_files(
        parent_folder_id, team_drive_id=None, include_trash=False
    ):
        return drive.ListFile(
            {
                "corpora": "drive",
                "driveId": team_drive_id,
                "includeItemsFromAllDrives": "true",
                "orderBy": "title",
                "q": "parents={} and trashed={}".format(
                    parent_folder_id, include_trash
                ),
                "supportsAllDrives": "true",
            }
        ).GetList()

    def google_drive_delete_file(file_name):
        file_list = drive.ListFile(
            {
                "corpora": "drive",
                "driveId": "0AFwkOXlitG48Uk9PVA",
                "includeItemsFromAllDrives": "true",
                "orderBy": "title",
                "q": "parents='1nB0B0fKxklHinZl-vIx6ddBOAo1WdAo7' and trashed=false",
                "supportsAllDrives": "true",
            }
        ).GetList()

        try:
            for file in file_list:
                print(file)
                if file["title"] == "Copy of daily_fx_rates1":
                    file.Delete()
        except:
            pass
