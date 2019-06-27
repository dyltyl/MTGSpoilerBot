CREATE TABLE cards
(
    name character varying COLLATE pg_catalog."default" NOT NULL,
    release_date date,
    oracle_text character varying COLLATE pg_catalog."default",
    url character varying COLLATE pg_catalog."default",
    mtg_set character varying COLLATE pg_catalog."default" NOT NULL,
    id character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT Cards_pkey PRIMARY KEY (id),
    CONSTRAINT SetLookup FOREIGN KEY (mtg_set)
        REFERENCES mtg_set (code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;
