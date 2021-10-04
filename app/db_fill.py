# -*- coding: utf-8 -*-

from app import app, db
from app.models import User, Alcohol, Log, Role

app_ctx = app.app_context()
app_ctx.push()
db.create_all()
Role.insert_roles()

admin = User(name=u'root', email='root@gmail.com', password='password', major='administrator',
             headline=u"Temporary Administrator One", about_me=u"Graduated from the Department of Management, and likes to read, so I work as a librarian part-time.")
user1 = User(name=u'Ihor', email='akarin@Gmail.com', password='123456', major='Computer Science', headline=u"Student")
user2 = User(name=u'test', email='test@test.com', password='123456')
user3 = User(name=u'Dentist', email='xiaoming@163.com', password='123456')
user4 = User(name=u'User_user', email='lihua@yahoo.com', password='123456')

alcohol1 = Alcohol(title=u"Flask Web Development", subtitle=u"Python-based Web Application Development Framework", manufacturer=u"Miguel Grinberg", isbn='9787115373991',
              tags_string=u"computer, programming, web development", image='http://img3.douban.com/lpic/s27906700.jpg',
             summary=u"""
# This book is not only suitable for junior Web developers to learn to read, but also an excellent reference book for Python programmers to learn advanced Web development techniques.

* Learn the basic structure of Flask applications and write sample applications;
* Use necessary components, including templates, databases, Web forms, and email support;
* Use packages and modules to build scalable large-scale applications;
* Realize user authentication, roles and personal data;
* Reuse templates, paging display lists, and use rich text in blog sites;
* Use Flask-based REST APIs to implement available functions on smartphones, tablets and other third-party clients;
* Learn to run unit tests and improve performance;
* Deploy the web application to the production server.
""")
alcohol2 = Alcohol(title=u"STL source code analysis", subtitle=u"Pa Ding Jie Niu is more than comfortable", manufacturer=u"Hou Jie", isbn='9787560926995',
              tags_string=u"computer, programming, C++", image='http://img3.doubanio.com/lpic/s1092076.jpg',
              summary=u"""* Anyone who learns programming knows that reading and analyzing famous codes is a shortcut to improve the level. Before the source code, there is no secret. The meticulous thinking, experience crystallization, technical ideas, and unique styles of the masters are all original Reflected in the source code.
* The source code presented in this book allows readers to see the realization of vector, list, heap, deque, Red Black tree, hash table, set/map; see various The realization of algorithms (sorting, searching, permutation and combination, data movement and copying technology); even the realization of the underlying memory pool and high-level abstract traits mechanism can be seen. """)
alcohol3 = Alcohol(title=u"Principle of Compilation (2nd Edition of the Original Book)", subtitle=u"Principle, Technology and Tools",
             manufacturer="Alfred V. Aho / Monica S. Lam / Ravi Sethi / Jeffrey D. Ullman ", isbn="9787111251217",
             tags_string=u"computer, compilation principle", image='http://img3.douban.com/lpic/s3392161.jpg',
             summary=u"""* This book comprehensively and in-depth explores important topics in compiler design, including lexical analysis, grammatical analysis, grammar-guided definition and grammar-guided translation, runtime environment, target code generation, code optimization technology, Parallelism detection and inter-process analysis technology, and a large number of examples are given in the relevant chapters. Compared with the previous edition, this book has undergone a comprehensive revision to cover the latest developments in compiler development. Each chapter provides A large number of systems and references.
                         * This book is a classic textbook for the course of compilation principles, with rich content. It is suitable as a textbook for the compilation principle courses for undergraduates and graduate students of computer and related majors in colleges and universities. It is also an excellent reference reading for the majority of technical personnel. """)
