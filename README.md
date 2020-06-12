# jupyter_testint
A testing integration to show how we can use single object to be our master

###
This is a python module that helps to connect Jupyter Notebooks to various datasets. 

Here is what it does:
-------
- Identifies line and cell magic for based on your keyword. (for example, jupyter_drill uses %drill and %%drill)
- Handles authentication in as sane of a way as possible, including password authentication (and not storing it in the notebook itself)
- (Future) Hook into a password safe to make it even more seamless
- Returns data to a Pandas Dataframe (and also uses BeakerX's awesome table to disaply)
- Provides cusomization options for display, and handline datastore specific items/quirks
- Provides a place to put limits on queries (limits/partitions etc)
- Provides a place to provide documentation built in


After installing this, to instantiate the module so you can use %testint and %%testint put this in a cell:

```
from testint_core import Testint
ipy = get_ipython()
Testint = Testint(ipy,  pd_display_grid="html")
ipy.register_magics(Testint)
```

