<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Dioptiscyma.jpg/440px-Dioptiscyma.jpg">

> **doid** (plural doids)
>
> 1. (zoology) Any member of the Doidae, a family of moths.

# DOID - Django ORM inspired DSL

> “Talent borrows. Genius Steals!” - Oscar Wilde.

DOID is a generic DSL for filtering and sorting inspired by projects like 
the Django ORM and SQLAlchemy. It is a generic container with `filter` and `order_by`
methods much like the result set managers from Django. This should be useful
if you are fond of Django's ORM idioms and would like to use the same patterns
on objects that are not Django Models like objects from API responses.


## Filter Interface

A filter object is a callable that receives an object and returns True or False. 
Filters can be combined using the bitwise and e or operators: `&` and `|`. For example:

    filter4 = filter1 | (filter2 & filter3)
    
You can turn any callable into a filter using a decorator:

    from doid.filter import doid_filter
    
    @doid_filter
    def milenials(value):
        return value.born.year > 2000
        
Filter should never mutate the value they receive.
    
## Sample data

It is easier to explain using examples. The containers are totally agnostic and 
take any dataclasses-style object, so lets generate some fake data:

    >>> data =[
        ['Adrian Mathews', 'Wilsonview', datetime.date(1944, 9, 5), 'PM'],
        ['Amanda Kaufman', 'East Franklin', datetime.date(1972, 8, 6), 'AM'],
        ['Benjamin Mcconnell', 'Wilsonview', datetime.date(1928, 8, 8), 'AM'],
        ['Carolyn Wilcox', 'Lake Benjaminbury', datetime.date(1944, 4, 21), 'PM'],
        ['Christina White', 'Angelamouth', datetime.date(1963, 10, 22), 'PM'],
        ['David Berry', 'Lake Benjaminbury', datetime.date(1950, 2, 10), 'PM'],
        ['Jacob Johnson', 'Wilsonview', datetime.date(1950, 5, 8), 'AM'],
        ['Jasmine Sanchez', 'Port Janefort', datetime.date(2008, 5, 13), 'AM'],
        ['John Robinson', 'Angelamouth', datetime.date(1945, 7, 16), 'PM'],
        ['Kenneth Hernandez', 'Port Janefort', datetime.date(1978, 10, 23), 'PM'],
        ['Monica Conley', 'East Franklin', datetime.date(1918, 9, 27), 'AM'],
        ['Paula Melendez', 'East Franklin', datetime.date(2017, 5, 21), 'AM'],
        ['Robin Harris', 'Angelamouth', datetime.date(1976, 2, 9), 'PM'],
        ['Sheri Kerr', 'East Franklin', datetime.date(1904, 1, 3), 'AM'],
        ['Shirley Gray', 'Lake Benjaminbury', datetime.date(1996, 8, 2), 'AM'],
        ['Stacy Weaver', 'East Franklin', datetime.date(1931, 10, 31), 'PM'],
        ['Tiffany Sullivan DVM', 'Wilsonview', datetime.date(1909, 1, 7), 'PM'],
        ['Tracy Norman', 'Wilsonview', datetime.date(1932, 5, 2), 'PM'],
        ['William Johnson', 'Angelamouth', datetime.date(1950, 3, 27), 'PM'],
        ['Xavier Harris', 'East Franklin', datetime.date(1903, 10, 5), 'AM']
    ]
    
    >>> class GenericObject(object):
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)
            def __repr__(self):
                return "<" + ", ".join(f"{k}={v}" for k, v in self.__dict__.items()) + ">"
                
    >>> from doid.container import ListContainer
    >>> results = ListContainer(
        GenericObject(name=name, city=city, born=born, ampm=ampm) for
        name, city, born, ampm in data
    )
    
    >>> results
    [<name=Adrian Mathews, city=Wilsonview, born=1944-09-05, ampm=PM>,
     <name=Amanda Kaufman, city=East Franklin, born=1972-08-06, ampm=AM>,
     <name=Benjamin Mcconnell, city=Wilsonview, born=1928-08-08, ampm=AM>,
     <name=Carolyn Wilcox, city=Lake Benjaminbury, born=1944-04-21, ampm=PM>,
     <name=Christina White, city=Angelamouth, born=1963-10-22, ampm=PM>,
     <name=David Berry, city=Lake Benjaminbury, born=1950-02-10, ampm=PM>,
     <name=Jacob Johnson, city=Wilsonview, born=1950-05-08, ampm=AM>,
     <name=Jasmine Sanchez, city=Port Janefort, born=2008-05-13, ampm=AM>,
     <name=John Robinson, city=Angelamouth, born=1945-07-16, ampm=PM>,
     <name=Kenneth Hernandez, city=Port Janefort, born=1978-10-23, ampm=PM>,
     <name=Monica Conley, city=East Franklin, born=1918-09-27, ampm=AM>,
     <name=Paula Melendez, city=East Franklin, born=2017-05-21, ampm=AM>,
     <name=Robin Harris, city=Angelamouth, born=1976-02-09, ampm=PM>,
     <name=Sheri Kerr, city=East Franklin, born=1904-01-03, ampm=AM>,
     <name=Shirley Gray, city=Lake Benjaminbury, born=1996-08-02, ampm=AM>,
     <name=Stacy Weaver, city=East Franklin, born=1931-10-31, ampm=PM>,
     <name=Tiffany Sullivan DVM, city=Wilsonview, born=1909-01-07, ampm=PM>,
     <name=Tracy Norman, city=Wilsonview, born=1932-05-02, ampm=PM>,
     <name=William Johnson, city=Angelamouth, born=1950-03-27, ampm=PM>,
     <name=Xavier Harris, city=East Franklin, born=1903-10-05, ampm=AM>]

    
