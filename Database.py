def configureSetTable():
    sql = "CREATE TABLE \"Set\"(\"Name\" character varying COLLATE pg_catalog.\"default\" NOT NULL,\"Code\" character varying COLLATE pg_catalog.\"default\" NOT NULL,\"ReleaseDate\" date NOT NULL,\"CardCount\" integer NOT NULL,\"SetType\" character varying COLLATE pg_catalog.\"default\",CONSTRAINT \"Set_pkey\" PRIMARY KEY (\"Code\"));"

def configureCardTable():
    sql = "CREATE TABLE \"Cards\"(\"Name\" character varying COLLATE pg_catalog.\"default\" NOT NULL,\"ReleaseDate\" date,\"OracleText\" character varying COLLATE pg_catalog.\"default\",\"URL\" character varying COLLATE pg_catalog.\"default\",\"Set\" character varying COLLATE pg_catalog.\"default\" NOT NULL,\"Id\" character varying COLLATE pg_catalog.\"default\" NOT NULL,CONSTRAINT \"Cards_pkey\" PRIMARY KEY (\"Id\"),CONSTRAINT \"SetLookup\" FOREIGN KEY (\"Set\")REFERENCES \"Set\" (\"Code\") MATCH SIMPLEON UPDATE NO ACTIONON DELETE CASCADE);"