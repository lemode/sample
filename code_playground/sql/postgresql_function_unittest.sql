/*
Create function to generate unittest results
Keeps the table formatted and any data being entered into the table in one place/format
*/

CREATE OR REPLACE
FUNCTION unittest_insert_results(
    task_category VARCHAR
	,task VARCHAR
	, outcome VARCHAR
	, sql_query VARCHAR
	, next_steps VARCHAR
	, etl_load_date TIMESTAMP DEFAULT NOW()
) RETURNS VOID AS $$ BEGIN CREATE TABLE IF NOT EXISTS public.unittest_task_results (
	task_category VARCHAR(300) NOT NULL
    ,task VARCHAR(300) NOT NULL
	, outcome VARCHAR(50) NULL
	, sql_query VARCHAR(10000) NULL
	, next_steps VARCHAR(10000) NULL
	, etl_load_date TIMESTAMP NULL
	, etl_load_user VARCHAR(100) NULL
	, etl_load_process_name VARCHAR(100) NULL
);

INSERT
	INTO
	public.unittest_task_results (
		task_category
        ,task
		, outcome
		, sql_query
		, next_steps
		, etl_load_date
	)
VALUES (
	task_category
    ,task
	, outcome
	, sql_query
	, next_steps
	, etl_load_date
);

END;

$$ LANGUAGE plpgsql;

/*
Generate view to unittest payments and refunds
PHASE1 - work with data staged each day
PHASE2 - build function to alternate between daily and archive staged data
*/

CREATE OR REPLACE VIEW dmv_unittest_payment_refund AS (
	WITH stage_data AS (
		SELECT
			l.*
			, d.dist_type
			, d.gl_account_number
			, SUBSTRING(d.gl_account_number, 15, 5) AS seg5_gl_account
			, d.dist_reference
			, d.debit_amount
			, d.credit_amount
			, d.dist_line_id
			, d.dist_id
			, (
				COALESCE(d.debit_amount, 0)-COALESCE(d.credit_amount, 0)
			) net_amount
		FROM
			payment_refund_lines l
		LEFT JOIN payment_refund_distributions d ON
			l.booking_no = d.booking_no
			AND l.line_id = d.dist_line_id
	)
	SELECT
		*
		, SUM(CASE WHEN seg5_gl_account = '12720' THEN net_amount ELSE 0 END ) OVER (
		ORDER BY
			seg5_gl_account
		) = 0 AS is_transfer_clearing_balanced
		, SUM(CASE WHEN seg5_gl_account = '12715' THEN net_amount ELSE 0 END ) OVER (PARTITION BY booking_no
		ORDER BY
			seg5_gl_account
		) = 0 AS is_credit_card_clearing_balanced
		,gl_account_number IS NOT NULL AS has_gl_mapping
	FROM
		stage_data
);


/*
OPTION #1 Create payment and refund unittest function to write to unittest task results
For overall payments and refunds to run just the test
*/

 
CREATE OR REPLACE
FUNCTION run_unittest_payment_refund(integration_run_date TIMESTAMP DEFAULT NOW()
) RETURNS void AS $$ 

DECLARE _task_category varchar := 'run_unittest_payment_refund';

DECLARE task varchar;
DECLARE sql_query varchar;
DECLARE next_steps varchar;


BEGIN

task := 'is_transfer_clearing_balanced';
sql_query := 'SELECT * FROM dmv_unittest_payment_refund WHERE is_transfer_clearing_balanced = false';
next_steps := NULL;

if exists (SELECT 1 FROM dmv_unittest_payment_refund WHERE is_transfer_clearing_balanced = false)
THEN PERFORM unittest_insert_results(_task_category,task,'FAIL',sql_query,next_steps);
ELSE PERFORM unittest_insert_results(_task_category,task,'PASS',sql_query,next_steps);
END IF; 

task := 'is_credit_card_clearing_balanced';
sql_query := 'SELECT * FROM dmv_unittest_payment_refund WHERE is_credit_card_clearing_balanced = false';
next_steps := NULL;

if exists (SELECT 1 FROM dmv_unittest_payment_refund WHERE is_credit_card_clearing_balanced = false)
THEN PERFORM unittest_insert_results(_task_category,task,'FAIL',sql_query,next_steps);
ELSE PERFORM unittest_insert_results(_task_category,task,'PASS',sql_query,next_steps);
END IF; 

task := 'has_gl_mapping';
sql_query := 'SELECT * FROM dmv_unittest_payment_refund WHERE has_gl_mapping = false';
next_steps := NULL;

