
CREATE TABLE networks(
    network_id UUID PRIMARY KEY,
    network_name TEXT NOT NULL,
    network_description TEXT
);
ALTER TABLE networks OWNER TO nethound;

CREATE TABLE network_stats(
    network_id UUID NOT NULL,
    event_timestamp TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'utc'),
    download_speed FLOAT NOT NULL,
    upload_speed FLOAT,
    exec_time FLOAT NOT NULL,
    PRIMARY KEY (network_id, event_timestamp)
);
ALTER TABLE network_stats OWNER TO nethound;