import psycopg2
import sqlalchemy
from io import StringIO
import pandas as pd

from constants import TopHatAnalyticsConfig as constants


class TopHatAnalyticsObject:
    def __init__(self):
        self.schema = constants.DB_SCHEMA

    def database_connect(self):
        """Connect to run queries"""
        return psycopg2.connect(
            user=constants.DB_USER,
            password=constants.DB_PASSWORD,
            host=constants.DB_HOST,
            port=constants.DB_PORT,
            database=constants.DB_DATABASE,
        )

    def database_engine_connect(self):
        """Connect to run load tables to database"""
        return sqlalchemy.create_engine(
            "postgresql://{user}:{password}@{host}:{port}/{database}".format(
                user=constants.DB_USER,
                password=constants.DB_PASSWORD,
                host=constants.DB_HOST,
                port=constants.DB_PORT,
                database=constants.DB_DATABASE,
            )
        )

    def execute_command(self, query):
        """Execute query on database"""
        with self.database_connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query)

    def load_query_to_dataframe(self, query):
        """Load query data into dataframe"""
        with self.database_connect() as conn:
            table = pd.read_sql_query(query.format(), conn)
            return table

    def copy_dataframe_to_csv(self, file_name, dataframe):
        """Load dataframe table to csv"""
        dataframe.to_csv(file_name, encoding="utf-8", index=False)

    def copy_dataframe_to_sql(self, table_name, dataframe):
        """Load dataframe table to database"""
        engine = self.database_engine_connect()
        dataframe.to_sql(
            table_name,
            con=engine,
            index=False,
            if_exists="replace",
            schema=self.schema,
            chunksize=1000,
        )

    def get_query_template_create_view(self, query, view_name):
        """Generate a create view sql template using existing query"""
        return constants.QUERY_TEMPLATE_CREATE_VIEW.format(
            query=query.format(schema=self.schema),
            schema=self.schema,
            view_name=view_name,
        )

    def load_query_to_sql_table(self, query, table_name):
        """Wrapper method to load directly from query to database table"""
        df = self.load_query_to_dataframe(query.format(schema=self.schema))
        self.copy_dataframe_to_sql(table_name, df)
        return df

    def load_view_to_database(self, query, view_name):
        """Wrapper method to load directly from query to database view"""
        query_template = self.get_query_template_create_view(query, view_name)
        self.execute_command(query_template)

    def load_query_to_csv(self, query, file_name):
        """Wrapper method to load directly from query to csv"""
        df = self.load_query_to_dataframe(query.format(schema=self.schema))
        self.copy_dataframe_to_csv(file_name, df)
        return df


if __name__ == "__main__":
    x = TopHatAnalyticsObject()

    # load table
    x.load_query_to_sql_table(
        query=constants.ANSWER_ONE_TOP_10_PROFESSOR,
        table_name="answer_one_top_professor",
    )
    x.load_query_to_sql_table(
        query=constants.ANSWER_TWO_STUDENT_LICENSE_2023,
        table_name="answer_two_student_license_2023",
    )
    x.load_query_to_sql_table(
        query=constants.ANSWER_THREE_ACTIVE_LICENSE,
        table_name="answer_three_active_license",
    )
    x.load_query_to_sql_table(
        query=constants.ANSWER_FOUR_PERCENTAGE_CHANGE,
        table_name="answer_four_percentage_change",
    )

    # load view
    x.load_view_to_database(
        query=constants.ANSWER_ONE_TOP_10_PROFESSOR,
        view_name="VW_ANSWER_ONE_TOP_10_PROFESSOR",
    )
    x.load_view_to_database(
        query=constants.ANSWER_TWO_STUDENT_LICENSE_2023,
        view_name="VW_ANSWER_TWO_STUDENT_LICENSE_2023",
    )
    x.load_view_to_database(
        query=constants.ANSWER_THREE_ACTIVE_LICENSE,
        view_name="VW_ANSWER_THREE_ACTIVE_LICENSE",
    )
    x.load_view_to_database(
        query=constants.ANSWER_FOUR_PERCENTAGE_CHANGE,
        view_name="VW_ANSWER_FOUR_PERCENTAGE_CHANGE",
    )

    # load csv
    x.load_query_to_csv(
        query=constants.ANSWER_ONE_TOP_10_PROFESSOR,
        file_name="VW_ANSWER_ONE_TOP_10_PROFESSOR.csv",
    )
    x.load_query_to_csv(
        query=constants.ANSWER_TWO_STUDENT_LICENSE_2023,
        file_name="VW_ANSWER_TWO_STUDENT_LICENSE_2023.csv",
    )
    x.load_query_to_csv(
        query=constants.ANSWER_THREE_ACTIVE_LICENSE,
        file_name="VW_ANSWER_THREE_ACTIVE_LICENSE.csv",
    )
    x.load_query_to_csv(
        query=constants.ANSWER_FOUR_PERCENTAGE_CHANGE,
        file_name="VW_ANSWER_FOUR_PERCENTAGE_CHANGE.csv",
    )
