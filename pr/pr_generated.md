---
marp: true
title: A Generic Schema Evolution Approach for NoSQL and Relational Databases
theme: default
headingDivider: 3
inlineSVG: true
#paginate: true
auto-scaling: true
size: 16:9
style: |
  /* Body sans font */
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;0,700;1,400;1,700&display=swap');
  /* Monospace for code blocks: use Google Sans Code */
  @import url('https://fonts.googleapis.com/css2?family=Google+Sans+Code:wght@400;700&display=swap');
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }

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

  /* Use Google Sans Code for code/pre blocks, with monospace fallback */
  pre, code, tt, kbd, marp-pre {
    font-family: 'Google Sans Code', monospace;
    /* a slightly smaller size for inline code vs. body text */
    font-size: 0.85em;
  /* Make code blocks visually match the slide: no distinct background or border */
  background: transparent;
  border: none;
  box-shadow: none;
  border-radius: 0;
  padding: 0;
    /*line-height: 1.3;*/
  }


---

<style scoped>
img[alt~="center"] {  display: block;  margin: 0 auto;}
</style>
![w:950 center](img/paper.png)


# A Generic Schema Evolution Approach for NoSQL and Relational Databases
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "1";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(0, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(80%);
  filter: saturate(80%);
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

<!-- _class: lead  -->
Alberto Hernández Chillón, Meike Klettke,
**Diego Sevilla Ruiz**, Jesús García Molina

Jornadas de Ingeniería del Software y Bases de Datos,
Córdoba, 2025

---
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "2";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(51, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(55%);
  filter: saturate(55%);
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
<style scoped>
img[alt~="center"] {  display: block;  margin: 0 auto;}
</style>

<p><img src="img/slide_schema1.png" alt="center" style="width:900px;" /></p>

---
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "3";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(103, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(80%);
  filter: saturate(80%);
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

```python
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

client: AsyncMongoClient = AsyncMongoClient(db_hostname, 27017)
db: AsyncDatabase = client.works

# Slideshow
jisbd2025: dict = {
    "name": "jisbd2025.md",
    "author": "Diego Sevilla Ruiz",
    "email": "dsevilla@um.es",
    "created_at": datetime.datetime.now()
}
await db.Slideshow.insert_one(jisbd2025)

# Slide
titleslide: dict = {
    "main_title": "A Generic Schema Evolution Approach for NoSQL and Relational Databases",
    "authors": "Alberto Hernández Chillón, Meike Klettke, Diego Sevilla Ruiz, Jesús García Molina",
    "notes": "..."
}
await db.Titleslide.insert_one(titleslide)

# Add slide to slideshow (slides)
jisbd2025.title_slide = titleslide._id

await db.Slideshow.replace_one(jisbd2025)
```

---
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "4";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(154, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(55%);
  filter: saturate(55%);
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

<div class="columns">

<div>

```python
async with aiosqlite.connect(db_path) as db:
# create tables
await db.execute('''
CREATE TABLE IF NOT EXISTS Slideshow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    author TEXT,
    created_at TIMESTAMP
)
''')

await db.execute('''
CREATE TABLE IF NOT EXISTS Titleslide (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    main_title TEXT,
    authors TEXT,
    date TIMESTAMP,
    additional_info TEXT,
    notes TEXT
)
''')
await db.commit()
```

</div>
<div>

```python
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
    "INSERT INTO slide (slideshow_id, idx, title, body, notes) VALUES (?, ?, ?, ?, ?)",
    (
        slideshow_id,
        1,
        "",
        """marp: true
title: A Generic Schema Evolution Approach for NoSQL and Relational Databases
theme: default
...""",
        "",
        "pr.md.j2",
    ),
)
await db.commit()
```
</div>
</div>

---
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "5";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(206, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(80%);
  filter: saturate(80%);
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

Athena Schema

<pre is="marp-pre" data-auto-scaling="downscale-only"><code class="language-Athena">Root entity Slideshow {
  +name String,
  email String,
  author String,
  created_at Timestamp,
  title_slide Ref&lt;Titleslide as uuid&gt;&amp;
}

Entity Titleslide {
  +id UUID,
  main_title String,
  authors String,
  date Timestamp,
  additional_info String,
  notes String
}</code></pre>

---
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "6";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(257, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(55%);
  filter: saturate(55%);
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

Orion

<pre is="marp-pre" data-auto-scaling="downscale-only"><code class="language-Orion">CREATE ENTITY Slideshow;
CREATE ENTITY Titleslide;</code></pre>



---
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "7";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(309, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(80%);
  filter: saturate(80%);
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
<style scoped>
img[alt~="center"] {  display: block;  margin: 0 auto;}
</style>

<p><img src="img/slide_schema2.png" alt="center" style="width:700px;" /></p>

---
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "8";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(0, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(55%);
  filter: saturate(55%);
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

* El esquema ha de cambiarse

* Los datos han de recolocarse

* El programa debe cambiar

---
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "9";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(51, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(80%);
  filter: saturate(80%);
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



## Almacenamiento

<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "10";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(103, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(55%);
  filter: saturate(55%);
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

<!-- _class: invert
-->

<style scoped>
  h2 {
    padding: 10%;
    font-size: 70pt;
  }
</style>


### Introducción

<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "11";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(154, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(80%);
  filter: saturate(80%);
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

<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "12";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(206, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(55%);
  filter: saturate(55%);
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

<!-- _class: invert
-->

<style scoped>
  h2 {
    padding: 10%;
    font-size: 70pt;
  }
</style>


### S3: PUT de un objeto
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "13";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(257, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(80%);
  filter: saturate(80%);
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
- PUT sube un objeto a un *Bucket*
- Se puede subir de una vez o *multipart*
- Ejemplo:

```python
import re
```

<pre is="marp-pre" data-auto-scaling="downscale-only"><code class="language-python">import boto3
S3API = boto3.client(&quot;s3&quot;, region_name=&quot;us-east-1&quot;)
bucket_name= &quot;samplebucket&quot;
filename = &quot;/resources/website/core.css&quot;
S3API.upload_file(filename, bucket_name, &quot;core.css&quot;,
        ExtraArgs={&quot;ContentType&quot;: &quot;text/css&quot;,
                   &quot;CacheControl&quot;: &quot;max-age=0&quot;})</code></pre>
---
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "14";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(309, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(55%);
  filter: saturate(55%);
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
<style scoped>
  pre {
    /* no special background or border so code matches slide background */
    background: transparent;
    padding: 10px;
    font-size: 300%;
    border: none;
    border-radius: 0;
    box-shadow: none;
  }
</style>

<pre>
abc
</pre>


### Other section
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "15";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(0, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(80%);
  filter: saturate(80%);
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

## Database Schema Example

<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "16";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(51, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(55%);
  filter: saturate(55%);
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

Here's an example of how to include ER diagrams in your presentation:

<style scoped>
img[alt~="center"] { display: block;  margin: 0 auto;}
</style>

<p><img src="img/user_schema.png" alt="center" style="width:400px;" /></p>


This diagram shows the schema evolution tracking system.

### More slides
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "17";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(103, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(80%);
  filter: saturate(80%);
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

### And more slides
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "18";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(154, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(55%);
  filter: saturate(55%);
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

### And even more
<style scoped>
  /* Large blurred pastel counter in the background of each slide */
  section::before {
    content: "19";
  position: absolute;
  /* Right-align the large slide number so 1- and 2-digit numbers line up */
  right: -6%;
  top: 60%;
  transform: translateY(-50%);
  text-align: right;
    font-family: 'Bodoni Moda', serif;
  /*font-style: italic;*/
  font-size: 720pt;
  line-height: 1;
  /* Color and saturation are computed per-slide for contrast (no blur) */
  color: hsla(206, 60%, 85%, 0.55); /* pastel rainbow HSL */
  -webkit-filter: saturate(80%);
  filter: saturate(80%);
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