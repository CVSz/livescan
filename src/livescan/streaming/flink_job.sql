CREATE TABLE source_events (
  ts BIGINT,
  src INT,
  dst INT,
  weight DOUBLE,
  reward DOUBLE,
  action INT,
  features ARRAY<DOUBLE>,
  WATERMARK FOR ts AS TO_TIMESTAMP_LTZ(ts, 3) - INTERVAL '5' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'livescan-events',
  'properties.bootstrap.servers' = 'kafka:9092',
  'format' = 'json',
  'scan.startup.mode' = 'latest-offset'
);

CREATE TABLE feature_sink (
  window_start TIMESTAMP(3),
  src INT,
  avg_reward DOUBLE,
  edge_count BIGINT
) WITH (
  'connector' = 'kafka',
  'topic' = 'livescan-features',
  'properties.bootstrap.servers' = 'kafka:9092',
  'format' = 'json'
);

INSERT INTO feature_sink
SELECT
  window_start,
  src,
  AVG(reward) AS avg_reward,
  COUNT(*) AS edge_count
FROM TABLE(
  TUMBLE(TABLE source_events, DESCRIPTOR(TO_TIMESTAMP_LTZ(ts, 3)), INTERVAL '1' MINUTE)
)
GROUP BY window_start, src;
