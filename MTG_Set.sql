CREATE TABLE mtg_set
(
    name character varying COLLATE pg_catalog."default" NOT NULL,
    code character varying COLLATE pg_catalog."default" NOT NULL,
    release_date date NOT NULL,
    card_count integer NOT NULL,
    set_type character varying COLLATE pg_catalog."default",
    CONSTRAINT Set_pkey PRIMARY KEY (code)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;
