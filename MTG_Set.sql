CREATE TABLE MTG_Set
(
    Name character varying COLLATE pg_catalog."default" NOT NULL,
    Code character varying COLLATE pg_catalog."default" NOT NULL,
    ReleaseDate date NOT NULL,
    CardCount integer NOT NULL,
    SetType character varying COLLATE pg_catalog."default",
    CONSTRAINT Set_pkey PRIMARY KEY (Code)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;
