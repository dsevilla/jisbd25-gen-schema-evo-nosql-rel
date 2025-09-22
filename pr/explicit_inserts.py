from pymongo import MongoClient
import asyncio
import aiosqlite
import json

client = MongoClient('mongodb://localhost:27017')
db = client['slideshows']

# slideshow insert (from pr.md.j2)
db.slideshow.insert_one({
    "name": """pr.md""",
    "meta": {},
    "source_file": """pr.md.j2""",
    "slides_count": 4,
})

# slide:
db.slide.insert_one({
    "title": """""",
    "body": """marp: true
title: A Generic Schema Evolution Approach for NoSQL and Relational Databases
theme: default
headingDivider: 3
inlineSVG: true
#paginate: true
auto-scaling: true
size: 16:9
style: |
  /* Slide numbering using CSS counters */
  /* Reset the counter at the document root */

  section {
    font-family: 'IBM Plex Sans';
    font-size: 25pt;
    display: inherit;
    #padding-top: 25pt;
    /* ensure pseudo-element positions correctly */
    position: relative;
    overflow: visible;
  }

{% set counter = namespace(n=1) %}
{% macro slide_style() -%}
  <style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "{{counter.n}}";
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate({% if counter.n>9 %}-22%{% else %}40%{% endif %}, -40%);
    font-family: 'Bodoni Moda', cursive;
    font-size: 700pt;
    line-height: 1;
    color: rgba(255, 200, 210, 0.55); /* pastel pink */
    #filter: blur(8px);
    opacity: 0.4;
    z-index: 0;
    pointer-events: none;
    white-space: nowrap;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  /* Keep slide content above the background digit */
  section > * {
    position: relative;
    z-index: 1;
  }
  </style>
{%- set counter.n = counter.n + 1 %}
{%- endmacro %}""",
    "notes": """""",
    "source_file": """pr.md.j2""",
})

# slide: A Generic Schema Evolution Approach for NoSQL and Relational Databases
db.slide.insert_one({
    "title": """A Generic Schema Evolution Approach for NoSQL and Relational Databases""",
    "body": """<style scoped>
img[alt~="center"] {  display: block;  margin: 0 auto;}
</style>
![w:950 center](img/paper.png)



{{ slide_style() }}


Alberto Hernández Chillón, Meike Klettke,
**Diego Sevilla Ruiz**, Jesús García Molina

Jornadas de Ingeniería del Software y Bases de Datos,
Córdoba. 2025""",
    "notes": """_class: lead""",
    "source_file": """pr.md.j2""",
})

# slide: Almacenamiento
db.slide.insert_one({
    "title": """Almacenamiento""",
    "body": """{{ slide_style() }}
<style scoped>
img[alt~="center"] {  display: block;  margin: 0 auto;}
</style>

{{ generate_mermaid_diagram('slide_schema1','''
    direction LR
    SLIDESHOW {
        string name PK
        string email
        string author
        timestamp created_at
    }

    SLIDE {
        uuid id PK
        string title
        text body
        text notes
    }

    SLIDESHOW |o..|{ SLIDE : slides
''', 900, -1, 'erDiagram', 'png') }}






{{ slide_style() }}



<style scoped>
  h2 {
    padding: 10%;
    font-size: 70pt;
  }
</style>


### Introducción

{{ slide_style() }}

<style scoped>
  section { font-size: 22pt; }
</style>

- El almacenamiento forma parte del concepto de estado de una aplicación o servicio
- Las principales dimensiones que valoramos para escoger un tipo de almacenamiento u otro son:
  - Unidad de acceso  mímina
  - Métricas y valores de rendimiento
  - Forma de acceso, concurrencia
  - Elasticidad
  - Disponibilidad
  - Capacidades extra (ej: versionado, ciclo de vida)


## Almacenamiento a nivel de bloque

{{ slide_style() }}



<style scoped>
  h2 {
    padding: 10%;
    font-size: 70pt;
  }
</style>


### S3: PUT de un objeto
{{ slide_style() }}
- PUT sube un objeto a un *Bucket*
- Se puede subir de una vez o *multipart*
- Ejemplo:

```python
import re
```

{{ generate_code_block('python', '''
import boto3
S3API = boto3.client("s3", region_name="us-east-1")
bucket_name= "samplebucket"
filename = "/resources/website/core.css"
S3API.upload_file(filename, bucket_name, "core.css",
        ExtraArgs={"ContentType": "text/css",
                   "CacheControl": "max-age=0"})'''
                   ) }}""",
    "notes": """_class: invert

_class: invert""",
    "source_file": """pr.md.j2""",
})

