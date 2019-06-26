CREATE TABLE public.Cards
(
    Name character varying COLLATE pg_catalog."default" NOT NULL,
    ReleaseDate date,
    OracleText character varying COLLATE pg_catalog."default",
    URL character varying COLLATE pg_catalog."default",
    MTG_Set character varying COLLATE pg_catalog."default" NOT NULL,
    Id character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT Cards_pkey PRIMARY KEY (Id),
    CONSTRAINT SetLookup FOREIGN KEY (Set)
        REFERENCES public.MTG_Set (Code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.Cards
    OWNER to postgres;