## Attribute getter protocol

The filter protocol folows a attribute-getter protocol much like one used by Django.
We can filter by any attribute using `.filter(name=value)`:

    >>> results.filter(city="East Franklin")
    [<name=Amanda Kaufman, city=East Franklin, born=1972-08-06, ampm=AM>,
     <name=Monica Conley, city=East Franklin, born=1918-09-27, ampm=AM>,
     <name=Paula Melendez, city=East Franklin, born=2017-05-21, ampm=AM>,
     <name=Sheri Kerr, city=East Franklin, born=1904-01-03, ampm=AM>,
     <name=Stacy Weaver, city=East Franklin, born=1931-10-31, ampm=PM>,
     <name=Xavier Harris, city=East Franklin, born=1903-10-05, ampm=AM>]

We can access nested attributes replacing the `.` by double underscores: 

    >>> results.filter(born__month=5)
    [<name=Jacob Johnson, city=Wilsonview, born=1950-05-08, ampm=AM>,
     <name=Jasmine Sanchez, city=Port Janefort, born=2008-05-13, ampm=AM>,
     <name=Paula Melendez, city=East Franklin, born=2017-05-21, ampm=AM>,
     <name=Tracy Norman, city=Wilsonview, born=1932-05-02, ampm=PM>]

Some operators ara available using the same names from the `operator` module, for example
you can append `__gt` to represent the `>` operator:

    >>> from doid.filter import Q
    >>> milenials = Q(born__year__gt=1980)
    >>> results.filter(milenials)
    [<name=Jasmine Sanchez, city=Port Janefort, born=2008-05-13, ampm=AM>,
     <name=Paula Melendez, city=East Franklin, born=2017-05-21, ampm=AM>,
     <name=Shirley Gray, city=Lake Benjaminbury, born=1996-08-02, ampm=AM>]

We can filter using regular expressions by appending `__match`:

    >>> results.filter(name__match='^S')
    [<name=Sheri Kerr, city=East Franklin, born=1904-01-03, ampm=AM>,
     <name=Shirley Gray, city=Lake Benjaminbury, born=1996-08-02, ampm=AM>,
     <name=Stacy Weaver, city=East Franklin, born=1931-10-31, ampm=PM>]

Like in the Django ORM, methods can be chained:

    >>> results.filter(name__match='^S').filter(milenials)
    [<name=Shirley Gray, city=Lake Benjaminbury, born=1996-08-02, ampm=AM>]
    
This is the same as:

    >>> results.filter(name__match='^S', milenials)
    [<name=Shirley Gray, city=Lake Benjaminbury, born=1996-08-02, ampm=AM>]
    
Again like in Django, we can express OR filters using Q objects:

    >>> results.filter(Q(name__match='^S') | milenials)
    [<name=Jasmine Sanchez, city=Port Janefort, born=2008-05-13, ampm=AM>,
     <name=Paula Melendez, city=East Franklin, born=2017-05-21, ampm=AM>,
     <name=Sheri Kerr, city=East Franklin, born=1904-01-03, ampm=AM>,
     <name=Shirley Gray, city=Lake Benjaminbury, born=1996-08-02, ampm=AM>,
     <name=Stacy Weaver, city=East Franklin, born=1931-10-31, ampm=PM>]
    
The `order_by` method accepts strings following the same protocol (keyword
arguments will be passed directly to the sort method):

    >>> results.order_by('born__year')[:5]
    [<name=Xavier Harris, city=East Franklin, born=1903-10-05, ampm=AM>,
     <name=Sheri Kerr, city=East Franklin, born=1904-01-03, ampm=AM>,
     <name=Tiffany Sullivan DVM, city=Wilsonview, born=1909-01-07, ampm=PM>,
     <name=Monica Conley, city=East Franklin, born=1918-09-27, ampm=AM>,
     <name=Benjamin Mcconnell, city=Wilsonview, born=1928-08-08, ampm=AM>,

    >>> results.order_by('born__year', reverse=True)[:5]
    [<name=Paula Melendez, city=East Franklin, born=2017-05-21, ampm=AM>,
     <name=Jasmine Sanchez, city=Port Janefort, born=2008-05-13, ampm=AM>,
     <name=Shirley Gray, city=Lake Benjaminbury, born=1996-08-02, ampm=AM>,
     <name=Kenneth Hernandez, city=Port Janefort, born=1978-10-23, ampm=PM>,
     <name=Robin Harris, city=Angelamouth, born=1976-02-09, ampm=PM>]
       
## Other ideas

This is pretty much a work in progress. Some ideas are:

 1. Implement getters that works also for dicts and lists
 1. Implement getters that fail gracefully it the attribute/key does not exist
 1. Create other container types like ordered sets

