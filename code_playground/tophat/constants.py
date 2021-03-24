class TopHatAnalyticsConfig:
    DB_USER = "lemode"
    DB_PASSWORD = ""
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_DATABASE = "lemode"
    DB_SCHEMA = "sample_data"

    QUERY_TEMPLATE_CREATE_VIEW = (
        "CREATE OR REPLACE VIEW {schema}.{view_name} AS ({query});"
    )

    RENAME_TABLES_TO_DATA_DICTIONARY_QUERY = """
        SELECT * INTO sample_data.course_enrollment_new FROM sample_data.transactions;
        SELECT * INTO sample_data.transactions_new FROM sample_data.course_enrollment;
        DROP TABLE transactions;
        DROP TABLE course_enrollment;
        SELECT * INTO sample_data.course_enrollment FROM sample_data.course_enrollment_new;
        SELECT * INTO sample_data.transactions FROM sample_data.transactions_new;
        DROP TABLE transactions_new;
        DROP TABLE course_enrollment_new;
    """

    # QUESTION #1 TOP PROFESSORS
    ANSWER_ONE_TOP_10_PROFESSOR = """
    WITH engagement_transaction_product AS (
    SELECT t.transaction_date::date + p.license_duration_days -1 AS subscription_end_date
        ,t.*,p.product_category,p.product_subcategory,p.license_duration_days
        FROM {schema}.transactions t
        LEFT JOIN {schema}.product_dimension p ON t.product_key = p.product_key 
        WHERE p.product_category = 'Engagement' 
        /* remove categories not equal to Engagement sales */
        ) 
    , course_transactions AS (
    SELECT 
    total/number_of_courses_per_transaction AS course_total
    ,total/number_of_courses_per_transaction/license_duration_days AS course_daily_total
    ,* 
    FROM (
        SELECT 
        COUNT(c.course_key) OVER (PARTITION BY c.student_key,etp.transaction_line_item_id) AS number_of_courses_per_transaction
            ,c.enrollment_date_utc,etp.*,c.*
        FROM {schema}.course_enrollment c 
        JOIN engagement_transaction_product etp 
        /* each course is always expected to have a related transaction */
            ON c.student_key = etp.student_key
            AND c.etl_created_at BETWEEN etp.transaction_date AND etp.subscription_end_date
            /* transaction only apply to a course between purchase date and the subscription end date
            enrollment date can sometime fall on the last few days of one license but etl_created_at would say under which license the course was enrolled */
        WHERE c.is_deleted = FALSE
    --	AND c.student_key IN (15975487,15987127,15993145,15965910,20972620)
        ORDER BY c.student_key,etp.product_key, etp.transaction_date
    --LIMIT 50
    )x
    )
    , aug_sep_revenue AS (
    SELECT 
    (full_period+partial_start_period+partial_end_period+partial_period_within) number_of_revenue_days
    ,(full_period+partial_start_period+partial_end_period+partial_period_within) * course_daily_total AS revenue_in_period
    ,* FROM (
    SELECT 
    CASE WHEN transaction_date::date < '2020-08-01'::date AND subscription_end_date::date > '2020-09-15'::date THEN '2020-09-15'::date - '2020-08-01'::date ELSE 0 END AS full_period
    ,CASE WHEN transaction_date::date < '2020-08-01'::date AND subscription_end_date::date between '2020-08-01'::date AND '2020-09-15'::date THEN subscription_end_date::date - '2020-08-01'::date ELSE 0 END AS partial_end_period
    ,CASE WHEN transaction_date::date between '2020-08-01'::date AND '2020-09-15'::date AND subscription_end_date::date > '2020-09-15'::date THEN '2020-09-15'::date - transaction_date::date  ELSE 0 END AS partial_start_period
    ,CASE WHEN transaction_date::date > '2020-08-01'::date AND subscription_end_date::date < '2020-09-15'::date THEN subscription_end_date::date - transaction_date::date ELSE 0 END AS partial_period_within
    ,*
    FROM course_transactions
    )x
    )
    SELECT 
    professor_key 
    ,SUM(revenue_in_period)::decimal(18,2)
    FROM aug_sep_revenue
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 10

    """

    # QUESTION #2 STUDENTS WITH A LICENSE AS OF FEB 1
    ANSWER_TWO_STUDENT_LICENSE_2023 = """
    WITH engagement_transaction_product AS (
    SELECT t.transaction_date::date + p.license_duration_days -1 AS subscription_end_date
        ,t.*,p.product_category,p.product_subcategory,p.license_duration_days
        FROM {schema}.transactions t
        LEFT JOIN {schema}.product_dimension p ON t.product_key = p.product_key 
        WHERE p.product_category = 'Engagement' 
        /* remove categories not equal to Engagement sales */
        ) SELECT DISTINCT student_key, count(student_key) number_of_licenses ,count(DISTINCT student_key) number_of_students_with_licenses FROM engagement_transaction_product
        WHERE subscription_end_date >= '2023-02-01'::date  --count of 7620 / 7587. They may not have signed up on a course
        group by 1
    """

    # QUESTION #3 ACTIVE LICENSES FOR EACH MONTH BETWEEN JANUARY AND DECEMBER 2020
    ANSWER_THREE_ACTIVE_LICENSE = """

    WITH engagement_transaction_product AS (
    SELECT t.transaction_date::date + p.license_duration_days -1 AS subscription_end_date
        ,t.*,p.product_category,p.product_subcategory,p.license_duration_days
        FROM {schema}.transactions t
        LEFT JOIN {schema}.product_dimension p ON t.product_key = p.product_key 
        WHERE p.product_category = 'Engagement' 
        /* remove categories not equal to Engagement sales */
        )
    , time_period AS (
    SELECT * FROM (
    SELECT start_date::date, (LEAD(start_date) OVER (ORDER BY start_date ASC)::date-1) AS end_date
    FROM generate_series
            ( '2020-01-01'::timestamp 
            , '2021-01-01'::timestamp
            , '1 month'::INTERVAL) start_date
    ORDER BY 1
    ) date_range
    WHERE end_date IS NOT null
    )
    SELECT start_date,count(*) FROM (
    SELECT 
    etp.transaction_line_item_id,etp.transaction_id, etp.transaction_date, etp.subscription_end_date,tp.*
    FROM engagement_transaction_product etp
    JOIN time_period tp
    ON (etp.subscription_end_date::date >= tp.start_date AND etp.transaction_date::date < tp.end_date)
    OR (etp.subscription_end_date::date < tp.end_date AND etp.transaction_date::date > tp.start_date)
    --WHERE etp.student_key IN (15975487,15987127,15993145,15965910,20972620,19486877)
    ORDER BY etp.transaction_date,etp.transaction_line_item_id
    ) active_license
    GROUP BY 1
    ORDER BY 1
    """

    # QUESTION #4 PERCENTAGE CHANGE OF STUDENTS BETWEEN FEB 1 AND OCT 1 WITH ACTIVE LICENSES
    ANSWER_FOUR_PERCENTAGE_CHANGE = """
    WITH engagement_transaction_product AS (
    SELECT t.transaction_date::date + p.license_duration_days -1 AS subscription_end_date
        ,t.*,p.product_category,p.product_subcategory,p.license_duration_days
        FROM {schema}.transactions t
        LEFT JOIN {schema}.product_dimension p ON t.product_key = p.product_key 
        WHERE p.product_category = 'Engagement' 
        /* remove categories not equal to Engagement sales */
        ) 
        SELECT start_month
        ,sum(number_of_students_with_licenses) AS student_count_with_licenses
        ,sum(feb_license) AS feb_license
        ,100*((sum(number_of_students_with_licenses)/sum(feb_license))-1) AS distinct_student_percent  
    FROM (
    SELECT start_month, number_of_students_with_licenses,FIRST_VALUE(number_of_students_with_licenses) OVER (ORDER BY start_month ASC) feb_license FROM (
        SELECT '2020-02-01'::date AS start_month,count(student_key) number_of_licenses ,count(DISTINCT student_key) number_of_students_with_licenses FROM engagement_transaction_product
        WHERE subscription_end_date >= '2020-02-01'::date
        AND transaction_date < '2020-02-01'
        UNION ALL
        SELECT '2020-10-01'::date AS start_month,count(student_key) number_of_licenses ,count(DISTINCT student_key) number_of_students_with_licenses FROM engagement_transaction_product
        WHERE subscription_end_date >= '2020-10-01'::date
        AND transaction_date < '2020-10-01' 
    ) active_license
    ) student_count
    GROUP BY 1
    """