alcohol4 = Alcohol(title=u"Understand computer systems in depth", manufacturer="Randal E.Bryant / David O'Hallaron", isbn="9787111321330",
             tags_string=u"computer, computer system", image='http://img3.douban.com/lpic/s4510534.jpg',
             summary=u"""* This book elaborates on the essential concepts of computer systems from the perspective of programmers, and shows how these concepts actually affect the correctness, performance and practicability of applications. The book has 12 chapters, the main content Including information representation and processing, machine-level representation of programs, processor architecture, optimized program performance, memory hierarchy, links, abnormal control flow, virtual memory, system-level I/O, network programming, concurrent programming, etc. In the book Provide a lot of examples and exercises, and give some answers to help readers deepen the understanding of the concepts and knowledge described in the text.
* The biggest advantage of this book is to describe the implementation details of the computer system for programmers, to help them construct a hierarchical computer system in the brain, from the representation of the lowest data in memory to the composition of pipeline instructions, to virtual memory, To the compilation system, to the dynamic loading library, to the final user mode application. By mastering how the program is mapped to the system and how the program is executed, readers can better understand why the program behaves like this and how inefficiency is caused.
* This book is suitable for programmers who want to write faster and more reliable programs. It is also suitable as a textbook for undergraduates and graduate students in computer science and related majors in colleges and universities. """)
alcohol5 = Alcohol(title=u"C# in a nutshell", subtitle=u"The Authoritative Guide to C#5.0", manufacturer=u"Joseph Albahari / Ben Albahari",
             isbn="9787517010845", tags_string=u"computer, programming, C#", image='http://img3.douban.com/lpic/s28152290.jpg',
             summary=u"""* "c# in the shell-the authoritative guide for c#5.0" is an authoritative technical guide for c#5.0 and the first learning material for the Chinese version of c#5.0. This book has passed 26 chapters The content of this book systematically, comprehensively and meticulously explains the commands, grammar and usage of c#5.0 from basic knowledge to various advanced features. The explanations in this book are simple and easy to understand. At the same time, it is specially designed for each knowledge point. Understanding learning cases, which can help readers accurately understand the meaning of the knowledge points and quickly apply what they have learned. Compared with the previous version of c#4.0, this book also adds a wealth of concurrent, asynchronous, dynamic programming, code refinement, Contents related to advanced features such as security and com interaction.
* "C# in the shell-c#5.0 authoritative guide" also incorporates the author's years of research and practical experience in software development and c#, which is very suitable as a self-study tutorial for c# technology, and it is also a book A must-have reference book for intermediate and advanced c# technicians. """)
alcohol6 = Alcohol(title=u"Introduction to Algorithms (2nd Edition of the Original Book)",
             manufacturer="Thomas H.Cormen / Charles E.Leiserson / Ronald L.Rivest / Clifford Stein",
             isbn="9787111187776", tags_string=u"computer, algorithm", image='http://img3.doubanio.com/lpic/s1959967.jpg',
             summary=u"This book provides a comprehensive introduction to computer algorithms. The analysis of each algorithm is easy to understand and very interesting, and maintains mathematical rigor. The design goals of this book are comprehensive and suitable for a variety of purposes. Covering The content includes: the role of algorithms in calculations, probability analysis and the introduction of random algorithms. The book specifically discusses linear programming, introduces two applications of dynamic programming, randomization and approximation algorithms for linear programming techniques, etc., as well as related Recursive solution, division method and expected linear time sequence statistical algorithm used in quick sort, as well as the discussion of greedy algorithm elements. This book also introduces the proof of the correctness of the strongly connected subgraph algorithm, and the calculation of Hamiltonian cycles and subset And the proof of the NP completeness of the question. The book provides more than 900 exercises and thinking questions, as well as more detailed case studies.")
logs = [Log(user1, alcohol2), Log(user1, alcohol3), Log(user1, alcohol4), Log(user1, alcohol6),
        Log(user2, alcohol1), Log(user2, alcohol3), Log(user2, alcohol5),
        Log(user3, alcohol2), Log(user3, alcohol5)]

db.session.add_all([admin, user1, user2, user3, user4, alcohol1, alcohol2, alcohol3, alcohol4, alcohol5, alcohol6] + logs)
db.session.commit()

app_ctx.pop()
