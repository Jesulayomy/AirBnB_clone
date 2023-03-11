<h1 align="center"> AirBnB - The Console </h1>
This is the first step towards building your first full web application: the AirBnB clone. This first step is very important because you will use what you build during this project with all other following projects: HTML/CSS templating, database storage, API, front-end integration.
Each task is linked and will help you to:

<h2> STEPS </h2>
<h3> The console </h3>:
<p> The first piece is to manipulate a powerful storage system. This storage engine will give us an abstraction between “My object” and “How they are stored and persisted”. This means: from your console code (the command interpreter itself) and from the front-end and RestAPI you will build later, you won’t have to pay attention (take care) of how your objects are stored.
This abstraction will also allow you to change the type of storage easily without updating all of your codebase.
The console will be a tool to validate this storage engine. </p>

<h3>Web static</h3>:
<p> <ul>
<li>learn HTML/CSS</li>
<li>create the HTML of your application</li>
<li>craete template of each project</li>
</ul>

<h3>MySQL storage</h3>:
<p> <ul>
<li>replace the file storage by a Database storage</li>
<li>map your models to a table in database by using an O.R.M.</li>
</ul>

<h3>Web framework - template</h3>
<p> <ul>
<li> create your first web server in Python </li>
<li> make your static HTML file dynamic by using objects stored in a file or database </li>
</ul>

<h3>RESTful API</h3>
<p> <ul>
<li> expose all your objects stored via a JSON web interface </li>
<li> manipulate your objects via a RESTful API </li>
</ul>

<h3>Web dynamic</h3>
<p> <ul>
<li> learn JQuery </li>
<li> load objects from the client side by using your own RESTful API </li>
</ul>

<h2 align="center"> STORAGE </h2>
<p> Persistency is really important for a web application. It means: every time your program is executed, it starts with all objects previously created from another execution. Without persistency, all the work done in a previous execution won’t be saved and will be gone.
In this project, you will manipulate 2 types of storage: file and database. For the moment, you will focus on file.
Why separate “storage management” from “model”? It’s to make your models modular and independent. With this architecture, you can easily replace your storage system without re-coding everything everywhere.

You will always use class attributes for any object. Why not instance attributes? For 3 reasons:
<ul>
<li>Provide easy class description: everybody will be able to see quickly what a model should contain (which attributes, etc…)</li>
<li>Provide default value of any attribute</li>
<li>In the future, provide the same model behavior for file storage or database storage</li>
</ul>

<h3> Execution </h3>
The (hbnb) shell should work in interactive mode
```commandline
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb) 
(hbnb) 
(hbnb) quit
$

```
And also in noninteractive mode
```commandline
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
```