if exists (SELECT 1 FROM dmv_unittest_payment_refund WHERE has_gl_mapping = false)
THEN PERFORM unittest_insert_results(_task_category,task,'FAIL',sql_query,next_steps);
ELSE PERFORM unittest_insert_results(_task_category,task,'PASS',sql_query,next_steps);
END IF; 

END;

$$ LANGUAGE plpgsql;

/*
OPTION #2 Create payment and refund unittest function to write to unittest task results
For each records that fails add a row into the file task results table
*/

CREATE OR REPLACE FUNCTION public.run_unittest_payment_refund(integration_run_date timestamp without time zone DEFAULT now())
 RETURNS void
 LANGUAGE plpgsql
AS $function$ 

DECLARE _task_category varchar := 'run_unittest_payment_refund';

DECLARE task varchar;
DECLARE source_keys varchar DEFAULT NULL;
DECLARE next_steps varchar DEFAULT NULL;
DECLARE row_data dmv_unittest_payment_refund%ROWTYPE;

BEGIN

task := 'has_transfer_clearing_balance';

IF EXISTS (SELECT 1 FROM dmv_unittest_payment_refund WHERE has_transfer_clearing_balance = true)
THEN 
    FOR row_data IN (SELECT * FROM dmv_unittest_payment_refund WHERE has_transfer_clearing_balance = true) LOOP
        PERFORM unittest_insert_results(_task_category,task,'FAIL',row_data.source_key,next_steps);
    END LOOP;
   
ELSE PERFORM unittest_insert_results(_task_category,task,'PASS',source_keys,next_steps);
END IF; 

task := 'has_credit_card_clearing_balance';


IF EXISTS (SELECT 1 FROM dmv_unittest_payment_refund WHERE has_credit_card_clearing_balance = true)
THEN 
    FOR row_data IN (SELECT * FROM dmv_unittest_payment_refund WHERE has_credit_card_clearing_balance = true) LOOP
        PERFORM unittest_insert_results(_task_category,task,'FAIL',row_data.source_key,next_steps);
    END LOOP;
   
ELSE PERFORM unittest_insert_results(_task_category,task,'PASS',source_keys,next_steps);
END IF; 

task := 'has_missing_gl_mapping';

IF EXISTS (SELECT 1 FROM dmv_unittest_payment_refund WHERE has_missing_gl_mapping = true)
THEN 
    FOR row_data IN (SELECT * FROM dmv_unittest_payment_refund WHERE has_missing_gl_mapping = true) LOOP
        PERFORM unittest_insert_results(_task_category,task,'FAIL',row_data.source_key,next_steps);
    END LOOP;
   
ELSE PERFORM unittest_insert_results(_task_category,task,'PASS',source_keys,next_steps);
END IF;

END;

$function$
;


/*
Run compass function to check source data
*/

CREATE OR REPLACE FUNCTION public.run_unittest_compass_to_datamart(integration_run_date timestamp without time zone DEFAULT now())
 RETURNS void
 LANGUAGE plpgsql
AS $function$ DECLARE _task_category VARCHAR := 'run_unittest_compass_to_datamart';

DECLARE task VARCHAR;

DECLARE source_keys VARCHAR DEFAULT NULL;

DECLARE next_steps VARCHAR DEFAULT NULL;

DECLARE row_data RECORD;

BEGIN task := 'is_combo_trip_code_missing_child_trips';


DROP TABLE IF EXISTS exception_records;

CREATE TEMP TABLE exception_records AS 

SELECT
		DISTINCT t."TripId"::text || '   KEYS: TripId' AS source_key

	FROM
		trip t
	LEFT JOIN child_trip ct ON
		t."TripId" = ct."TripId"
	WHERE
		t."Is_Combo" = 1
		AND t."TripId" IN (
			SELECT
				id
			FROM
				tx_log tl
		UNION ALL
			SELECT
				id
			FROM
				tx_log_archive tla
		)
		AND ct."TripId" IS NULL
	ORDER BY
		1 DESC
;



IF EXISTS (
	SELECT
		1
	FROM exception_records
) THEN FOR row_data IN (SELECT * FROM exception_records
	
) LOOP PERFORM unittest_insert_results(
	_task_category
	, task
	, 'FAIL'
	, row_data.source_key
	, next_steps
);

END LOOP;
ELSE PERFORM unittest_insert_results(
	_task_category
	, task
	, 'PASS'
	, source_keys
	, next_steps
);

END IF;

END;

$function$
;


/*
Run master function
*/

CREATE OR REPLACE FUNCTION public.run_unittest_daily_integration()
 RETURNS void
 LANGUAGE plpgsql
AS $function$ 

BEGIN 
PERFORM run_unittest_compass_to_datamart();
PERFORM run_unittest_payment_refund();

END;

$function$
;