# slide: Other section
db.slide.insert_one({
    "title": """Other section""",
    "body": """{{ slide_style() }}
<style scoped>
  pre {
    background: #f4f4f4;
    padding: 10px;
    font-size: 300%;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
</style>

<pre>
abc
</pre>



{{ slide_style() }}

## Database Schema Example

{{ slide_style() }}

Here's an example of how to include ER diagrams in your presentation:

<style scoped>
img[alt~="center"] { display: block;  margin: 0 auto;}
</style>

{{ generate_mermaid_diagram('user_schema','''
    USER {
        uuid id PK
        string email UK
        timestamp created_at
    }

    SCHEMA_VERSION {
        int version PK
        timestamp applied_at
        text description
    }

    MIGRATION {
        uuid id PK
        int from_version FK
        int to_version FK
        text sql_script
        boolean applied
    }

    SCHEMA_VERSION ||--o{ MIGRATION : from_version
    SCHEMA_VERSION ||--o{ MIGRATION : to_version
''', 400, -1, 'erDiagram', 'png') }}


This diagram shows the schema evolution tracking system.

### More slides
{{ slide_style() }}

### And more slides
{{ slide_style() }}

### And even more
{{ slide_style() }}""",
    "notes": """""",
    "source_file": """pr.md.j2""",
})

client.close()


