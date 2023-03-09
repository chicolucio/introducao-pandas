# Tutorial de Pandas

Material de introdução ao Pandas (EM CONSTRUÇÃO)

## Uso

1. Clone o repositório
2. Crie um ambiente virtual com Python 3.10+
3. Ative o ambiente virtual
4. Instale as dependências
5. Use o notebook `eda_meteorite.ipynb`

Para o material de PyODBC:

6. Instale o PostgreSQL de acordo com a documentação oficial
7. Crie um `.env` com base no `env_sample` fornecido
8. Use os notebooks `postgresql.ipynb` e `sqlite.ipynb` 

### Detalhes

```bash
git clone git@github.com:chicolucio/introducao-pandas.git
cd introducao-pandas
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp env-sample .env
```

Para criar a tabela `teachers` mostrada no Notebook `postgresql.ipynb`:

```sql
CREATE TABLE teachers (
    id bigserial,
    first_name varchar(25),
    last_name varchar(50),
    school varchar(50),
    hire_date date,
    salary numeric
);

INSERT INTO teachers (first_name, last_name, school, hire_date, salary)
VALUES ('Janet', 'Smith', 'F.D. Roosevelt HS', '2011-10-30', 36200),
       ('Lee', 'Reynolds', 'F.D. Roosevelt HS', '1993-05-22', 65000),
       ('Samuel', 'Cole', 'Myers Middle School', '2005-08-01', 43500),
       ('Samantha', 'Bush', 'Myers Middle School', '2011-10-30', 36200),
       ('Betty', 'Diaz', 'Myers Middle School', '2005-08-30', 43500),
       ('Kathleen', 'Roush', 'F.D. Roosevelt HS', '2010-10-22', 38500);
```

Para criar a tabela `us_countries_pop_est_2019` mostrada no Notebook `postgresql.ipynb`:

```sql
CREATE TABLE us_countries_pop_est_2019 (
    state_fips text,                         -- State FIPS code
    county_fips text,                        -- County FIPS code
    region smallint,                         -- Region
    state_name text,                         -- State name	
    county_name text,                        -- County name
    area_land bigint,                        -- Area (Land) in square meters
    area_water bigint,                       -- Area (Water) in square meters
    internal_point_lat numeric(10,7),        -- Internal point (latitude)
    internal_point_lon numeric(10,7),        -- Internal point (longitude)
    pop_est_2018 integer,                    -- 2018-07-01 resident total population estimate
    pop_est_2019 integer,                    -- 2019-07-01 resident total population estimate
    births_2019 integer,                     -- Births from 2018-07-01 to 2019-06-30
    deaths_2019 integer,                     -- Deaths from 2018-07-01 to 2019-06-30
    international_migr_2019 integer,         -- Net international migration from 2018-07-01 to 2019-06-30
    domestic_migr_2019 integer,              -- Net domestic migration from 2018-07-01 to 2019-06-30
    residual_2019 integer,                   -- Residual for 2018-07-01 to 2019-06-30
    CONSTRAINT counties_2019_key PRIMARY KEY (state_fips, county_fips)	
);
```

Importe os dados do CSV fornecido:

```sql
COPY us_countries_pop_est_2019
FROM "data/us_countries_pop_est_2019.csv"
WITH (FORMAT CSV, HEADER);
```
