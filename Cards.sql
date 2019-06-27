CREATE TABLE Cards
(
    Name character varying COLLATE pg_catalog."default" NOT NULL,
    ReleaseDate date,
    OracleText character varying COLLATE pg_catalog."default",
    URL character varying COLLATE pg_catalog."default",
    MTG_Set character varying COLLATE pg_catalog."default" NOT NULL,
    Id character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT Cards_pkey PRIMARY KEY (Id),
    CONSTRAINT SetLookup FOREIGN KEY (MTG_Set)
        REFERENCES MTG_Set (Code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;
