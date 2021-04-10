import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def google_drive_authenticate_and_upload(
    dataframe, target_filename, parent_folder_id, shared_drive_id=None
):
    # Authenticate and create the PyDrive client.
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    dataframe.to_csv(target_filename)

    #   team_drive_id = 'XXXXX'
    #   parent_folder_id = 'XXXXX-YYYYY'

    if shared_drive_id:
        gfile = drive.CreateFile(
            {
                "title": target_filename,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [
                    {
                        "kind": "drive#file",
                        "driveId": shared_drive_id,
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

    # gfile.SetContentFile(target_filename) --only if its a file

    gfile.Upload(param={"supportsTeamDrives": True})


def google_drive_list_files(
    parent_folder_id, shared_drive_id=None, include_trash=False
):
    # Authenticate and create the PyDrive client.
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    return drive.ListFile(
        {
            "corpora": "drive",
            "driveId": shared_drive_id,
            "includeItemsFromAllDrives": "true",
            "orderBy": "title",
            "q": "parents={} and trashed={}".format(parent_folder_id, include_trash),
            "supportsTeamDrives": "true",
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


# google_drive_authenticate_and_upload(
#     pd.DataFrame(),
#     "linda",
#     "1-M86F6y5hm4J9zQNgIBdbOKND3dgKZ7V",
#     "0AJtUdmSRqmfpUk9PVA",
# )

google_drive_list_files("1-M86F6y5hm4J9zQNgIBdbOKND3dgKZ7V", "0AJtUdmSRqmfpUk9PVA")
