'''
This file shall contain implemented Blueprint views : public and authorized.

Structure for each View and routes:
|-View
| |-controller
| | |-route
| | | |-strategy.py - contains a respective custom Strategy class.
| | | |-__init__.py - contains fully configured Controller - using the implemented Strategy.
| | |-__init__.py - contains imported controllers from each initialized route
| |-__init__.py - contains initialized routes for the view.
Note:
For the Strategy pattern - each controller [handle]s the request -> based on a respective Strategy , which [accept]s the data and using the explicitly enacted custom Template validates the data.
For the Builder pattern - each Template is constructed of Fields, which on its own are built using the Requirements.
[To learn more about each Strategy,Template view the respective files at [method]/strategy.py|template.py]
[To learn more about the Builder Patterns and the Requirement classes , view the files at chathouse/utilities/security/validation/data/*]

'''

from chathouse.views.public import public
from chathouse.views.authorized import authorized