# # Supposing that all the classes developed for the project
# # are contained in the file 'impl.py', then:

# # 1) Importing all the classes for handling the relational database
# from src.query.bibliographic_query_handler import BibliographicEntityQueryHandler
# from src.upload.bibliographic_upload_handler import BibliographicEntityUploadHandler
# # 2) Importing all the classes for handling graph database
# from src.upload.citation_upload_handler import CitationUploadHandler
# from src.query.citation_query_handler import CitationQueryHandler
# # 3) Importing the class for dealing with mashup queries
# from src.engine.full_query_engine import FullQueryEngine
# # 4) Importing config file
# from config import grp_endpoint

# # Once all the classes are imported, first create the relational
# # database using the related source data
# rel_path = "relational.db"
# be = BibliographicEntityUploadHandler()
# be.setDbPathOrUrl(rel_path)
# be.pushDataToDb("data/dh_metadata.json")
# # Please remember that one could, in principle, push one or more files
# # calling the method one or more times (even calling the method twice
# # specifying the same file!)

# # Then, create the graph database (remember first to run the
# # Blazegraph instance) using the related source data
# cit = CitationUploadHandler()
# cit.setDbPathOrUrl(grp_endpoint)
# cit.pushDataToDb("data/dh_citations.csv")
# # Please remember that one could, in principle, push one or more files
# # calling the method one or more times (even calling the method twice
# # specifying the same file!)

# # In the next passage, create the query handlers for both
# # the databases, using the related classes
# be_qh = BibliographicEntityQueryHandler()
# be_qh.setDbPathOrUrl(rel_path)

# cit_qh = CitationQueryHandler()
# cit_qh.setDbPathOrUrl(grp_endpoint)

# # Finally, create a advanced mashup object for asking
# # about data
# que = FullQueryEngine()
# que.addBibliographicEntityHandler(be_qh)
# que.addCitationHandler(cit_qh)

# result_q1 = que.getAllCitations()
# result_q2 = que.getCitationsWithinTimespan("P1Y","P5Y")
# result_q3 = que.getBibliographicEntitiesWithTitle("Machine learning")
# # etc...

# from src.query.bibliographic_query_handler import BibliographicEntityQueryHandler

# handler = BibliographicEntityQueryHandler()
# handler.setDbPathOrUrl("relational.db")

# df = handler.getAllBibliographicEntities()
# print(df.head())

# ✅ 1. 所有 import 放最上面
from src.upload.bibliographic_upload_handler import BibliographicEntityUploadHandler
from src.query.bibliographic_query_handler import BibliographicEntityQueryHandler

# ✅ 2. 数据库路径
rel_path = "relational.db"


#be = BibliographicEntityUploadHandler()
#be.setDbPathOrUrl(rel_path)
#be.pushDataToDb("data/dh_metadata.json")

# ✅ 4. 测试 query handler
handler = BibliographicEntityQueryHandler()
handler.setDbPathOrUrl("relational.db")

print("\n--- All bibliographic entities ---")
df = handler.getAllBibliographicEntities()
print(df.head())
print(df.shape)

print("\n--- Search by title ---")
df = handler.getBibliographicEntitiesWithTitle("machine")
print(df.head())
print(df.shape)

print("\n--- Search by author ---")
df = handler.getBibliographicEntitiesWithAuthor("Rovira")
print(df.head())
print(df.shape)

print("\n--- Search by publication date ---")
df = handler.getBibliographicEntitiesWithinPublicationDate("2018", "2020")
print(df.head())
print(df.shape)

print("\n--- Search by venue ---")
df = handler.getBibliographicEntitiesWithVenue("journal")
print(df.head())
print(df.shape)

print("\n--- Search by ID ---")
all_df = handler.getAllBibliographicEntities()
first_id = all_df["omid"].iloc[0]
df = handler.getById(first_id)
print(df)
print(df.shape)