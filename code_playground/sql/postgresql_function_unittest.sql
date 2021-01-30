/*
Writing Postgres Functions and Stored Procedures
http://sqlines.com/postgresql/how-to/return_result_set_from_stored_procedure
http://sqlines.com/postgresql/stored_procedures_functions
Add Defaults to Functions: https://stackoverflow.com/questions/39896329/how-to-write-function-for-optional-parameters-in-postgresql
*/

CREATE OR REPLACE FUNCTION unittest_data_payment_refund(
	is_mapping_missing refcursor DEFAULT 'is_mapping_missing'
	, is_transfer_net_zero refcursor DEFAULT 'is_transfer_net_zero'
	, is_credit_card_net_zero refcursor DEFAULT 'is_credit_card_net_zero'
) RETURNS SETOF refcursor AS $$
--DECLARE c_service refcursor;
--DECLARE c_booking refcursor;
 BEGIN DROP TABLE IF EXISTS unittest_data;

CREATE TEMP TABLE unittest_data AS (
	SELECT
		l.*
		, d.dist_type
		, d.gl_account_number
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
);

OPEN is_mapping_missing FOR
SELECT
	*
FROM
	unittest_data
WHERE
	gl_account_number IS NULL;

RETURN NEXT is_mapping_missing;

OPEN is_transfer_net_zero FOR WITH raw AS (
	SELECT
		*
	FROM
		unittest_data
	WHERE
		SUBSTRING(gl_account_number, 15, 5) = '12720'
)
SELECT
	*
FROM
	raw
WHERE
	(
		(
			SELECT
				SUM(net_amount) net_amount
			FROM
				raw
		) <> 0
	);

RETURN NEXT is_transfer_net_zero;

OPEN is_credit_card_net_zero FOR WITH raw AS (
	SELECT
		*
	FROM
		unittest_data
	WHERE
		SUBSTRING(gl_account_number, 15, 5) = '12715'
)
SELECT
	*
FROM
	raw	
WHERE
 object_id IN 
		( SELECT object_id FROM (
			SELECT
				booking_no,
				object_id,
				SUM(net_amount) net_amount
			FROM raw
			GROUP BY 1,2
			HAVING SUM(net_amount) <> 0
		) x
	);

RETURN NEXT is_credit_card_net_zero;

END;

$$ LANGUAGE plpgsql;

BEGIN;

SELECT
	COUNT(*)
FROM
	(
		SELECT
			 unittest_data_payment_refund()
	) x;

SELECT
	unittest_data_payment_refund();

FETCH ALL IN "is_mapping_missing";

FETCH ALL IN "is_transfer_net_zero";

FETCH ALL IN "is_credit_card_net_zero";

COMMIT;