# --- Equivalent inserts using aiosqlite (SQLite async) ---
async def sqlite_inserts(db_path: str = 'slideshows.db'):
    async with aiosqlite.connect(db_path) as db:
        # create tables
        await db.execute('''
        CREATE TABLE IF NOT EXISTS slideshow (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            meta TEXT,
            source_file TEXT,
            slides_count INTEGER
        )
        ''')

        await db.execute('''
        CREATE TABLE IF NOT EXISTS slide (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slideshow_id INTEGER,
            idx INTEGER,
            title TEXT,
            body TEXT,
            notes TEXT,
            source_file TEXT,
            FOREIGN KEY(slideshow_id) REFERENCES slideshow(id)
        )
        ''')
        await db.commit()

        # explicit slideshow insert (matches MongoDB slideshow insert above)
        slideshow_meta = {}
        await db.execute(
            "INSERT INTO slideshow (name, meta, source_file, slides_count) VALUES (?, ?, ?, ?)",
            ("pr.md", json.dumps(slideshow_meta), "pr.md.j2", 4),
        )
        await db.commit()

        # get last slideshow id
        async with db.execute("SELECT last_insert_rowid()") as cur:
            row = await cur.fetchone()
            slideshow_id = row[0]

        # explicit slide inserts (no loop) — mirror the MongoDB slides above
        await db.execute(
            "INSERT INTO slide (slideshow_id, idx, title, body, notes, source_file) VALUES (?, ?, ?, ?, ?, ?)",
            (
                slideshow_id,
                1,
                "",
                """marp: true
title: A Generic Schema Evolution Approach for NoSQL and Relational Databases
theme: default
headingDivider: 3
inlineSVG: true
#paginate: true
auto-scaling: true
size: 16:9
style: |
  /* Slide numbering using CSS counters */
  /* Reset the counter at the document root */

  section {
    font-family: 'IBM Plex Sans';
    font-size: 25pt;
    display: inherit;
    #padding-top: 25pt;
    /* ensure pseudo-element positions correctly */
    position: relative;
    overflow: visible;
  }

{% set counter = namespace(n=1) %}
{% macro slide_style() -%}
  <style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "{{counter.n}}";
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate({% if counter.n>9 %}-22%{% else %}40%{% endif %}, -40%);
    font-family: 'Bodoni Moda', cursive;
    font-size: 700pt;
    line-height: 1;
    color: rgba(255, 200, 210, 0.55); /* pastel pink */
    #filter: blur(8px);
    opacity: 0.4;
    z-index: 0;
    pointer-events: none;
    white-space: nowrap;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  /* Keep slide content above the background digit */
  section > * {
    position: relative;
    z-index: 1;
  }
  </style>
{%- set counter.n = counter.n + 1 %}
{%- endmacro %}""",
                "",
                "pr.md.j2",
            ),
        )
        await db.commit()

        await db.execute(
            "INSERT INTO slide (slideshow_id, idx, title, body, notes, source_file) VALUES (?, ?, ?, ?, ?, ?)",
            (
                slideshow_id,
                2,
                "A Generic Schema Evolution Approach for NoSQL and Relational Databases",
                """<style scoped>
img[alt~="center"] {  display: block;  margin: 0 auto;}
</style>
![w:950 center](img/paper.png)


{{ slide_style() }}


Alberto Hernández Chillón, Meike Klettke,
**Diego Sevilla Ruiz**, Jesús García Molina

Jornadas de Ingeniería del Software y Bases de Datos,
Córdoba. 2025""",
                "_class: lead",
                "pr.md.j2",
            ),
        )
        await db.commit()

        await db.execute(
            "INSERT INTO slide (slideshow_id, idx, title, body, notes, source_file) VALUES (?, ?, ?, ?, ?, ?)",
            (
                slideshow_id,
                3,
                "Almacenamiento",
                """{{ slide_style() }}
<style scoped>
img[alt~="center"] {  display: block;  margin: 0 auto;}
</style>

{{ generate_mermaid_diagram('slide_schema1','''
    direction LR
    SLIDESHOW {
        string name PK
        string email
        string author
        timestamp created_at
    }

    SLIDE {
        uuid id PK
        string title
        text body
        text notes
    }

    SLIDESHOW |o..|{ SLIDE : slides
''', 900, -1, 'erDiagram', 'png') }}





{{ slide_style() }}



<style scoped>
  h2 {
    padding: 10%;
    font-size: 70pt;
  }
</style>


### Introducción

{{ slide_style() }}

<style scoped>
  section { font-size: 22pt; }
</style>

- El almacenamiento forma parte del concepto de estado de una aplicación o servicio
- Las principales dimensiones que valoramos para escoger un tipo de almacenamiento u otro son:
  - Unidad de acceso  mímina
  - Métricas y valores de rendimiento
  - Forma de acceso, concurrencia
  - Elasticidad
  - Disponibilidad
  - Capacidades extra (ej: versionado, ciclo de vida)


## Almacenamiento a nivel de bloque

{{ slide_style() }}



<style scoped>
  h2 {
    padding: 10%;
    font-size: 70pt;
  }
</style>


### S3: PUT de un objeto
{{ slide_style() }}
- PUT sube un objeto a un *Bucket*
- Se puede subir de una vez o *multipart*
- Ejemplo:

```python
import re
```

{{ generate_code_block('python', '''
import boto3
S3API = boto3.client("s3", region_name="us-east-1")
bucket_name= "samplebucket"
filename = "/resources/website/core.css"
S3API.upload_file(filename, bucket_name, "core.css",
        ExtraArgs={"ContentType": "text/css",
                   "CacheControl": "max-age=0"})'''
                   ) }}""",
                "_class: invert\n\n_class: invert",
                "pr.md.j2",
            ),
        )
        await db.commit()

        await db.execute(
            "INSERT INTO slide (slideshow_id, idx, title, body, notes, source_file) VALUES (?, ?, ?, ?, ?, ?)",
            (
                slideshow_id,
                4,
                "Other section",
                """{{ slide_style() }}
<style scoped>
  pre {
    background: #f4f4f4;
    padding: 10px;
    font-size: 300%;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
</style>

<pre>
abc
</pre>



{{ slide_style() }}

## Database Schema Example

{{ slide_style() }}

Here's an example of how to include ER diagrams in your presentation:

<style scoped>
img[alt~="center"] { display: block;  margin: 0 auto;}
</style>

{{ generate_mermaid_diagram('user_schema','''
    USER {
        uuid id PK
        string email UK
        timestamp created_at
    }

    SCHEMA_VERSION {
        int version PK
        timestamp applied_at
        text description
    }

    MIGRATION {
        uuid id PK
        int from_version FK
        int to_version FK
        text sql_script
        boolean applied
    }

    SCHEMA_VERSION ||--o{ MIGRATION : from_version
    SCHEMA_VERSION ||--o{ MIGRATION : to_version
''', 400, -1, 'erDiagram', 'png') }}


This diagram shows the schema evolution tracking system.

### More slides
{{ slide_style() }}

### And more slides
{{ slide_style() }}

### And even more
{{ slide_style() }}""",
                "",
                "pr.md.j2",
            ),
        )
        await db.commit()

        print("SQLite inserts completed")


if __name__ == '__main__':
    asyncio.run(sqlite_inserts())
