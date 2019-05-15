from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Catalog, CatalogItem

engine = create_engine('postgres://catalog:catalogpw@/catalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Catalog for Snowboarding
catalog1 = Catalog(name="Snowboarding")

session.add(catalog1)
session.commit()

catalogItem2 = CatalogItem(name="Snowboard",
                           description="Lets you surf, but on snow!",
                           catalog=catalog1)

session.add(catalogItem2)
session.commit()


catalogItem1 = CatalogItem(name="Goggles", description="Covers for your eyes",
                           catalog=catalog1)

session.add(catalogItem1)
session.commit()


# Catalog for Basketball
catalog2 = Catalog(name="Basketball")

session.add(catalog2)
session.commit()


catalogItem1 = CatalogItem(name="Basketball",
                           description="Rubber orange globe",
                           catalog=catalog2)

session.add(catalogItem1)
session.commit()


# catalog1 for Panda Garden
catalog1 = Catalog(name="Frisbee")

session.add(catalog1)
session.commit()


menuItem1 = CatalogItem(name="Disc", description="A circular object.",
                        catalog=catalog1)

session.add(menuItem1)
session.commit()

catalog1 = Catalog(name="Soccer")
session.add(catalog1)
session.commit()


print("added catalog items!")
