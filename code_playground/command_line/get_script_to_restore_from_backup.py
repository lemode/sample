import pandas as pd

from code_playground.secrets import DatabaseProductionConfig as database_production
from code_playground.command_line.constants import RestoreFromBackupTemplateConfig as constants

"""
Purpose:
    1. to be able to get specific tables from a backup to run testing or repushes in order to decrease the amount of time a restore process takes
    2. to be able to restore a few different back ups at the same time, especially when the same table is needed

Backups location
Backups are stored on a network drive and accessed from TORDCETLSTG01 to the T: Drive ["E:\Cosmos9_Work\Batch_Scripts\Live\BKP_MOUNT.bat"] where datamart backups are stored and then used for the individual file restore
:: Example of backup_path_name = 'T:\Datamart_Backups\datamart_20200201_20200202_021901_full.backup'

Procedure to perform restore
    1. Mount server so that backups are available and network drive is opened
    2. Copy file from FS_Scripts folder to My Documents on TORDCETLSTG01
    3. Run bat file
"""


class ScriptToRestoreFromBackupCommandObject:
    def __init__(
        self,
        server=database_production.DB_HOST,
        port=database_production.DB_PORT,
        username=database_production.DB_USER,
        password=database_production.DB_PASSWORD,
    ):
        self.server=server
        self.port=port
        self.username=username
        self.password=password

    def generate_filename(self, table_group):
        return constants.RESTORE_SCRIPT_FILENAME[table_group]

    def generate_script_for_single_database_restore(
        self,
        backup_path_name,
        table_group,
        schema_name,
        database_name,
    ):

        restore_bat_filename = self.generate_filename(table_group)

        file = open(restore_bat_filename, "w")  # 'r' for reading and 'w' for writing
        file.write(constants.CMD_DIRECTORY)

        tables_to_restore = constants.TABLES_TO_RESTORE[table_group]

        for item in tables_to_restore:
            restore_script = constants.CMD_SCRIPT_TEMPLATE.format(
                server=self.server,
                port=self.port,
                username=self.username,
                password=self.password,
                backup_path_name=backup_path_name,
                table=item,
                schema=schema_name,
                database=database_name,
            )

            file.write(restore_script)

        file.close()

    def read_restore_script_from_file(self, restore_bat_filename):
        file = open(restore_bat_filename, "r")
        return file.read()

    def delete_restore_file(self, restore_bat_filename):
        return os.remove(restore_bat_filename)

    def handle(
        self,
        backup_path_name,
        table_group,
        schema_name=constants.RESTORE_SCHEMA,
        database_name=constants.RESTORE_DATABASE,
    ):
        self.generate_script_for_single_database_restore(
            backup_path_name,
            table_group,
            schema_name,
            database_name,
        )

        restore_bat_filename = self.generate_filename(table_group)
        contents = self.read_restore_script_from_file(restore_bat_filename)

        return contents


def handle_gafrica(
    backup_path_name="T:\Datamart_Backups\datamart_20200427_20200428_020535_full.backup",
    table_group="gafrica",
):
    cmd = ScriptToRestoreFromBackupCommandObject()
    return cmd.handle(backup_path_name, table_group)
