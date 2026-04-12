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

from src.query.bibliographic_query_handler import BibliographicEntityQueryHandler


def test_bibliographic_queries():
    handler = BibliographicEntityQueryHandler()
    handler.setDbPathOrUrl("relational.db")

    print("===== TEST getById (by omid) =====")
    df = handler.getById("omid:br/060142")
    print(df)
    print()

    print("===== TEST getAllBibliographicEntities =====")
    df = handler.getAllBibliographicEntities()
    print(df.head())
    print("shape:", df.shape)
    print()

    print("===== TEST getBibliographicEntitiesWithTitle =====")
    df = handler.getBibliographicEntitiesWithTitle("digital")
    print(df.head())
    print(df[["title"]].head())
    print()

    print("===== TEST getBibliographicEntitiesWithAuthor =====")
    df = handler.getBibliographicEntitiesWithAuthor("Silvio")
    print(df.head())
    print()

    print("===== TEST getBibliographicEntitiesWithinPublicationDate =====")
    df = handler.getBibliographicEntitiesWithinPublicationDate("2020-01-01", "2024-12-31")
    print(df.head())
    print(df[["pub_date"]].head())
    print()

    print("===== TEST getBibliographicEntitiesWithVenue =====")
    df = handler.getBibliographicEntitiesWithVenue("journal")
    print(df.head())
    print(df[["venue"]].head())
    print()


if __name__ == "__main__":
    test_bibliographic_queries()