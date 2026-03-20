BEGIN;

CREATE TABLE IF NOT EXISTS messages (
 message_user VARCHAR(64),
 message_ts TIMESTAMP,
 message_content VARCHAR,
 response VARCHAR
)
;

COMMIT;
