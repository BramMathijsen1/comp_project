# Supposing that all the classes developed for the project
# are contained in the file 'impl.py', then:

# 1) Importing all the classes for handling the relational database
from impl import BibliographicEntityUploadHandler, BibliographicEntityQueryHandler

# 2) Importing all the classes for handling graph database
from impl import CitationUploadHandler, CitationQueryHandler

# 3) Importing the class for dealing with mashup queries
from impl import FullQueryEngine

# Once all the classes are imported, first create the relational
# database using the related source data
rel_path = "relational.db"
be = BibliographicEntityUploadHandler()
be.setDbPathOrUrl(rel_path)
be.pushDataToDb("data/dh_metadata.json")
# Please remember that one could, in principle, push one or more files
# calling the method one or more times (even calling the method twice
# specifying the same file!)

# Then, create the graph database (remember first to run the
# Blazegraph instance) using the related source data
grp_endpoint = "http://127.0.0.1:9999/blazegraph/sparql"
cit = CitationUploadHandler()
cit.setDbPathOrUrl(grp_endpoint)
cit.pushDataToDb("data/dh_citations.csv")
# Please remember that one could, in principle, push one or more files
# calling the method one or more times (even calling the method twice
# specifying the same file!)

# In the next passage, create the query handlers for both
# the databases, using the related classes
be_qh = BibliographicEntityQueryHandler()
be_qh.setDbPathOrUrl(rel_path)

cit_qh = CitationQueryHandler()
cit_qh.setDbPathOrUrl(grp_endpoint)

# Finally, create a advanced mashup object for asking
# about data
que = FullQueryEngine()
que.addBibliographicEntityHandler(be_qh)
que.addCitationHandler(cit_qh)

result_q1 = que.getAllCitations()
result_q2 = que.getCitationsWithinTimespan("P1Y","P5Y")
result_q3 = que.getBibliographicEntitiesWithTitle("Machine learning")
# etc...